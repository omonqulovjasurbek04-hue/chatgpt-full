import time
import logging
from typing import Callable, Any, Awaitable
from collections import defaultdict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

from bot.config import RATE_LIMIT_SECONDS

logger = logging.getLogger(__name__)

class RateLimitMiddleware(BaseMiddleware):

    def __init__(self):
        self.user_last_request: dict[int, float] = defaultdict(float)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message) or not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        now = time.time()

        if now - self.user_last_request[user_id] < RATE_LIMIT_SECONDS:
            logger.info(f"Rate limit: user {user_id} juda tez yozmoqda")
            await event.answer("⏳ Iltimos, biroz kuting...")
            return

        self.user_last_request[user_id] = now
        return await handler(event, data)


class ErrorHandlerMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(
                f"Handler xatosi (user={getattr(event, 'from_user', None)}): {e}",
                exc_info=True
            )
            if isinstance(event, Message):
                try:
                    await event.answer(
                        "❌ Kutilmagan xato yuz berdi. Iltimos, keyinroq urinib ko'ring.\n"
                        "Muammo davom etsa, /clear buyrug'ini ishlating."
                    )
                except Exception:
                    pass
