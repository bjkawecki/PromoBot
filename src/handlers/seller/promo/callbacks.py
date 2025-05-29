import uuid

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link

from config import verkaeufer_kanal_id
from database.repositories.promos import create_promotion, get_promotions_by_seller_id
from keyboards.common import get_abort_keyboard, get_main_menu_keyboard
from keyboards.seller.promo import get_inline_keyboard, get_promo_list_keyboard
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
    print(data)
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
    promo_list = get_promotions_by_seller_id(callback.from_user.id)
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
