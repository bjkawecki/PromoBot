from aiogram.fsm.state import State, StatesGroup


class AddSeller(StatesGroup):
    waiting_for_seller_telegram_id = State()
