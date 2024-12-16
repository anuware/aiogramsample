from sqlalchemy import select, update, delete, desc
from app.database.models import async_session, User
from app.const import RANKS_HIERARCHY, Ranks
from datetime import datetime


async def set_user(tg_id: int, username: str):
    async with async_session() as session:
        try:
            # Проверяем существование пользователя
            user = await session.scalar(
                select(User).where(User.tg_id == tg_id)
            )
            
            if not user:
                # Создаем нового пользователя
                new_user = User(
                    tg_id=tg_id, 
                    username=username,
                    rank=Ranks.USER.value  
                )
                session.add(new_user)
                await session.commit()
                print(f"Создан новый пользователь: {username}")
            else:
                # Обновляем существующего пользователя
                if user.username != username:
                    user.username = username
                    user.last_active = datetime.utcnow()
                    await session.commit()
                    print(f"Обновлен пользователь: {username}")
                    
        except Exception as e:
            print(f"Ошибка при работе с БД: {e}")
            await session.rollback()
            raise

async def init_owner_rank(user_id: int) -> bool:
    async with async_session() as session:
        # Проверяем, есть ли уже пользователь с рангом владельца
        owner = await session.scalar(
            select(User).where(User.rank == Ranks.OWNER.value)
        )
        
        if owner is not None:
            return False
            
        # Если владельца нет, назначаем
        await change_user_rank(user_id, Ranks.OWNER.value)
        return True


async def change_user_rank(target_id: int, new_rank: str):
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == target_id)
            .values(rank=new_rank, last_active=datetime.utcnow())
        )
        await session.commit()

async def get_user_rank(user_id: int) -> str | None:
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.tg_id == user_id)
        )
        if user:
            user.last_active = datetime.utcnow()
            await session.commit()
            return user.rank
        return None

async def check_rank_permission(user_id: int, required_rank: str) -> bool:
    user_rank = await get_user_rank(user_id)
    if not user_rank:
        return False
    return RANKS_HIERARCHY.get(user_rank, 0) >= RANKS_HIERARCHY.get(required_rank, 0)

