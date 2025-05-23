from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.start import get_back_to_start_keyboard

router = Router()


@router.callback_query(F.data == "display_product_description")
async def display_product_description(callback: CallbackQuery):
    await callback.message.answer(
        "*🔍 Produktbeschreibung*\n\n_Hier kann man mehr über das beworbene Produkt erfahren\\._",
        reply_markup=get_back_to_start_keyboard(),
        parse_mode="MarkdownV2",
    )
    await callback.answer()
