from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import UserDAO
from app.utils.constants import UserRoles
from app.keyboards import get_admin_keyboard
from app.core.logger import logger

router = Router()

@router.message(Command("init_owner"))
async def init_owner(message: Message, session: AsyncSession):
    dao = UserDAO(session)
    user = await dao.get_or_create_user(message.from_user.id, message.from_user.username)
    
    if await dao.get_owner():
        await message.answer("❌ Владелец бота уже назначен")
        return
        
    await dao.update_role(message.from_user.id, UserRoles.OWNER)
    await message.answer("✅ Вы назначены владельцем бота", reply_markup=get_admin_keyboard())

@router.message(Command("admin"))
async def admin_panel(message: Message, session: AsyncSession):
    dao = UserDAO(session)
    user = await dao.get_or_create_user(message.from_user.id, message.from_user.username)
    
    if user.role not in [UserRoles.OWNER.value, UserRoles.ADMIN.value]:
        await message.answer("❌ Недостаточно прав")
        return
        
    await message.answer("🔧 Панель администратора", reply_markup=get_admin_keyboard())

@router.callback_query(F.data == "users_list")
async def show_users(call: CallbackQuery, session: AsyncSession):
    dao = UserDAO(session)
    user = await dao.get_or_create_user(call.from_user.id, call.from_user.username)
    
    if user.role not in [UserRoles.OWNER.value, UserRoles.ADMIN.value]:
        await call.answer("❌ Недостаточно прав", show_alert=True)
        return

    users = await dao.get_all_users(limit=10)
    text = "👥 Список последних пользователей:\n\n"
    
    for user in users:
        text += f"ID: {user.tg_id}\n"
        text += f"Роль: {user.role}\n"
        text += f"Дата: {user.created_at.strftime('%d.%m.%Y')}\n\n"
    
    await call.message.answer(text)
    await call.answer()

@router.callback_query(F.data == "stats")
async def show_stats(call: CallbackQuery, session: AsyncSession):
    dao = UserDAO(session)
    user = await dao.get_or_create_user(call.from_user.id, call.from_user.username)
    
    if user.role not in [UserRoles.OWNER.value, UserRoles.ADMIN.value]:
        await call.answer("❌ Недостаточно прав", show_alert=True)
        return

    total = await dao.get_users_count()
    admins = await dao.get_users_by_role(UserRoles.ADMIN)
    mods = await dao.get_users_by_role(UserRoles.MODERATOR)
    
    text = "📊 Статистика бота:\n\n"
    text += f"Всего пользователей: {total}\n"
    text += f"Администраторов: {len(admins)}\n"
    text += f"Модераторов: {len(mods)}"
    
    await call.message.answer(text)
    await call.answer()

@router.callback_query(F.data == "settings")
async def show_settings(call: CallbackQuery, session: AsyncSession):
    dao = UserDAO(session)
    user = await dao.get_or_create_user(call.from_user.id, call.from_user.username)
    
    if user.role != UserRoles.OWNER.value:
        await call.answer("❌ Доступно только владельцу", show_alert=True)
        return
        
    text = "⚙️ Настройки бота:\n\n"
    text += "- Управление администраторами\n"
    text += "- Управление модераторами\n"
    text += "- Настройки бота"
    
    await call.message.answer(text)
    await call.answer()