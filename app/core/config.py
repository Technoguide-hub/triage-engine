from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-5.2"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # EMAIL
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str

    class Config:
        env_file = ".env"
        extra = "forbid"

settings = Settings()
