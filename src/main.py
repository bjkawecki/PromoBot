import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from middleware import RoleMiddleware
from routers import routers

dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(RoleMiddleware())
bot = Bot(token=TOKEN)
dp.include_router(routers)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot läuft...")
    asyncio.run(main())
