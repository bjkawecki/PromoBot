from aiogram.types import Message

from keyboards.seller.promo import get_promo_detailview_keyboard
from services.s3 import generate_presigned_url
from utils.misc import format_promo_details


async def send_promo_detailview(message: Message, promo: dict):
    image_key = promo.get("image")
    status = promo.get("status", False)
    promo_id = promo.get("promo_id", False)
    if not image_key:
        await message.answer("❌ Kein Bild vorhanden.")
        return
    try:
        image_url = generate_presigned_url(key=image_key)
        caption = format_promo_details(promo)

        await message.answer_photo(
            photo=image_url,
            caption=caption,
            parse_mode="HTML",
            reply_markup=get_promo_detailview_keyboard(promo_id, status),
        )
    except Exception as e:
        await message.answer(
            f"❌ Fehler beim Laden des Bildes:\n<code>{e}</code>", parse_mode="HTML"
        )
