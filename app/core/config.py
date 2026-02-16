from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-5.2"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # OWNER (para criação automática)
    OWNER_EMAIL: str | None = None
    OWNER_PASSWORD: str | None = None

    # EMAIL
    EMAIL_HOST: str | None = None
    EMAIL_PORT: int | None = None
    EMAIL_USER: str | None = None
    EMAIL_PASSWORD: str | None = None
    EMAIL_FROM: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()