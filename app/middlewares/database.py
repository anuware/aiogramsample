from sqlalchemy.ext.asyncio import AsyncSession
from app.database.base import get_session

class DatabaseMiddleware:
    async def __call__(self, event, data, *args, **kwargs):
        async with get_session() as session:
            data["session"] = session
            try:
                return await self.handler(event, data, *args, **kwargs)  
            finally:
                await session.close() 