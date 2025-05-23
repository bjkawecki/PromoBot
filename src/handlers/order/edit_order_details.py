from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.order.collect_order_details import show_order_summary
from keyboards.order import (
    get_edit_order_details_back_to_summary_keyboard,
    get_edit_order_details_keyboard,
)
from states.order import OrderState

router = Router()


@router.callback_query(F.data == "edit_order_details")
async def edit_order_details(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "*📝 Änderung deiner Eingaben\\.*\n\nWas möchtest du ändern?",
        reply_markup=get_edit_order_details_keyboard(),
        parse_mode="MarkdownV2",
    )
    await state.set_state(OrderState.name)
    await callback.answer()


@router.callback_query(F.data == "edit_name")
async def edit_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.name)
    await state.update_data(edit_mode=True)
    await callback.message.edit_text(
        "Name ändern:",
        reply_markup=get_edit_order_details_back_to_summary_keyboard(),
        parse_mode="MarkdownV2",
    )


@router.callback_query(F.data == "edit_street_adress")
async def edit_street_adress(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.street_address)
    await state.update_data(edit_mode=True)
    await callback.message.edit_text(
        "Straße und Hausnummer ändern:",
        reply_markup=get_edit_order_details_back_to_summary_keyboard(),
        parse_mode="MarkdownV2",
    )


@router.callback_query(F.data == "edit_city")
async def edit_city(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.city)
    await state.update_data(edit_mode=True)
    await callback.message.edit_text(
        "PLZ und Ort ändern:",
        reply_markup=get_edit_order_details_back_to_summary_keyboard(),
        parse_mode="MarkdownV2",
    )


@router.callback_query(F.data == "edit_quantity")
async def edit_quantity(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.quantity)
    await state.update_data(edit_mode=True)
    await callback.message.edit_text(
        "Anzahl des Produkts ändern:",
        reply_markup=get_edit_order_details_back_to_summary_keyboard(),
        parse_mode="MarkdownV2",
    )


@router.callback_query(F.data == "back_to_summary")
async def back_to_summary(callback: CallbackQuery, state: FSMContext):
    await show_order_summary(callback, state)
    await callback.answer()
