from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_molecule_keyboard(response_data: dict[str]):
    # Инициализация создателя клавиатуры
    kb_builder = InlineKeyboardBuilder()
    # Формирование списка кнопок
    buttons: list[InlineKeyboardButton] = []
    for property in response_data["Properties"]:
        buttons.append(
            InlineKeyboardButton(
                text=property,
                callback_data="select:{}:{}".format(response_data["CID"], property)
            )
        )
    # Их добавление в клавиатуру
    kb_builder.row(*buttons, width=2)
    # Возвращение кнопок в виде list[list][button]
    return kb_builder.as_markup()