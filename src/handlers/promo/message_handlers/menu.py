from aiogram.types import Message

from database.repositories.promos import update_promo_field
from keyboards.seller.promo import get_promo_detailview_keyboard
from services.s3 import generate_presigned_url
from utils.misc import format_promo_details


async def send_promo_detailview(message: Message, promo: dict):
    file_id = promo.get("telegram_image_file_id")
    image_key = promo.get("image", "")
    seller_id = promo.get("seller_id")
    promo_id = promo.get("promo_id")
    caption = format_promo_details(promo)
    promo_status = promo.get("promo_status")

    try:
        if file_id:
            await message.answer_photo(
                photo=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_promo_detailview_keyboard(promo_id, promo_status),
            )
        elif image_key:
            image_url = generate_presigned_url(key=image_key)
            msg = await message.answer_photo(
                photo=image_url,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_promo_detailview_keyboard(promo_id, promo_status),
            )
            # Zwischenspeichern des neuen file_id für spätere Nutzung
            new_file_id = msg.photo[-1].file_id
            update_promo_field(
                field="telegram_image_file_id",
                new_value=new_file_id,
                seller_id=seller_id,
                promo_id=promo_id,
            )
        else:
            # 📭 Kein Bild vorhanden – nur Textnachricht senden
            await message.answer(
                text=caption,
                parse_mode="HTML",
                reply_markup=get_promo_detailview_keyboard(promo_id, promo_status),
            )
    except Exception as e:
        # Fehler beim Laden/Senden des Bildes – fallback auf Text
        await message.answer(
            f"⚠️ Bild konnte nicht geladen werden, zeige nur Text:\n\n{caption}",
            parse_mode="HTML",
            reply_markup=get_promo_detailview_keyboard(promo_id, promo_status),
        )
