from aiogram import Router

from handlers.buyer.message_handlers.order import (
    router as order_message_handlers_router,
)

router = Router()

router.include_router(order_message_handlers_router)
