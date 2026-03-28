import logging

from mistralai import Mistral

from bot.config import MISTRAL_API_KEY, SYSTEM_PROMPT, MAX_HISTORY, get_user_model

logger = logging.getLogger(__name__)

# ===== Mistral Client =====
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

# ===== Chat tarixi (user_id -> messages) =====
chat_histories: dict[int, list[dict]] = {}


def _trim_history(user_id: int):
    """Tarixni MAX_HISTORY ga cheklash (memory leak oldini olish)"""
    if len(chat_histories[user_id]) > MAX_HISTORY:
        chat_histories[user_id] = chat_histories[user_id][-MAX_HISTORY:]


def clear_history(user_id: int):
    """Foydalanuvchi tarixini tozalash"""
    chat_histories[user_id] = []


async def mistral_chat(user_id: int, user_message: str) -> str:
    """Mistral AI bilan asinxron chat qilish — foydalanuvchi tanlagan model bilan"""
    if user_id not in chat_histories:
        chat_histories[user_id] = []

    chat_histories[user_id].append({
        "role": "user",
        "content": user_message
    })

    _trim_history(user_id)

    # Foydalanuvchi tanlagan chat modelini olish
    chat_model = get_user_model(user_id, "chat")

    # System prompt + oxirgi xabarlar
    messages = [SYSTEM_PROMPT] + chat_histories[user_id]

    try:
        response = await mistral_client.chat.complete_async(
            model=chat_model,
            messages=messages
        )

        assistant_message = response.choices[0].message.content

        chat_histories[user_id].append({
            "role": "assistant",
            "content": assistant_message
        })

        _trim_history(user_id)
        return assistant_message

    except Exception as e:
        logger.error(f"Mistral chat xatosi (model={chat_model}): {e}", exc_info=True)
        return "❌ Xato yuz berdi. Iltimos, keyinroq urinib ko'ring."


async def mistral_ocr(user_id: int, document_url: str) -> str:
    """Hujjatni asinxron OCR qilish — foydalanuvchi tanlagan model bilan"""
    ocr_model = get_user_model(user_id, "ocr")

    try:
        response = await mistral_client.ocr.process_async(
            model=ocr_model,
            document={
                "type": "document_url",
                "document_url": document_url
            },
            include_image_base64=False
        )

        result_text = ""
        if hasattr(response, 'pages'):
            for page in response.pages:
                if hasattr(page, 'markdown'):
                    result_text += page.markdown + "\n\n"
                elif hasattr(page, 'text'):
                    result_text += page.text + "\n\n"

        return result_text.strip() if result_text else str(response)

    except Exception as e:
        logger.error(f"OCR xatosi (model={ocr_model}): {e}", exc_info=True)
        return "❌ OCR xatosi yuz berdi. URL to'g'riligini tekshiring."


async def mistral_transcribe(user_id: int, audio_url: str) -> str:
    """Audio faylni asinxron matnga aylantirish — foydalanuvchi tanlagan model bilan"""
    audio_model = get_user_model(user_id, "audio")

    try:
        response = await mistral_client.audio.transcriptions.create_async(
            model=audio_model,
            file_url=audio_url
        )

        if hasattr(response, 'text'):
            return response.text
        return str(response)

    except Exception as e:
        logger.error(f"Transkripsiya xatosi (model={audio_model}): {e}", exc_info=True)
        return "❌ Transkripsiya xatosi yuz berdi. Audio URL to'g'riligini tekshiring."


async def close_client():
    """Mistral client sessiyasini yopish (graceful shutdown)"""
    try:
        await mistral_client.close_async()
        logger.info("Mistral client yopildi")
    except Exception as e:
        logger.warning(f"Mistral client yopishda xato: {e}")
