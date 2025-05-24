from typing import Any, Callable, Dict

from aiogram import BaseMiddleware, types

from config import ADMIN_USER_NAME
from database import ROLE_MAP


class RoleMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, event: types.TelegramObject, data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user:
            if user.username == ADMIN_USER_NAME:
                role = "admin"
            else:
                role = ROLE_MAP.get(user.username, "unknown")
            data["role"] = role
        else:
            data["role"] = "unknown"
        return await handler(event, data)
