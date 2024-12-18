import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.handlers.user import user
from app.handlers.admin import admin
from app.logging import setup_logger
from app.core import config
from app.database.models import Base
from app.database.session import engine, init_db

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await init_db()
    
    bot = Bot(
        token=config.TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    dp.include_routers(user, admin)
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())