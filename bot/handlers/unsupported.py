from aiogram import Router, F
from aiogram.types import Message

router = Router()

@router.message(~F.text)
async def unsupported_content(message: Message):
    await message.answer(
        "⚠️ Hozircha faqat matnli xabarlar qo'llab-quvvatlanadi.\n\n"
        "💡 Rasm yoki hujjatni OCR qilish uchun URL yuboring:\n"
        "<code>/ocr https://example.com/document.pdf</code>",
        parse_mode="HTML"
    )
