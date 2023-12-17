from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, invert_f
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

import logging
import sys
import asyncio

dp = Dispatcher()

TOKEN = "2019051844:AAHECSV_1GAHqjPD-ifUYKOXqA55SxvL66s"

# HANDLERS

@dp.message(Command("start"))
async def handler_start(message: Message) -> None:
    await message.answer("Hello! Wait a bit.")

@dp.message()
async def handler_message(message: Message) -> None:
    await message.answer(message.text)

# Reply Keyboards
    


# Inline Keyboards



# DB



async def main() -> None:

    global bot

    bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())