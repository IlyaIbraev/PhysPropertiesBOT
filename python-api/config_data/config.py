from dataclasses import dataclass
from os import environ


@dataclass
class PostgreSQLConfig:
    host: str
    username: str
    password: str
    dbname: str

@dataclass
class Config:
    db_config: PostgreSQLConfig

def load_config(path: str | None = None) -> Config:

    return Config(
        db_config=PostgreSQLConfig(
            host=environ.get('DB_HOST'),
            username=environ.get('DB_USER'),
            password=environ.get('DB_PASSWORD'),
            dbname=environ.get('DB_NAME'),
        )
    )