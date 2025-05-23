from aiogram import Router

from handlers.order.cancel_order import router as cancel_order_router
from handlers.order.collect_order_details import router as collect_order_details_router
from handlers.order.edit_order_details import router as edit_order_details_router

handlers_router = Router()
handlers_router.include_router(edit_order_details_router)
handlers_router.include_router(collect_order_details_router)
handlers_router.include_router(cancel_order_router)
