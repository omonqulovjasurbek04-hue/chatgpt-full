import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN, MISTRAL_API_KEY
from bot.ai_client import close_client
from bot.middlewares import RateLimitMiddleware, ErrorHandlerMiddleware
from bot.handlers import commands, chat, ocr, audio
from bot.handlers.unsupported import router as unsupported_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties())
dp = Dispatcher()

async def set_bot_commands():
    bot_commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="help", description="Yordam"),
        BotCommand(command="clear", description="Chat tarixini tozalash"),
        BotCommand(command="ocr", description="Hujjat OCR (PDF, rasm)"),
        BotCommand(command="audio", description="Audio transkripsiya"),
    ]
    await bot.set_my_commands(bot_commands)

async def on_shutdown():
    logger.info("🛑 Bot to'xtatilmoqda...")
    await close_client()
    await bot.session.close()
    logger.info("✅ Barcha sessiyalar yopildi")

async def main():
    logger.info("🚀 Bot ishga tushmoqda...")

    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN topilmadi! .env faylini tekshiring.")
        return
    if not MISTRAL_API_KEY:
        logger.error("❌ MISTRAL_API_KEY topilmadi! .env faylini tekshiring.")
        return

    dp.message.middleware(ErrorHandlerMiddleware())
    dp.message.middleware(RateLimitMiddleware())

    dp.include_router(commands.router)
    dp.include_router(ocr.router)
    dp.include_router(audio.router)
    dp.include_router(chat.router)
    dp.include_router(unsupported_router)

    dp.shutdown.register(on_shutdown)

    await set_bot_commands()

    logger.info("✅ Bot tayyor! Xabarlar kutilmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
