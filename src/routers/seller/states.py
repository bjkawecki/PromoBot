from aiogram.fsm.state import State, StatesGroup


class SellerState(StatesGroup):
    business_name = State()
    display_name = State()
    contact_name = State()
    contact_email = State()
    contact_phone = State()
    homepage = State()
    stripe_account_id = State()
    confirm = State()
