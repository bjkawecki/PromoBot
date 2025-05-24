from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_inline_keyboard(link) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Jetzt bestellen",
                    url=link,
                )
            ]
        ]
    )
    return keyboard
