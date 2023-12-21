from aiogram.fsm.state import default_state, State, StatesGroup


class RegistrationForm(StatesGroup):
    # Состояние зарегистрированного в DB пользователя
    registration_completed = State()  