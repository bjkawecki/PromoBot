from aiogram import Router

from commands.start import router as start_router

commands_router = Router()
commands_router.include_router(start_router)
