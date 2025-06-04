from aiogram import F, Router
from aiogram.types import CallbackQuery
from boto3.dynamodb.conditions import Attr

from database.repositories.promos import count_all_promos, count_promos_filtered
from database.repositories.sellers import count_all_sellers, count_sellers_filtered
from keyboards.common import get_main_menu_keyboard

router = Router()


@router.callback_query(F.data == "admin_stats")
async def statistics_callback(callback: CallbackQuery):
    await callback.answer("📊 Statistiken werden berechnet...")

    total_sellers = count_all_sellers()
    active_sellers = count_sellers_filtered(Attr("seller_status").eq("active"))
    inactive_sellers = count_sellers_filtered(Attr("seller_status").eq("inactive"))
    registered_sellers = count_sellers_filtered(Attr("is_registered").eq(True))

    total_promos = count_all_promos()
    active_promos = count_promos_filtered(Attr("promo_status").eq("active"))
    inactive_promos = count_promos_filtered(Attr("promo_status").eq("inactive"))
    deleted_promos = count_promos_filtered(Attr("promo_status").eq("deleted"))

    # Nachricht senden
    message = (
        "<b>PromoBot-Statistik</b>\n\n"
        f"<b>Verkäufer: {total_sellers}</b>\n"
        f"📝 Registriert: {registered_sellers}\n"
        f"✅ Aktiv: {active_sellers}\n"
        f"🚫 Gesperrt: {inactive_sellers}\n\n"
        f"<b>Promos: {total_promos}</b>\n"
        f"✅ Aktiv: {active_promos}\n"
        f"🚫 Inaktiv: {inactive_promos}\n"
        f"🗑 Gelöscht: {deleted_promos}"
    )

    await callback.message.edit_text(
        message, reply_markup=get_main_menu_keyboard(), parse_mode="HTML"
    )
