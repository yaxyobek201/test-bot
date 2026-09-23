# ╔══════════════════════════════════════════════════════════════╗
# ║  AUTO-INSTALL + ANAGRAM BOT — Aiogram 3.x | EN + RU        ║
# ║  Tokenni kiriting → Run → Tayyor!                           ║
# ╚══════════════════════════════════════════════════════════════╝

import subprocess, sys

def install(pkg):
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])

try:
    import aiogram
except ImportError:
    print("📦 aiogram o'rnatilmoqda...")
    install("aiogram==3.13.1")
    print("✅ aiogram o'rnatildi!")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
import asyncio, random, logging
from typing import Dict, Any

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.markdown import bold

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🔑  TOKENNI SHU YERGA KIRITING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOT_TOKEN = 
# Misol: BOT_TOKEN = "1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

# ── So'z bazalari ────────────────────────────────────────────────────────────
EN_WORDS: Dict[str, str] = {
    "python":   "🐍 A popular programming language",
    "keyboard": "⌨️ You type with it",
    "monitor":  "🖥️ You see things on it",
    "library":  "📚 A place full of books",
    "network":  "🌐 Connects computers together",
    "elephant": "🐘 Largest land animal",
    "journey":  "🗺️ A long trip or travel",
    "science":  "🔬 Study of the natural world",
    "dragon":   "🐉 A mythical fire-breathing creature",
    "culture":  "🎭 Art, music, traditions of a society",
    "history":  "📜 Study of past events",
    "balance":  "⚖️ Equal weight on both sides",
    "cabinet":  "🗄️ Furniture for storing things",
    "diamond":  "💎 The hardest natural material",
    "fortune":  "🍀 Luck or great wealth",
    "gallery":  "🖼️ A place to display art",
    "harvest":  "🌾 Gathering crops from fields",
    "imagine":  "💭 To picture in your mind",
    "lantern":  "🏮 A portable light source",
    "mystery":  "🔍 Something unexplained or secret",
    "quarter":  "🪙 One fourth of something",
    "silence":  "🤫 Complete absence of sound",
    "thunder":  "⛈️ Loud sound during a storm",
    "vintage":  "🍷 Something old and high quality",
    "warrior":  "⚔️ A brave fighter or soldier",
    "bicycle":  "🚲 Two-wheeled human-powered vehicle",
    "captain":  "⚓ Leader of a ship or team",
    "dolphin":  "🐬 An intelligent sea mammal",
    "fiction":  "📖 Stories that are not real",
    "giraffe":  "🦒 Tallest living terrestrial animal",
    "horizon":  "🌅 Where sky meets the earth",
    "kitchen":  "🍳 Room where food is cooked",
    "leopard":  "🐆 A spotted wild cat",
    "compass":  "🧭 Navigation tool showing directions",
    "feather":  "🪶 Light covering of a bird",
    "glacier":  "🏔️ A slow-moving mass of ice",
    "hamster":  "🐹 A small furry pet rodent",
    "lantern":  "🏮 A portable light source",
    "blanket":  "🛏️ Keeps you warm at night",
    "captain":  "⚓ Leader of a ship or team",
}

RU_WORDS: Dict[str, str] = {
    "привет":  "👋 Слово приветствия",
    "солнце":  "☀️ Звезда в центре нашей системы",
    "книга":   "📚 В ней есть страницы и текст",
    "город":   "🏙️ Большое населённое место",
    "земля":   "🌍 Наша планета",
    "огонь":   "🔥 Горячее и светящееся явление",
    "небо":    "☁️ Голубое пространство над нами",
    "море":    "🌊 Большое солёное водное пространство",
    "школа":   "🏫 Место, где учатся дети",
    "наука":   "🔬 Изучение мира вокруг нас",
    "музыка":  "🎵 Звуки, создающие мелодию",
    "танец":   "💃 Движения тела под музыку",
    "цветок":  "🌸 Красивое растение с лепестками",
    "звезда":  "⭐ Светящийся объект в небе ночью",
    "камень":  "🪨 Твёрдый природный материал",
    "дерево":  "🌳 Высокое растение с ветвями",
    "птица":   "🐦 Существо с крыльями и перьями",
    "кошка":   "🐱 Популярное домашнее животное",
    "собака":  "🐶 Верный друг человека",
    "красный": "🔴 Цвет огня и крови",
    "синий":   "🔵 Цвет неба и моря",
    "зелёный": "🟢 Цвет травы и листьев",
    "новый":   "✨ Только что сделанный",
    "добрый":  "😊 Добросердечный и отзывчивый",
    "умный":   "🧠 Обладающий большим умом",
    "быстрый": "⚡ Движущийся с большой скоростью",
    "тихий":   "🤫 Издающий мало шума",
    "сильный": "💪 Обладающий большой силой",
    "весна":   "🌷 Время года после зимы",
    "осень":   "🍂 Время года перед зимой",
    "зима":    "❄️ Самое холодное время года",
    "лето":    "🌞 Самое тёплое время года",
    "рыба":    "🐟 Животное, живущее в воде",
    "волк":    "🐺 Дикое животное из леса",
    "орёл":    "🦅 Крупная хищная птица",
    "гора":    "⛰️ Высокая возвышенность",
    "река":    "🏞️ Поток пресной воды",
    "ветер":   "🌬️ Движение воздуха",
    "месяц":   "🌙 Ночное светило",
    "сердце":  "❤️ Главный орган тела",
}

