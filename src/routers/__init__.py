from routers.callbacks import callbacks_router
from routers.commands import commands_router

all_routers = [
    commands_router,
    callbacks_router,
]
