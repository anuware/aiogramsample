from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database.requests import set_user

import app.keyboards as kb

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    await set_user(message.from_user.id, message.from_user.username)
    await message.answer('qq')
    