ANSWER_TIME = 10
TIMER_BARS  = ["🟥🟥🟥🟥🟥", "🟧🟧🟧🟧⬜", "🟨🟨🟨⬜⬜", "🟩🟩⬜⬜⬜", "🟩⬜⬜⬜⬜"]

scores: Dict[int, Dict[str, Any]] = {}

def get_score(uid: int) -> Dict[str, Any]:
    if uid not in scores:
        scores[uid] = {"en": 0, "ru": 0, "total": 0, "streak": 0, "best": 0}
    return scores[uid]

class GS(StatesGroup):
    choose = State()
    en     = State()
    ru     = State()

def scramble(word: str) -> str:
    letters = list(word)
    for _ in range(100):
        random.shuffle(letters)
        if "".join(letters) != word:
            return "".join(letters)
    return "".join(letters)

def hint(word: str) -> str:
    return word[0].upper() + " " + " ".join("_" for _ in word[1:])

def tbar(left: int) -> str:
    idx = max(0, min(4, 4 - (left - 1) // 2))
    return TIMER_BARS[idx]

def main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇬🇧 English", callback_data="L_en"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="L_ru"),
        ],
        [
            InlineKeyboardButton(text="📊 Natija", callback_data="score"),
            InlineKeyboardButton(text="❓ Yordam",  callback_data="help"),
        ],
    ])

def game_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💡 Maslahat"), KeyboardButton(text="⏭ O'tkazish")],
            [KeyboardButton(text="🛑 To'xtatish")],
        ],
        resize_keyboard=True,
    )

bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher(storage=MemoryStorage())

# ── /start ────────────────────────────────────────────────────────────────────
@dp.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.clear()
    name = msg.from_user.first_name or "Do'st"
    await msg.answer(
        f"👋 *Salom, {name}! Xush kelibsiz!* 🎉\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🎮 *ANAGRAM O'YINI*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📌 *Qoidalar:*\n"
        "• Aralashtirilgan harflardan so'z toping\n"
        f"• Har savol uchun ⏱ *{ANSWER_TIME} soniya*\n"
        "• To'g'ri javob = *+1 ball* 🏆\n"
        "• Ketma-ket to'g'ri = *🔥 combo!*\n"
        "• 💡 Maslahat = birinchi harf ko'rinadi\n\n"
        "🌍 *Qaysi tilda o'ynamoqchisiz?*",
        reply_markup=main_kb(), parse_mode="Markdown"
    )
    await state.set_state(GS.choose)

