from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatAction

from bot.ai_client import mistral_chat
from bot.utils.sender import send_long_message

router = Router()

@router.message(F.text)
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_text = message.text

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    processing_msg = await message.answer("⏳ O'ylayapman...")

    result = await mistral_chat(user_id, user_text)
    await send_long_message(message, processing_msg, result)
