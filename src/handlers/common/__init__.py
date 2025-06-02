from aiogram import Router

from handlers.common.callbacks.start import router as start_router

router = Router()

router.include_router(start_router)
