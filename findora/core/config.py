from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Findora"
    app_version: str = "0.1.0"
    debug: bool = True

    secret_key: str = "your-secret-key"
    session_cookie_name: str = "findora_session"

    upload_dir: str = "findora/uploads"
    max_upload_size_mb: int = 5
    allowed_image_types: str = "image/jpeg,image/png,image/webp"

    # Database settings
    database_url: str = "sqlite:///./findora.db"

    rate_limit_enabled: bool = True
    rate_limit_storage_uri: str = "memory://"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
settings = Settings()