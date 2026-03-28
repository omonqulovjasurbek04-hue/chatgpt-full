import os
from dotenv import load_dotenv

load_dotenv()

# ===== Bot Config =====
BOT_TOKEN = os.getenv("BOT_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# ===== Chat Settings =====
MAX_HISTORY = 20
RATE_LIMIT_SECONDS = 2

# ===== AI Models — Mavjud variantlar =====
CHAT_MODELS = {
    "mistral-medium-latest": "🧠 Mistral Medium",
    "mistral-large-latest": "🚀 Mistral Large",
    "mistral-small-latest": "⚡ Mistral Small",
    "open-mistral-nemo": "🌟 Mistral Nemo",
}

OCR_MODELS = {
    "mistral-ocr-latest": "📄 Mistral OCR",
}

AUDIO_MODELS = {
    "voxtral-mini-latest": "🎙 Voxtral Mini",
}

# ===== Default modellar =====
DEFAULT_CHAT_MODEL = "mistral-medium-latest"
DEFAULT_OCR_MODEL = "mistral-ocr-latest"
DEFAULT_AUDIO_MODEL = "voxtral-mini-latest"

# ===== Foydalanuvchi sozlamalari (user_id -> settings) =====
user_settings: dict[int, dict[str, str]] = {}


def get_user_model(user_id: int, model_type: str) -> str:
    """Foydalanuvchining tanlagan modelini olish"""
    if user_id in user_settings and model_type in user_settings[user_id]:
        return user_settings[user_id][model_type]

    defaults = {
        "chat": DEFAULT_CHAT_MODEL,
        "ocr": DEFAULT_OCR_MODEL,
        "audio": DEFAULT_AUDIO_MODEL,
    }
    return defaults.get(model_type, DEFAULT_CHAT_MODEL)


def set_user_model(user_id: int, model_type: str, model_name: str):
    """Foydalanuvchi modelini o'zgartirish"""
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id][model_type] = model_name


# ===== System Prompt =====
SYSTEM_PROMPT = {
    "role": "system",
    "content": (
        "Siz foydali, do'stona va aqlli AI yordamchisiz. "
        "Foydalanuvchi qaysi tilda yozsa, o'sha tilda javob bering. "
        "Javoblaringiz aniq, lo'nda va foydali bo'lsin. "
        "Agar savolga javob bilmasangiz, ochiq ayting."
    )
}
