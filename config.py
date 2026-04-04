from pathlib import Path
from typing import TYPE_CHECKING, Any, Self

from pydantic import BaseModel, DirectoryPath, FilePath, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class HTTPClientConfig(BaseModel):
    url: HttpUrl
    timeout: float

    @property
    def client_url(self) -> str:
        return str(self.url)


class TestDataConfig(BaseModel):
    image_png_file: FilePath


class SwaggerCoverageService(BaseModel):
    key: str
    name: str
    tags: list[str]
    repository: str
    swagger_url: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
    )

    test_data: TestDataConfig
    http_client: HTTPClientConfig
    swagger_coverage_services: list[SwaggerCoverageService]
    allure_results_dir: DirectoryPath

    if TYPE_CHECKING:

        def __init__(self, **kwargs: Any) -> None: ...

    # Добавили метод initialize
    @classmethod
    def initialize(cls) -> Self:  # Возвращает экземпляр класса Settings
        allure_results_dir = Path("./allure-results")
        allure_results_dir.mkdir(exist_ok=True)

        # Передаем allure_results_dir в инициализацию настроек
        return cls(allure_results_dir=allure_results_dir)


# Инициализируем настройки
settings = Settings.initialize()
