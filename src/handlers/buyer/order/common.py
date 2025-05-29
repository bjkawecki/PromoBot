from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.buyer.order import get_finish_collect_order_details_keyboard
from states.buyer import OrderState


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
