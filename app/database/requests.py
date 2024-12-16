from sqlalchemy import select, update
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
from app.const import RANKS_HIERARCHY, Ranks
from app.database.session import session

async def set_user(tg_id: int, username: str):
    try:
        user = await session.scalar(
            select(User).where(User.tg_id == tg_id)
        )
        
        if not user:
            new_user = User(
                tg_id=tg_id, 
                username=username,
                rank=Ranks.USER.value  
            )
            session.add(new_user)
            await session.commit()
        else:
            if user.username != username:
                user.username = username
                user.last_active = datetime.utcnow()
                await session.commit()
                
    except Exception as e:
        await session.rollback()
        raise

async def get_user_rank(user_id: int) -> str | None:
    user = await session.scalar(
        select(User).where(User.tg_id == user_id)
    )
    if user:
        user.last_active = datetime.utcnow()
        await session.commit()
        return user.rank
    return None

async def change_user_rank(session: AsyncSession, target_id: int, new_rank: str):
    await session.execute(
        update(User)
        .where(User.tg_id == target_id)
        .values(rank=new_rank, last_active=datetime.utcnow())
    )
    await session.commit()

async def init_owner_rank(session: AsyncSession, user_id: int) -> bool:
    owner = await session.scalar(
        select(User).where(User.rank == Ranks.OWNER.value)
    )
    
    if owner is not None:
        return False
        
    await change_user_rank(session, user_id, Ranks.OWNER.value)
    return True

async def check_rank_permission(session: AsyncSession, user_id: int, required_rank: str) -> bool:
    user_rank = await get_user_rank(session, user_id)
    if not user_rank:
        return False
    return RANKS_HIERARCHY.get(user_rank, 0) >= RANKS_HIERARCHY.get(required_rank, 0)