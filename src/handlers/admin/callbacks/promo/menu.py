from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.repositories.promos import (
    get_promo_by_promo_id,
    get_promotion_list,
    update_promo_field,
)
from keyboards.admin.manage_promos import (
    get_admin_promo_detailview_keyboard,
    get_admin_promo_list_keyboard,
)
from services.s3 import generate_presigned_url
from utils.misc import format_promo_details

router = Router()


@router.callback_query(F.data == "admin_promo_list_menu")
async def admin_promo_list_menu_callback(callback: CallbackQuery, state: FSMContext):
    promo_list = get_promotion_list()
    if not promo_list:
        await callback.answer("❌ Verkäufer hat noch keine Promos erstellt.")
        return
    keyboard = get_admin_promo_list_keyboard(promo_list)
    await callback.message.answer(
        "<b>📢 Promos</b>\n\nWähle eine Promo aus:",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("admin_promo_details_menu:"))
async def admin_promo_details_menu_callback(callback: CallbackQuery, state: FSMContext):
    promo_id = callback.data.split(":")[1]
    promo = get_promo_by_promo_id(promo_id)
    if not promo:
        await callback.answer("Promo nicht gefunden.")
        return
    await state.update_data(promo=promo)
    await admin_promo_details(callback.message, state)
    await callback.answer()


async def admin_promo_details(message: Message, state: FSMContext):
    data = await state.get_data()
    promo = data.get("promo")
    file_id = promo.get("telegram_image_file_id")
    image_key = promo.get("image", "")
    seller_id = promo.get("seller_id")
    promo_id = promo.get("promo_id")
    promo_status = promo.get("promo_status")
    caption = format_promo_details(promo)

    try:
        if file_id:
            await message.answer_photo(
                photo=file_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_admin_promo_detailview_keyboard(promo_status),
            )
        elif image_key:
            image_url = generate_presigned_url(key=image_key)
            msg = await message.answer_photo(
                photo=image_url,
                caption=caption,
                parse_mode="HTML",
                reply_markup=get_admin_promo_detailview_keyboard(promo_status),
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
                reply_markup=get_admin_promo_detailview_keyboard(promo_status),
            )
    except Exception as e:
        # Fehler beim Laden/Senden des Bildes – fallback auf Text
        await message.answer(
            f"Fehler: {e}"
            f"⚠️ Bild konnte nicht geladen werden, zeige nur Text:\n\n{caption}",
            parse_mode="HTML",
            reply_markup=get_admin_promo_detailview_keyboard(promo_status),
        )
