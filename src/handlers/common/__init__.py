from aiogram import Router

from handlers.common.start import router as start_router

router = Router()

router.include_router(start_router)
