from aiogram import Router

from handlers.seller.message_handlers.promo.create import (
    router as create_promo_message_handler_router,
)
from handlers.seller.message_handlers.promo.edit import (
    router as edit_promo_message_handler_router,
)

router = Router()

router.include_router(create_promo_message_handler_router)
router.include_router(edit_promo_message_handler_router)
