from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="UTF8")
    API_GATEWAY_URL: str
    REDIS_HOST: str
    REDIS_PORT: int


PRELOAD_FOLDER = "./preload_files"
TTL = 3600
settings = Settings()
