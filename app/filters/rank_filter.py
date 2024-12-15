from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.database.requests import check_rank_permission

class RankFilter(BaseFilter):
    def __init__(self, rank: str) -> None:
        self.rank = rank

    async def __call__(self, message: Message) -> bool:
        return await check_rank_permission(message.from_user.id, self.rank)