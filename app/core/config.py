from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "MedLink Ethiopia API"
    VERSION: str = "1.1.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    AUTO_CREATE_TABLES: bool = True

    DATABASE_URL: str | None = None
    POSTGRES_SERVER: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "medlink"
    POSTGRES_PASSWORD: str = "medlink"
    POSTGRES_DB: str = "medlink"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "medplum"
    REDIS_STREAM_PREFIX: str = "medlink"

    MEILI_HOST: str = "http://meilisearch:7700"
    MEILI_MASTER_KEY: str = "masterKey"
    MEILI_ENABLED: bool = True

    MEDPLUM_CLIENT_ID: str = ""
    MEDPLUM_CLIENT_SECRET: str = ""
    MEDPLUM_BASE_URL: str = "http://medplum-server:8103"

    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET: str = "change-me-in-production"
    ALLOWED_CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["http://localhost:3000"])
    MAX_RESERVATION_QTY: int = 5
    DEFAULT_RESERVATION_WINDOW_MINUTES: int = 45
    SEARCH_RESULT_LIMIT: int = 10
    PRESCRIPTION_STORAGE_DIR: str = "storage/prescriptions"
    SIGNING_SECRET: str = "change-me-storage-signing-key"
    SIGNED_URL_TTL_SECONDS: int = 900
    MAX_UPLOAD_BYTES: int = 5242880
    RATE_LIMIT_REQUESTS: int = 60
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    OTEL_ENABLED: bool = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


settings = Settings()
