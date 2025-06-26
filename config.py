from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    tawk_webhook_secret: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="TAWK_")

settings = Settings()
