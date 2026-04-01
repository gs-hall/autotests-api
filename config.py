from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, FilePath, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientConfig(BaseModel):
    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        return str(self.url)


class TestDataConfig(BaseModel):
    image_png_file: FilePath


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    test_data: TestDataConfig
    http_client: HTTPClientConfig

    if TYPE_CHECKING:
        # Only for static analyzers (Pylance/Pyright), runtime is unchanged.
        def __init__(self, **kwargs: Any) -> None: ...


# Инициализируем настройки
settings = Settings()
