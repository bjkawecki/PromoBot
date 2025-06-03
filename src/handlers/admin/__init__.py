from aiogram import Router

from handlers.admin.callbacks import router as callbacks_router
from handlers.admin.message_handlers import router as message_handlers_router

router = Router()
router.include_router(callbacks_router)
router.include_router(message_handlers_router)
