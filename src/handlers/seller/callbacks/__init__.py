from aiogram import Router

from handlers.seller.callbacks.help import router as help_callback_router
from handlers.seller.callbacks.profile import router as profile_callback_router
from handlers.seller.callbacks.promo import router as promo_callback_router

router = Router()

router.include_router(help_callback_router)
router.include_router(profile_callback_router)
router.include_router(promo_callback_router)
