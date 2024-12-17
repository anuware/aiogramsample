from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from app.database.models import User
from app.utils.constants import Ranks

class UserDAO:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, tg_id: int) -> User | None:
        return await self.session.scalar(
            select(User).where(User.tg_id == tg_id)
        )

    async def create_or_update(self, tg_id: int, username: str) -> User:
        user = await self.get_by_id(tg_id)
        if not user:
            user = User(
                tg_id=tg_id,
                username=username,
                rank=Ranks.USER.value
            )
            self.session.add(user)
        else:
            user.username = username
            user.last_active = datetime.utcnow()
        
        await self.session.commit()
        return user

    async def set_rank(self, tg_id: int, new_rank: str) -> None:
        await self.session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(rank=new_rank, last_active=datetime.utcnow())
        )
        await self.session.commit()