from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode, ChatAction

from bot.ai_client import mistral_ocr
from bot.utils.sender import send_long_message
from bot.utils.validator import is_valid_url

router = Router()

@router.message(Command("ocr"))
async def cmd_ocr(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "📄 <b>OCR foydalanish:</b>\n"
            "<code>/ocr &lt;hujjat_url&gt;</code>\n\n"
            "Misol: <code>/ocr https://arxiv.org/pdf/2201.04234</code>",
            parse_mode=ParseMode.HTML
        )
        return

    url = args[1].strip()

    if not is_valid_url(url):
        await message.answer("⚠️ Noto'g'ri URL format. Iltimos, to'g'ri HTTP/HTTPS havola yuboring.")
        return

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    processing_msg = await message.answer("⏳ Hujjat o'qilmoqda...")

    user_id = message.from_user.id
    result = await mistral_ocr(user_id, url)
    await send_long_message(message, processing_msg, result, "📄 <b>OCR natijasi:</b>\n\n")
