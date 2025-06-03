from aiogram import Router

from handlers.admin.callbacks.promo import router as promo_callbacks_router
from handlers.admin.callbacks.seller import router as seller_callbacks_router
from handlers.admin.callbacks.stats import router as stats_callbacks_router

router = Router()

router.include_router(seller_callbacks_router)
router.include_router(stats_callbacks_router)
router.include_router(promo_callbacks_router)
