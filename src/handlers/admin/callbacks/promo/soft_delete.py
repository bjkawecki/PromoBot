from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.promos import set_promo_status_to_deleted
from keyboards.admin.manage_promos import get_confirm_soft_delete_promo_keyboard
from keyboards.common import get_main_menu_keyboard

router = Router()


@router.callback_query(F.data == "admin_soft_delete_promo")
async def admin_soft_delete_promo_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    promo = data.get("promo")
    display_name = promo.get("display_name")
    promo_id = promo.get("promo_id")
    keyboard = get_confirm_soft_delete_promo_keyboard(promo_id)

    await callback.message.answer(
        f"❗️Bist du sicher, dass du die Promo <b>'{display_name}'</b> als 'gelöscht' markieren willst?",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data == "confirm_soft_delete_promo")
async def seller_delete_execute(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    promo = data.get("promo")
    seller_id = promo.get("seller_id")
    promo_id = promo.get("promo_id")
    display_name = promo.get("display_name")

    try:
        _ = set_promo_status_to_deleted(promo_id, seller_id)
        if _:
            await callback.message.edit_text(
                f"✅ Promo '{display_name}' wurde gelöscht.",
                reply_markup=get_main_menu_keyboard(),
            )
        else:
            raise Exception
    except Exception as e:
        await callback.message.edit_text(f"❌ Fehler beim Löschen: {e}")
    await state.clear()
    await callback.answer()
