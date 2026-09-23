# bot.py — Aiogram 3.x | Anagram O'yini (EN + RU)
import asyncio
import random
import logging
from typing import Dict, Any

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import bold, italic

from config import BOT_TOKEN

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

# ── Word banks ───────────────────────────────────────────────────────────────
EN_WORDS = [
    "python", "keyboard", "monitor", "library", "network",
    "algorithm", "elephant", "journey", "science", "bracket",
    "dragon", "culture", "history", "message", "balance",
    "cabinet", "diamond", "fortune", "gallery", "harvest",
    "imagine", "lantern", "mystery", "network", "palette",
    "quarter", "silence", "thunder", "vintage", "warrior",
    "bicycle", "captain", "dolphin", "empire", "fiction",
    "giraffe", "horizon", "kitchen", "leopard", "mustard",
]

RU_WORDS = [
    "привет", "солнце", "книга", "город", "земля",
    "вода", "огонь", "небо", "море", "лето",
    "зима", "весна", "осень", "школа", "наука",
    "музыка", "танец", "цветок", "звезда", "камень",
    "дерево", "птица", "рыба", "кошка", "собака",
    "белый", "чёрный", "красный", "синий", "зелёный",
    "большой", "малый", "новый", "старый", "добрый",
    "умный", "быстрый", "тихий", "громкий", "сильный",
]

ANSWER_TIME = 10  # seconds

# ── Scores storage (in-memory) ────────────────────────────────────────────────
scores: Dict[int, Dict[str, Any]] = {}

def get_score(user_id: int) -> Dict[str, Any]:
    if user_id not in scores:
        scores[user_id] = {"en": 0, "ru": 0, "total": 0}
    return scores[user_id]

# ── FSM States ───────────────────────────────────────────────────────────────
class GameState(StatesGroup):
    choosing_lang = State()
    playing_en    = State()
    playing_ru    = State()

# ── Helpers ──────────────────────────────────────────────────────────────────
def scramble(word: str) -> str:
    letters = list(word)
    while True:
        random.shuffle(letters)
        scrambled = "".join(letters)
        if scrambled != word:
            return scrambled

def lang_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
        ],
        [InlineKeyboardButton(text="📊 Natijalarim", callback_data="my_score")],
    ])

def stop_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🛑 To'xtatish")]],
        resize_keyboard=True,
        one_time_keyboard=False,
    )

# ── Bot & Dispatcher ──────────────────────────────────────────────────────────
bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())

# ── /start ────────────────────────────────────────────────────────────────────
@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    name = message.from_user.first_name or "Do'st"
    text = (
        f"👋 Salom, {bold(name)}! Xush kelibsiz!\n\n"
        f"🎮 {bold('Anagram O\'yini')} ga xush kelibsiz!\n\n"
        "📌 Qoidalar:\n"
        "• Aralashtirilgan harflardan to'g'ri so'z toping\n"
        f"• Har bir savol uchun ⏱ {bold(str(ANSWER_TIME))} soniya vaqt bor\n"
        "• To'g'ri javob = +1 ball\n\n"
        "🌍 Qaysi tilda o'ynamoqchisiz?"
    )
    await message.answer(text, reply_markup=lang_keyboard(), parse_mode="Markdown")
    await state.set_state(GameState.choosing_lang)


# ── /menu ─────────────────────────────────────────────────────────────────────
@dp.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "🏠 Asosiy menyu — til tanlang:",
        reply_markup=lang_keyboard()
    )
    await state.set_state(GameState.choosing_lang)


# ── Score callback ─────────────────────────────────────────────────────────────
@dp.callback_query(F.data == "my_score")
async def cb_my_score(call: CallbackQuery):
    uid  = call.from_user.id
    sc   = get_score(uid)
    text = (
        f"📊 {bold('Sizning natijangiz:')}\n\n"
        f"🇬🇧 English: {sc['en']} ball\n"
        f"🇷🇺 Русский: {sc['ru']} ball\n"
        f"🏆 Jami: {sc['total']} ball"
    )
    await call.message.answer(text, parse_mode="Markdown")
    await call.answer()


