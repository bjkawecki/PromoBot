from aiogram.fsm.state import State, StatesGroup


class SellerState(StatesGroup):
    username: State()
    business_name = State()
    display_name: State()
    contact_name = State()
    contact_email: State()
    phone_number = State()
    email = State()
    website = State()
    stripe_account_id = State()
