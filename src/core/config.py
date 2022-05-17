from typing import Optional, Dict, Any

from pydantic import BaseSettings, PostgresDsn, validator

from src.util import parse2module


class Settings(BaseSettings):

    POSTGRES_SERVER: str = "localost"
    POSTGRES_PORT: str = "5000"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "dariela1109"
    POSTGRES_DB: str = "azcuba"
    DATABASE_URI: Optional[PostgresDsn] = None

    TORTOISE_INIT: Optional[dict] = None

    @validator("DATABASE_URI", pre=True)
    def production_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgres",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    def routes_config(self):
        return {
            "connections": {"master": "sqlite://memory", "slave": "sqlite://memory"},
            "apps": {
                "models": {
                    "models": parse2module("src/models"),
                    "default_connection": "master",
                }
            },
            "routers": ["src.core.app.Router"],
        }

    @validator("TORTOISE_INIT", pre=True)
    def tortoise_init(cls, v: Optional[dict], values: Dict[str, Any]) -> Any:
        if isinstance(v, dict):
            return v
        return {
            "connections": {"default": str(values.get("DATABASE_URI"))},
            "apps": {
                "models": {
                    "models": parse2module("src"),
                    "default_connection": "default",
                }
            },
        }


s = Settings()
