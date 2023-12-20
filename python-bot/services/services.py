import random
import requests
from config_data.config import load_config

from lexicon.lexicon_ru import LEXICON_RU

def get_properties(nametype, name) -> str:
    api = load_config().api
    response = requests.get(f"{api.url}:{api.port}/properties/{nametype}/{name}")
    # print(response.text)

    answer = ""

    for field in response.json():
        answer += str(field)
        answer += "\n"
        for value in response.json()[field]:
            answer += "   "+str(value)
            answer += "\n"

    return answer


# Функция, возвращающая случайный выбор бота в игре
def get_bot_choice() -> str:
    return random.choice(['rock', 'paper', 'scissors'])


# Функция, возвращающая ключ из словаря, по которому
# хранится значение, передаваемое как аргумент - выбор пользователя
def _normalize_user_answer(user_answer: str) -> str:
    for key in LEXICON_RU:
        if LEXICON_RU[key] == user_answer:
            break
    return key


# Функция, определяющая победителя
def get_winner(user_choice: str, bot_choice: str) -> str:
    user_choice = _normalize_user_answer(user_choice)
    rules = {'rock': 'scissors',
             'scissors': 'paper',
             'paper': 'rock'}
    if user_choice == bot_choice:
        return 'nobody_won'
    elif rules[user_choice] == bot_choice:
        return 'user_won'
    return 'bot_won'