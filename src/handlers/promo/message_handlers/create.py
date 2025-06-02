from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from PIL import Image

from keyboards.common import get_abort_keyboard
from keyboards.seller.promo import get_confirm_create_promo_keyboard
from services.s3 import upload_image_to_s3
from states.seller import PromoState
from utils.validation import validate_and_resize_image

router = Router()


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
