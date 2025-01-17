from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete, desc


async def set_user(tg_id: int, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id, User.username == username))
        
        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

