from pydantic_settings import BaseSettings
from pydantic import InstanceOf
from functools import lru_cache
from typing import Dict, List


class Tag(BaseSettings):
    name: str
    description: str


class AppDescription(BaseSettings):
    title: str = "Test API"
    description: str = "Web-приложение для определения заполненных форм"
    version: str = "1.0.0"
    debug: bool = False
    openapi_tags: List[InstanceOf[Tag]] = [
        Tag(name="Forms", description="Forms endpoints")
    ]


class MongoSettings(BaseSettings):

    MONGO_DB_ROOT_USERNAME: str
    MONGO_DB_ROOT_PASSWORD: str
    MONGO_DB_HOST: str
    MONGO_DB_PORT: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"


@lru_cache
class Settings(BaseSettings):
    app_description: Dict = AppDescription().model_dump()
    mongo: InstanceOf[MongoSettings] = MongoSettings()
    MAX_POSSIBLE_TEMPLATES: int = 10


settings = Settings()
