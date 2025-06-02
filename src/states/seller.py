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


class PromoState(StatesGroup):
    promo_id = State()
    display_name = State()
    display_message = State()
    description = State()

    image = State()
    price = State()
    shipping_costs = State()
    channel_id = State()
    start_date = State()
    end_date = State()
    options = State()
    confirm = State()


class EditPromoField(StatesGroup):
    waiting_for_field_value = State()
    confirm_new_value = State()
