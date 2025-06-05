from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from messages.keyboards.confirm import PROMO_LIST, SELLER_LIST_BUTTON, STATS


def get_admin_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=SELLER_LIST_BUTTON, callback_data="admin_sellers_menu"
                )
            ],
            [
                InlineKeyboardButton(
                    text=PROMO_LIST, callback_data="admin_promo_list_menu"
                )
            ],
            [InlineKeyboardButton(text=STATS, callback_data="admin_stats")],
        ]
    )
