import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, seller_table
from middleware import RoleMiddleware
from routers import router

dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(RoleMiddleware(seller_table))
bot = Bot(token=TOKEN)
dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot läuft...")
    asyncio.run(main())
