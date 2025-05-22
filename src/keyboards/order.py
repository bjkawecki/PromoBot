from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_cancel_enter_order_info_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Abbrechen", callback_data="cancel_order")]
        ]
    )
    return keyboard


def get_finish_enter_order_info_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Weiter zur Zahlung",
                    callback_data="start_payment",
                )
            ],
            [
                InlineKeyboardButton(
                    text="📝 Eingaben ändern",
                    callback_data="edit_order_info",
                ),
            ],
            [
                InlineKeyboardButton(text="❌ Abbrechen", callback_data="cancel_order"),
            ],
        ]
    )
    return keyboard


def get_edit_order_info_back_to_summary_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Zurück", callback_data="confirm_order")],
        ]
    )
    return keyboard
