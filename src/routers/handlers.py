from aiogram import Router

from handlers.help import router as help_router
from handlers.order.cancel_order import router as cancel_order_router
from handlers.order.collect_order_details import router as collect_order_details_router
from handlers.order.edit_order_details import router as edit_order_details_router
from handlers.product import router as product_details_router
from handlers.start import router as start_router

handlers_router = Router()
handlers_router.include_router(edit_order_details_router)
handlers_router.include_router(collect_order_details_router)
handlers_router.include_router(cancel_order_router)
handlers_router.include_router(start_router)
handlers_router.include_router(help_router)
handlers_router.include_router(product_details_router)
