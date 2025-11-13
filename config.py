import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    db_type: str = "postgresql"
    host: str = os.getenv("DB_HOST", "localhost")
    port: str = os.getenv("DB_PORT", "5432")
    database: str = os.getenv("DB_NAME", "employees")
    username: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PASSWORD", "password")


DB_CONFIG = DatabaseConfig()
