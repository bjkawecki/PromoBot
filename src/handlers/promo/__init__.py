from aiogram import Router

from handlers.promo.callbacks import router as promo_callbacks_router
from handlers.promo.message_handlers import (
    router as promo_message_handlers_router,
)

router = Router()

router.include_router(promo_callbacks_router)
router.include_router(promo_message_handlers_router)
