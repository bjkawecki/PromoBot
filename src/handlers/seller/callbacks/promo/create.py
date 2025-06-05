import uuid

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.promos import create_promotion
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from messages.seller.promo import CREATE_PROMO_MESSAGE, confirm_promo_created_message
from states.seller import PromoState
from utils.misc import format_new_promo

router = Router()


@router.callback_query(F.data == "create_promo")
async def start_create_promo(callback: CallbackQuery, state: FSMContext):
    promo_id = str(uuid.uuid4())
    seller_id = callback.from_user.id

    await state.set_data({"promo_id": promo_id, "seller_id": seller_id})
    await state.set_state(PromoState.display_name)

    await callback.message.edit_text(
        CREATE_PROMO_MESSAGE,
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "confirm_create_promo")
async def confirm_create_promo_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    new_promo = format_new_promo(data)

    _, msg = create_promotion(data=new_promo)
    if _:
        await callback.message.edit_text(
            confirm_promo_created_message({data.get("display_name")}),
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
