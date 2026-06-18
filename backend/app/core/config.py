from pathlib import Path
from pydantic_settings import BaseSettings

_root = Path(__file__).parent.parent.parent.parent  # it-asset-manager/


class Settings(BaseSettings):
    database_url: str = "sqlite:///./dev.db"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480
    templates_dir: str = str(_root / "frontend" / "templates")
    static_dir: str = str(_root / "frontend" / "static")

    model_config = {"env_file": ".env"}


settings = Settings()
