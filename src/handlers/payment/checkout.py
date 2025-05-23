import stripe
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import STRIPE_SECRET_KEY

router = Router()
stripe.api_key = STRIPE_SECRET_KEY


@router.callback_query(lambda c: c.data == "continue_to_payment")
async def start_checkout(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    product_name = data.get("product_name")
    amount = data.get("amount")  # in cent, z. B. 1999 für 19,99 €
    quantity = data.get("quantity")
    address = data.get("address")
    seller = data.get("seller")  # seller = dict mit .stripe_account_id etc.

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[
            {
                "price_data": {
                    "currency": "eur",
                    "unit_amount": amount,
                    "product_data": {
                        "name": product_name,
                    },
                },
                "quantity": quantity,
            }
        ],
        success_url="https://deinbot.de/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://deinbot.de/cancel",
        payment_intent_data={
            "application_fee_amount": 300,  # 3 € Plattform-Gebühr (optional)
            "transfer_data": {
                "destination": seller["stripe_account_id"],
            },
        },
        metadata={
            "telegram_user_id": str(callback.from_user.id),
            "product_name": product_name,
            "address": address,
            "seller_id": str(seller["id"]),
        },
    )

    await callback.message.answer(
        "✅ Fast fertig! Bezahle hier sicher mit Stripe:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="🔐 Jetzt bezahlen", url=checkout_session.url
                    )
                ]
            ]
        ),
    )
    await callback.answer()
