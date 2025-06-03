from aiogram.types import Message

from database.repositories.promos import update_promo_field
from keyboards.seller.promo import get_promo_detailview_keyboard
from services.s3 import generate_presigned_url
from utils.misc import format_promo_details


async def send_promo_detailview(message: Message, promo: dict, seller_id):
    file_id = promo.get("telegram_image_file_id")
    image_key = promo.get("image")
    status = promo.get("status", False)
    promo_id = promo.get("promo_id", False)
    if not image_key:
        await message.answer("❌ Kein Bild vorhanden.")
        return
    try:
        caption = format_promo_details(promo)
        if file_id:
            await message.answer_photo(
                photo=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_promo_detailview_keyboard(promo_id, status),
            )
        else:
            image_url = generate_presigned_url(key=image_key)
            msg = await message.answer_photo(
                photo=image_url,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_promo_detailview_keyboard(promo_id, status),
            )
            new_file_id = msg.photo[-1].file_id
            update_promo_field(
                field="telegram_image_file_id",
                new_value=new_file_id,
                seller_id=seller_id,
                promo_id=promo_id,
            )
    except Exception as e:
        await message.answer(
            f"❌ Fehler beim Laden des Bildes:\n<code>{e}</code>", parse_mode="HTML"
        )
