from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import ADMIN_USER_NAME
from database.dynamodb import dynamodb
from database.seller_repository import get_seller_by_id, save_seller
from keyboards.common import get_back_to_start_keyboard
from misc import format_datetime
from routers.admin.states import AddSeller

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
        reply_markup=get_back_to_start_keyboard(),
    )
    await callback.answer()
    await state.set_state(AddSeller.waiting_for_username)


@router.callback_query(F.data == "display_sellers")
async def display_sellers_callback(callback: CallbackQuery):
    table = dynamodb.Table("seller")
    try:
        response = table.scan()
        seller_list = response.get("Items", [])
        if not seller_list:
            await callback.message.answer(
                "❌ Es sind noch keine Verkäufer registriert."
            )
            return

        # Liste formatieren
        buttons = []
        for seller in seller_list:
            display_name = seller.get("display_name", None)
            telegram_id = seller["telegram_user_id"]
            button_text = display_name if display_name else str(telegram_id)
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=button_text, callback_data=f"seller_detail:{telegram_id}"
                    )
                ]
            )
        buttons.append(
            [
                InlineKeyboardButton(text="Abbrechen", callback_data="back_to_start"),
            ],
        )
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)

        await callback.message.answer("Wähle einen Verkäufer aus:", reply_markup=markup)
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
        f"Nutzername: {seller.get('Nutzername')}\n"
        f"Nutzer-ID: {seller.get('telegram_user_id', '-')}\n"
        f"Firma: {seller.get('business_name', '-')}\n"
        f"E-Mail: {seller.get('contact_email', '-')}\n"
        f"Telefon: {seller.get('contact_phone', '-')}\n"
        f"Homepage: {seller.get('homepage', '-')}\n"
        f"Aktiv: {'Ja' if seller.get('active') else 'Nein'}\n"
        f"Registriert: {'Ja' if seller.get('registered') else 'Nein'}\n"
        f"Hinzugefügt: {format_datetime(seller.get('created_at'))}"
    )

    inline_keyboard = []
    if seller.get("active", False):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="🚫 Deaktivieren",
                    callback_data=f"seller_toggle:{telegram_id}:deactivate",
                )
            ],
        )
    else:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="✅ Aktivieren",
                    callback_data=f"seller_toggle:{telegram_id}:activate",
                )
            ]
        )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔙 Zurück zur Übersicht", callback_data="display_sellers"
            )
        ]
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await callback.message.edit_text(msg, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("seller_toggle:"))
async def seller_toggle_callback(callback: CallbackQuery):
    _, telegram_id, action = callback.data.split(":")

    confirm_text = (
        "❗️Bist du sicher, dass du diesen Verkäufer "
        f"{'aktivieren' if action == 'activate' else 'deaktivieren'} möchtest?"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ja", callback_data=f"confirm_toggle:{telegram_id}:{action}"
                ),
                InlineKeyboardButton(
                    text="❌ Abbrechen", callback_data=f"cancel_toggle:{telegram_id}"
                ),
            ]
        ]
    )

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
