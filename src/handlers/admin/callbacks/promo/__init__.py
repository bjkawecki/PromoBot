from aiogram import Router

from handlers.admin.callbacks.promo.common import router as common_router
from handlers.admin.callbacks.promo.hard_delete import router as hard_delete_router
from handlers.admin.callbacks.promo.menu import router as menu_router
from handlers.admin.callbacks.promo.soft_delete import router as soft_delete_router

router = Router()

router.include_router(menu_router)
router.include_router(hard_delete_router)
router.include_router(soft_delete_router)
router.include_router(common_router)
