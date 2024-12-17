from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.dao import UserDAO
from app.utils.constants import Ranks
from app.utils.filters import RankFilter
from app.keyboards.admin import AdminKeyboards

router = Router()

@router.message(Command("init_owner"))
async def init_owner(message: Message, session: AsyncSession):
    dao = UserDAO(session)
    user = await dao.get_by_id(message.from_user.id)
    
    if not await dao.get_owner():
        await dao.set_rank(message.from_user.id, Ranks.OWNER.value)
        await message.answer("✅ Вы назначены владельцем бота")
    else:
        await message.answer("❌ Владелец уже назначен")