from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Bot

from keyboards.keyboards import create_molecule_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_properties
from filters.registration_filter import RegistrationForm

router = Router()

# /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await state.update_data(nametype="name")
    await state.set_state(RegistrationForm.registration_completed)
    await message.answer(text=LEXICON_RU['/start'])

# registration check
@router.message(~StateFilter(RegistrationForm.registration_completed))
async def process_nonregister(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['unregistered'])

# /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/help'])

# /name
@router.message(Command(commands="name"))
async def process_name_command(message: Message, state: FSMContext):
    await state.update_data(nametype="name")
    await message.answer(text=LEXICON_RU["/name"])

# /smiles
@router.message(Command(commands="smiles"))
async def process_name_command(message: Message, state: FSMContext):
    await state.update_data(nametype="smiles")
    await message.answer(text=LEXICON_RU["/smiles"])

# Отработчик названий
@router.message(F.text[0] != "/")
async def process_get_properties(message: Message, state: FSMContext):
    # Заявленное название вещества
    name = message.text
    # Получение информации том, какой nametype выбран у пользователя
    user_data = await state.get_data()
    nametype = user_data["nametype"]
    # Получение информации по веществу и статусу ответа
    response_data, status = get_properties(nametype, name)
    
    # Обработка статуса
    match status:
        case 200:
            molecule_name = response_data["Name"]
            molecule_image = response_data["Image"]
            molecule_keyboard = create_molecule_keyboard(response_data=response_data)
            await message.answer(
                text=LEXICON_RU["finder_200"].format(molecule_name, molecule_image),
                reply_markup=molecule_keyboard
                )
        case 400:
            await message.answer(text=LEXICON_RU["finder_400"])
        case 404:
            await message.answer(text=LEXICON_RU["finder_404"])

# callback r"select:+"
@router.callback_query(F.data.startswith("select:"))
async def process_select_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Получение информации по веществу по CID
    response_data, _ = get_properties("cid", callback.data.split(":")[1])
    # Полученеи свойств вещества
    property = response_data["Properties"][callback.data.split(":")[2]]
    # Формирование ответа
    answer = [callback.data.split(":")[2]]
    for elem in property:
        answer.append(elem)
    answer = "\n   ".join(map(str, answer))
        
    # Попытка отправить ответ на запрос алертом
    try:
        await callback.answer(answer, show_alert=True)
    # Иначе ответ отправляется сообщением.
    except:
        await callback.answer(text=LEXICON_RU["answer_too_long"])
        await bot.send_message(chat_id=callback.from_user.id, text=answer)