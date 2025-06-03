from aiogram import Router

from handlers.admin.callbacks.seller import router as seller_callbacks_router

router = Router()

router.include_router(seller_callbacks_router)
