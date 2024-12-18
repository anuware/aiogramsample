from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_admin_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="👥 Пользователи", callback_data="users_list"),
            InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")
        ],
        [
            InlineKeyboardButton(text="📊 Статистика", callback_data="stats")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)