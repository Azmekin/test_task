import os
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_VERSION: str = "0.0.0"  # Изменять вручную
    PROJECT_NAME: str = "Weather"

    # API
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = os.getenv("PORT", 8000)


settings = Settings()
