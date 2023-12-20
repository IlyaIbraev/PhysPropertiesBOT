from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Bot

from keyboards.keyboards import create_molecule_keyboard
from lexicon.lexicon_ru import LEXICON_RU
from services.services import get_bot_choice, get_properties, get_winner
from filters.registration_filter import RegistrationForm

router = Router()


# /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text=str(await state.get_state()))
    await state.set_state(RegistrationForm.registration_completed)
    await state.update_data(nametype="name")
    await message.answer(text=LEXICON_RU['/start'])
    await message.answer(text=str(await state.get_data()))
    await message.answer(text=str(await state.get_state()))

# registration check
@router.message(~StateFilter(RegistrationForm.registration_completed))
async def process_nonregister(message: Message, state: FSMContext):
    await message.answer("reg check")
    await message.answer(text=str(await state.get_data()))

# /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['/help'])
    await message.answer(text=str(await state.get_data()))

# /name
@router.message(Command(commands="name"))
async def process_name_command(message: Message, state: FSMContext):
    await state.update_data(nametype="name")
    await message.answer(text=LEXICON_RU["/name"])
    await message.answer(text=str(await state.get_data()))

# /smiles
@router.message(Command(commands="smiles"))
async def process_name_command(message: Message, state: FSMContext):
    await state.update_data(nametype="smiles")
    await message.answer(text=LEXICON_RU["/smiles"])
    await message.answer(text=str(await state.get_data()))

# Название
@router.message(F.text[0] != "/")
async def process_get_properties(message: Message, state: FSMContext):
    name = message.text
    user_data = await state.get_data()
    nametype = user_data["nametype"]
    response_data, status = get_properties(nametype, name)

    # properties = response_data["Properties"]
    molecule_name = response_data["Name"]
    molecule_image = response_data["Image"]

    molecule_keyboard = create_molecule_keyboard(response_data=response_data)

    print(status, type(status))
    match status:
        case 200:
            await message.answer(
                text="{}\n{}".format(molecule_name, molecule_image),
                reply_markup=molecule_keyboard
                )
        case 400:
            await message.answer("error")
        case 404:
            await message.answer("not found")
            
@router.callback_query(F.data.startswith("select:"))
async def process_select_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    
    response_data, status = get_properties("cid", callback.data.split(":")[1])

    property = response_data["Properties"][callback.data.split(":")[2]]

    answer = [callback.data.split(":")[2]]

    for elem in property:
        answer.append(elem)

    answer = "\n   ".join(map(str, answer))
        

    # await callback.answer(text=str(answer), show_alert=True)
    try:
        await callback.answer(answer, show_alert=True)
    except:
        await callback.answer("Response too long to show as alert")
        await bot.send_message(chat_id=callback.from_user.id, text=answer)