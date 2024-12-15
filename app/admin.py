from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, CommandStart, Command
import app.keyboards as kb
from aiogram.filters import Command
from aiogram.types import Message
from app.const import Ranks
from app.filters.rank_filter import RankFilter
from app.database.requests import change_user_rank, get_user_rank

admin = Router()


class Admin(Filter):
    def __init__(self):
        self.admins = []

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins
    

@admin.message(Admin(), Command('admin'))
async def cmd_start(message: Message):
    await message.answer('Admin panel')

@admin.message(Command("setrank"), RankFilter(Ranks.CREATOR))
async def set_rank_command(message: Message):
    try:
        # Формат команды: /setrank @username ранг
        args = message.text.split()[1:]
        if len(args) < 2:
            await message.answer("❌ Использование: /setrank @username ранг")
            return

        username = args[0].replace("@", "")
        new_rank = " ".join(args[1:])

        # Проверяем, существует ли такой ранг
        if new_rank not in RANKS_HIERARCHY:
            await message.answer("❌ Недопустимый ранг!")
            return

        # Находим пользователя и меняем ранг
        async with async_session() as session:
            user = await session.scalar(
                select(User).where(User.username == username)
            )
            if not user:
                await message.answer("❌ Пользователь не найден!")
                return

            await change_user_rank(user.tg_id, new_rank)
            await message.answer(f"✅ Пользователю @{username} выдан ранг {new_rank}")

    except Exception as e:
        await message.answer("❌ Произошла ошибка при выдаче ранга")

@admin.message(Command("rank"))
async def check_rank_command(message: Message):
    user_rank = await get_user_rank(message.from_user.id)
    if user_rank:
        await message.answer(f"🎖 Ваш ранг: {user_rank}")
    else:
        await message.answer("❌ Вы не зарегистрированы в системе")

@admin.message(Command("ranks"), RankFilter(Ranks.MODERATOR))
async def list_ranks_command(message: Message):
    ranks_list = "\n".join([f"• {rank}" for rank in RANKS_HIERARCHY.keys()])
    await message.answer(f"📋 Доступные ранги:\n{ranks_list}")
