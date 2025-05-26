from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from keyboards.buyer import (
    get_cancel_collect_order_details_keyboard,
    get_edit_order_details_back_to_summary_keyboard,
    get_edit_order_details_keyboard,
    get_finish_collect_order_details_keyboard,
)
from keyboards.start import get_main_menu_deeplink
from messages.welcome_text import welcome_text

router = Router()


class OrderState(StatesGroup):
    name = State()
    street_address = State()
    city = State()
    state = State()
    quantity = State()
    confirm = State()
    edit_mode = State()


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


@router.message(OrderState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    if data.get("edit_mode"):
        await state.update_data(edit_mode=None)
        await state.set_state(OrderState.confirm)
        await show_order_summary(message, state)
    else:
        name = data.get("name")
        await message.answer(
            f"*📫 Adresseingabe*\n\nName: {name}\n\n*Straße und Hausnummer:*",
            reply_markup=get_cancel_collect_order_details_keyboard(),
            parse_mode="MarkdownV2",
        )
        await state.set_state(OrderState.street_address)


@router.message(OrderState.street_address)
async def process_street_adress(message: Message, state: FSMContext):
    await state.update_data(street_address=message.text)
    data = await state.get_data()
    if data.get("edit_mode"):
        await state.update_data(edit_mode=None)
        await state.set_state(OrderState.confirm)
        await show_order_summary(message, state)
    else:
        name = data.get("name")
        street_address = data.get("street_address")
        await message.answer(
            f"*📫 Adresseingabe*\n\nName: {name}\nStraße: {street_address}\n\n*Postleitzahl und Ort:*",
            reply_markup=get_cancel_collect_order_details_keyboard(),
            parse_mode="MarkdownV2",
        )
        await state.set_state(OrderState.city)


@router.message(OrderState.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    if data.get("edit_mode"):
        await state.update_data(edit_mode=None)
        await state.set_state(OrderState.confirm)
        await show_order_summary(message, state)
    else:
        name = data.get("name")
        street_address = data.get("street_address")
        city = data.get("city")
        await message.answer(
            f"*📫 Adresseingabe*\n\nName: {name}\nStraße: {street_address}\nOrt: {city}\n\n*Wie viele Stück möchtest du bestellen?*",
            reply_markup=get_cancel_collect_order_details_keyboard(),
            parse_mode="MarkdownV2",
        )
        await state.set_state(OrderState.quantity)


@router.message(OrderState.quantity)
async def get_quantity(message: Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await show_order_summary(message, state)
    await state.set_state(OrderState.confirm)


@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    await show_order_summary(callback, state)
    await callback.answer()
    # Hier dann Logik zur endgültigen Bestellbestätigung
    # await state.clear()  # oder in nächsten State wechseln


async def show_order_summary(destination, state: FSMContext):
    data = await state.get_data()
    name = data.get("name", "_Name nicht angegeben_")
    street_address = data.get("street_address", "_Straße/Hausnummer nicht angegeben_")
    city = data.get("city", "_PLZ/Ort nicht angegeben_")
    quantity = data.get("quantity", "1")

    summary = (
        f"*📦 Bestellübersicht*\n\n"
        f"{quantity} x Wald\\-T\\-Shirt\n\n"
        f"*📫 Anschrift des Empfängers:*\n\n"
        f"{name}\n"
        f"{street_address}\n"
        f"{city}\n\n"
        f"*Fahre fort, wenn alle Angaben korrekt sind\\.*"
    )

    if isinstance(destination, CallbackQuery):
        await destination.message.answer(
            summary,
            reply_markup=get_finish_collect_order_details_keyboard(),
            parse_mode="MarkdownV2",
        )
    elif isinstance(destination, Message):
        await destination.answer(
            summary,
            reply_markup=get_finish_collect_order_details_keyboard(),
            parse_mode="MarkdownV2",
        )

    await state.set_state(OrderState.confirm)


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
