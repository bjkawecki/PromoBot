from aiogram import Router

from routers.admin.callbacks import router as callbacks_router
from routers.admin.messages import router as messages_router

router = Router()
router.include_router(callbacks_router)
router.include_router(messages_router)
