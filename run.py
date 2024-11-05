import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.user_handlers import user
from app.admin import admin
from app.middlewares import UserMiddleware

from config_reader import config


    
async def main():
    bot = Bot(token=config.TOKEN.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    dp = Dispatcher()
    dp.update.middleware(UserMiddleware())
    dp.include_routers(user, admin)
    

    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
