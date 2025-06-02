from aiogram import Router

from handlers.promo.message_handlers.create import (
    router as create_promo_message_handler_router,
)
from handlers.promo.message_handlers.edit import (
    router as edit_promo_message_handler_router,
)

router = Router()

router.include_router(create_promo_message_handler_router)
router.include_router(edit_promo_message_handler_router)
