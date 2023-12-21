from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from lexicon.lexicon import LEXICON

router = Router()


# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=LEXICON[data["language"]]['other_answer'])