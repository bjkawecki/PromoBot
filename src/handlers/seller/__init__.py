from aiogram import Router

from handlers.seller.callbacks import router as callbacks_router
from handlers.seller.message_handlers import router as messages_router

router = Router()
router.include_router(messages_router)
router.include_router(callbacks_router)
