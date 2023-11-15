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


@lru_cache
class Settings(BaseSettings):
    app_description: Dict[str, str | bool | List[Dict[str, str]]] = AppDescription().model_dump()


settings = Settings().model_dump()


# @lru_cache
# class Settings(BaseSettings):
#     """ Креды для БД подгружаются из .env """
#     DB_USER: str
#     DB_PASSWORD: str
#     DB_SCHEMA: str
#     DB_HOST: str
#     DB_PORT: str
#     DB_URL: str
#     app_description: AppDescription = AppDescription()
#
#     class Config:
#         env_file = ".env"
