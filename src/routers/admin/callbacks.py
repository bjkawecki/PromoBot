from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from config import ADMIN_USER_NAME
from database.dynamodb import dynamodb
from database.repositories.sellers import (
    delete_seller_by_id,
    get_seller_by_id,
    save_seller,
)
from keyboards.admin import (
    get_confirm_delete_seller_keyboard,
    get_confirm_toggle_keyboard,
    get_seller_detail_keyboard,
    get_seller_list_keyboard,
)
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from routers.admin.states import AddSeller
from utils.misc import format_datetime

router = Router()


@router.callback_query(F.data == "add_seller")
async def add_seller_callback(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.username != ADMIN_USER_NAME:
        await callback.answer("Keine Berechtigung.", show_alert=True)
        return

    await callback.message.answer(
        "*Neuer Verkäufer hinzufügen*\n\n"
        "Bitte sende die Telegram\\-Nutzer\\-ID des neuen Verkäufers:",
        parse_mode="MarkdownV2",
        reply_markup=get_abort_keyboard(),
    )
    await callback.answer()
    await state.set_state(AddSeller.waiting_for_username)


@router.callback_query(F.data == "display_sellers")
async def display_sellers_callback(callback: CallbackQuery):
    table = dynamodb.Table("sellers")
    try:
        response = table.scan()
        seller_list = response.get("Items", [])
        if not seller_list:
            await callback.answer("❌ Es sind noch keine Verkäufer registriert.")
            return

        keyboard = get_seller_list_keyboard(seller_list)
        await callback.message.answer(
            "Wähle einen Verkäufer aus:", reply_markup=keyboard
        )
        await callback.answer()
    except Exception as e:
        await callback.message.answer("⚠️ Fehler beim Abrufen der Verkäufer.")
        print(f"[ERROR] {e}")


@router.callback_query(F.data.startswith("seller_detail:"))
async def seller_detail_callback(callback: CallbackQuery):
    telegram_id = callback.data.split(":")[1]

    seller = get_seller_by_id(int(telegram_id))
    if not seller:
        await callback.message.answer("Verkäufer nicht gefunden.")
        return

    msg = (
        f"<b>Verkäufer: {seller.get('display_name', '-')}</b>\n"
        f"Nutzername: {seller.get('Nutzername', '–')}\n"
        f"Nutzer-ID: {seller.get('telegram_user_id', '-')}\n"
        f"Firma: {seller.get('business_name', '-')}\n"
        f"E-Mail: {seller.get('contact_email', '-')}\n"
        f"Telefon: {seller.get('contact_phone', '-')}\n"
        f"Homepage: {seller.get('homepage', '-')}\n"
        f"Aktiv: {'Ja' if seller.get('active') else 'Nein'}\n"
        f"Registriert: {'Ja' if seller.get('registered') else 'Nein'}\n"
        f"Hinzugefügt: {format_datetime(seller.get('created_at'))}"
    )

    keyboard = get_seller_detail_keyboard(telegram_id, seller.get("active", False))

    await callback.message.answer(msg, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()


@router.callback_query(F.data.startswith("seller_toggle:"))
async def seller_toggle_callback(callback: CallbackQuery):
    _, telegram_id, action = callback.data.split(":")

    confirm_text = (
        "❗️Bist du sicher, dass du diesen Verkäufer "
        f"{'aktivieren' if action == 'activate' else 'deaktivieren'} möchtest?"
    )

    keyboard = get_confirm_toggle_keyboard(telegram_id, action)

    await callback.message.answer(confirm_text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("cancel_toggle"))
async def cancel_toggle_callback(callback: CallbackQuery):
    await callback.answer("❎ Vorgang abgebrochen.")
    await seller_detail_callback(callback)
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_toggle:"))
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

    keyboard = get_confirm_delete_seller_keyboard(telegram_id)

    await callback.message.answer(
        f"❗️Bist du sicher, dass du den Verkäufer mit ID {telegram_id} löschen möchtest?",
        reply_markup=keyboard,
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
