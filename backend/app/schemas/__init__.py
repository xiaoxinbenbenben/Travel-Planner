"""业务 Schema 导出。

统一收口 Trip 与 Map 相关数据模型，减少调用方导入复杂度。
"""

from app.schemas.map import (
    POIDetailResponse,
    POIPhotoResponse,
    POIInfo,
    POISearchRequest,
    POISearchResponse,
    RouteInfo,
    RouteRequest,
    RouteResponse,
    WeatherResponse,
)
from app.schemas.trip import (
    Attraction,
    Budget,
    DayPlan,
    Hotel,
    Location,
    Meal,
    TripPlan,
    TripPlanResponse,
    TripRequest,
    WeatherInfo,
)

__all__ = [
    "Attraction",
    "Budget",
    "DayPlan",
    "Hotel",
    "Location",
    "Meal",
    "TripPlan",
    "TripPlanResponse",
    "TripRequest",
    "WeatherInfo",
    "POIDetailResponse",
    "POIPhotoResponse",
    "POIInfo",
    "POISearchRequest",
    "POISearchResponse",
    "RouteInfo",
    "RouteRequest",
    "RouteResponse",
    "WeatherResponse",
]
