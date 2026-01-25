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
# ========= Handler Tombol =========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # Pergantian Menu
    if data == "menu_main":
        await query.edit_message_text("🏠 Kembali ke menu utama:", reply_markup=main_menu())
        return
    if data == "menu_mood":
        await query.edit_message_text("😊 Alat Suasana Hati:", reply_markup=mood_menu())
        return
    if data == "menu_games":
        await query.edit_message_text("🎮 Mini Game:", reply_markup=games_menu())
        return
    if data == "menu_brain":
        await query.edit_message_text("🧠 Latihan Otak:", reply_markup=brain_menu())
        return
    if data == "menu_daily":
        await query.edit_message_text("🧺 Asisten Harian:", reply_markup=daily_menu())
        return
    if data == "menu_cards":
        await query.edit_message_text("📌 Kartu Harian:", reply_markup=cards_menu())
        return

    # Alat Suasana Hati
    if data == "mood_sentence":
        await mood_sentence(query)
        return
    if data == "mood_color":
        await mood_color(query)
        return
    if data == "mood_relax":
        await mood_relax(query)
        return
    if data == "mood_quote":
        await mood_quote(query)
        return

    # Mini Game
    if data == "game_rps":
        await game_rps(query)
        return
    if data.startswith("game_rps_"):
        await game_rps_result(query, data)
        return
    if data == "game_dice":
        await game_dice(query)
        return
    if data == "game_guess":
        await game_guess(query, context)
        return
    if data.startswith("game_guess_"):
        await game_guess_result(query, context, data)
        return
    if data == "game_emoji":
        await game_emoji(query)
        return

    # Latihan Otak
    if data == "brain_task":
        await brain_task(query)
        return
    if data == "brain_memory":
        await brain_memory_start(query, context)
        return
    if data.startswith("brain_memory_answer_"):
        await brain_memory_answer(query, context, data)
        return
    if data == "brain_puzzle":
        await brain_puzzle(query)
        return
    if data == "brain_reaction":
        await brain_reaction(query, context)
        return
    if data == "brain_reaction_click":
        await brain_reaction_click(query, context)
        return

    # Asisten Harian
    if data == "daily_todo":
        await daily_todo(query)
        return
    if data == "daily_break":
        await daily_break(query)
        return
    if data == "daily_clean":
        await daily_clean(query)
        return
    if data == "daily_contact":
        await daily_contact(query)
        return

    # Kartu Harian
    if data == "card_tip":
        await card_tip(query)
        return
    if data == "card_idea":
        await card_idea(query)
        return
    if data == "card_self":
        await card_self(query)
        return
    if data == "card_goal":
        await card_goal(query)
        return

    # Fallback
    await query.edit_message_text("Operasi tidak didukung, silakan kirim /start untuk kembali ke menu utama.")


# ========= Implementasi Alat Suasana Hati =========
async def mood_sentence(query):
    sentences = [
        "Hari ini, perlakukan dirimu dengan lembut sedikit demi sedikit.",
        "Tidak harus hebat, yang penting tetap maju sedikit demi sedikit.",
        "Izinkan diri sendiri sesekali melambat, itu juga keberanian.",
        "Kamu sudah melakukan lebih baik dari yang kamu kira.",
    ]
    await query.edit_message_text(
        "💬 Kalimat Suasana Hati:\n\n" + random.choice(sentences),
        reply_markup=mood_menu(),
    )


async def mood_color(query):
    colors = [
        "🔵 Biru: Cocok untuk berpikir tenang, beri otak sedikit ruang.",
        "🟢 Hijau: Cocok untuk relaksasi, seperti berjalan di taman.",
        "🟡 Kuning: Cocok untuk berbagi lelucon atau ngobrol dengan teman.",
        "🟣 Ungu: Cocok untuk membuat karya kecil, misalnya menulis beberapa kalimat.",
        "🔴 Merah: Cocok untuk menyelesaikan satu hal yang sudah lama ingin dilakukan.",
    ]
    await query.edit_message_text(
        "🎨 Warna Suasana Hati:\n\n" + random.choice(colors),
        reply_markup=mood_menu(),
    )


