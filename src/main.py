import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from database.dynamodb import dynamodb
from middleware import RoleMiddleware
from routers import router

seller_table = dynamodb.Table("sellers")
dp = Dispatcher(storage=MemoryStorage())
dp.message.middleware(RoleMiddleware(seller_table))
dp.callback_query.middleware(RoleMiddleware(seller_table))

bot = Bot(token=TOKEN)
dp.include_router(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    print("Bot läuft...")
    asyncio.run(main())
