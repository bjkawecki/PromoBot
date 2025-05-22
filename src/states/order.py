from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    name = State()
    street_address = State()
    city = State()
    state = State()
    quantity = State()
    confirm = State()
