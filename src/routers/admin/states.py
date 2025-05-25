from aiogram.fsm.state import State, StatesGroup


class AddSeller(StatesGroup):
    waiting_for_username = State()
