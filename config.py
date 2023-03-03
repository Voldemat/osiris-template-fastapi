import os

DEBUG: bool = os.environ.get("DEBUG", "false") in ("true", "t", "1")
LOG_LEVEL: str = os.environ.get("LOG_LEVEL", "INFO")
HOST: str = os.environ.get("HOST", "localhost")
PORT: int = int(os.environ.get("PORT", "8000"))
ROOT_PATH: str = os.environ.get("ROOT_PATH", "")


POSTGRES_HOST: str = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT: int = int(os.environ.get("POSTGRES_PORT", "5432"))
POSTGRES_USER: str = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD: str | None = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB: str = os.environ.get("POSTGRES_DB", POSTGRES_USER)
