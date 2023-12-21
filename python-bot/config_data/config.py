from dataclasses import dataclass
from environs import Env


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

    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
        ),
        redis=RedisConfig(
            host=env('REDIS_HOST'),
            port=env('REDIS_PORT'),
            db=env('REDIS_DB'),
        ),
        api=PersonalPUBChemAPI(
            url=env('API_URL'),
            port=env('API_PORT'),
        )
    )