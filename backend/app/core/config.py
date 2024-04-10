from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from .log import Logger

log = Logger(__name__, 'base.log').logger

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file='/backend/back_dev.env')

    # Domain
    DOMAIN: str

    # Backend
    SUPERUSER_USERNAME: str
    SUPERUSER_PASSWORD: str
    BACKEND_CORS_ORIGINS: str

    # Postgres
    POSTGRES_DB: str
    POSTGRES_USER : str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_EXTERNAL_PORT: int

    # JWT auth
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    TOKEN_SECRET_KEY: str
    ALGORITHM: str

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

settings = Settings()
