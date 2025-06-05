from aiogram import Router

from handlers.admin import router as admin_router
from handlers.buyer import router as buyer_router
from handlers.common import router as common_router
from handlers.seller import router as seller_router

router = Router()
router.include_router(admin_router)
router.include_router(buyer_router)
router.include_router(common_router)
router.include_router(seller_router)
