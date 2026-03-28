from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode, ChatAction

from bot.ai_client import mistral_transcribe
from bot.utils.sender import send_long_message
from bot.utils.validator import is_valid_url

router = Router()


# ===== /audio <url> =====
@router.message(Command("audio"))
async def cmd_audio(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "🎙 <b>Audio foydalanish:</b>\n"
            "<code>/audio &lt;audio_url&gt;</code>\n\n"
            "Misol: <code>/audio https://docs.mistral.ai/audio/obama.mp3</code>",
            parse_mode=ParseMode.HTML
        )
        return

    url = args[1].strip()

    # URL validatsiya
    if not is_valid_url(url):
        await message.answer("⚠️ Noto'g'ri URL format. Iltimos, to'g'ri HTTP/HTTPS havola yuboring.")
        return

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    processing_msg = await message.answer("⏳ Audio transkripsiya qilinmoqda...")

    user_id = message.from_user.id
    result = await mistral_transcribe(user_id, url)
    await send_long_message(message, processing_msg, result, "🎙 <b>Transkripsiya:</b>\n\n")
