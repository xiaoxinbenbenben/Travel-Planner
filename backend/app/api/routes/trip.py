"""Trip 路由。

对外暴露旅行计划生成入口，保持 `/api/trip/plan` API 兼容。
"""

from fastapi import APIRouter

from app.core import AppError, to_http_exception
from app.schemas import TripPlanResponse, TripRequest
from app.services import build_trip_plan

# 单一路由入口，便于前端和契约测试稳定依赖。
router = APIRouter(prefix="/trip", tags=["旅行规划"])


@router.post("/plan", response_model=TripPlanResponse, summary="生成旅行计划")
async def plan_trip(request: TripRequest) -> TripPlanResponse:
    """根据输入参数生成旅行计划。"""
    try:
        # 入口只负责触发 Trip service，编排逻辑在 service/workflow 内完成。
        plan = await build_trip_plan(request)
        return TripPlanResponse(success=True, message="旅行计划生成成功", data=plan)
    except Exception as exc:
        # 统一错误映射，避免路由层散落 HTTPException 细节。
        raise to_http_exception(exc if isinstance(exc, AppError) else AppError(str(exc))) from exc
