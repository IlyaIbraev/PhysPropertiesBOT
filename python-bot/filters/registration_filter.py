from aiogram.fsm.state import default_state, State, StatesGroup


class RegistrationForm(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодейтсвия с пользователем
    registration_completed = State()        # Состояние ожидания регистрации