async def mood_relax(query):
    text = (
        "🧘 Latihan Relaksasi:\n\n"
        "1️⃣ Duduk atau berdiri dengan nyaman\n"
        "2️⃣ Tutup mata (jika memungkinkan)\n"
        "3️⃣ Lakukan 5 kali napas dalam perlahan\n"
        "   Tarik napas sampai 4, hembuskan sampai 4\n\n"
        "Hanya butuh setengah menit, beri diri sedikit istirahat."
    )
    await query.edit_message_text(text, reply_markup=mood_menu())


async def mood_quote(query):
    quotes = [
        "Terkadang, berhenti sejenak dan tarik napas saja sudah hebat.",
        "Emosi datang dan pergi, tapi kamu selalu ada.",
        "Tidak perlu membuat hari ini sempurna, cukup jalani 'lumayan' saja sudah bagus.",
    ]
    await query.edit_message_text(
        "📖 Kata Penghibur:\n\n" + random.choice(quotes),
        reply_markup=mood_menu(),
    )
# ========= Implementasi Mini Game =========
async def game_rps(query):
    keyboard = [
        [
            InlineKeyboardButton("✊ Batu", callback_data="game_rps_rock"),
            InlineKeyboardButton("✋ Kertas", callback_data="game_rps_paper"),
            InlineKeyboardButton("✌ Gunting", callback_data="game_rps_scissors"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Mini Game", callback_data="menu_games")],
    ]
    await query.edit_message_text(
        "✊ Batu, Gunting, Kertas: Pilih gerakanmu:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def game_rps_result(query, data: str):
    user = data.split("_")[-1]
    options = ["rock", "paper", "scissors"]
    bot = random.choice(options)
    emoji = {"rock": "✊ Batu", "paper": "✋ Kertas", "scissors": "✌ Gunting"}

    if user == bot:
        result = "Seri~ Kita cocok banget 😆"
    elif (
        (user == "rock" and bot == "scissors")
        or (user == "scissors" and bot == "paper")
        or (user == "paper" and bot == "rock")
    ):
        result = "Kamu menang! Hari ini feeling-mu bagus ✨"
    else:
        result = "Aku menang kali ini, ayo coba lagi 😉"

    text = (
        "🎮 Hasil Batu, Gunting, Kertas:\n\n"
        f"Kamu memilih: {emoji[user]}\n"
        f"Aku memilih: {emoji[bot]}\n\n"
        f"{result}"
    )
    await query.edit_message_text(text, reply_markup=games_menu())


async def game_dice(query):
    n = random.randint(1, 6)
    await query.edit_message_text(
        f"🎲 Kamu melempar dadu dan mendapat: {n}!\n\nCoba beberapa kali lagi untuk melihat 'nasib angka' hari ini.",
        reply_markup=games_menu(),
    )


async def game_guess(query, context: ContextTypes.DEFAULT_TYPE):
    secret = random.randint(1, 5)
    context.user_data["guess_number"] = secret

    keyboard = [
        [
            InlineKeyboardButton("1", callback_data="game_guess_1"),
            InlineKeyboardButton("2", callback_data="game_guess_2"),
            InlineKeyboardButton("3", callback_data="game_guess_3"),
            InlineKeyboardButton("4", callback_data="game_guess_4"),
            InlineKeyboardButton("5", callback_data="game_guess_5"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Mini Game", callback_data="menu_games")],
    ]
    await query.edit_message_text(
        "🔢 Tebak Angka: Aku memikirkan angka antara 1~5, coba tebak angka berapa?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def game_guess_result(query, context: ContextTypes.DEFAULT_TYPE, data: str):
    secret = context.user_data.get("guess_number")
    try:
        user = int(data.split("_")[-1])
    except ValueError:
        user = None

    if secret is None or user is None:
        text = "Data permainan sudah kadaluarsa, silakan mulai ulang tebakan angka~"
    elif secret == user:
        text = f"🎉 Kamu menebak benar! Angka yang aku pikirkan adalah {secret}."
    else:
        text = f"😆 Sayang sekali! Sebenarnya angkanya adalah {secret}."

    await query.edit_message_text(text, reply_markup=games_menu())


async def game_emoji(query):
    emojis = ["😀", "😆", "😎", "🥳", "🤩", "🤗", "🙌", "🌈", "⭐", "✨", "🔥", "🍀"]
    seq = " ".join(random.sample(emojis, 5))
    text = (
        "😊 Kombinasi Emoji Inspirasi:\n\n"
        f"{seq}\n\n"
        "Kamu bisa menyalin kombinasi ini, kirim ke grup untuk bermain tebak emoji atau sebagai 'kombinasi suasana hati hari ini'."
    )
    await query.edit_message_text(text, reply_markup=games_menu())
# ========= Implementasi Latihan Otak =========
async def brain_task(query):
    tasks = [
        "🧠 Tugas: Hitung mundur dari 30 sampai 1 dalam hati, usahakan tidak terputus.",
        "🧠 Tugas: Ingat tiga hal kecil yang membuatmu senang hari ini.",
        "🧠 Tugas: Coba ingat 5 benda yang kamu lihat di sekitarmu, ulangi dalam hati.",
    ]
    await query.edit_message_text(
        "🧠 Tugas Otak Hari Ini:\n\n" + random.choice(tasks),
        reply_markup=brain_menu(),
    )


async def brain_memory_start(query, context: ContextTypes.DEFAULT_TYPE):
    number = random.randint(100, 9999)
    context.user_data["brain_memory_number"] = number
    keyboard = [
        [
            InlineKeyboardButton(
                "Sudah diingat, mulai jawab", callback_data=f"brain_memory_answer_{number}"
            )
        ],
        [InlineKeyboardButton("⬅ Kembali ke Latihan Otak", callback_data="menu_brain")],
    ]
    await query.edit_message_text(
        f"🔢 Latihan Memori Angka:\n\nIngat angka ini:\n\n👉 {number}\n\nSiap? Klik tombol.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def brain_memory_answer(query, context: ContextTypes.DEFAULT_TYPE, data: str):
    original = context.user_data.get("brain_memory_number")
    try:
        answer = int(data.split("_")[-1])
    except ValueError:
        answer = None

    if original is None or answer is None:
        text = "Data latihan memori sudah kadaluarsa, silakan mulai ulang."
    elif original == answer:
        text = f"🎉 Bagus! Kamu berhasil mengingat angka: {original}"
    else:
        text = f"😆 Sedikit berbeda, angka yang benar adalah: {original}"

    await query.edit_message_text(text, reply_markup=brain_menu())


async def brain_puzzle(query):
    puzzles = [
        "🧩 Teka-teki:\nAda sebuah ruangan dengan satu lampu dan tiga saklar di luar. Kamu hanya boleh masuk sekali. Bagaimana cara mengetahui saklar mana yang mengendalikan lampu?",
        "🧩 Teka-teki:\nAda seutas tali yang terbakar dari satu ujung ke ujung lain dalam 1 jam, tapi laju pembakarannya tidak merata. Bagaimana mengukurnya selama 15 menit?",
    ]
    await query.edit_message_text(random.choice(puzzles), reply_markup=brain_menu())


async def brain_reaction(query, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["reaction_start"] = time.time()
    keyboard = [
        [InlineKeyboardButton("⚡ Klik aku sekarang!", callback_data="brain_reaction_click")],
        [InlineKeyboardButton("⬅ Kembali ke Latihan Otak", callback_data="menu_brain")],
    ]
    await query.edit_message_text(
        "🎯 Begitu kamu melihat tombol ini, segera klik untuk menguji kecepatan reaksi:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def brain_reaction_click(query, context: ContextTypes.DEFAULT_TYPE):
    start = context.user_data.get("reaction_start")
    if not start:
        text = "Data tes sudah kadaluarsa, silakan mulai ulang."
    else:
        ms = int((time.time() - start) * 1000)
        text = f"🎯 Waktu reaksi kamu: {ms} ms\n\nCoba beberapa kali untuk melihat kemajuanmu."
    await query.edit_message_text(text, reply_markup=brain_menu())
# ========= Implementasi Asisten Harian =========
async def daily_todo(query):
    todos = [
        "📋 Saran tugas hari ini:\n\n• Selesaikan satu hal kecil yang benar-benar penting\n• Balas satu pesan yang belum sempat dibalas\n• Luangkan 10 menit untuk bersantai",
        "📋 Saran tugas hari ini:\n\n• Rapikan satu folder atau laci kecil\n• Minum segelas air\n• Pikirkan satu hal untuk dilakukan besok dan catat",
    ]
    await query.edit_message_text(random.choice(todos), reply_markup=daily_menu())


async def daily_break(query):
    text = (
        "🍵 Pengingat Istirahat:\n\nJika kamu sudah menatap layar cukup lama, coba lakukan:\n"
        "• Berdiri dan berjalan sebentar\n"
        "• Lihat pemandangan jauh\n"
        "• Gerakkan bahu dan leher\n\n"
        "Istirahat singkat membantu fokus kembali."
    )
    await query.edit_message_text(text, reply_markup=daily_menu())


async def daily_clean(query):
    tasks = [
        "🧹 Coba rapikan meja atau area kecil sekitar selama 3 menit.",
        "🧹 Susun sedikit kertas/pena/barang kecil di meja, beri rasa 'bersih' sejenak.",
    ]
    await query.edit_message_text(
        "🧹 Rapikan sedikit:\n\n" + random.choice(tasks),
        reply_markup=daily_menu(),
    )


async def daily_contact(query):
    text = (
        "📨 Pengingat Kontak:\n\nPertimbangkan untuk menghubungi salah satu:\n"
        "• Teman yang sudah lama tidak dihubungi\n"
        "• Orang yang baru saja membantumu\n"
        "• Keluarga atau orang penting\n\n"
        "Sebuah sapaan sederhana adalah cara menghubungkan dengan lembut."
    )
    await query.edit_message_text(text, reply_markup=daily_menu())


# ========= Implementasi Kartu Harian =========
async def card_tip(query):
    tips = [
        "📌 Kartu Tips Hari Ini:\n\nFokuslah pada 'apa yang bisa dilakukan', bukan 'apa yang tidak bisa'.",
        "📌 Kartu Tips Hari Ini:\n\nJika terlalu banyak hal, pilih satu yang paling kecil dan mudah diselesaikan sebagai awal.",
    ]
    await query.edit_message_text(random.choice(tips), reply_markup=cards_menu())


async def card_idea(query):
    ideas = [
        "💡 Kartu Inspirasi:\n\nTuliskan satu ide atau kalimat yang tiba-tiba muncul hari ini, tidak perlu lengkap, cukup nyata.",
        "💡 Kartu Inspirasi:\n\nBayangkan jika hari ini difoto, apa yang akan kamu ambil? Pikirkan secara singkat.",
    ]
    await query.edit_message_text(random.choice(ideas), reply_markup=cards_menu())


async def card_self(query):
    texts = [
        "❤️ Kartu Perhatian Diri:\n\nKamu tidak harus selalu kuat, kadang berkata 'sedikit lelah' juga tidak apa-apa.",
        "❤️ Kartu Perhatian Diri:\n\nCoba ucapkan pada diri sendiri 'terima kasih sudah bertahan sampai sekarang', meski hari ini belum sempurna.",
    ]
    await query.edit_message_text(random.choice(texts), reply_markup=cards_menu())


async def card_goal(query):
    texts = [
        "⭐ Kartu Tujuan Kecil:\n\nHari ini cukup selesaikan satu hal 'kecil dan spesifik', misal: rapikan satu halaman, tulis satu paragraf, berjalan 5 menit.",
        "⭐ Kartu Tujuan Kecil:\n\nPikirkan satu tujuan kecil yang bisa selesai dalam 10 menit, setelah selesai beri pujian kecil pada diri sendiri.",
    ]
    await query.edit_message_text(random.choice(texts), reply_markup=cards_menu())
