"""服务模块导出。

统一聚合业务服务入口，便于路由层按需依赖。
"""

from app.services.map_service import get_map_service
from app.services.photo_service import get_photo_service
from app.services.trip_service import build_trip_plan

__all__ = [
    "build_trip_plan",
    "get_map_service",
    "get_photo_service",
]
