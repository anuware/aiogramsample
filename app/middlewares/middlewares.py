from aiogram import BaseMiddleware
from aiogram.types import Update

from typing import Callable, Any, Awaitable

from database import User

class UserMiddleware(BaseMiddleware):
    
    async def __cal__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any]
    ) -> Any: 
        current_event = (
            event.message
            or event.callback_query
            or event.inline_query
            or event.choisen_inline_result
        )
        
        user = await User.get_or_create(
            id=current_event.from_user.id,
            username=current_event.from_user.username
        )
        
        
        data["user"] = user[0]
        return await handler(event, data)    
