from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from bot.ai_client import clear_history
from bot.config import (
    CHAT_MODELS, OCR_MODELS, AUDIO_MODELS,
    get_user_model, set_user_model
)

router = Router()

def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💬 Chat"),
                KeyboardButton(text="📄 OCR"),
                KeyboardButton(text="🎙 Audio"),
            ],
            [
                KeyboardButton(text="⚙️ Modellar"),
                KeyboardButton(text="🗑 Tozalash"),
                KeyboardButton(text="📖 Yordam"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Savolingizni yozing..."
    )
    return keyboard

def get_models_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="💬 Chat modeli", callback_data="models_chat")],
        [InlineKeyboardButton(text="📄 OCR modeli", callback_data="models_ocr")],
        [InlineKeyboardButton(text="🎙 Audio modeli", callback_data="models_audio")],
        [InlineKeyboardButton(text="❌ Yopish", callback_data="models_close")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_chat_models_keyboard(user_id: int) -> InlineKeyboardMarkup:
    current = get_user_model(user_id, "chat")
    buttons = []
    for model_id, model_name in CHAT_MODELS.items():
        check = " ✅" if model_id == current else ""
        buttons.append([
            InlineKeyboardButton(
                text=f"{model_name}{check}",
                callback_data=f"set_chat_{model_id}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="models_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_ocr_models_keyboard(user_id: int) -> InlineKeyboardMarkup:
    current = get_user_model(user_id, "ocr")
    buttons = []
    for model_id, model_name in OCR_MODELS.items():
        check = " ✅" if model_id == current else ""
        buttons.append([
            InlineKeyboardButton(
                text=f"{model_name}{check}",
                callback_data=f"set_ocr_{model_id}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="models_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_audio_models_keyboard(user_id: int) -> InlineKeyboardMarkup:
    current = get_user_model(user_id, "audio")
    buttons = []
    for model_id, model_name in AUDIO_MODELS.items():
        check = " ✅" if model_id == current else ""
        buttons.append([
            InlineKeyboardButton(
                text=f"{model_name}{check}",
                callback_data=f"set_audio_{model_id}"
            )
        ])
    buttons.append([InlineKeyboardButton(text="⬅️ Orqaga", callback_data="models_back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_current_models_text(user_id: int) -> str:
    chat_model = get_user_model(user_id, "chat")
    ocr_model = get_user_model(user_id, "ocr")
    audio_model = get_user_model(user_id, "audio")

    chat_name = CHAT_MODELS.get(chat_model, chat_model)
    ocr_name = OCR_MODELS.get(ocr_model, ocr_model)
    audio_name = AUDIO_MODELS.get(audio_model, audio_model)

    return (
        "⚙️ <b>Model sozlamalari</b>\n\n"
        f"💬 <b>Chat:</b> {chat_name}\n"
        f"   <code>{chat_model}</code>\n\n"
        f"📄 <b>OCR:</b> {ocr_name}\n"
        f"   <code>{ocr_model}</code>\n\n"
        f"🎙 <b>Audio:</b> {audio_name}\n"
        f"   <code>{audio_model}</code>\n\n"
        "Modelni o'zgartirish uchun quyidagi tugmalarni bosing:"
    )

@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome = (
        "🤖 <b>Salom! Men Mistral AI botman!</b>\n\n"
        "Men sizga quyidagi xizmatlarni taqdim etaman:\n\n"
        "💬 <b>Chat</b> — Menga istalgan savolingizni yozing\n"
        "📄 <b>OCR</b> — Hujjatni o'qish\n"
        "🎙 <b>Audio</b> — Audioni matnga aylantirish\n"
        "⚙️ <b>Modellar</b> — AI modelini tanlash\n"
        "🗑 <b>Tozalash</b> — Chat tarixini tozalash\n\n"
        "Quyidagi tugmalardan foydalaning yoki oddiy xabar yozing! ⬇️"
    )
    await message.answer(welcome, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())

@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "📖 <b>Yordam</b>\n\n"
        "<b>Tugmalar:</b>\n"
        "💬 <b>Chat</b> — Chat rejimiga o'tish\n"
        "📄 <b>OCR</b> — Hujjat URL kiritish\n"
        "🎙 <b>Audio</b> — Audio URL kiritish\n"
        "⚙️ <b>Modellar</b> — AI modelini tanlash\n"
        "🗑 <b>Tozalash</b> — Tarixni tozalash\n\n"
        "<b>Buyruqlar:</b>\n"
        "/start — Botni ishga tushirish\n"
        "/help — Yordam\n"
        "/clear — Chat tarixini tozalash\n"
        "/models — Model sozlamalari\n"
        "/ocr <code>&lt;url&gt;</code> — Hujjat OCR\n"
        "/audio <code>&lt;url&gt;</code> — Audio transkripsiya\n\n"
        "<b>Foydalanish:</b>\n"
        "Oddiy xabar yozing — men javob beraman!\n"
        "Hujjat: <code>/ocr https://arxiv.org/pdf/2201.04234</code>\n"
        "Audio: <code>/audio https://example.com/audio.mp3</code>"
    )
    await message.answer(help_text, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())

@router.message(Command("clear"))
async def cmd_clear(message: Message):
    user_id = message.from_user.id
    clear_history(user_id)
    await message.answer(
        "🗑 Chat tarixi tozalandi! Yangi suhbat boshlashingiz mumkin.",
        reply_markup=get_main_keyboard()
    )

@router.message(Command("models"))
async def cmd_models(message: Message):
    user_id = message.from_user.id
    text = get_current_models_text(user_id)
    await message.answer(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_models_menu_keyboard()
    )

@router.message(lambda m: m.text == "📖 Yordam")
async def btn_help(message: Message):
    await cmd_help(message)

@router.message(lambda m: m.text == "🗑 Tozalash")
async def btn_clear(message: Message):
    await cmd_clear(message)

@router.message(lambda m: m.text == "⚙️ Modellar")
async def btn_models(message: Message):
    await cmd_models(message)

@router.message(lambda m: m.text == "💬 Chat")
async def btn_chat(message: Message):
    await message.answer(
        "💬 <b>Chat rejimi faol!</b>\n\n"
        "Menga istalgan savolingizni yozing, men javob beraman.",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

@router.message(lambda m: m.text == "📄 OCR")
async def btn_ocr(message: Message):
    await message.answer(
        "📄 <b>OCR rejimi</b>\n\n"
        "Hujjat URL ni quyidagi formatda yuboring:\n"
        "<code>/ocr https://example.com/document.pdf</code>\n\n"
        "Qo'llab-quvvatlanadigan formatlar: PDF, rasm (JPG, PNG)",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

@router.message(lambda m: m.text == "🎙 Audio")
async def btn_audio(message: Message):
    await message.answer(
        "🎙 <b>Audio transkripsiya</b>\n\n"
        "Audio URL ni quyidagi formatda yuboring:\n"
        "<code>/audio https://example.com/audio.mp3</code>\n\n"
        "Qo'llab-quvvatlanadigan formatlar: MP3, WAV, FLAC, OGG",
        parse_mode=ParseMode.HTML,
        reply_markup=get_main_keyboard()
    )

@router.callback_query(lambda c: c.data == "models_chat")
async def cb_models_chat(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        "💬 <b>Chat modelini tanlang:</b>\n\n"
        "Tanlangan model barcha chat so'rovlari uchun ishlatiladi.",
        parse_mode=ParseMode.HTML,
        reply_markup=get_chat_models_keyboard(user_id)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "models_ocr")
async def cb_models_ocr(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        "📄 <b>OCR modelini tanlang:</b>\n\n"
        "Tanlangan model hujjat o'qish uchun ishlatiladi.",
        parse_mode=ParseMode.HTML,
        reply_markup=get_ocr_models_keyboard(user_id)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "models_audio")
async def cb_models_audio(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        "🎙 <b>Audio modelini tanlang:</b>\n\n"
        "Tanlangan model audio transkripsiya uchun ishlatiladi.",
        parse_mode=ParseMode.HTML,
        reply_markup=get_audio_models_keyboard(user_id)
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "models_back")
async def cb_models_back(callback: CallbackQuery):
    user_id = callback.from_user.id
    text = get_current_models_text(user_id)
    await callback.message.edit_text(
        text,
        parse_mode=ParseMode.HTML,
        reply_markup=get_models_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(lambda c: c.data == "models_close")
async def cb_models_close(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer("✅ Menyu yopildi")

@router.callback_query(lambda c: c.data and c.data.startswith("set_chat_"))
async def cb_set_chat_model(callback: CallbackQuery):
    user_id = callback.from_user.id
    model_id = callback.data.replace("set_chat_", "")

    if model_id in CHAT_MODELS:
        set_user_model(user_id, "chat", model_id)
        model_name = CHAT_MODELS[model_id]
        await callback.answer(f"✅ {model_name} tanlandi!")
        await callback.message.edit_text(
            f"💬 <b>Chat modelini tanlang:</b>\n\n"
            f"✅ Hozirgi model: <b>{model_name}</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_chat_models_keyboard(user_id)
        )
    else:
        await callback.answer("❌ Model topilmadi", show_alert=True)

@router.callback_query(lambda c: c.data and c.data.startswith("set_ocr_"))
async def cb_set_ocr_model(callback: CallbackQuery):
    user_id = callback.from_user.id
    model_id = callback.data.replace("set_ocr_", "")

    if model_id in OCR_MODELS:
        set_user_model(user_id, "ocr", model_id)
        model_name = OCR_MODELS[model_id]
        await callback.answer(f"✅ {model_name} tanlandi!")
        await callback.message.edit_text(
            f"📄 <b>OCR modelini tanlang:</b>\n\n"
            f"✅ Hozirgi model: <b>{model_name}</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_ocr_models_keyboard(user_id)
        )
    else:
        await callback.answer("❌ Model topilmadi", show_alert=True)

@router.callback_query(lambda c: c.data and c.data.startswith("set_audio_"))
async def cb_set_audio_model(callback: CallbackQuery):
    user_id = callback.from_user.id
    model_id = callback.data.replace("set_audio_", "")

    if model_id in AUDIO_MODELS:
        set_user_model(user_id, "audio", model_id)
        model_name = AUDIO_MODELS[model_id]
        await callback.answer(f"✅ {model_name} tanlandi!")
        await callback.message.edit_text(
            f"🎙 <b>Audio modelini tanlang:</b>\n\n"
            f"✅ Hozirgi model: <b>{model_name}</b>",
            parse_mode=ParseMode.HTML,
            reply_markup=get_audio_models_keyboard(user_id)
        )
    else:
        await callback.answer("❌ Model topilmadi", show_alert=True)
