from aiogram import Router

from handlers.seller.help.callbacks import router as help_callbacks_router
from handlers.seller.profile.callbacks import router as profile_callbacks_router
from handlers.seller.profile.message_handlers import (
    router as profile_message_handlers_router,
)
from handlers.seller.promo.callbacks import router as promo_callbacks_router
from handlers.seller.promo.message_handlers import (
    router as promo_message_handlers_router,
)

router = Router()
router.include_router(profile_message_handlers_router)
router.include_router(promo_message_handlers_router)
router.include_router(profile_callbacks_router)
router.include_router(promo_callbacks_router)
router.include_router(help_callbacks_router)
