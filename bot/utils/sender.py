import logging

from aiogram.types import Message
from aiogram.enums import ParseMode

from bot.utils.formatter import format_to_html

logger = logging.getLogger(__name__)

async def send_long_message(message: Message, processing_msg: Message, text: str, prefix: str = ""):
    full_text = f"{prefix}{text}" if prefix else text

    chunks = [full_text[i:i + 4000] for i in range(0, len(full_text), 4000)]

    for i, chunk in enumerate(chunks):
        html_chunk = format_to_html(chunk)

        try:
            if i == 0:
                await processing_msg.edit_text(html_chunk, parse_mode=ParseMode.HTML)
            else:
                await message.answer(html_chunk, parse_mode=ParseMode.HTML)
        except Exception as e:
            logger.warning(f"HTML yuborishda xato: {e}, oddiy matn sifatida yuborilmoqda.")
            try:
                if i == 0:
                    await processing_msg.edit_text(chunk)
                else:
                    await message.answer(chunk)
            except Exception as inner_e:
                logger.error(f"Fallback xabar yuborishda xato: {inner_e}")
