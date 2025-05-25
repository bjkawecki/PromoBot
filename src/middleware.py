from typing import Any, Callable, Dict

from aiogram import BaseMiddleware, types

from config import ADMIN_USER_NAME


class RoleMiddleware(BaseMiddleware):
    def __init__(self, seller_table):
        super().__init__()
        self.seller_table = seller_table

    async def is_seller(self, user_id: int) -> bool:
        response = self.seller_table.get_item(Key={"id": user_id})
        return "Item" in response

    async def __call__(
        self, handler: Callable, event: types.TelegramObject, data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user:
            if user.username == ADMIN_USER_NAME:
                role = "admin"
            elif "Item" in self.seller_table.get_item(
                Key={"telegram_user_id": user.id}
            ):
                role = "seller"
            else:
                role = "unknown_buyer"
            data["role"] = role
        else:
            data["role"] = "unknown_buyer"
        return await handler(event, data)
