"""图片相关服务。

优先使用 Unsplash API；当外部服务不可用时，
自动降级到免鉴权图片链接以保证页面可展示。
"""

from __future__ import annotations

from urllib.parse import quote_plus

from app.core import ExternalServiceError, get_settings
from app.integrations.photos import UnsplashClient


class PhotoService:
    """图片服务：优先 Unsplash，失败时降级到 source.unsplash.com。"""

    def __init__(self, client: UnsplashClient | None = None) -> None:
        self.client = client

    def get_attraction_photo(self, name: str) -> str:
        # 关键词为空时使用兜底词，避免返回无效 URL。
        query = name.strip()
        if not query:
            query = "travel"

        if self.client is not None:
            try:
                url = self.client.get_photo_url(query)
            except ExternalServiceError:
                # 图片服务失败不应阻断主流程，直接降级。
                url = None
            if isinstance(url, str) and url:
                return url

        keyword = quote_plus(query)
        return f"https://source.unsplash.com/featured/?{keyword}"


def _build_default_photo_service() -> PhotoService:
    settings = get_settings()
    client: UnsplashClient | None = None
    if settings.unsplash_access_key:
        client = UnsplashClient(access_key=settings.unsplash_access_key)
    return PhotoService(client=client)


_photo_service = _build_default_photo_service()


def get_photo_service() -> PhotoService:
    return _photo_service
