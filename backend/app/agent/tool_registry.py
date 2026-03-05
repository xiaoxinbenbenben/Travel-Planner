"""工具注册与分发。

统一处理工具注册、参数校验与异常包装，
对上层屏蔽同步/异步工具实现差异。
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Optional

from pydantic import BaseModel, ValidationError as PydanticValidationError

from app.core import ToolExecutionError, ToolNotFoundError, ToolValidationError

ToolHandler = Callable[[Dict[str, Any]], Any]


@dataclass
class ToolDefinition:
    """工具定义。"""

    name: str
    handler: ToolHandler
    args_model: type[BaseModel] | None = None
    description: str = ""


class ToolRegistry:
    """工具注册中心。"""

    def __init__(self) -> None:
        self._tools: Dict[str, ToolDefinition] = {}

    def register(
        self,
        name: str,
        handler: ToolHandler,
        *,
        args_model: type[BaseModel] | None = None,
        description: str = "",
    ) -> None:
        # 注册时做 strip，避免调用方因多余空格导致找不到工具。
        key = name.strip()
        self._tools[key] = ToolDefinition(
            name=key,
            handler=handler,
            args_model=args_model,
            description=description,
        )

    def has_tool(self, name: str) -> bool:
        return name in self._tools

    def list_tools(self) -> Dict[str, ToolDefinition]:
        return dict(self._tools)

    async def dispatch(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        if name not in self._tools:
            raise ToolNotFoundError(name)

        tool = self._tools[name]
        payload = arguments or {}

        if tool.args_model is not None:
            try:
                # 统一在入口完成参数模型校验，业务函数可直接使用强约束 payload。
                validated = tool.args_model.model_validate(payload)
                payload = validated.model_dump()
            except PydanticValidationError as exc:
                raise ToolValidationError(name, f"参数校验失败: {exc}") from exc

        try:
            result = tool.handler(payload)
            if inspect.isawaitable(result):
                result = await result
            return result
        except ToolNotFoundError:
            raise
        except ToolValidationError:
            raise
        except Exception as exc:
            raise ToolExecutionError(name, f"工具执行失败: {exc}") from exc
