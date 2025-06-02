from aiogram import Router

from handlers.admin.message_handlers.add_seller import (
    router as add_seller_admin_message_handler_router,
)

router = Router()

router.include_router(add_seller_admin_message_handler_router)
