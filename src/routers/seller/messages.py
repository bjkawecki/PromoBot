from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.repositories.sellers import update_seller_field
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from keyboards.seller import (
    get_confirm_update_seller_field_keyboard,
    get_optional_phone_field_keyboard,
    get_optional_website_field_keyboard,
)
from routers.seller.states import EditSellerField, PromoState, SellerState
from utils.misc import FIELD_LABELS

router = Router()


@router.message(SellerState.company_name)
async def set_company_name(message: Message, state: FSMContext):
    user = message.from_user
    await state.update_data(company_name=message.text)
    update_seller_field(user.id, "company_name", message.text)
    await state.set_state(SellerState.display_name)
    await message.edit_text(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {message.text}\n"
        "\nBitte gib den <b>Anzeigename</b> deines Unternehmens an:",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.display_name)
async def set_display_name(message: Message, state: FSMContext):
    user = message.from_user
    data = await state.get_data()
    await state.update_data(display_name=message.text)
    update_seller_field(user.id, "display_name", message.text)
    await state.set_state(SellerState.contact_name)
    await message.edit_text(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
        f"Anzeigename: {message.text}\n"
        "\nBitte gib einen <b>Ansprechpartner</b> an:",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.contact_name)
async def set_contact_name(message: Message, state: FSMContext):
    user = message.from_user
    data = await state.get_data()
    await state.update_data(contact_name=message.text)
    update_seller_field(user.id, "contact_name", message.text)
    await state.set_state(SellerState.contact_email)
    await message.edit_text(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"Ansprechpartner: {message.text}\n"
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
    await message.edit_text(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
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
    await state.set_state(SellerState.website)
    await message.edit_text(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        "\nBitte gib die <b>Webseite</b> deiner Firma an (optional):",
        reply_markup=get_optional_website_field_keyboard(),
        parse_mode="HTML",
    )


@router.message(SellerState.website)
async def set_website_name(message: Message, state: FSMContext):
    user = message.from_user
    website = message.text
    await state.update_data(website=website)
    data = await state.get_data()
    update_seller_field(user.id, "website", website)
    await state.set_state(SellerState.stripe_account_id)
    await message.edit_text(
        "📝 Registrierung als Verkäufer\n\n"
        f"Unternehmen: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email', '–')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"website: {data.get('website', '–')}\n"
        "\nBitte gib die <b>ID deines Stripe-Kontos</b> an (optional, benötigt für das Starten von Promos):",
        reply_markup=get_optional_website_field_keyboard(),
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
    await message.edit_text(
        "📝 Registrierung als Verkäufer\n\n"
        f"Firma: {data.get('company_name')}\n"
        f"Anzeigename: {data.get('display_name')}\n"
        f"E-Mail: {data.get('contact_email', '–')}\n"
        f"Telefon: {data.get('contact_phone', '–')}\n"
        f"website: {data.get('website', '–')}\n"
        f"Stripe-Konto-ID: {data.get('stripe_account_id', '–')}\n"
        "\n✅ <b>Der Registriervorgang als Verkäufer ist abgeschlossen!<b>\n\n"
        "Du kannst nun <b>Promos</b> hinzufügen oder dein <b>Profil</b> bearbeiten.\n\n",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(EditSellerField.waiting_for_new_value)
async def receive_new_field_value(message: Message, state: FSMContext):
    await state.update_data(new_value=message.text)

    data = await state.get_data()
    field = data["field"]
    field_label = FIELD_LABELS.get(field, field)
    await message.edit_text(
        f"Neuer Wert für <b>{field_label}</b>:\n\n{message.text}\n\n<b>Bestätigen?</b>",
        reply_markup=get_confirm_update_seller_field_keyboard(),
        parse_mode="HTML",
    )
    await state.set_state(EditSellerField.confirm_update)


@router.message(PromoState.display_name)
async def get_display_name(message: Message, state: FSMContext):
    await state.update_data(display_name=message.text)
    await state.set_state(PromoState.display_message)

    await message.answer(
        "📄 Neue Promo erstellen\n\n<b>Erstelle eine Beschreibung</b>\n\n"
        "Dieser Text erscheint unter dem Titel in der Werbenachricht.\n\n"
        "(Beispiel: <i>Bestelle Buch XY mit Gratisversand.</i>)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )
