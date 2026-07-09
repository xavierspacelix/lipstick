from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7
    s3_endpoint: str
    s3_bucket: str
    s3_access_key: str
    s3_secret_key: str
    ai_service_url: str
    cors_allowed_origins: str = "http://localhost:3000"
    cookie_domain: Optional[str] = None

    max_upload_size_mb: int = 10
    supported_image_types: list[str] = ["image/jpeg", "image/png"]
    top_n_recommendations: int = 3

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
