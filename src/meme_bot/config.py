from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Файл .env читается, если он есть. Лишние переменные окружения игнорируются.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    token: str  # переменная окружения TOKEN
    max_photo_size: int = 10 * 1024 * 1024
    font_path: str = "fonts/font.ttf"


@lru_cache
def get_settings() -> Settings:
    # Объект создаётся один раз на весь процесс. Если TOKEN не задан, здесь будет ValidationError.
    return Settings()  # type: ignore[call-arg]


class _SettingsProxy:
    # Settings создаётся при первом обращении к полю, а не при импорте модуля.
    def __getattr__(self, name: str) -> object:
        return getattr(get_settings(), name)


settings: Settings = _SettingsProxy()  # type: ignore[assignment]
