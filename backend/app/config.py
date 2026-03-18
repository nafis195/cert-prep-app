import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Cert Prep App"

    # Default to a local SQLite database so the app runs without requiring
    # a separate PostgreSQL server in development.
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./cert_prep_app.db",
    )

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


settings = Settings()

