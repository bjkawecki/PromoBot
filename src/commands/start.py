from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.inline import get_main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    welcome_text = (
        "Hallo, ich bin Promo-Bot!\n\n"
        "Folgendes Produkt gibt es nur für Kanal-Abonnenten mit exklusivem Rabatt.\n\n"
        "T-Shirt, Baumwolle, statt 20 € nur 10 €!"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu())
