from aiogram import Router

from routers.buyer.callback_handler import router as buyer_callbacks_router
from routers.buyer.start_handler import router as buyer_start_router
from routers.buyer.state_handler import router as buyer_state_router
from routers.common.start_handler import router as common_start_router

routers = Router()
routers.include_router(buyer_callbacks_router)
routers.include_router(buyer_start_router)
routers.include_router(buyer_state_router)
routers.include_router(common_start_router)
