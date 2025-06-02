from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.seller.promo import (
    get_confirm_edit_promo_keyboard,
)
from states.seller import EditPromoField
from utils.misc import PROMO_FIELD_LABELS, PROMO_VALIDATOR_MAP

router = Router()


@router.message(EditPromoField.waiting_for_field_value)
async def handle_edit_promo_field_input(message: Message, state: FSMContext):
    value = message.text.strip()
    data = await state.get_data()
    promo_id = data.get("promo_id")
    field = data["field"]
    field_label = PROMO_FIELD_LABELS[field]
    validator = PROMO_VALIDATOR_MAP.get(field)
    if not validator:
        await message.answer("❌ Für dieses Feld ist keine Validierung definiert.")
        return
        # Eingabe validieren
    validated_value = await validator(message, value)
    if validated_value is None:
        return  # Fehler wurde vom Validator behandelt
    await state.update_data(new_value=value)

    await message.answer(
        f"<b>Neue Eingabe für {field_label}:</b>\n\n{value}\n\n💾 <b>Eingabe speichern?</b>",
        reply_markup=get_confirm_edit_promo_keyboard(promo_id),
        parse_mode="HTML",
    )

    await state.set_state(EditPromoField.confirm_new_value)
