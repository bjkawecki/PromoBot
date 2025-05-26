from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.repositories.sellers import update_seller_field
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from states.seller import SellerState

router = Router()


@router.callback_query(F.data == "register_seller")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user
    update_seller_field(telegram_user_id=user.id, field="username", value=user.username)
    await state.set_state(SellerState.business_name)
    await callback.message.answer(
        f"<b>Registrierung als Verkäufer</b>\n\n"
        f"Nutzername: {user.username}"
        f"\n\n🏢 Bitte gib Unternehmensname und Rechtsform ein:",
        reply_markup=get_abort_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "skip_add_phone")
async def skip_add_phone_handler(callback_query: CallbackQuery, state: FSMContext):
    user = callback_query.from_user
    data = await state.get_data()

    # Im State speichern, dass Telefonnummer übersprungen wurde
    await state.update_data(contact_phone=None)
    update_seller_field(user.id, "contact_phone", None)

    # Hier kannst du den State wechseln (z.B. zur nächsten Frage/State)
    await state.set_state(SellerState.contact_phone)  # Falls das der nächste State ist

    # Antwort an den Nutzer mit der nächsten Frage
    await callback_query.message.answer(
        f"<b>Registrierung als Verkäufer</b>\n\n"
        f"Nutzername: @{user.username}"
        f"\nFirma: {data.get('business_name')}"
        f"\nAnzeigename: {data.get('display_name')}"
        f"\nE-Mail: {data.get('contact_email', '–')}"
        f"\nTelefon: {data.get('contact_phone', '–')}"
        f"\n\n📞 Bitte gib die Homepage deiner Firma an (optional):",
        reply_markup=get_abort_keyboard(),  # Oder ggf. anderer Keyboard
        parse_mode="HTML",
    )

    # Callback-Query als beantwortet markieren, damit im Chat der Lade-Kreis verschwindet
    await callback_query.answer()


@router.message(SellerState.confirm)
async def confirm_registration(message: Message, state: FSMContext):
    user = message.from_user
    stripe_account_id = message.text

    # Optional: speichern in DB
    update_seller_field(user.id, "stripe_account_id", stripe_account_id)

    # FSM-Daten speichern (optional, wenn du noch was brauchst)
    await state.update_data(stripe_account_id=stripe_account_id)

    # Registrierung ist fertig → FSM beenden
    await state.clear()

    # Abschlussnachricht senden
    await message.answer(
        "✅ Deine Registrierung als Verkäufer ist abgeschlossen!\n\n"
        "Du kannst jetzt Produkte hinzufügen oder dein Profil weiter bearbeiten.",
        reply_markup=get_main_menu_keyboard(),  # optional
    )
