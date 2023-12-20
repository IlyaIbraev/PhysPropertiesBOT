import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers

# Логгер
logger = logging.getLogger(__name__)


# Конфигурирование и инициализация бота
async def main():
    # Конфигурирование логгера
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Оповещение о том, что бот запущен
    logger.info('Starting bot')

    # Загругза конфигурации бота из .env
    config: Config = load_config()

    # Инициализация долгосрочного хранилища Redis
    redis = Redis(host='localhost')
    storage = RedisStorage(redis=redis)

    # Инициализация бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    # Регистрация роутеров
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Запуск лонг пула
    await dp.start_polling(bot)

# Запуск main в асинхронном режиме (требует asyncio)
if __name__ == '__main__':
    asyncio.run(main())