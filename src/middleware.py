from typing import Any, Callable, Dict

from aiogram import BaseMiddleware, types

from config import ADMIN_USER_NAME


class RoleMiddleware(BaseMiddleware):
    def __init__(self, seller_table):
        super().__init__()
        self.seller_table = seller_table

    async def get_seller(self, user_id: int) -> bool:
        response = self.seller_table.get_item(Key={"telegram_user_id": user_id})
        return response.get("Item", False)

    async def __call__(
        self, handler: Callable, event: types.TelegramObject, data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user:
            seller = await self.get_seller(user.id)
            if user.username == ADMIN_USER_NAME:
                role = "admin"
            elif seller:
                role = "seller"
            else:
                role = "unknown_buyer"
            data["role"] = role
            data["seller"] = seller
        else:
            data["role"] = "unknown_buyer"
        return await handler(event, data)
