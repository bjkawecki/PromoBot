from aiogram import F, Router
from aiogram.types import CallbackQuery
from boto3.dynamodb.conditions import Attr

from database.repositories.sellers import count_all_items, count_items_filtered
from keyboards.common import get_main_menu_keyboard

router = Router()


@router.callback_query(F.data == "admin_stats")
async def statistics_callback(callback: CallbackQuery):
    await callback.answer("📊 Statistiken werden berechnet...")

    total = count_all_items()

    active = count_items_filtered(Attr("seller_status").eq("active"))
    inactive = count_items_filtered(Attr("seller_status").eq("inactive"))
    registered = count_items_filtered(Attr("is_registered").eq(True))

    # Nachricht senden
    message = (
        "<b>📈 PromoBot-Statistik</b>\n\n"
        f"🔢 Gesamtanzahl Verkäufer: <b>{total}</b>\n"
        f"✅ Aktiv: <b>{active}</b>\n"
        f"🚫 Inaktiv: <b>{inactive}</b>\n"
        f"📝 Registriert: <b>{registered}</b>\n"
    )

    await callback.message.edit_text(
        message, reply_markup=get_main_menu_keyboard(), parse_mode="HTML"
    )
