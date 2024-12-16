from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, CommandStart, Command
import app.keyboards as kb
from aiogram.filters import Command
from aiogram.types import Message
from app.const import Ranks
from app.filters.rank_filter import RankFilter
from app.database.requests import change_user_rank, get_user_rank, init_owner_rank

admin = Router()

@admin.message(Command("init_owner"))
async def init_owner(message: Message):
    success = await init_owner_rank(message.from_user.id)
    if success:
        await message.answer("✅ Вы назначены владельцем бота")
    else:
        await message.answer("❌ Владелец уже назначен")

@admin.message(Command('admin'))
async def admin_cmd_start(message: Message):
    user_rank = await get_user_rank(message.from_user.id)
    keyboard = await kb.get_admin_keyboard(user_rank)
    await message.answer(
        text="🔧 Панель администратора\n\n"
             "Выберите нужное действие:",
        reply_markup=keyboard
    )

@admin.message(Command("setrank"), RankFilter(Ranks.OWNER.value))
async def set_rank_command(message: Message):
    try:
        args = message.text.split()[1:]
        if len(args) < 2:
            await message.answer("❌ Использование: /setrank @username ранг")
            return

        username = args[0].replace("@", "")
        new_rank = " ".join(args[1:])

        if new_rank not in [rank.value for rank in Ranks]:
            await message.answer("❌ Недопустимый ранг!")
            return

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
        print(f"Ошибка при выдаче ранга: {e}")
        await message.answer("❌ Произошла ошибка при выдаче ранга")

@admin.message(Command("rank"))
async def check_rank_command(message: Message):
    user_rank = await get_user_rank(message.from_user.id)
    if user_rank:
        await message.answer(f"🎖 Ваш ранг: {user_rank}")
    else:
        await message.answer("❌ Вы не зарегистрированы в системе")

@admin.message(Command("ranks"), RankFilter(Ranks.MODERATOR.value))
async def list_ranks_command(message: Message):
    ranks_list = "\n".join([f"• {rank.value}" for rank in Ranks])
    await message.answer(f"📋 Доступные ранги:\n{ranks_list}")
