from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_cancel_collect_order_details_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Abbrechen", callback_data="cancel_order")]
        ]
    )
    return keyboard


def get_finish_collect_order_details_keyboard() -> InlineKeyboardMarkup:
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
                    text="📝 Angaben ändern",
                    callback_data="edit_order_details",
                ),
            ],
            [
                InlineKeyboardButton(text="❌ Abbrechen", callback_data="cancel_order"),
            ],
        ]
    )
    return keyboard


def get_edit_order_details_back_to_summary_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔙 Zurück zur Bestellübersicht",
                    callback_data="back_to_summary",
                )
            ],
        ]
    )
    return keyboard


def get_edit_order_details_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Name", callback_data="edit_name")],
            [
                InlineKeyboardButton(
                    text="Straße/Hausnummer", callback_data="edit_street_adress"
                )
            ],
            [InlineKeyboardButton(text="PLZ/Ort", callback_data="edit_city")],
            [InlineKeyboardButton(text="Anzahl", callback_data="edit_quantity")],
            [
                InlineKeyboardButton(
                    text="🔙 Zurück zur Bestellübersicht",
                    callback_data="back_to_summary",
                )
            ],
        ]
    )
    return keyboard
