from aiogram import Router

from handlers.admin.callbacks.add_seller import (
    router as add_seller_router_callbacks_router,
)
from handlers.admin.callbacks.delete_seller import (
    router as delete_seller_router_callbacks_router,
)
from handlers.admin.callbacks.menu import router as menu_callbacks_router
from handlers.admin.callbacks.toggle_seller_is_active import (
    router as toggle_seller_is_active_callbacks_router,
)

router = Router()

router.include_router(add_seller_router_callbacks_router)
router.include_router(delete_seller_router_callbacks_router)
router.include_router(menu_callbacks_router)
router.include_router(toggle_seller_is_active_callbacks_router)
