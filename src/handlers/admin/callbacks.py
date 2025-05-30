from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import ADMIN_USER_NAME
from database.repositories.sellers import (
    delete_seller_by_id,
    get_all_sellers,
    get_seller_by_id,
    save_seller,
)
from keyboards.admin.manage_seller import (
    get_confirm_delete_seller_keyboard,
    get_confirm_toggle_keyboard,
    get_seller_detail_keyboard,
    get_seller_list_keyboard,
)
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from states.admin import AddSeller
from utils.misc import get_seller_info

router = Router()


@router.callback_query(F.data == "add_seller")
async def add_seller_callback(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.username != ADMIN_USER_NAME:
        await callback.answer("Keine Berechtigung.", show_alert=True)
        return

    await callback.message.edit_text(
        "Neuen Verkäufer hinzufügen\n\n"
        "Bitte gib die *Telegram\\-Nutzer\\-ID* des neuen Verkäufers an:",
        parse_mode="MarkdownV2",
        reply_markup=get_abort_keyboard(),
    )
    await callback.answer()
    await state.set_state(AddSeller.waiting_for_username)


@router.callback_query(F.data == "display_sellers")
async def display_sellers_callback(callback: CallbackQuery):
    seller_list = get_all_sellers()

    if not seller_list:
        await callback.answer("❌ Es sind noch keine Verkäufer registriert.")
        return

    keyboard = get_seller_list_keyboard(seller_list)
    await callback.message.edit_text(
        "Wähle einen Verkäufer aus:", reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(F.data.startswith("seller_detail:"))
async def seller_detail_callback(callback: CallbackQuery):
    print(f"DEBUG: callback.data = {repr(callback.data)}")

    telegram_id = callback.data.split(":")[1]

    seller = get_seller_by_id(int(telegram_id))
    if not seller:
        await callback.message.answer("Verkäufer nicht gefunden.")
        return

    seller_info = get_seller_info(seller)

    keyboard = get_seller_detail_keyboard(telegram_id, seller.get("active", False))

    await callback.message.edit_text(
        seller_info, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("seller_toggle:"))
async def seller_toggle_callback(callback: CallbackQuery):
    _, telegram_id, action = callback.data.split(":")
    seller = get_seller_by_id(int(telegram_id))

    seller_info = get_seller_info(seller)

    confirm_text = (
        "❗️<b>Bist du sicher, dass du den folgenden Verkäufer "
        f"{'aktivieren' if action == 'activate' else 'deaktivieren'} möchtest?</b>\n\n"
        f"{seller_info}"
    )

    keyboard = get_confirm_toggle_keyboard(telegram_id, action)

    await callback.message.edit_text(
        confirm_text, reply_markup=keyboard, parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_toggle_seller_is_active"))
async def cancel_toggle_callback(callback: CallbackQuery):
    await callback.answer("❎ Vorgang abgebrochen.")
    await seller_detail_callback(callback)
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_toggle_seller_is_active:"))
async def confirm_toggle_callback(callback: CallbackQuery):
    _, telegram_id, action = callback.data.split(":")

    seller = get_seller_by_id(int(telegram_id))
    if not seller:
        await callback.message.answer("❌ Verkäufer nicht gefunden.")
        return

    seller["active"] = True if action == "activate" else False
    save_seller(seller)

    status_text = (
        "✅ Verkäufer wurde aktiviert."
        if seller["active"]
        else "🚫 Verkäufer wurde deaktiviert."
    )
    await callback.answer(status_text)

    await seller_detail_callback(callback)
    await callback.answer()


@router.callback_query(F.data.startswith("seller_delete:"))
async def seller_delete_confirm(callback: CallbackQuery):
    _, telegram_id = callback.data.split(":")
    seller = get_seller_by_id(int(telegram_id))
    seller_info = get_seller_info(seller)
    keyboard = get_confirm_delete_seller_keyboard(telegram_id)

    await callback.message.edit_text(
        f"❗️<b>Bist du sicher, dass du den folgenden Verkäufer löschen möchtest?</b>\n\n"
        f"{seller_info}",
        reply_markup=keyboard,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_delete_seller"))
async def cancel_delete_seller_callback(callback: CallbackQuery):
    await callback.answer("❎ Vorgang abgebrochen.")
    await seller_detail_callback(callback)
    await callback.answer()


@router.callback_query(F.data.startswith("seller_delete_confirm:"))
async def seller_delete_execute(callback: CallbackQuery):
    _, telegram_id = callback.data.split(":")
    seller = get_seller_by_id(int(telegram_id))

    if not seller:
        await callback.answer(
            f"❌ Verkäufer mit ID {telegram_id} nicht gefunden.", show_alert=True
        )
        await seller_detail_callback(callback)
        return

    if seller.get("active"):
        await callback.answer(
            f"⚠️ Verkäufer mit ID {telegram_id} ist noch aktiv und kann daher nicht gelöscht werden.\n"
            "Bitte deaktiviere ihn zuerst.",
            show_alert=True,
        )
        await seller_detail_callback(callback)
        return

    try:
        delete_seller_by_id(telegram_id)
        await callback.message.edit_text(
            f"✅ Verkäufer mit ID {telegram_id} wurde gelöscht.",
            reply_markup=get_main_menu_keyboard(),
        )
    except Exception as e:
        await callback.message.edit_text(f"❌ Fehler beim Löschen: {e}")

    await callback.answer()
