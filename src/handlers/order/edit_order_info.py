from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from keyboards.order import (
    get_edit_order_info_back_to_summary_keyboard,
    get_finish_enter_order_info_keyboard,
)
from states.order import OrderState

router = Router()


@router.callback_query(F.data == "edit_order_info")
async def enter_order_info(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "*Anpassung deiner Angaben\\.*\n\n*Bitte Name eingeben:*\n\n",
        reply_markup=get_edit_order_info_back_to_summary_keyboard(),
        parse_mode="MarkdownV2",
    )
    await state.set_state(OrderState.name)


@router.callback_query(F.data == "edit_name")
async def edit_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Bitte gib deinen neuen Namen ein:",
        reply_markup=get_edit_order_info_back_to_summary_keyboard(),
        parse_mode="MarkdownV2",
    )
    await state.set_state(OrderState.name)


@router.callback_query(F.data == "back_to_summary")
async def back_to_summary_callback(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    street_address = data.get("street_address")
    city = data.get("city")
    quantity = data.get("quantity")

    summary = (
        f"📦 Produkt: Wald-T-Shirt\n"
        f"👤 Name: {name}\n"
        f"🏠 Straße und Hausnummer: {street_address}\n"
        f"🏙️ PLZ und Stadt: {city}\n"
        f"🔢 Stückzahl: {quantity}\n\n"
        f"Stimmen die Eingaben?"
    )

    await call.message.edit_text(
        summary,
        reply_markup=get_finish_enter_order_info_keyboard(),
    )
    await call.answer()
