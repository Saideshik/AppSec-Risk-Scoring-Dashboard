from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_prefix = ""
        env_file = ".env"

settings = Settings()
