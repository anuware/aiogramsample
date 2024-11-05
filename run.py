import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.user_handlers import user
from app.admin import admin
from app.logging import setup_logger
from config_reader import config


    
async def main():
    logger = setup_logger()
    bot = Bot(token=config.TOKEN.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp = Dispatcher()
    dp.include_routers(user, admin)
    
    logger.info("Бот запущен")
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger = setup_logger()
        logger.info("Бот остановлен")
