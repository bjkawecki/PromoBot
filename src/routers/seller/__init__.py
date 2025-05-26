from aiogram import Router

from routers.seller.callbacks import router as callbacks_router
from routers.seller.messages import router as messages_router

router = Router()
router.include_router(messages_router)
router.include_router(callbacks_router)
