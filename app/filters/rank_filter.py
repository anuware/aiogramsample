from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.requests import check_rank_permission

class RankFilter(BaseFilter):
    def __init__(self, rank: str) -> None:
        self.rank = rank

    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        return await check_rank_permission(session, message.from_user.id, self.rank)