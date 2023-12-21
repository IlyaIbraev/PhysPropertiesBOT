from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import Bot

from keyboards.keyboards import create_molecule_keyboard
from lexicon.lexicon import LEXICON
from services.services import get_properties
from filters.registration_filter import RegistrationForm
from utils.utils import html_formation

router = Router()

# /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext, bot: Bot):
    # Если не указана data, задаем базовую
    data = await state.get_data()
    if not data:
        await state.update_data(nametype="name", language="EN")
        data = {"nametype": "name", "language": "EN"}

    await state.set_state(RegistrationForm.registration_completed)
    await message.answer(text=LEXICON[data["language"]]['/start'],
                         reply_markup=ReplyKeyboardRemove()
                         )

# registration check
@router.message(~StateFilter(RegistrationForm.registration_completed))
async def process_nonregister(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=LEXICON[data["language"]]['unregistered'])

# /russian
@router.message(Command(commands="russian"))
async def process_russian_command(message: Message, state: FSMContext):
    await state.update_data(language="RU")
    data = await state.get_data()
    await message.answer(text=LEXICON[data["language"]]['/russian'])

# /english
@router.message(Command(commands="english"))
async def process_english_command(message: Message, state: FSMContext):
    await state.update_data(language="EN")
    data = await state.get_data()
    await message.answer(text=LEXICON[data["language"]]['/english'])

# /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(text=LEXICON[data["language"]]['/help'])

# /name
@router.message(Command(commands="name"))
async def process_name_command(message: Message, state: FSMContext):
    await state.update_data(nametype="name")
    data = await state.get_data()
    await message.answer(text=LEXICON[data["language"]]["/name"],
                         parse_mode="html")

# /smiles
@router.message(Command(commands="smiles"))
async def process_name_command(message: Message, state: FSMContext):
    await state.update_data(nametype="smiles")
    data = await state.get_data()
    await message.answer(text=LEXICON[data["language"]]["/smiles"],
                         parse_mode="html")

# Отработчик названий
@router.message(F.text[0] != "/")
async def process_get_properties(message: Message, state: FSMContext, bot: Bot):
    # Заявленное название вещества
    name = message.text
    # Получение информации том, какой nametype выбран у пользователя
    data = await state.get_data()
    nametype = data["nametype"]
    # Получение информации по веществу и статусу ответа
    response_data, status = await get_properties(nametype, name)
    
    # Обработка статуса
    match status:
        case 200:
            molecule_name = response_data["Name"]
            molecule_image = response_data["Image"]
            molecule_keyboard = create_molecule_keyboard(response_data=response_data)
            await message.answer_photo(
                photo=molecule_image,
                caption=LEXICON[data["language"]]["finder_200"].format(html_formation(molecule_name)),
                reply_markup=molecule_keyboard,
                parse_mode="html"
                )
        case 400:
            await message.answer(text=LEXICON[data["language"]]["finder_400"])
        case 404:
            await message.answer(text=LEXICON[data["language"]]["finder_404"])

# callback r"select:+"
@router.callback_query(F.data.startswith("select:"))
async def process_select_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    # Получение информации по веществу по CID
    response_data, _ = await get_properties("cid", callback.data.split(":")[1])
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
        await callback.answer(text=LEXICON[data["language"]]["answer_too_long"])
        await bot.send_message(chat_id=callback.from_user.id, text=answer)