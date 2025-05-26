from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.repositories.sellers import update_seller_field
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from keyboards.seller import (
    get_optional_homepage_field_keyboard,
    get_optional_phone_field_keyboard,
)
from routers.seller.states import SellerState

router = Router()


@router.message(SellerState.business_name)
async def set_business_name(message: Message, state: FSMContext):
    user = message.from_user
    await state.update_data(business_name=message.text)
    update_seller_field(user.id, "business_name", message.text)
    await state.set_state(SellerState.display_name)
    await message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {message.text}\n"
        "\nBitte die <b>Bezeichnung</b> deines Unternehmens an, die <b>öffentlich sichbtar</b> sein soll:",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.display_name)
async def set_display_name(message: Message, state: FSMContext):
    user = message.from_user
    data = await state.get_data()
    await state.update_data(display_name=message.text)
    update_seller_field(user.id, "display_name", message.text)
    await state.set_state(SellerState.contact_email)
    await message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('business_name')}\n"
        f"Anzeigename: {message.text}\n"
        "\nBitte gib eine <b>geschäftliche E-Mail-Adresse</b> an:",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.contact_email)
async def set_contact_email_name(message: Message, state: FSMContext):
    user = message.from_user
    contact_email = message.text
    await state.update_data(contact_email=contact_email)
    data = await state.get_data()
    update_seller_field(user.id, "contact_email", contact_email)
    await state.set_state(SellerState.contact_phone)
    await message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('business_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {message.text}\n"
        "\nBitte gib eine <b>geschäftliche Telefonnummer</b> an (optional):",
        reply_markup=get_optional_phone_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.contact_phone)
async def set_contact_phone_name(message: Message, state: FSMContext):
    user = message.from_user
    contact_phone = message.text
    await state.update_data(contact_phone=contact_phone)
    data = await state.get_data()
    update_seller_field(user.id, "contact_phone", contact_phone)
    await state.set_state(SellerState.homepage)
    await message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('business_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        "\nBitte gib die <b>Homepage</b> deiner Firma an (optional):",
        reply_markup=get_optional_homepage_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.homepage)
async def set_homepage_name(message: Message, state: FSMContext):
    user = message.from_user
    homepage = message.text
    await state.update_data(homepage=homepage)
    data = await state.get_data()
    update_seller_field(user.id, "homepage", homepage)
    await state.set_state(SellerState.stripe_account_id)
    await message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('business_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email', '–')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"Homepage: {data.get('homepage', '–')}\n"
        "\nBitte gib die <b>ID deines Stripe-Kontos</b> an (optional, benötigt für das Starten von Promos):",
        reply_markup=get_optional_homepage_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.stripe_account_id)
async def set_stripe_account_id(message: Message, state: FSMContext):
    user = message.from_user
    stripe_account_id = message.text
    await state.update_data(stripe_account_id=stripe_account_id)
    data = await state.get_data()
    update_seller_field(user.id, "stripe_account_id", stripe_account_id)
    update_seller_field(user.id, "is_registered", True)
    await state.set_state(SellerState.confirm)
    await message.answer(
        "📝 Registrierung als Verkäufer\n\n"
        f"Firma: {data.get('business_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email', '–')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"Homepage: {data.get('homepage', '–')}\n"
        "\n✅ Deine Registrierung als Verkäufer ist abgeschlossen!\n\n"
        "Du kannst jetzt Produkte hinzufügen oder dein Profil weiter bearbeiten.",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
