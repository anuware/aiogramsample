from datetime import datetime
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
from app.utils.constants import UserRoles
from app.core.logger import logger

class UserDAO:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_or_create_user(self, tg_id: int, username: str | None = None) -> User:
        query = select(User).where(User.tg_id == tg_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            user = User(tg_id=tg_id, username=username)
            self.session.add(user)
            logger.info(f"Создан новый пользователь: {tg_id}")
        elif user.username != username:
            user.username = username
            user.updated_at = datetime.utcnow()
            logger.info(f"Обновлен username пользователя {tg_id}")
            
        await self.session.commit()
        return user
    
    async def get_owner(self) -> User | None:
        query = select(User).where(User.role == UserRoles.OWNER.value)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def update_role(self, tg_id: int, new_role: UserRoles) -> None:
        query = update(User).where(User.tg_id == tg_id).values(
            role=new_role.value,
            updated_at=datetime.utcnow()
        )
        await self.session.execute(query)
        await self.session.commit()
        logger.info(f"Обновлена роль пользователя {tg_id} на {new_role.value}")
    
    async def delete_user(self, tg_id: int) -> bool:
        query = delete(User).where(User.tg_id == tg_id)
        result = await self.session.execute(query)
        await self.session.commit()
        deleted = result.rowcount > 0
        if deleted:
            logger.info(f"Удален пользователь: {tg_id}")
        return deleted
    
    async def get_all_users(self, limit: int = 100, offset: int = 0) -> list[User]:
        query = select(User).order_by(User.created_at).limit(limit).offset(offset)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_users_by_role(self, role: UserRoles) -> list[User]:
        query = select(User).where(User.role == role.value)
        result = await self.session.execute(query)
        return list(result.scalars().all())
    
    async def get_users_count(self) -> int:
        query = select(func.count()).select_from(User)
        result = await self.session.execute(query)
        return result.scalar()
    
    async def search_users(self, username_query: str) -> list[User]:
        query = select(User).where(User.username.ilike(f"%{username_query}%"))
        result = await self.session.execute(query)
        return list(result.scalars().all())