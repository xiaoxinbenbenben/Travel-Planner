"""LLM 集成导出。

封装对 OpenAI 兼容协议客户端的统一导入入口。
"""

from app.integrations.llm.client import OpenAICompatibleLLMClient, build_llm_client

__all__ = ["OpenAICompatibleLLMClient", "build_llm_client"]
