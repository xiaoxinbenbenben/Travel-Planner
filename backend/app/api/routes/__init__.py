"""路由模块。

集中导出 FastAPI 路由子模块，供入口文件统一挂载。
"""

from app.api.routes import map, poi, trip

__all__ = ["map", "poi", "trip"]
