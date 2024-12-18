import asyncio
import logging
from typing import NoReturn

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from app.core import config
from app.core import logger
from app.handlers import routers
from app.database import engine
from app.database import Base
from app.middlewares import DatabaseMiddleware


class BotApp:
    def __init__(self):
        self.storage = MemoryStorage()
        self.bot = Bot(token=config.token, parse_mode=ParseMode.HTML)
        self.dp = Dispatcher(storage=self.storage)


    async def setup_database(self) -> None:
        logger.info("Инициализация базы данных")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    

    def setup_middlewares(self) -> None:
        logger.info("Подключение middleware")
        self.dp.update.middleware(DatabaseMiddleware())
    

    def setup_routers(self) -> None:
        logger.info("Подключение роутеров")
        for router in routers:
            self.dp.include_router(router)
    

    async def setup(self) -> None:
        await self.setup_database()
        self.setup_middlewares()
        self.setup_routers()
        logger.info("Бот успешно настроен")
    
    
    async def start(self) -> None:
        logger.info("Запуск бота")
        try:
            await self.setup()
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Ошибка при запуске: {e}")
            raise
        finally:
            await self.stop()
    

    async def stop(self) -> None:
        logger.info("Остановка бота")
        await self.bot.session.close()



async def main() -> NoReturn:
    bot_app = BotApp()
    try:
        await bot_app.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен вручную")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())