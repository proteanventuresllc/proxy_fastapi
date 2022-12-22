from pydantic import BaseSettings


class Settings(BaseSettings):
    target_host: str

settings = Settings()
