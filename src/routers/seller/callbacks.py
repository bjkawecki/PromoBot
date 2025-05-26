from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.repositories.sellers import update_seller_field
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from keyboards.seller import (
    get_optional_homepage_field_keyboard,
    get_optional_stripe_id_field_keyboard,
)
from routers.seller.states import SellerState

router = Router()


@router.callback_query(F.data == "register_seller")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user
    update_seller_field(telegram_user_id=user.id, field="username", value=user.username)
    await state.set_state(SellerState.business_name)
    await callback.message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        "Bitte gib den <b>Unternehmensnamen</b> oder die <b>Geschäftsbezeichnung</b> an:",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "skip_add_phone")
async def skip_add_phone_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(SellerState.homepage)
    await callback_query.message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        f"Firma: {data.get('business_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"\nBitte gib die Homepage deiner Firma an (optional):",
        reply_markup=get_optional_homepage_field_keyboard(),
        parse_mode="HTML",
    )
    await callback_query.answer()


@router.callback_query(lambda c: c.data == "skip_add_homepage")
async def skip_add_homepage_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_state(SellerState.stripe_account_id)
    await callback_query.message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        f"Firma: {data.get('business_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"Homepage: {data.get('homepage', '–')}\n"
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
    await callback_query.message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        f"Firma: {data.get('business_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"Homepage: {data.get('homepage', '–')}\n"
        f"Stripe-ID: {data.get('stripe_account_id', '–')}\n"
        "\n✅ Deine Registrierung als Verkäufer ist abgeschlossen!\n\n"
        "Du kannst jetzt Produkte hinzufügen oder dein Profil weiter bearbeiten.",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback_query.answer()
