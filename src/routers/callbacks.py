# src/routers/callbacks.py
from aiogram import Router

from handlers.callbacks import router as show_product_callback

callbacks_router = Router()
callbacks_router.include_router(show_product_callback)
