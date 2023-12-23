from dataclasses import dataclass
# from environs import Env
from os import environ

@dataclass
class RedisConfig:
    host: str
    port: str
    db: str


@dataclass
class TgBot:
    token: str            # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота

@dataclass
class PersonalPUBChemAPI:
    url: str
    port: str

@dataclass
class Config:
    tg_bot: TgBot
    redis: RedisConfig
    api: PersonalPUBChemAPI


def load_config(path: str | None = None) -> Config:

    return Config(
        tg_bot=TgBot(
            token=environ.get('BOT_TOKEN'),
            admin_ids=environ.get('ADMIN_IDS'),
        ),
        redis=RedisConfig(
            host=environ.get('REDIS_HOST'),
            port=environ.get('REDIS_PORT'),
            db=environ.get('REDIS_DB'),
        ),
        api=PersonalPUBChemAPI(
            url=environ.get('API_URL'),
            port=environ.get('API_PORT'),
        )
    )