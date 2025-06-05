from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.repositories.sellers import update_seller_field
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from keyboards.seller.create import (
    get_optional_phone_field_keyboard,
    get_optional_website_field_keyboard,
)
from keyboards.seller.update import get_confirm_update_seller_field_keyboard
from messages.common.info import NO_VALIDATION_ERROR
from messages.seller.profile import (
    confirm_edit_field_message,
    register_add_company_name_message,
    register_add_contact_name_message,
    register_add_email_message,
    register_add_phone_message,
    register_add_stripe_account_id,
    register_add_website_message,
    registration_completed_message,
)
from states.seller import EditSellerField, SellerState
from utils.misc import SELLER_FIELD_LABELS, SELLER_VALIDATOR_METHODS_MAP
from utils.validation import (
    validate_email,
    validate_phone,
    validate_string_length_max_50,
    validate_stripe_account_id,
    validate_url,
)

router = Router()


@router.message(SellerState.company_name)
async def set_company_name(message: Message, state: FSMContext):
    user = message.from_user
    company_name = await validate_string_length_max_50(message, message.text)
    if not company_name:
        return
    await state.update_data(company_name=company_name)
    update_seller_field(user.id, "company_name", company_name)
    await state.set_state(SellerState.display_name)
    await message.edit_text(
        register_add_company_name_message(company_name),
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.display_name)
async def set_display_name(message: Message, state: FSMContext):
    user = message.from_user
    display_name = await validate_string_length_max_50(message, message.text)
    if not display_name:
        return
    data = await state.get_data()
    await state.update_data(display_name=display_name)
    update_seller_field(user.id, "display_name", display_name)
    await state.set_state(SellerState.contact_name)
    await message.edit_text(
        register_add_contact_name_message(data, display_name),
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.contact_name)
async def set_contact_name(message: Message, state: FSMContext):
    user = message.from_user
    contact_name = await validate_string_length_max_50(message, message.text)
    if not contact_name:
        return
    data = await state.get_data()
    await state.update_data(contact_name=contact_name)
    update_seller_field(user.id, "contact_name", contact_name)
    await state.set_state(SellerState.contact_email)
    await message.edit_text(
        register_add_email_message(data, contact_name),
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.contact_email)
async def set_contact_email_name(message: Message, state: FSMContext):
    user = message.from_user
    contact_email = validate_email(message, message.text)
    if not contact_email:
        return
    await state.update_data(contact_email=contact_email)
    data = await state.get_data()
    update_seller_field(user.id, "contact_email", contact_email)
    await state.set_state(SellerState.contact_phone)
    await message.edit_text(
        register_add_phone_message(data, contact_email),
        reply_markup=get_optional_phone_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.contact_phone)
async def set_contact_phone_name(message: Message, state: FSMContext):
    user = message.from_user
    contact_phone = validate_phone(message, message.text)
    if not contact_phone:
        return
    await state.update_data(contact_phone=contact_phone)
    data = await state.get_data()
    update_seller_field(user.id, "contact_phone", contact_phone)
    await state.set_state(SellerState.website)
    await message.edit_text(
        register_add_website_message(data, contact_phone),
        reply_markup=get_optional_website_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.website)
async def set_website_name(message: Message, state: FSMContext):
    user = message.from_user
    website = validate_url(message, message.text)
    if not website:
        return
    await state.update_data(website=website)
    data = await state.get_data()
    update_seller_field(user.id, "website", website)
    await state.set_state(SellerState.stripe_account_id)
    await message.edit_text(
        register_add_stripe_account_id(data),
        reply_markup=get_optional_website_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.stripe_account_id)
async def set_stripe_account_id(message: Message, state: FSMContext):
    user = message.from_user
    stripe_account_id = validate_stripe_account_id(message, message.text)
    if not stripe_account_id:
        return
    await state.update_data(stripe_account_id=stripe_account_id)
    data = await state.get_data()
    update_seller_field(user.id, "stripe_account_id", stripe_account_id)
    update_seller_field(user.id, "is_registered", True)
    await state.set_state(SellerState.confirm)
    await message.edit_text(
        registration_completed_message(data),
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(EditSellerField.waiting_for_new_value)
async def receive_new_field_value(message: Message, state: FSMContext):
    value = message.text.strip()
    data = await state.get_data()
    field = data["field"]
    field_label = SELLER_FIELD_LABELS.get(field, field)
    validator = SELLER_VALIDATOR_METHODS_MAP.get(field)

    if not validator:
        await message.answer(NO_VALIDATION_ERROR)
        return

    # Eingabe validieren
    validated_value = await validator(message, value)
    if validated_value is None:
        return  # Fehler wurde vom Validator behandelt

    # Erfolg: Nutzer bestätigen lassen
    await state.update_data(new_value=validated_value)
    await message.answer(
        confirm_edit_field_message(field_label, validated_value),
        reply_markup=get_confirm_update_seller_field_keyboard(),
        parse_mode="HTML",
    )
    await state.set_state(EditSellerField.confirm_update)