# ── Language selection ────────────────────────────────────────────────────────
@dp.callback_query(F.data.in_({"lang_en", "lang_ru"}))
async def cb_lang(call: CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    await call.answer()

    if lang == "en":
        await state.set_state(GameState.playing_en)
        await call.message.answer(
            "🇬🇧 *English mode* tanlandi!\nO'yin boshlanmoqda...",
            parse_mode="Markdown",
            reply_markup=stop_keyboard()
        )
        await send_question(call.message, state, "en")
    else:
        await state.set_state(GameState.playing_ru)
        await call.message.answer(
            "🇷🇺 *Русский режим* выбран!\nИгра начинается...",
            parse_mode="Markdown",
            reply_markup=stop_keyboard()
        )
        await send_question(call.message, state, "ru")


# ── Send question ─────────────────────────────────────────────────────────────
async def send_question(message: Message, state: FSMContext, lang: str):
    word_list = EN_WORDS if lang == "en" else RU_WORDS
    word      = random.choice(word_list)
    scrambled = scramble(word)

    await state.update_data(current_word=word, lang=lang, answered=False)

    if lang == "en":
        text = (
            f"🔤 {bold('Anagram:')} `{scrambled.upper()}`\n\n"
            f"Bu harflardan inglizcha so'z toping!\n"
            f"⏱ {ANSWER_TIME} soniya vaqtingiz bor..."
        )
    else:
        text = (
            f"🔤 {bold('Анаграмма:')} `{scrambled.upper()}`\n\n"
            f"Найдите русское слово из этих букв!\n"
            f"⏱ У вас {ANSWER_TIME} секунд..."
        )

    sent = await message.answer(text, parse_mode="Markdown")

    # Schedule timeout
    asyncio.create_task(check_timeout(message.chat.id, state, word, lang, ANSWER_TIME))


async def check_timeout(chat_id: int, state: FSMContext, word: str, lang: str, delay: int):
    await asyncio.sleep(delay)
    data = await state.get_data()

    # If already answered or game stopped, skip
    if data.get("answered", True) or data.get("current_word") != word:
        return

    await state.update_data(answered=True)

    if lang == "en":
        msg = f"⏰ Vaqt tugadi! To'g'ri javob: {bold(word.upper())}"
    else:
        msg = f"⏰ Время вышло! Правильный ответ: {bold(word.upper())}"

    try:
        await bot.send_message(chat_id, msg + "\n\n➡️ Keyingi so'z...", parse_mode="Markdown")
        await asyncio.sleep(1.5)

        # Continue game
        current_state = await state.get_state()
        if current_state in (GameState.playing_en.state, GameState.playing_ru.state):
            class FakeMsg:
                def __init__(self, cid): self.chat = type("C", (), {"id": cid})()
                async def answer(self, *a, **kw): return await bot.send_message(chat_id, *a, **kw)
            await send_question(FakeMsg(chat_id), state, lang)
    except Exception:
        pass


# ── Answer handler — English ──────────────────────────────────────────────────
@dp.message(GameState.playing_en)
async def handle_answer_en(message: Message, state: FSMContext):
    if message.text == "🛑 To'xtatish":
        await stop_game(message, state)
        return

    data     = await state.get_data()
    word     = data.get("current_word", "")
    answered = data.get("answered", False)

    if answered:
        return

    guess = message.text.strip().lower()

    if guess == word:
        await state.update_data(answered=True)
        uid = message.from_user.id
        sc  = get_score(uid)
        sc["en"]    += 1
        sc["total"] += 1

        await message.answer(
            f"✅ {bold('To\'g\'ri!')} +1 ball 🎉\n"
            f"So'z: {bold(word.upper())}\n"
            f"🇬🇧 Ballingiz: {sc['en']}",
            parse_mode="Markdown"
        )
        await asyncio.sleep(1.5)
        await send_question(message, state, "en")
    else:
        await message.answer(
            f"❌ Noto'g'ri! Qaytadan urinib ko'ring... ⏱",
            parse_mode="Markdown"
        )


# ── Answer handler — Russian ──────────────────────────────────────────────────
@dp.message(GameState.playing_ru)
async def handle_answer_ru(message: Message, state: FSMContext):
    if message.text == "🛑 To'xtatish":
        await stop_game(message, state)
        return

    data     = await state.get_data()
    word     = data.get("current_word", "")
    answered = data.get("answered", False)

    if answered:
        return

    guess = message.text.strip().lower()

    if guess == word:
        await state.update_data(answered=True)
        uid = message.from_user.id
        sc  = get_score(uid)
        sc["ru"]    += 1
        sc["total"] += 1

        await message.answer(
            f"✅ {bold('Правильно!')} +1 очко 🎉\n"
            f"Слово: {bold(word.upper())}\n"
            f"🇷🇺 Очков: {sc['ru']}",
            parse_mode="Markdown"
        )
        await asyncio.sleep(1.5)
        await send_question(message, state, "ru")
    else:
        await message.answer(
            f"❌ Неверно! Попробуйте ещё раз... ⏱",
            parse_mode="Markdown"
        )


# ── Stop game ─────────────────────────────────────────────────────────────────
async def stop_game(message: Message, state: FSMContext):
    uid = message.from_user.id
    sc  = get_score(uid)
    await state.clear()

    text = (
        f"🛑 {bold('O\'yin tugadi!')}\n\n"
        f"📊 Sizning natijangiz:\n"
        f"🇬🇧 English: {sc['en']} ball\n"
        f"🇷🇺 Русский: {sc['ru']} ball\n"
        f"🏆 Jami: {sc['total']} ball\n\n"
        "Qayta o'ynash uchun /start bosing!"
    )
    await message.answer(text, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")


# ── /score ────────────────────────────────────────────────────────────────────
@dp.message(Command("score"))
async def cmd_score(message: Message):
    uid = message.from_user.id
    sc  = get_score(uid)
    text = (
        f"📊 {bold('Sizning natijangiz:')}\n\n"
        f"🇬🇧 English: {sc['en']} ball\n"
        f"🇷🇺 Русский: {sc['ru']} ball\n"
        f"🏆 Jami: {sc['total']} ball"
    )
    await message.answer(text, parse_mode="Markdown")


# ── /help ─────────────────────────────────────────────────────────────────────
@dp.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        f"📖 {bold('Yordam')}\n\n"
        "🎮 Buyruqlar:\n"
        "/start — Botni ishga tushirish\n"
        "/menu  — Til tanlash menyusi\n"
        "/score — Natijalaringizni ko'rish\n"
        "/help  — Yordam\n\n"
        "🎯 O'yin qoidalari:\n"
        "• Aralashtirilgan harflardan to'g'ri so'z yozing\n"
        f"• Har savol uchun {ANSWER_TIME} soniya\n"
        "• To'g'ri javob = +1 ball\n"
        "• 🛑 To'xtatish tugmasi bilan o'yinni to'xtatishingiz mumkin"
    )
    await message.answer(text, parse_mode="Markdown")


# ── Main ──────────────────────────────────────────────────────────────────────
async def main():
    log.info("Bot ishga tushmoqda...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
