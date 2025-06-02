import uuid

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from config import verkaeufer_kanal_id
from database.repositories.promos import (
    create_promotion,
    get_promo_by_id,
    get_promo_field,
    get_promotions_by_seller_id,
    save_promo,
    update_promo_field,
)
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from keyboards.seller.promo import (
    get_abort_edit_promo_field_keyboard,
    get_back_to_promo_detailview_keyboard,
    get_confirm_toggle_promo_status_keyboard,
    get_edit_promo_keyboard,
    get_inline_keyboard,
    get_promo_detailview_keyboard,
    get_promo_list_keyboard,
    get_promo_menu_keyboard,
)
from states.seller import EditPromoField, PromoState
from utils.misc import PROMO_FIELD_LABELS, get_promo_details

router = Router()


@router.callback_query(F.data == "promo_menu")
async def promo_menu_callback(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "<b>📢 Promo-Menu</b>",
        reply_markup=get_promo_menu_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


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
        "end_data": data.get("end_date"),
        "image": data.get("image", ""),
        "status": "inactive",
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


@router.callback_query(F.data == "get_seller_promos")
async def display_seller_promos(callback: CallbackQuery, state: FSMContext):
    seller_id = callback.from_user.id
    promo_list = get_promotions_by_seller_id(seller_id)
    if not promo_list:
        await callback.answer("❌ Du hast noch keine Promo erstellt.")
        return
    keyboard = get_promo_list_keyboard(promo_list)
    await callback.message.edit_text("Wähle eine Promo aus:", reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "send_product_promo")
async def send_product_promo(callback: CallbackQuery, bot):
    link = await create_start_link(bot, "PROMO1")

    await bot.send_message(
        chat_id=verkaeufer_kanal_id,
        text="Unser neues Produkt XY! Bestelle jetzt bequem hier:",
        reply_markup=get_inline_keyboard(link),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("promo_detail:"))
async def promo_detailview_callback(callback: CallbackQuery):
    seller_id = callback.from_user.id
    promo_id = callback.data.split(":")[1]

    promo = get_promo_by_id(promo_id, seller_id)

    if not promo:
        await callback.answer("Promo nicht gefunden.")
        return
    status = promo.get("status", False)
    promo_details = get_promo_details(promo)

    keyboard = get_promo_detailview_keyboard(promo_id, status)

    await callback.message.answer(
        promo_details, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("promo_status:"))
async def toggle_promo_status_callback(callback: CallbackQuery):
    _, promo_id, action = callback.data.split(":")

    confirm_text = (
        "❗️<b>Bist du sicher, dass du die Promo "
        f"{'aktivieren' if action == 'a' else 'deaktivieren'} möchtest?</b>\n\n"
    )

    keyboard = get_confirm_toggle_promo_status_keyboard(promo_id, action)

    await callback.message.answer(
        confirm_text, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_toggle_promo"))
async def cancel_toggle_callback(callback: CallbackQuery):
    await callback.answer("❎ Vorgang abgebrochen.")
    await promo_detailview_callback(callback)


@router.callback_query(F.data.startswith("confirm_toggle_promo:"))
async def confirm_toggle_callback(callback: CallbackQuery):
    seller_id = callback.from_user.id
    _, promo_id, action = callback.data.split(":")

    promo = get_promo_by_id(promo_id=promo_id, seller_id=seller_id)
    if not promo:
        await callback.message.answer("❌ Promo nicht gefunden.")
        return

    promo["status"] = "active" if action == "a" else "inactive"
    save_promo(promo)

    status_text = (
        "✅ Promo wurde aktiviert."
        if promo["status"] == "active"
        else "🚫 Promo wurde deaktiviert."
    )
    await callback.answer(status_text)

    await promo_detailview_callback(callback)
    await callback.answer()


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
    await callback.message.edit_text(
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

    await promo_detailview_callback(callback)
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