@dp.message(Command("menu"))
async def menu(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer("🏠 Til tanlang:", reply_markup=main_kb(), parse_mode="Markdown")
    await state.set_state(GS.choose)

@dp.message(Command("score"))
async def score_cmd(msg: Message):
    s = get_score(msg.from_user.id)
    await msg.answer(
        f"📊 *Natijangiz*\n━━━━━━━━━━━━━━━\n"
        f"🇬🇧 English:  *{s['en']}* ball\n"
        f"🇷🇺 Русский:  *{s['ru']}* ball\n"
        f"🏆 Jami:      *{s['total']}* ball\n"
        f"🔥 Eng yaxshi: *{s['best']}* ketma-ket",
        parse_mode="Markdown"
    )

@dp.message(Command("help"))
async def help_cmd(msg: Message):
    await msg.answer(
        "❓ *Yordam*\n━━━━━━━━━━━━━━━\n"
        "/start — Boshlash\n/menu — Til tanlash\n"
        "/score — Natija\n/help — Yordam\n\n"
        "💡 Maslahat — birinchi harf\n"
        "⏭ O'tkazish — keyingi so'z\n"
        "🛑 To'xtatish — o'yinni tugatish",
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "score")
async def cb_score(call: CallbackQuery):
    s = get_score(call.from_user.id)
    await call.message.answer(
        f"📊 *Natijangiz*\n━━━━━━━━━━━━━━━\n"
        f"🇬🇧 English:  *{s['en']}* ball\n"
        f"🇷🇺 Русский:  *{s['ru']}* ball\n"
        f"🏆 Jami:      *{s['total']}* ball\n"
        f"🔥 Eng yaxshi: *{s['best']}* ketma-ket",
        parse_mode="Markdown"
    ); await call.answer()

@dp.callback_query(F.data == "help")
async def cb_help(call: CallbackQuery):
    await call.message.answer(
        "❓ *Yordam*\n━━━━━━━━━━━━━━━\n"
        "/start — Boshlash\n/menu — Til tanlash\n"
        "/score — Natija\n\n"
        "💡 Maslahat — birinchi harf\n"
        "⏭ O'tkazish — keyingi so'z\n"
        "🛑 To'xtatish — o'yinni tugatish",
        parse_mode="Markdown"
    ); await call.answer()

@dp.callback_query(F.data.in_({"L_en", "L_ru"}))
async def cb_lang(call: CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[1]
    await call.answer()
    if lang == "en":
        await state.set_state(GS.en)
        await call.message.answer(
            "🇬🇧 *English mode!* O'yin boshlanmoqda... 🚀",
            reply_markup=game_kb(), parse_mode="Markdown"
        )
    else:
        await state.set_state(GS.ru)
        await call.message.answer(
            "🇷🇺 *Русский режим!* Игра начинается... 🚀",
            reply_markup=game_kb(), parse_mode="Markdown"
        )
    await asyncio.sleep(0.6)
    await send_q(call.message, state, lang)

# ── Savol yuborish ────────────────────────────────────────────────────────────
async def send_q(msg: Message, state: FSMContext, lang: str):
    wd    = EN_WORDS if lang == "en" else RU_WORDS
    word  = random.choice(list(wd.keys()))
    scr   = scramble(word)
    data  = await state.get_data()
    qn    = data.get("qn", 0) + 1

    await state.update_data(word=word, lang=lang, answered=False, hint_used=False, qn=qn)

    flag = "🇬🇧 English" if lang == "en" else "🇷🇺 Русский"
    lbl  = "Anagram" if lang == "en" else "Анаграмма"
    sub  = "So'zni yozing 👇" if lang == "en" else "Напишите слово 👇"

    text = (
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔢 #{qn}  |  {flag}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🔀 *{lbl}:*\n"
        f"┌──────────────────┐\n"
        f"│  `{scr.upper():^16}` │\n"
        f"└──────────────────┘\n\n"
        f"⏱ *{ANSWER_TIME} soniya*  {tbar(ANSWER_TIME)}\n\n"
        f"{sub}"
    )
    sent = await msg.answer(text, parse_mode="Markdown")
    await state.update_data(mid=sent.message_id)
    asyncio.create_task(timer_task(msg.chat.id, state, word, lang, sent.message_id, scr, qn))

# ── Timer ─────────────────────────────────────────────────────────────────────
async def timer_task(chat_id: int, state: FSMContext, word: str, lang: str,
                     mid: int, scr: str, qn: int):
    flag = "🇬🇧 English" if lang == "en" else "🇷🇺 Русский"
    lbl  = "Anagram" if lang == "en" else "Анаграмма"
    sub  = "So'zni yozing 👇" if lang == "en" else "Напишите слово 👇"

    for left in range(ANSWER_TIME - 1, 0, -1):
        await asyncio.sleep(1)
        d = await state.get_data()
        if d.get("answered") or d.get("word") != word:
            return
        if left not in (7, 5, 3, 1):
            continue
        extra = ""
        if left <= 5 and not d.get("hint_used"):
            extra = f"\n\n💡 *Maslahat:* `{hint(word)}`"
        try:
            await bot.edit_message_text(
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔢 #{qn}  |  {flag}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🔀 *{lbl}:*\n"
                f"┌──────────────────┐\n"
                f"│  `{scr.upper():^16}` │\n"
                f"└──────────────────┘\n\n"
                f"⏱ *{left} soniya*  {tbar(left)}\n\n"
                f"{sub}{extra}",
                chat_id=chat_id, message_id=mid, parse_mode="Markdown"
            )
        except Exception:
            pass

    await asyncio.sleep(1)
    d = await state.get_data()
    if d.get("answered") or d.get("word") != word:
        return
    await state.update_data(answered=True)

    wd = EN_WORDS if lang == "en" else RU_WORDS
    if lang == "en":
        tout = f"⏰ *Vaqt tugadi!*\n\n✅ Javob: *{word.upper()}*\n📖 {wd[word]}\n\n➡️ Keyingi so'z..."
    else:
        tout = f"⏰ *Время вышло!*\n\n✅ Ответ: *{word.upper()}*\n📖 {wd[word]}\n\n➡️ Следующее слово..."

    try:
        await bot.send_message(chat_id, tout, parse_mode="Markdown")
        await asyncio.sleep(2)
        cur = await state.get_state()
        if cur in (GS.en.state, GS.ru.state):
            class _M:
                def __init__(self, c): self.chat = type("C", (), {"id": c})()
                async def answer(self, *a, **kw): return await bot.send_message(chat_id, *a, **kw)
            await send_q(_M(chat_id), state, lang)
    except Exception as e:
        log.error(e)

# ── Javob handler ─────────────────────────────────────────────────────────────
async def process(msg: Message, state: FSMContext, lang: str):
    txt = msg.text.strip() if msg.text else ""

    if txt == "🛑 To'xtatish":
        uid = msg.from_user.id
        s   = get_score(uid)
        await state.clear()
        medal = "🥇" if s["total"] >= 20 else "🥈" if s["total"] >= 10 else "🥉" if s["total"] >= 5 else "🎮"
        await msg.answer(
            f"🛑 *O'yin tugadi!*\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{medal} *Yakuniy natija*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🇬🇧 English:  *{s['en']}* ball\n"
            f"🇷🇺 Русский:  *{s['ru']}* ball\n"
            f"🏆 Jami:      *{s['total']}* ball\n"
            f"🔥 Eng yaxshi: *{s['best']}* ketma-ket\n\n"
            "Qayta o'ynash: /start 🎮",
            reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown"
        )
        return

    if txt == "💡 Maslahat":
        d = await state.get_data()
        w = d.get("word", "")
        if d.get("hint_used"):
            await msg.answer("💡 Maslahat allaqachon berilgan!")
        else:
            await state.update_data(hint_used=True)
            await msg.answer(f"💡 *Maslahat:* `{hint(w)}`\n_(birinchi harf: *{w[0].upper()}*)_",
                             parse_mode="Markdown")
        return

    if txt == "⏭ O'tkazish":
        d  = await state.get_data()
        w  = d.get("word", "")
        wd = EN_WORDS if lang == "en" else RU_WORDS
        await state.update_data(answered=True)
        await msg.answer(f"⏭ O'tkazildi!\n✅ Javob: *{w.upper()}*\n📖 {wd.get(w,'')}",
                         parse_mode="Markdown")
        await asyncio.sleep(1.2)
        await send_q(msg, state, lang)
        return

    d        = await state.get_data()
    word     = d.get("word", "")
    answered = d.get("answered", False)
    if answered:
        await msg.answer("⏳ Keyingi savol kelmoqda..."); return

    if txt.lower() == word:
        await state.update_data(answered=True)
        uid = msg.from_user.id
        s   = get_score(uid)
        s[lang]   += 1
        s["total"] += 1
        s["streak"] += 1
        if s["streak"] > s["best"]:
            s["best"] = s["streak"]

        wd     = EN_WORDS if lang == "en" else RU_WORDS
        flag   = "🇬🇧" if lang == "en" else "🇷🇺"
        combo  = f"\n🔥 *{s['streak']} ketma-ket! COMBO!*" if s["streak"] >= 3 else ""

        await msg.answer(
            f"✅ *To'g'ri!* +1 ball 🎉\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"💬 So'z: *{word.upper()}*\n"
            f"📖 {wd[word]}\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"{flag} Ball: *{s[lang]}*  |  🏆 Jami: *{s['total']}*{combo}",
            parse_mode="Markdown"
        )
        await asyncio.sleep(1.2)
        await send_q(msg, state, lang)
    else:
        s = get_score(msg.from_user.id)
        s["streak"] = 0
        if lang == "en":
            await msg.answer("❌ *Noto'g'ri!* Qayta urinib ko'ring ⏱", parse_mode="Markdown")
        else:
            await msg.answer("❌ *Неверно!* Попробуйте ещё раз ⏱", parse_mode="Markdown")

@dp.message(GS.en)
async def h_en(msg: Message, state: FSMContext): await process(msg, state, "en")

@dp.message(GS.ru)
async def h_ru(msg: Message, state: FSMContext): await process(msg, state, "ru")

# ── Main ──────────────────────────────────────────────────────────────────────
async def main():
    log.info("🤖 Bot ishga tushmoqda...")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
