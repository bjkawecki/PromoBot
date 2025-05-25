from aiogram import Router

from routers.buyer.callbacks import router as callbacks_router
from routers.buyer.start import router as start_router
from routers.buyer.states import router as states_router

router = Router()
router.include_router(callbacks_router)
router.include_router(start_router)
router.include_router(states_router)
