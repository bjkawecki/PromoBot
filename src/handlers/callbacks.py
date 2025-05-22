from aiogram import Router
from aiogram.filters import Filter
from aiogram.types import CallbackQuery

from keyboards.inline import get_main_menu

router = Router()


class CallbackDataFilter(Filter):
    def __init__(self, expected_data: str) -> None:
        self.expected_data = expected_data

    async def __call__(self, callback: CallbackQuery) -> bool:
        return callback.data == self.expected_data


@router.callback_query(CallbackDataFilter("show_product"))
async def show_product_callback(callback: CallbackQuery):
    await callback.message.answer(
        "Hier ist das aktuell beworbene Produkt:\nProdukt XYZ\nPreis: 10 €",
        reply_markup=get_main_menu(),
    )
    await callback.answer()
