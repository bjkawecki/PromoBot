from aiogram import Router

from handlers.seller.callbacks import router as seller_callbacks_router
from handlers.seller.message_handlers import router as seller_message_handlers_router
from handlers.seller.message_handlers.promo import (
    router as promo_message_handlers_router,
)

router = Router()
router.include_router(seller_callbacks_router)
router.include_router(seller_message_handlers_router)
router.include_router(promo_message_handlers_router)
