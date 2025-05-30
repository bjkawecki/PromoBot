from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.common import get_main_menu_keyboard

router = Router()


@router.callback_query(F.data == "display_product_description")
async def display_product_description(callback: CallbackQuery):
    await callback.message.answer(
        "*🔍 Produktbeschreibung*\n\n_Hier kann man mehr über das beworbene Produkt erfahren\\._",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()
