from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass(frozen=True)
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    skip_ssl: bool = False


def _parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_db_config(env_path: str | None = None) -> DatabaseConfig:
    """Load database settings from environment variables and report missing keys."""
    load_dotenv(dotenv_path=env_path)

    required_keys = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]
    values: dict[str, str] = {}
    missing: list[str] = []

    for key in required_keys:
        raw = os.getenv(key)
        if raw is None or raw.strip() == "":
            missing.append(key)
        else:
            values[key] = raw.strip()

    if missing:
        joined = ", ".join(missing)
        raise ValueError(f"Variables d'environnement manquantes ou vides : {joined}")

    try:
        port = int(values["DB_PORT"])
    except ValueError as exc:
        raise ValueError(f"DB_PORT doit être un entier valide, reçu : {values['DB_PORT']!r}") from exc

    skip_ssl = _parse_bool(os.getenv("DB_SKIP_SSL"), default=False)

    return DatabaseConfig(
        host=values["DB_HOST"],
        port=port,
        database=values["DB_NAME"],
        user=values["DB_USER"],
        password=values["DB_PASSWORD"],
        skip_ssl=skip_ssl,
    )
