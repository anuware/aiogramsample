from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.const import Ranks

async def get_admin_keyboard(user_rank: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    # Базовые кнопки для всех админов
    builder.add(InlineKeyboardButton(
        text="👥 Список рангов",
        callback_data="admin_ranks"
    ))
    
    # Кнопки только для владельца
    if user_rank == Ranks.OWNER.value:
        builder.add(InlineKeyboardButton(
            text="🎖 Выдать ранг",
            callback_data="give_rank"
        ))
    
    builder.adjust(1)  # Размещаем кнопки в один столбец
    return builder.as_markup()

async def get_ranks_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for rank in Ranks:
        builder.add(InlineKeyboardButton(
            text=rank.value,
            callback_data=f"select_rank_{rank.value}"
        ))
    
    builder.add(InlineKeyboardButton(
        text="↩️ Назад",
        callback_data="back_to_admin"
    ))
    
    builder.adjust(1)
    return builder.as_markup()
