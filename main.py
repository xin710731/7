import logging
import os
import random
import time

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ========= Konfigurasi Dasar =========
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ========= Area Menu =========
def main_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("😊 Alat Suasana Hati", callback_data="menu_mood")],
        [
            InlineKeyboardButton("🎮 Mini Game", callback_data="menu_games"),
            InlineKeyboardButton("🧠 Latihan Otak", callback_data="menu_brain"),
        ],
        [
            InlineKeyboardButton("🧺 Asisten Harian", callback_data="menu_daily"),
            InlineKeyboardButton("📌 Kartu Harian", callback_data="menu_cards"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def mood_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("💬 Kalimat Suasana Hati", callback_data="mood_sentence"),
            InlineKeyboardButton("🎨 Warna Suasana Hati", callback_data="mood_color"),
        ],
        [
            InlineKeyboardButton("🧘 Latihan Relaksasi", callback_data="mood_relax"),
            InlineKeyboardButton("📖 Kata Penghibur", callback_data="mood_quote"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu Utama", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def games_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("✊ Batu Gunting Kertas", callback_data="game_rps"),
            InlineKeyboardButton("🎲 Lempar Dadu", callback_data="game_dice"),
        ],
        [
            InlineKeyboardButton("🔢 Tebak Angka", callback_data="game_guess"),
            InlineKeyboardButton("😊 Kombinasi Emoji", callback_data="game_emoji"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Game", callback_data="menu_games")],
    ]
    return InlineKeyboardMarkup(keyboard)


def brain_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🧠 Tantangan Otak Hari Ini", callback_data="brain_task")],
        [
            InlineKeyboardButton("🔢 Ingat Angka", callback_data="brain_memory"),
            InlineKeyboardButton("🧩 Teka-teki", callback_data="brain_puzzle"),
        ],
        [
            InlineKeyboardButton("🎯 Tes Reaksi", callback_data="brain_reaction"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu Utama", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


def daily_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📋 Tugas Kecil Hari Ini", callback_data="daily_todo"),
            InlineKeyboardButton("🍵 Pengingat Istirahat", callback_data="daily_break"),
        ],
        [
            InlineKeyboardButton("🧹 Rapikan Sedikit", callback_data="daily_clean"),
            InlineKeyboardButton("📨 Hubungi Seseorang", callback_data="daily_contact"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu Utama", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(daily_menu)


def cards_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📌 Kartu Tips Hari Ini", callback_data="card_tip"),
            InlineKeyboardButton("💡 Kartu Inspirasi", callback_data="card_idea"),
        ],
        [
            InlineKeyboardButton("❤️ Kartu Perawatan Diri", callback_data="card_self"),
            InlineKeyboardButton("⭐ Kartu Tujuan Kecil", callback_data="card_goal"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu Utama", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(keyboard)


# ========= Perintah: /start /help /about =========
START_TEXT = (
    "👋 Selamat datang di «Santai Sehari-hari FunBox»!\n\n"
    "Ini adalah bot berbahasa Indonesia yang fokus pada *hiburan ringan · alat kecil · relaksasi*, kamu bisa:\n\n"
    "😊 *Alat Suasana Hati*\n"
    "• Kalimat suasana hati acak\n"
    "• Warna suasana hati\n"
    "• Latihan relaksasi & kata penghibur\n\n"
    "🎮 *Mini Game*\n"
    "• Batu gunting kertas\n"
    "• Lempar dadu\n"
    "• Tebak angka\n"
    "• Inspirasi kombinasi emoji\n\n"
    "🧠 *Latihan Otak*\n"
    "• Tantangan otak sederhana\n"
    "• Latihan ingatan angka\n"
    "• Teka-teki berpikir\n"
    "• Tes kecepatan reaksi\n\n"
    "🧺 *Asisten Harian*\n"
    "• Saran tugas kecil hari ini\n"
    "• Pengingat istirahat\n"
    "• Tugas rapih-rapih ringan\n"
    "• Pengingat untuk menghubungi orang lain\n\n"
    "📌 *Kartu Harian*\n"
    "• Kartu tips hari ini\n"
    "• Kartu inspirasi\n"
    "• Kartu perawatan diri\n"
    "• Kartu tujuan kecil\n\n"
    "Bot ini hanya menyediakan hiburan ringan dan pengingat harian, tidak mengandung uang, hadiah, judi, investasi, atau konten sensitif apa pun.\n\n"
    "👇 Klik menu di bawah untuk mulai!"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            START_TEXT, reply_markup=main_menu(), parse_mode="Markdown"
        )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📝 Panduan Penggunaan\n\n"
        "• Kirim /start untuk membuka menu utama\n"
        "• Gunakan tombol bawah untuk masuk ke berbagai fitur\n"
        "• Semua fitur bersifat ringan, tanpa hadiah nyata atau konten sensitif\n"
        "• Jika bot tidak merespons, kirim /start untuk kembali ke menu utama\n"
    )
    await update.message.reply_text(text)


async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ Tentang Bot Ini\n\n"
        "«Santai Sehari-hari FunBox» adalah kumpulan alat kecil untuk membantu kamu bersantai di waktu luang:\n"
        "• Mini game dan latihan otak ringan\n"
        "• Alat suasana hati dan kartu harian untuk merawat diri\n"
        "• Sepenuhnya gratis, tanpa elemen uang atau hadiah\n"
        "Cocok digunakan di chat pribadi maupun grup."
    )
    await update.message.reply_text(text)

# （以下逻辑代码保持不变，仅文本已翻译）
