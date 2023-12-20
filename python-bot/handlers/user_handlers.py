from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from keyboards.keyboards import game_kb, yes_no_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_bot_choice, get_properties, get_winner

router = Router()


# /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)


# /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)

# Название
@router.message(F.text[0] != "/")
async def process_get_properties(message: Message):
    
    name = message.text
    nametype = "name"

    await message.answer(get_properties(nametype, name))

# # Этот хэндлер срабатывает на согласие пользователя играть в игру
# @router.message(F.text == LEXICON_RU['yes_button'])
# async def process_yes_answer(message: Message):
#     await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)


# # Этот хэндлер срабатывает на отказ пользователя играть в игру
# @router.message(F.text == LEXICON_RU['no_button'])
# async def process_no_answer(message: Message):
#     await message.answer(text=LEXICON_RU['no'])


# # Этот хэндлер срабатывает на любую из игровых кнопок
# @router.message(F.text.in_([LEXICON_RU['rock'],
#                             LEXICON_RU['paper'],
#                             LEXICON_RU['scissors']]))
# async def process_game_button(message: Message):
#     bot_choice = get_bot_choice()
#     await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
#                               f'- {LEXICON_RU[bot_choice]}')
#     winner = get_winner(message.text, bot_choice)
#     await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)