from aiogram import Router

from handlers.buyer.callbacks.help import router as help_callbacks_router
from handlers.buyer.callbacks.menu import router as menu_callbacks_router
from handlers.buyer.callbacks.order import router as order_callbacks_router

router = Router()

router.include_router(help_callbacks_router)
router.include_router(menu_callbacks_router)
router.include_router(order_callbacks_router)
