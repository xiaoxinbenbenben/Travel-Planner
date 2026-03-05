"""工作流模块。

汇总对外可用的工作流入口，避免外层直接依赖具体文件路径。
"""

from app.agent.workflows.trip_workflow import TripWorkflow

__all__ = ["TripWorkflow"]
