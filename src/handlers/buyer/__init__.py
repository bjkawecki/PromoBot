from aiogram import Router

from handlers.buyer.help.callbacks import router as help_callbacks_router
from handlers.buyer.order.callbacks import router as order_callbacks_router
from handlers.buyer.order.message_handlers import router as order_messages_router
from handlers.buyer.product_details.callbacks import (
    router as product_details_callback_router,
)

router = Router()
router.include_router(help_callbacks_router)
router.include_router(order_callbacks_router)
router.include_router(order_messages_router)
router.include_router(product_details_callback_router)
