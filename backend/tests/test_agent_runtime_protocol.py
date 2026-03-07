"""MiniAgent 协议一致性测试。"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List, Sequence

import pytest

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.agent.runtime import MiniAgent
from app.agent.tool_registry import ToolRegistry


class _StrictLLM:
    """模拟严格网关：拒绝含 role=tool 但无原生 tool_calls 的上下文。"""

    def __init__(self) -> None:
        self.turn = 0
        self.history_snapshots: List[List[Dict[str, str]]] = []

    async def chat(self, messages: Sequence[Dict[str, str]]):  # noqa: ANN201
        snapshot = [dict(item) for item in messages]
        self.history_snapshots.append(snapshot)

        if any(item.get("role") == "tool" for item in messages):
            raise AssertionError("unexpected role=tool message")

        if self.turn == 0:
            self.turn += 1
            return [
                {
                    "tool_name": "search_poi",
                    "arguments": {"keywords": "博物馆", "city": "北京", "citylimit": True},
                }
            ]
        return "done"


@pytest.mark.asyncio
async def test_runtime_uses_text_protocol_for_tool_result() -> None:
    llm = _StrictLLM()
    registry = ToolRegistry()

    async def _search_poi(_: Dict[str, str]) -> Dict[str, str]:
        return {"name": "示例景点"}

    registry.register("search_poi", _search_poi)

    agent = MiniAgent(llm_client=llm, tool_registry=registry, max_steps=3)
    result = await agent.run(
        [
            {"role": "system", "content": "你是测试助手"},
            {"role": "user", "content": "请帮我规划"},
        ]
    )

    assert result.content == "done"
    assert len(result.traces) == 1
    assert len(llm.history_snapshots) == 2

    second_turn_history = llm.history_snapshots[1]
    assert not any(item.get("role") == "tool" for item in second_turn_history)
    assistant_message = next(item for item in second_turn_history if item.get("role") == "assistant")
    assistant_payload = json.loads(assistant_message["content"])
    assert assistant_payload["tool_name"] == "search_poi"
    assert assistant_payload["arguments"] == {"keywords": "博物馆", "city": "北京", "citylimit": True}
    assert any(
        item.get("role") == "user" and item.get("content", "").startswith("[TOOL_RESULT:search_poi]")
        for item in second_turn_history
    )
