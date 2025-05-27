from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.sellers import get_seller_by_id, update_seller_field
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from keyboards.seller import (
    get_abort_update_seller_keyboard,
    get_back_to_update_seller_keyboard,
    get_optional_stripe_id_field_keyboard,
    get_optional_website_field_keyboard,
    get_update_seller_profile_keyboard,
)
from routers.seller.states import EditSellerField, SellerState
from utils.misc import FIELD_LABELS

router = Router()


@router.callback_query(F.data == "register_seller")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user
    update_seller_field(telegram_user_id=user.id, field="username", value=user.username)
    await state.set_state(SellerState.company_name)
    await callback.message.answer(
        "📜 Registrierung als Verkäufer\n\n"
        "Bitte gib den <b>Unternehmensnamen</b> oder die <b>Geschäftsbezeichnung</b> an:",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "skip_add_phone")
async def skip_add_phone_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(SellerState.website)
    await callback_query.message.answer(
        "📜 Registrierung als Verkäufer\n\n"
        f"Firma: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"\nBitte gib die website deiner Firma an (optional):",
        reply_markup=get_optional_website_field_keyboard(),
        parse_mode="HTML",
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "skip_add_website")
async def skip_add_website_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(SellerState.stripe_account_id)
    await callback_query.message.answer(
        "📜 Registrierung als Verkäufer\n\n"
        f"Firma: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"website: {data.get('website', '–')}\n"
        "\nBitte gib die <b>ID deines Stripe-Kontos</b> an (optional, benötigt für das Starten von Promos):",
        reply_markup=get_optional_stripe_id_field_keyboard(),
        parse_mode="HTML",
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "skip_add_stripe_id")
async def skip_add_stripe_id_handler(callback_query: CallbackQuery, state: FSMContext):
    user = callback_query.from_user
    data = await state.get_data()
    update_seller_field(user.id, "is_registered", True)
    await state.set_state(SellerState.confirm)
    register_success_message = (
        "📜 Registrierung als Verkäufer\n\n"
        f"Firma: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"website: {data.get('website', '–')}\n"
    )

    if data.get("stripe_account_id"):
        register_success_message += (
            f"Stripe-Konto-ID: {data.get('stripe_account_id')}\n"
            "\n✅ <b>Der Registriervorgang als Verkäufer ist abgeschlossen!<b>\n\n"
            "Du kannst nun <b>Promos</b> hinzufügen oder dein <b>Profil</b> bearbeiten.\n\n"
        )
    else:
        register_success_message += (
            "Stripe-Konto-ID: – \n"
            "\n✅ <b>Der Registriervorgang als Verkäufer ist abgeschlossen!<b>\n\n"
            "Du kannst nun <b>Promos</b> hinzufügen oder dein <b>Profil</b> bearbeiten.\n\n"
            "Denk daran, dass du eine gültige <b>Stripe-Konto-ID</b> angeben musst, um Promos starten zu können."
        )

    await callback_query.message.answer(
        register_success_message,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback_query.answer()


@router.callback_query(F.data == "update_seller_profile")
async def update_seller_profile_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        text="📝 Änderung deines Profils\\.\n\nWas möchtest du ändern?",
        reply_markup=get_update_seller_profile_keyboard(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("edit_seller_profile_field:"))
async def edit_seller_profile_field_callback(
    callback: CallbackQuery, state: FSMContext
):
    _, field = callback.data.split(":")
    seller = get_seller_by_id(callback.from_user.id)
    current_value = seller.get(field, "Kein Wert gesetzt")

    await state.update_data(field=field)
    field_label = FIELD_LABELS.get(field, field)
    await callback.message.edit_text(
        f"<b>{field_label}</b>:\n\n{current_value}\n\n📝 Bitte gib den neuen Wert ein:",
        reply_markup=get_abort_update_seller_keyboard(),
        parse_mode="HTML",
    )
    await state.set_state(EditSellerField.waiting_for_new_value)


@router.callback_query(
    lambda c: c.data == "confirm_seller_profile_update_field",
    EditSellerField.confirm_update,
)
async def confirm_seller_profile_update_field(
    callback: CallbackQuery, state: FSMContext
):
    data = await state.get_data()
    field = data["field"]
    new_value = data["new_value"]
    field_label = FIELD_LABELS.get(field, field)
    update_seller_field(callback.from_user.id, field, new_value)

    await callback.message.edit_text(
        f"✅ <b>{field_label}</b> wurde aktualisiert auf:\n\n{new_value}",
        reply_markup=get_back_to_update_seller_keyboard(),
        parse_mode="HTML",
    )
    await state.clear()
