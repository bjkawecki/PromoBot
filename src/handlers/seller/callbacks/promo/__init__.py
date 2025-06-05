from aiogram import Router

from handlers.seller.callbacks.promo.create import (
    router as create_promo_callback_router,
)
from handlers.seller.callbacks.promo.delete import (
    router as delete_promo_callback_router,
)
from handlers.seller.callbacks.promo.edit import router as edit_promo_callback_router
from handlers.seller.callbacks.promo.menu import router as menu_promo_callback_router
from handlers.seller.callbacks.promo.publish import (
    router as publish_promo_callback_router,
)
from handlers.seller.callbacks.promo.status import (
    router as status_promo_callback_router,
)

router = Router()
router.include_router(create_promo_callback_router)
router.include_router(edit_promo_callback_router)
router.include_router(menu_promo_callback_router)
router.include_router(publish_promo_callback_router)
router.include_router(status_promo_callback_router)
router.include_router(delete_promo_callback_router)
