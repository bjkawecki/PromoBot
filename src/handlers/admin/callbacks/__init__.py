from aiogram import Router

from handlers.admin.callbacks.seller import router as seller_callbacks_router
from handlers.admin.callbacks.stats import router as stats_callback_router

router = Router()

router.include_router(seller_callbacks_router)
router.include_router(stats_callback_router)
