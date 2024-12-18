from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.dao import UserDAO

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = data["session"]
        dao = UserDAO(session)
        
        # Автоматическое создание пользователя при первом взаимодействии
        user = await dao.get_user(event.from_user.id)
        if not user:
            await dao.create_user(
                event.from_user.id,
                event.from_user.username
            )
        
        return await handler(event, data)