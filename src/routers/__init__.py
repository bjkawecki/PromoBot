from aiogram import Router

from routers.admin import router as admin_router
from routers.buyer import router as buyer_router
from routers.common import router as common_router

router = Router()
router.include_router(admin_router)
router.include_router(buyer_router)
router.include_router(common_router)
