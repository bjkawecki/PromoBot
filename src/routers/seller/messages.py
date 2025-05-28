from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from PIL import Image

from database.repositories.sellers import update_seller_field
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from keyboards.seller import (
    get_confirm_create_promo_keyboard,
    get_confirm_update_seller_field_keyboard,
    get_optional_phone_field_keyboard,
    get_optional_website_field_keyboard,
)
from routers.seller.states import EditSellerField, PromoState, SellerState
from services.s3 import upload_image_to_s3, validate_and_resize_image
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
async def create_promo_display_name(message: Message, state: FSMContext):
    await state.update_data(display_name=message.text)
    await state.set_state(PromoState.display_message)

    await message.answer(
        "📄 Neue Promo erstellen (2/9)\n\n<b>Erstelle eine Nachricht</b>\n\n"
        "Dieser Text erscheint im Beitrag unter dem Titel.\n\n"
        "(Beispiel: <i>Bestelle Buch XY mit Gratisversand.</i>)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.display_message)
async def create_promo_price(message: Message, state: FSMContext):
    await state.update_data(display_message=message.text)
    await state.set_state(PromoState.price)
    await message.answer(
        "📄 Neue Promo erstellen (3/9)\n\n<b>Gib den Preis ohne Versandkosten an</b>\n\n"
        "Zahl mit maximal zwei Nachkommastellen, ohne Eurozeichen.\n\n"
        "(Beispiel: 12,99)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.price)
async def create_promo_shipping_costs(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(PromoState.shipping_costs)
    await message.answer(
        "📄 Neue Promo erstellen (4/9)\n\n<b>Gib die Versandkosten an</b>\n\n"
        "Zahl mit maximal zwei Nachkommastellen, ohne Eurozeichen.\n\n"
        "(Beispiel: 3,99)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.shipping_costs)
async def create_promo_description(message: Message, state: FSMContext):
    await state.update_data(shipping_costs=message.text)
    await state.set_state(PromoState.description)
    await message.answer(
        "📄 Neue Promo erstellen (5/9)\n\n<b>Erstelle eine Beschreibung</b>\n\n"
        "Ein detaillierte Beschreibung, die Käufer bei der Interaktion mit dem Bot abrufen können.\n\n"
        "(optional)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.description)
async def create_promo_channel_id(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(PromoState.channel_id)
    await message.answer(
        "📄 Neue Promo erstellen (6/9)\n\n<b>Gib die Kanal-Id an</b>\n\n"
        "Die Id des Ausgabekanals, in den der Bot die Promo posten soll.\n\n"
        "(Bot und Verkäufer müssen Zugriff auf diesen Kanal haben.)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.channel_id)
async def create_promo_start_date(message: Message, state: FSMContext):
    await state.update_data(channel_id=message.text)
    await state.set_state(PromoState.start_date)
    await message.answer(
        "📄 Neue Promo erstellen (7/9)\n\n<b>Gib das Startdatum ein</b>\n\n"
        "Ab diesem Datum darf die Promo im Ausgabekanal gepostet werden.\n\n"
        "Die Eingabe muss das Format DD.MM.YYYY haben. (Beispiel: 20.10.2025)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.start_date)
async def create_promo_end_date(message: Message, state: FSMContext):
    await state.update_data(start_date=message.text)
    await state.set_state(PromoState.end_date)
    await message.answer(
        "📄 Neue Promo erstellen (8/9)\n\n<b>Gib das Startdatum ein</b>\n\n"
        "Bis zu diesem Datum darf die Promo im Ausgabekanal gepostet werden.\n\n"
        "Die Eingabe muss das Format DD.MM.YYYY haben. (Beispiel: 01.11.2025)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.end_date)
async def create_promo_image(message: Message, state: FSMContext):
    await state.update_data(end_date=message.text)
    await state.set_state(PromoState.image)

    await message.answer(
        "📄 Neue Promo erstellen (9/9)\n\n<b>Füge ein Bild hinzu</b>\n\n"
        "Das Bild wird Teil der Werbenachricht.\n\n"
        "(Optional)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.image)
async def create_promo_confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    seller_id = data.get("seller_id") or "default_seller"
    promo_id = data.get("promo_id") or "123"

    photo = message.photo[-1]
    file = await message.bot.get_file(photo.file_id)
    file_stream = await message.bot.download_file(file.file_path)

    # Öffne Bild direkt
    img = Image.open(file_stream)
    img_format = img.format

    # Überprüfe Bildformat (jpeg, png)
    if img_format.lower() not in ("jpeg", "png"):
        await message.answer("Bitte sende ein JPEG- oder PNG-Bild.")
        return

    # Reset BytesIO Cursor, da read() den Pointer verschiebt
    file_stream.seek(0)
    image_bytes = file_stream.read()
    # Validieren und ggf. Größe anpassen
    image_bytes = validate_and_resize_image(image_bytes, max_width=1280, max_height=720)
    # Datei-Endung ableiten
    extension = "jpg" if img_format == "jpeg" else "png"
    # Upload zu S3
    path = upload_image_to_s3(image_bytes, seller_id, promo_id, extension)
    # Speichere URL im State oder DB
    await state.update_data(image=path)

    # Optional: nächsten State setzen oder Flow abschließen
    await state.set_state(PromoState.confirm)
    await message.answer(
        "Neue Promo erstellen: abgeschlossen\n\nEingaben speichern?",
        reply_markup=get_confirm_create_promo_keyboard(),
        parse_mode="HTML",
    )
