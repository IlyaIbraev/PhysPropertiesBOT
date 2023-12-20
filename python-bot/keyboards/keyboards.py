from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon_ru import LEXICON_RU

def create_molecule_keyboard(response_data: dict[str]):
    
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    for property in response_data["Properties"]:
        buttons.append(
            InlineKeyboardButton(
                text=property,
                callback_data="select:{}:{}".format(response_data["CID"], property)
            )
        )
    kb_builder.row(*buttons, width=2)
    return kb_builder.as_markup()