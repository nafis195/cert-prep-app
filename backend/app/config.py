import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Cert Prep App"

    # Postgres DB for the UUID/RLS schema in `cert-prep-app/db/`.
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24


settings = Settings()

if not settings.DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is required. Set it before starting the app, e.g.:\n"
        "export DATABASE_URL='postgresql://<user>:<pass>@localhost:5432/cert_prep_app'"
    )

