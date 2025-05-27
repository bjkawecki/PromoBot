from aiogram.fsm.state import State, StatesGroup


class SellerState(StatesGroup):
    company_name = State()
    display_name = State()
    contact_name = State()
    contact_email = State()
    contact_phone = State()
    website = State()
    stripe_account_id = State()
    confirm = State()


class EditSellerField(StatesGroup):
    waiting_for_new_value = State()
    confirm_update = State()
