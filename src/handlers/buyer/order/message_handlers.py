from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.buyer.order.common import show_order_summary
from keyboards.buyer.order import get_cancel_collect_order_details_keyboard
from states.buyer import OrderState

router = Router()


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
