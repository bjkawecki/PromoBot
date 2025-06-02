from aiogram import Router

from handlers.buyer.callbacks import router as buyer_callbacks_router
from handlers.buyer.message_handlers import router as buyer_message_handler_router

router = Router()
router.include_router(buyer_callbacks_router)
router.include_router(buyer_message_handler_router)
