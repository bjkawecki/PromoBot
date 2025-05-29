from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from handlers.buyer.order.common import show_order_summary
from keyboards.buyer.order import (
    get_cancel_collect_order_details_keyboard,
    get_edit_order_details_back_to_summary_keyboard,
    get_edit_order_details_keyboard,
)
from keyboards.buyer.start import get_main_menu_deeplink
from messages.welcome_text import welcome_text
from states.buyer import OrderState

router = Router()


@router.callback_query(F.data == "collect_order_details")
async def collect_order_details(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "▶️ *Bestellvorgang gestartet\\.*\n\n"
        "Wir benötigen eine Versandadresse\\.\n\n"
        "*Bitte Name eingeben:*\n\n",
        reply_markup=get_cancel_collect_order_details_keyboard(),
        parse_mode="MarkdownV2",
    )
    await state.set_state(OrderState.name)
    await callback.answer()


@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    await show_order_summary(callback, state)
    await callback.answer()
    # Hier dann Logik zur endgültigen Bestellbestätigung
    # await state.clear()  # oder in nächsten State wechseln


@router.callback_query(F.data == "cancel_order")
async def cancel_order(callback: CallbackQuery, state: FSMContext):
    await state.clear()  # FSM Zustand zurücksetzen
    await callback.message.edit_text("🚫 Bestellung abgebrochen.")

    # Optional: Zurück zum Startmenü
    await callback.message.answer(
        welcome_text,
        reply_markup=get_main_menu_deeplink(),
        parse_mode="MarkdownV2",
    )


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
