from typing import Any, Callable, Dict

from aiogram import BaseMiddleware, types

from config import ADMIN_USER_NAME


class RoleMiddleware(BaseMiddleware):
    def __init__(self, seller_table):
        super().__init__()
        self.seller_table = seller_table

    async def is_seller(self, user_id: int) -> bool:
        response = self.seller_table.get_item(Key={"telegram_user_id": user_id})
        return "Item" in response

    async def is_registered(self, user_id: int) -> bool:
        response = self.seller_table.get_item(Key={"telegram_user_id": user_id})
        item = response.get("Item")
        return item.get("is_registered", False)

    async def __call__(
        self, handler: Callable, event: types.TelegramObject, data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user:
            is_registered = None
            if user.username == ADMIN_USER_NAME:
                role = "admin"
            elif await self.is_seller(user.id):
                role = "seller"
                is_registered = await self.is_registered(user.id)
            else:
                role = "unknown_buyer"
            data["role"] = role
            data["is_registered"] = is_registered
        else:
            data["role"] = "unknown_buyer"
        return await handler(event, data)
