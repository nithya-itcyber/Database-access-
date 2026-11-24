import pymysql
from pymysql.cursors import DictCursor
from config import DatabaseConfig, load_db_config


def get_connection(config: DatabaseConfig | None = None) -> pymysql.connections.Connection:
    """Open and return a PyMySQL connection configured to return dictionary rows."""
    cfg = config if config is not None else load_db_config()

    connect_kwargs: dict[str, object] = {
        "host": cfg.host,
        "port": cfg.port,
        "user": cfg.user,
        "password": cfg.password,
        "database": cfg.database,
        "charset": "utf8mb4",
        "cursorclass": DictCursor,
    }

    if cfg.skip_ssl:
        connect_kwargs["ssl"] = {}

    return pymysql.connect(**connect_kwargs)
