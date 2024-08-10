from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.database.requests import set_user

import app.keyboards as kb

user = Router()

@user.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('qq')
    