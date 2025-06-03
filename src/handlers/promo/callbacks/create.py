import uuid

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.promos import create_promotion
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from states.seller import PromoState

router = Router()


@router.callback_query(F.data == "create_promo")
async def start_create_promo(callback: CallbackQuery, state: FSMContext):
    promo_id = str(uuid.uuid4())
    seller_id = callback.from_user.id

    await state.set_data({"promo_id": promo_id, "seller_id": seller_id})
    await state.set_state(PromoState.display_name)

    await callback.message.edit_text(
        "📄 Neue Promo erstellen (1/9)\n\n<b>Wie heißt deine Promo?</b>\n\n"
        "Der Name wird als <b>Überschrift</b> in der Werbenachricht angezeigt.\n\n"
        "(Beispiel: 🎄 <i>Weihnachtsangebot 2025</i>)",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "confirm_create_promo")
async def confirm_create_promo_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_promo = {
        "promo_id": data.get("promo_id"),
        "seller_id": data.get("seller_id"),
        "display_name": data.get("display_name"),
        "display_message": data.get("display_message"),
        "description": data.get("description", ""),
        "price": data.get("price"),
        "shipping_costs": data.get("shipping_costs"),
        "channel_id": data.get("channel_id"),
        "start_date": data.get("start_date"),
        "end_date": data.get("end_date"),
        "image": data.get("image", ""),
        "promo_status": "inactive",
    }

    _, msg = create_promotion(data=new_promo)
    if _:
        await callback.message.edit_text(
            f"<b>✅ Neue Promo '{data.get('display_name')}' wurde erstellt</b>.",
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML",
        )
        await callback.answer()
        return
    await callback.message.edit_text(
        f"<b>{msg}</b>",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
