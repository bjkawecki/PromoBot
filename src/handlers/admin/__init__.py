from aiogram import Router

from handlers.admin.callbacks import router as admin_callbacks_router
from handlers.admin.message_handlers import router as admin_messages_router

router = Router()
router.include_router(admin_callbacks_router)
router.include_router(admin_messages_router)
