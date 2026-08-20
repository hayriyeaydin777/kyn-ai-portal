from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "mysql+pymysql://portal:portal_dev_password@localhost:3306/portal"
    policy_service_url: str = "http://localhost:5142"
    ai_provider: str = "fake"


settings = Settings()
