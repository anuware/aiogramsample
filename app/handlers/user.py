from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import UserDAO
from app.utils.constants import UserRoles
from app.keyboards import get_user_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message, session: AsyncSession):
    dao = UserDAO(session)
    user = await dao.get_or_create_user(message.from_user.id, message.from_user.username)
    await message.answer("qq you added to database")