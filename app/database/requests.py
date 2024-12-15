from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete, desc
from app.const import RANKS_HIERARCHY, Ranks


async def set_user(tg_id: int, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id, User.username == username))
        
        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

async def change_user_rank(target_id: int, new_rank: str):
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == target_id)
            .values(rank=new_rank)
        )
        await session.commit()

async def get_user_rank(user_id: int) -> str | None:
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.tg_id == user_id)
        )
        return user.rank if user else None

async def check_rank_permission(user_id: int, required_rank: str) -> bool:
    user_rank = await get_user_rank(user_id)
    if not user_rank:
        return False
    return RANKS_HIERARCHY.get(user_rank, 0) >= RANKS_HIERARCHY.get(required_rank, 0)

