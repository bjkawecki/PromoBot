import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI, Request
from uvicorn import Config, Server

from config import TOKEN
from routers import all_routers

app = FastAPI()


@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    # TODO: Stripe Webhook verarbeiten
    return {"status": "ok"}


async def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    for router in all_routers:
        dp.include_router(router)
    await dp.start_polling(bot)


async def main():
    # Uvicorn-Server als async-Task starten
    config = Config(app=app, host="0.0.0.0", port=8000, loop="asyncio")
    server = Server(config)

    # Starte Bot und API parallel
    await asyncio.gather(start_bot(), server.serve())


if __name__ == "__main__":
    print("Bot und FastAPI laufen...")
    asyncio.run(main())
