from aiogram import F, Router
from aiogram.types import CallbackQuery
from boto3.dynamodb.conditions import Attr

from database.repositories.promos import count_all_promos, count_promos_filtered
from database.repositories.sellers import count_all_sellers, count_sellers_filtered
from keyboards.common import get_main_menu_keyboard
from messages.admin.stats import CALCULATING_STATS, returnStatsInfoMessage

router = Router()


@router.callback_query(F.data == "admin_stats")
async def statistics_callback(callback: CallbackQuery):
    await callback.answer(CALCULATING_STATS)

    stats = {}
    stats.update(
        {
            "total_sellers": count_all_sellers(),
            "registered_sellers": count_sellers_filtered(
                Attr("seller_status").eq("active")
            ),
            "active_sellers": count_sellers_filtered(
                Attr("seller_status").eq("inactive")
            ),
            "inactive_sellers": count_sellers_filtered(Attr("is_registered").eq(True)),
            "total_promos": count_all_promos(),
            "active_promos": count_promos_filtered(Attr("promo_status").eq("active")),
            "inactive_promos": count_promos_filtered(
                Attr("promo_status").eq("inactive")
            ),
            "deleted_promos": count_promos_filtered(Attr("promo_status").eq("deleted")),
        }
    )

    await callback.message.edit_text(
        returnStatsInfoMessage(stats),
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
