from aiogram import Router

from handlers.order.cancel_order import router as cancel_order_router
from handlers.order.edit_order_info import router as edit_order_info_router
from handlers.order.enter_order_info import router as enter_order_info_router

handlers_router = Router()
handlers_router.include_router(edit_order_info_router)
handlers_router.include_router(enter_order_info_router)
handlers_router.include_router(cancel_order_router)
