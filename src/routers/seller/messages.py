from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.repositories.sellers import update_seller_field
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from keyboards.seller import (
    get_optional_homepage_field_keyboard,
    get_optional_phone_field_keyboard,
)
from states.seller import SellerState

router = Router()


@router.message(SellerState.business_name)
async def set_business_name(message: Message, state: FSMContext):
    user = message.from_user
    await state.update_data(business_name=message.text)
    update_seller_field(user.id, "business_name", message.text)
    await state.set_state(SellerState.display_name)
    await message.answer(
        f"<b>Registrierung als Verkäufer</b>\n\n"
        f"Nutzername: @{user.username}"
        f"\nFirma: {message.text}"
        "\n\n📛 Wie lautet der öffentlich sichtbare Name deines Unternehmens (z. B. ohne Rechtsform)?",
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
        f"<b>Registrierung als Verkäufer</b>\n\n"
        f"Nutzername: @{user.username}"
        f"\nFirma: {data.get('business_name')}"
        f"\nAnzeigename: {message.text}"
        "\n\n📧 Bitte gib eine geschäftliche Kontakt-Email an:",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.contact_email)
async def set_contact_email_name(message: Message, state: FSMContext):
    user = message.from_user
    contact_email = message.text
    data = await state.get_data()
    await state.update_data(contact_email=contact_email)
    update_seller_field(user.id, "contact_email", contact_email)
    await state.set_state(SellerState.contact_phone)
    await message.answer(
        f"<b>Registrierung als Verkäufer</b>\n\n"
        f"Nutzername: @{user.username}"
        f"\nFirma: {data.get('business_name')}"
        f"\nAnzeigename: {data.get('display_name')}"
        f"\nE-Mail: {message.text}"
        "\n\n📞 Bitte gib eine geschäftliche Telefonnummer an (optional):",
        reply_markup=get_optional_phone_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.contact_phone)
async def set_contact_phone_name(message: Message, state: FSMContext):
    user = message.from_user
    contact_phone = message.text
    data = await state.get_data()
    await state.update_data(contact_phone=contact_phone)
    update_seller_field(user.id, "contact_phone", contact_phone)
    await state.set_state(SellerState.homepage)
    await message.answer(
        f"<b>Registrierung als Verkäufer</b>\n\n"
        f"Nutzername: @{user.username}"
        f"\nFirma: {data.get('business_name')}"
        f"\nAnzeigename: {data.get('display_name')}"
        f"\nE-Mail: {data.get('contact_email', '–')}"
        f"\nTelefon: {message.text}"
        "\n\n📞 Bitte gib die Homepage deiner Firma an (optional):",
        reply_markup=get_optional_homepage_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.homepage)
async def set_homepage_name(message: Message, state: FSMContext):
    user = message.from_user
    homepage = message.text
    data = await state.get_data()
    await state.update_data(homepage=homepage)
    update_seller_field(user.id, "homepage", homepage)
    await state.set_state(SellerState.stripe_account_id)
    await message.answer(
        f"<b>Registrierung als Verkäufer</b>\n\n"
        f"Nutzername: @{user.username}"
        f"\nFirma: {data.get('business_name')}"
        f"\nAnzeigename: {data.get('display_name')}"
        f"\nE-Mail: {data.get('contact_email', '–')}"
        f"\nTelefon: {data.get('contact_phone', '–')}"
        f"\nHomepage: {homepage}"
        "\n\n📞 Bitte gib deine Stripe-Konto-ID an (optional, nötig für das Anlegen von Werbeaktionen):",
        reply_markup=get_optional_homepage_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.stripe_account_id)
async def set_stripe_account_id(message: Message, state: FSMContext):
    user = message.from_user
    stripe_account_id = message.text
    data = await state.get_data()
    await state.update_data(stripe_account_id=stripe_account_id)
    update_seller_field(user.id, "stripe_account_id", stripe_account_id)
    await state.set_state(SellerState.confirm)
    await message.answer(
        f"<b>Registrierung als Verkäufer</b>\n\n"
        f"Nutzername: @{user.username}"
        f"\nFirma: {data.get('business_name')}"
        f"\nAnzeigename: {data.get('display_name')}"
        f"\nE-Mail: {data.get('contact_email', '–')}"
        f"\nTelefon: {data.get('contact_phone', '–')}"
        f"\nHomepage: {data.get('homepage', '–')}"
        "\n\n✅ Deine Registrierung als Verkäufer ist abgeschlossen!\n\n"
        "Du kannst jetzt Produkte hinzufügen oder dein Profil weiter bearbeiten.",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
