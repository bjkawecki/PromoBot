from aiogram import Router

from handlers.seller.message_handlers.profile import (
    router as profile_message_handler_router,
)

router = Router()
router.include_router(profile_message_handler_router)
