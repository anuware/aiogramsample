from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.const import Ranks
from app.filters.rank_filter import RankFilter
from app.database.requests import (
    change_user_rank, 
    get_user_rank, 
    init_owner_rank,
    #find_user_by_username
)
import app.keyboards as kb

admin = Router()

class RankStates(StatesGroup):
    waiting_for_username = State()

@admin.message(Command("init_owner"))
async def init_owner(message: Message):
    is_success = await init_owner_rank(message.from_user.id)
    await message.answer(
        "✅ Вы назначены владельцем бота" if is_success 
        else "❌ Владелец уже назначен"
    )

@admin.message(Command('admin'))
async def admin_panel(message: Message):
    keyboard = await kb.get_admin_keyboard(
        await get_user_rank(session, message.from_user.id)
    )
    await message.answer(
        "🔧 Панель администратора\n\nВыберите нужное действие:",
        reply_markup=keyboard
    )

@admin.message(Command("setrank"), RankFilter(Ranks.OWNER.value))
async def set_rank(message: Message):
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

        user = await find_user_by_username(username)
        if not user:
            await message.answer("❌ Пользователь не найден!")
            return

        await change_user_rank(user.tg_id, new_rank)
        await message.answer(f"✅ Пользователю @{username} выдан ранг {new_rank}")

    except Exception as e:
        print(f"Ошибка при выдаче ранга: {e}")
        await message.answer("❌ Произошла ошибка при выдаче ранга")

@admin.message(Command("rank"))
async def check_rank(message: Message):
    rank = await get_user_rank(message.from_user.id)
    await message.answer(
        f"🎖 Ваш ранг: {rank}" if rank 
        else "❌ Вы не зарегистрированы в системе"
    )

@admin.message(Command("ranks"), RankFilter(Ranks.MODERATOR.value))
async def list_ranks(message: Message):
    ranks = "\n".join(f"• {rank.value}" for rank in Ranks)
    await message.answer(f"📋 Доступные ранги:\n{ranks}")

@admin.callback_query(lambda c: c.data == "admin_ranks")
async def show_ranks_list(callback: CallbackQuery):
    ranks = "\n".join(f"• {rank.value}" for rank in Ranks)
    await callback.message.edit_text(
        f"📋 Доступные ранги:\n{ranks}",
        reply_markup=await kb.get_admin_keyboard(
            await get_user_rank(callback.from_user.id)
        )
    )

@admin.callback_query(lambda c: c.data == "give_rank")
async def start_give_rank(callback: CallbackQuery, state: FSMContext):
    if await get_user_rank(callback.from_user.id) != Ranks.OWNER.value:
        await callback.answer("❌ Недостаточно прав!", show_alert=True)
        return
    
    await callback.message.edit_text(
        "👤 Введите @username пользователя, которому хотите выдать ранг:",
        reply_markup=await kb.get_ranks_keyboard()
    )
    await state.set_state(RankStates.waiting_for_username)

@admin.message(RankStates.waiting_for_username)
async def process_username(message: Message, state: FSMContext):
    username = message.text.replace("@", "")
    
    user = await find_user_by_username(username)
    if not user:
        await message.answer(
            "❌ Пользователь не найден!",
            reply_markup=await kb.get_admin_keyboard(
                await get_user_rank(message.from_user.id)
            )
        )
        await state.clear()
        return
    
    await state.update_data(target_username=username)
    await message.answer(
        f"🎯 Выберите ранг для пользователя @{username}:",
        reply_markup=await kb.get_ranks_keyboard()
    )

@admin.callback_query(lambda c: c.data.startswith("select_rank_"))
async def process_rank_selection(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    username = data.get("target_username")
    
    if not username:
        await callback.answer("❌ Ошибка: не указан пользователь", show_alert=True)
        await state.clear()
        return
    
    new_rank = callback.data.replace("select_rank_", "")
    user = await find_user_by_username(username)
    
    if not user:
        await callback.answer("❌ Пользователь не найден!", show_alert=True)
        await state.clear()
        return
    
    await change_user_rank(user.tg_id, new_rank)
    await callback.message.edit_text(
        f"✅ Пользователю @{username} выдан ранг {new_rank}",
        reply_markup=await kb.get_admin_keyboard(
            await get_user_rank(callback.from_user.id)
        )
    )
    await state.clear()

@admin.callback_query(lambda c: c.data == "back_to_admin")
async def back_to_admin_panel(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        "🔧 Панель администратора\n\nВыберите нужное действие:",
        reply_markup=await kb.get_admin_keyboard(
            await get_user_rank(callback.from_user.id)
        )
    )