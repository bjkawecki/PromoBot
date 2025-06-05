from aiogram import F, Router
from aiogram.types import CallbackQuery

from keyboards.common import get_main_menu_keyboard
from messages.buyer.menu import product_details_menu_message

router = Router()


@router.callback_query(F.data == "product_details_menu")
async def product_details_menu_callback(callback: CallbackQuery):
    await callback.message.answer(
        product_details_menu_message,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()
