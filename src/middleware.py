from typing import Any, Callable, Dict

from aiogram import BaseMiddleware, types

from database import ROLE_MAP


# --- Middleware zur Rollenerkennung ---
class RoleMiddleware(BaseMiddleware):
    async def __call__(
        self, handler: Callable, event: types.TelegramObject, data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user:
            role = ROLE_MAP.get(str(user.id), "unknown")
            data["role"] = role
        else:
            data["role"] = "unknown"
        return await handler(event, data)
