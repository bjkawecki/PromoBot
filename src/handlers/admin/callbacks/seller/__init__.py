from aiogram import Router

from handlers.admin.callbacks.seller.add import router as add_router
from handlers.admin.callbacks.seller.delete import router as delete_router
from handlers.admin.callbacks.seller.menu import router as menu_router
from handlers.admin.callbacks.seller.toggle_status import router as toggle_status_router

router = Router()

router.include_router(add_router)
router.include_router(delete_router)
router.include_router(menu_router)
router.include_router(toggle_status_router)
