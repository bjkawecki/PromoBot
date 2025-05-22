from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.order import (
    get_cancel_enter_order_info_keyboard,
    get_finish_enter_order_info_keyboard,
)
from states.order import OrderState

router = Router()


@router.callback_query(F.data == "enter_order_info")
async def enter_order_info(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "▶️ *Bestellvorgang gestartet\\.*\n\n"
        "Wir benötigen eine Versandadresse\\.\n\n"
        "*Bitte Name eingeben:*\n\n",
        reply_markup=get_cancel_enter_order_info_keyboard(),
        parse_mode="MarkdownV2",
    )
    await state.set_state(OrderState.name)


@router.message(OrderState.name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()
    name = data.get("name")
    await message.answer(
        f"*Eingabe\n\n*Name: {name}\n\n*Straße und Hausnummer:*",
        reply_markup=get_cancel_enter_order_info_keyboard(),
        parse_mode="MarkdownV2",
    )
    await state.set_state(OrderState.street_address)


@router.message(OrderState.street_address)
async def get_street_adress(message: Message, state: FSMContext):
    await state.update_data(street_address=message.text)
    data = await state.get_data()
    name = data.get("name")
    street_address = data.get("street_address")
    await message.answer(
        f"*Eingabe\n\n*Name: {name}\nStraße: {street_address}\n\n*Postleitzahl und Stadt:*",
        reply_markup=get_cancel_enter_order_info_keyboard(),
        parse_mode="MarkdownV2",
    )
    await state.set_state(OrderState.city)


@router.message(OrderState.city)
async def get_city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    data = await state.get_data()
    name = data.get("name")
    street_address = data.get("street_address")
    city = data.get("city")
    await message.answer(
        f"*Eingabe\n\n*Name: {name}\nStraße: {street_address}\nStadt: {city}\n\n*Wie viele Stück möchtest du bestellen?*",
        reply_markup=get_cancel_enter_order_info_keyboard(),
        parse_mode="MarkdownV2",
    )
    await state.set_state(OrderState.quantity)


@router.message(OrderState.quantity)
async def get_quantity(message: Message, state: FSMContext):
    await state.update_data(quantity=message.text)

    # Zeige Zusammenfassung mit Inline-Buttons
    data = await state.get_data()
    summary = (
        f"*Bestellung:*\n\n"
        f"{data['quantity']}x Wald\\-T\\-Shirt\n\n"
        f"*Empfänger:*\n\n"
        f"{data['name']}\n"
        f"{data['street_address']}\n"
        f"{data['city']}\n\n"
    )

    await message.answer(
        summary,
        reply_markup=get_finish_enter_order_info_keyboard(),
        parse_mode="MarkdownV2",
    )
    await state.set_state(OrderState.confirm)


@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data.get("name")
    street_address = data.get("street_address")
    city = data.get("city")
    quantity = data.get("quantity")

    summary = (
        f"*Bestellung:*\n\n"
        f"{quantity}x Wald\\-T\\-Shirt\n\n"
        f"*Empfänger:*\n\n"
        f"{name}\n"
        f"{street_address}\n"
        f"{city}\n\n"
    )

    await callback.message.answer(
        summary,
        reply_markup=get_finish_enter_order_info_keyboard(),
        parse_mode="MarkdownV2",
    )
    # Hier dann Logik zur endgültigen Bestellbestätigung
    await state.clear()  # oder in nächsten State wechseln
