from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.repositories.promos import get_promo_field, update_promo_field
from handlers.promo.callbacks.menu import seller_promo_list_menu_callback
from keyboards.seller.promo import (
    get_abort_edit_promo_field_keyboard,
    get_back_to_promo_detailview_keyboard,
    get_edit_promo_keyboard,
)
from states.seller import EditPromoField
from utils.misc import PROMO_FIELD_LABELS

router = Router()


@router.callback_query(F.data.startswith("edit_promo:"))
async def edit_promo_callback(callback: CallbackQuery, state: FSMContext):
    _, promo_id = callback.data.split(":")
    await state.update_data(promo_id=promo_id)
    keyboard = get_edit_promo_keyboard(promo_id, PROMO_FIELD_LABELS)
    await callback.message.edit_text(
        "<b>Promo bearbeiten</b>\n\nWähle ein Feld zum Bearbeiten:",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("edit_promo_field:"))
async def edit_promo_field_callback(callback: CallbackQuery, state: FSMContext):
    seller_id = callback.from_user.id
    _, field = callback.data.split(":")
    await state.update_data({"field": field})
    data = await state.get_data()
    promo_id = data.get("promo_id")
    field_value = get_promo_field(promo_id, seller_id, field)
    field_label = PROMO_FIELD_LABELS.get(field)
    await state.update_data(promo_id=promo_id, field=field)
    await callback.message.answer(
        f"<b>Änderung der Promo</b>\n\n"
        f"<b>{field_label}:</b> {field_value}\n\n"
        "📝 Bitte mach eine neue Eingabe.",
        reply_markup=get_abort_edit_promo_field_keyboard(promo_id),
        parse_mode="HTML",
    )
    await state.set_state(EditPromoField.waiting_for_field_value)


@router.callback_query(F.data.startswith("confirm_edit_promo"))
async def confirm_save_callback(callback: CallbackQuery, state: FSMContext):
    _, promo_id = callback.data.split(":")
    seller_id = callback.from_user.id
    data = await state.get_data()
    seller_id = callback.from_user.id
    field = data["field"]
    new_value = data["new_value"]
    try:
        update_promo_field(promo_id, seller_id, field, new_value)
        await callback.answer("✅ Promo wurde aktualisiert.")
    except Exception as e:
        await callback.message.edit_text(f"❌ Fehler beim Speichern: {e}")

    await seller_promo_list_menu_callback(callback)
    await state.clear()


@router.callback_query(F.data == "cancel_edit_promo")
async def cancel_edit_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    promo_id = data.get("promo_id")
    await callback.message.edit_text(
        "❌ Bearbeitung abgebrochen.",
        reply_markup=get_back_to_promo_detailview_keyboard(promo_id),
        parse_mode="HTML",
    )

    await state.clear()
