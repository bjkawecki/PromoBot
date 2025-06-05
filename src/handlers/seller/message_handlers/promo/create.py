from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from PIL import Image

from keyboards.seller.promo import (
    get_back_to_promo_menu_keyboard,
    get_confirm_create_promo_keyboard,
)
from messages.seller.promo import (
    CONFIRM_SAVE_PROMO_MESSAGE,
    PROMO_ADD_CHANNEL_ID,
    PROMO_ADD_DESCRIPTION,
    PROMO_ADD_END_DATE,
    PROMO_ADD_IMAGE,
    PROMO_ADD_MESSAGE,
    PROMO_ADD_PRICE,
    PROMO_ADD_SHIPPING_COSTS,
    PROMO_ADD_START_DATE,
    PROMO_IMAGE_FORMAT_ERROR,
    PROMO_VALIDATE_PRICE_ANSWER,
    promo_validate_description_answer,
    promo_validate_message_answer,
    promo_validate_name_answer,
)
from services.s3 import upload_image_to_s3
from states.seller import PromoState
from utils.validation import (
    is_valid_length,
    validate_and_resize_image,
    validate_date,
    validate_decimal,
    validate_telegram_username,
)

router = Router()


@router.message(PromoState.display_name)
async def create_promo_display_name(message: Message, state: FSMContext):
    display_name = message.text.strip()
    max_length = 50
    if not is_valid_length(display_name, min_length=3, max_length=max_length):
        await message.answer(
            promo_validate_name_answer(max_length),
            reply_markup=get_back_to_promo_menu_keyboard(),
        )
        return
    await state.update_data(display_name=display_name)
    await state.set_state(PromoState.display_message)
    await message.answer(
        PROMO_ADD_MESSAGE,
        reply_markup=get_back_to_promo_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.display_message)
async def create_promo_price(message: Message, state: FSMContext):
    display_message = message.text.strip()
    max_length = 100
    if not is_valid_length(display_message, min_length=3, max_length=max_length):
        await message.answer(promo_validate_message_answer(max_length))
        return
    await state.update_data(display_message=display_message)
    await state.set_state(PromoState.price)
    await message.answer(
        PROMO_ADD_PRICE,
        reply_markup=get_back_to_promo_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.price)
async def create_promo_shipping_costs(message: Message, state: FSMContext):
    price = message.text.strip()
    price = await validate_decimal(message, price, "Preis")
    if price is None:
        await message.answer(PROMO_VALIDATE_PRICE_ANSWER)
        return
    await state.update_data(price=price)
    await state.set_state(PromoState.shipping_costs)
    await message.answer(
        PROMO_ADD_SHIPPING_COSTS,
        reply_markup=get_back_to_promo_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.shipping_costs)
async def create_promo_description(message: Message, state: FSMContext):
    shipping_costs = message.text.strip()
    shipping_costs = await validate_decimal(message, shipping_costs, "Versandkosten")
    if shipping_costs is None:
        return
    await state.update_data(shipping_costs=shipping_costs)
    await state.set_state(PromoState.description)
    await message.answer(
        PROMO_ADD_DESCRIPTION,
        reply_markup=get_back_to_promo_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.description)
async def create_promo_channel_id(message: Message, state: FSMContext):
    description = message.text.strip()
    max_length = 100
    if not is_valid_length(description, min_length=3, max_length=max_length):
        await message.answer(
            promo_validate_description_answer(max_length),
            reply_markup=get_back_to_promo_menu_keyboard(),
        )
        return
    await state.update_data(description=description)
    await state.set_state(PromoState.channel_id)
    await message.answer(
        PROMO_ADD_CHANNEL_ID,
        reply_markup=get_back_to_promo_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.channel_id)
async def create_promo_start_date(message: Message, state: FSMContext):
    channel_id = message.text.strip()
    channel_id = await validate_telegram_username(message, channel_id, "Ausgabekanal")
    if channel_id is None:
        return
    await state.update_data(channel_id=channel_id)
    await state.set_state(PromoState.start_date)
    await message.answer(
        PROMO_ADD_START_DATE,
        reply_markup=get_back_to_promo_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.start_date)
async def create_promo_end_date(message: Message, state: FSMContext):
    start_date = message.text.strip()
    start_date = await validate_date(message, start_date, "Startdatum")
    if start_date is None:
        return
    await state.update_data(start_date=message.text)
    await state.set_state(PromoState.end_date)
    await message.answer(
        PROMO_ADD_END_DATE,
        reply_markup=get_back_to_promo_menu_keyboard(),
        parse_mode="HTML",
    )


@router.message(PromoState.end_date)
async def create_promo_image(message: Message, state: FSMContext):
    end_date = message.text.strip()
    end_date = await validate_date(message, end_date, "Enddatum")
    if end_date is None:
        return
    await state.update_data(end_date=end_date)
    await state.set_state(PromoState.image)

    await message.answer(
        PROMO_ADD_IMAGE,
        reply_markup=get_back_to_promo_menu_keyboard(),
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
        await message.answer(PROMO_IMAGE_FORMAT_ERROR)
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
        CONFIRM_SAVE_PROMO_MESSAGE,
        reply_markup=get_confirm_create_promo_keyboard(),
        parse_mode="HTML",
    )
