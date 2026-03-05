"""图片集成模块。

对外暴露 Unsplash 客户端与构造函数，供服务层按需接入。
"""

from app.integrations.photos.unsplash_client import UnsplashClient, build_unsplash_client

__all__ = ["UnsplashClient", "build_unsplash_client"]
