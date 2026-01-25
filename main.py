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

# ========= Menu =========
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
            InlineKeyboardButton("💬 Satu Kalimat Suasana Hati", callback_data="mood_sentence"),
            InlineKeyboardButton("🎨 Warna Suasana Hati", callback_data="mood_color"),
        ],
        [
            InlineKeyboardButton("🧘 Latihan Santai", callback_data="mood_relax"),
            InlineKeyboardButton("📖 Kutipan Penghibur", callback_data="mood_quote"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu Utama", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def games_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("✊ Batu-Gunting-Kertas", callback_data="game_rps"),
            InlineKeyboardButton("🎲 Lempar Dadu", callback_data="game_dice"),
        ],
        [
            InlineKeyboardButton("🔢 Tebak Angka", callback_data="game_guess"),
            InlineKeyboardButton("😊 Kombinasi Emoji", callback_data="game_emoji"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Mini Game", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def brain_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🧠 Tugas Otak Hari Ini", callback_data="brain_task")],
        [
            InlineKeyboardButton("🔢 Ingat Angka", callback_data="brain_memory"),
            InlineKeyboardButton("🧩 Teka-teki Kecil", callback_data="brain_puzzle"),
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
            InlineKeyboardButton("📋 Tugas Harian", callback_data="daily_todo"),
            InlineKeyboardButton("🍵 Pengingat Istirahat", callback_data="daily_break"),
        ],
        [
            InlineKeyboardButton("🧹 Rapikan Sedikit", callback_data="daily_clean"),
            InlineKeyboardButton("📨 Pengingat Kontak", callback_data="daily_contact"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu Utama", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

def cards_menu() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton("📌 Kartu Tips Hari Ini", callback_data="card_tip"),
            InlineKeyboardButton("💡 Kartu Inspirasi", callback_data="card_idea"),
        ],
        [
            InlineKeyboardButton("❤️ Kartu Perhatian Diri", callback_data="card_self"),
            InlineKeyboardButton("⭐ Kartu Tujuan Kecil", callback_data="card_goal"),
        ],
        [InlineKeyboardButton("⬅ Kembali ke Menu Utama", callback_data="menu_main")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ========= Perintah /start /help /about =========
START_TEXT = (
    "👋 Selamat datang di 'FunBox Santai Sehari-hari'!\n\n"
    "Ini adalah bot berbahasa Indonesia yang fokus pada *hiburan ringan·alat kecil·relaksasi suasana hati*. Kamu bisa:\n\n"
    "😊 *Alat Suasana Hati*\n"
    "• Satu kalimat acak suasana hati\n"
    "• Warna suasana hati\n"
    "• Latihan santai & kutipan penghibur\n\n"
    "🎮 *Mini Game*\n"
    "• Batu-Gunting-Kertas\n"
    "• Lempar Dadu\n"
    "• Tebak Angka\n"
    "• Kombinasi Emoji\n\n"
    "🧠 *Latihan Otak*\n"
    "• Tugas otak harian\n"
    "• Latihan memori angka\n"
    "• Teka-teki kecil\n"
    "• Tes kecepatan reaksi\n\n"
    "🧺 *Asisten Harian*\n"
    "• Saran tugas hari ini\n"
    "• Pengingat istirahat\n"
    "• Rapikan sedikit\n"
    "• Pengingat kontak\n\n"
    "📌 *Kartu Harian*\n"
    "• Kartu tips\n"
    "• Kartu inspirasi\n"
    "• Kartu perhatian diri\n"
    "• Kartu tujuan kecil\n\n"
    "Bot ini hanya untuk hiburan ringan dan pengingat sehari-hari, aman untuk semua pengguna.\n\n"
    "👇 Klik menu di bawah untuk memulai!"
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
        "• Gunakan tombol di bawah untuk masuk ke: Alat Suasana Hati, Mini Game, Latihan Otak, Asisten Harian, Kartu Harian\n"
        "• Setiap fitur berupa interaksi ringan atau teks, tanpa konten sensitif atau hadiah nyata\n"
        "• Jika tidak merespon, kirim /start lagi untuk kembali ke menu utama\n"
    )
    await update.message.reply_text(text)

async def about_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ Tentang Bot Ini\n\n"
        "'FunBox Santai Sehari-hari' membantu kamu bersantai di waktu luang:\n"
        "• Main mini game atau latihan otak untuk rileks\n"
        "• Gunakan alat suasana hati dan kartu harian untuk perhatian diri\n"
        "• Gratis sepenuhnya, tanpa uang, hadiah, atau konten sensitif\n"
        "Nikmati bot ini di chat pribadi atau grup."
    )
    await update.message.reply_text(text)

# ========= Handler Tombol =========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    # Menu Utama
    if data == "menu_main":
        await query.edit_message_text("🏠 Kembali ke Menu Utama:", reply_markup=main_menu())
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

    await query.edit_message_text("Operasi tidak didukung, kirim /start untuk kembali ke menu utama.")

# ========= Alat Suasana Hati =========
async def mood_sentence(query):
    sentences = [
        "Hari ini bersikap lembut pada diri sendiri sedikit saja.",
        "Tidak harus hebat, yang penting tetap maju.",
        "Izinkan diri sesekali lambat, itu juga keberanian.",
        "Kamu sudah lebih baik dari yang kamu kira.",
    ]
    await query.edit_message_text(
        "💬 Satu Kalimat Suasana Hati:\n\n" + random.choice(sentences),
        reply_markup=mood_menu(),
    )

async def mood_color(query):
    colors = [
        "🔵 Biru: Cocok untuk berpikir tenang, beri otak ruang.",
        "🟢 Hijau: Cocok untuk bersantai, seperti berjalan di taman.",
        "🟡 Kuning: Cocok untuk berbagi lelucon atau ngobrol dengan teman.",
        "🟣 Ungu: Cocok untuk sedikit berkreasi, misal menulis beberapa kata.",
        "🔴 Merah: Cocok menyelesaikan satu hal yang sudah lama ingin dilakukan.",
    ]
    await query.edit_message_text(
        "🎨 Warna Suasana Hati:\n\n" + random.choice(colors),
        reply_markup=mood_menu(),
    )

async def mood_relax(query):
    text = (
        "🧘 Latihan Santai:\n\n"
        "1️⃣ Duduk atau berdiri dengan nyaman\n"
        "2️⃣ Pejamkan mata (jika bisa)\n"
        "3️⃣ Lakukan 5 kali pernapasan dalam secara perlahan\n"
        "   Tarik napas hitung 4, hembuskan hitung 4\n\n"
        "Hanya butuh setengah menit untuk istirahat sejenak."
    )
    await query.edit_message_text(text, reply_markup=mood_menu())

async def mood_quote(query):
    quotes = [
        "Kadang berhenti sejenak dan tarik napas saja sudah hebat.",
        "Emosi datang dan pergi, tapi kamu tetap ada.",
        "Tidak perlu membuat hari ini sempurna, cukup 'lumayan' sudah cukup baik.",
    ]
    await query.edit_message_text(
        "📖 Kutipan Penghibur:\n\n" + random.choice(quotes),
        reply_markup=mood_menu(),
    )

# ========= Mini Game =========
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
        "✊ Batu-Gunting-Kertas: Pilih pilihanmu:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def game_rps_result(query, data: str):
    user = data.split("_")[-1]
    options = ["rock", "paper", "scissors"]
    bot = random.choice(options)
    emoji = {"rock": "✊ Batu", "paper": "✋ Kertas", "scissors": "✌ Gunting"}

    if user == bot:
        result = "Seri~ Kita cocok 😆"
    elif (
        (user == "rock" and bot == "scissors")
        or (user == "scissors" and bot == "paper")
        or (user == "paper" and bot == "rock")
    ):
        result = "Kamu menang! Mantap ✨"
    else:
        result = "Aku menang kali ini, coba lagi? 😉"

    text = (
        "🎮 Hasil Batu-Gunting-Kertas:\n\n"
        f"Kamu: {emoji[user]}\n"
        f"Aku: {emoji[bot]}\n\n"
        f"{result}"
    )
    await query.edit_message_text(text, reply_markup=games_menu())

async def game_dice(query):
    n = random.randint(1, 6)
    await query.edit_message_text(
        f"🎲 Kamu melempar: {n}!\n\nCoba beberapa kali, lihat 'untung-untungan' hari ini.",
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
        "🔢 Tebak Angka: Aku memilih angka antara 1~5, tebak angka berapa?",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def game_guess_result(query, context: ContextTypes.DEFAULT_TYPE, data: str):
    secret = context.user_data.get("guess_number")
    try:
        user = int(data.split("_")[-1])
    except ValueError:
        user = None

    if secret is None or user is None:
        text = "Data permainan sudah kadaluarsa, mulai ulang Tebak Angka."
    elif secret == user:
        text = f"🎉 Kamu benar! Aku memilih {secret}."
    else:
        text = f"😆 Sayang! Aku sebenarnya memilih {secret}."

    await query.edit_message_text(text, reply_markup=games_menu())

async def game_emoji(query):
    emojis = ["😀", "😆", "😎", "🥳", "🤩", "🤗", "🙌", "🌈", "⭐", "✨", "🔥", "🍀"]
    seq = " ".join(random.sample(emojis, 5))
    text = (
        "😊 Kombinasi Emoji:\n\n"
        f"{seq}\n\n"
        "Bisa dicopy dan dimainkan di grup atau sebagai 'kombinasi mood hari ini'."
    )
    await query.edit_message_text(text, reply_markup=games_menu())

# ========= Latihan Otak =========
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
        user_input = int(data.split("_")[-1])
    except ValueError:
        user_input = None

    if original == user_input:
        text = "🎉 Benar! Memori kamu luar biasa."
    else:
        text = f"😆 Ingatanmu berbeda, sebenarnya: {original}."
    await query.edit_message_text(text, reply_markup=brain_menu())

async def brain_puzzle(query):
    puzzles = [
        "🧩 Teka-teki: Aku selalu datang tapi tidak pernah tiba. Apa aku? (Jawaban: Besok)",
        "🧩 Teka-teki: Apa yang memiliki tangan tapi tidak bisa memeluk? (Jawaban: Jam)",
    ]
    await query.edit_message_text(random.choice(puzzles), reply_markup=brain_menu())

async def brain_reaction(query, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Klik Cepat!", callback_data="brain_reaction_click")],
        [InlineKeyboardButton("⬅ Kembali ke Latihan Otak", callback_data="menu_brain")],
    ]
    context.user_data["reaction_start"] = time.time()
    await query.edit_message_text("🎯 Klik tombol secepat mungkin!", reply_markup=InlineKeyboardMarkup(keyboard))

async def brain_reaction_click(query, context: ContextTypes.DEFAULT_TYPE):
    start = context.user_data.get("reaction_start", time.time())
    elapsed = time.time() - start
    text = f"⌛ Waktu reaksi kamu: {elapsed:.2f} detik."
    await query.edit_message_text(text, reply_markup=brain_menu())

# ========= Asisten Harian =========
async def daily_todo(query):
    todos = [
        "📋 Saran tugas hari ini:\n• Selesaikan satu hal kecil yang benar-benar penting\n• Balas satu pesan yang belum sempat dibalas\n• Luangkan 10 menit untuk bersantai",
        "📋 Saran tugas hari ini:\n• Rapikan satu folder atau laci kecil\n• Minum segelas air\n• Pikirkan satu hal untuk dilakukan besok dan catat",
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

# ========= Kartu Harian =========
async def card_tip(query):
    tips = [
        "📌 Kartu Tips Hari Ini:\nFokuslah pada 'apa yang bisa dilakukan', bukan 'apa yang tidak bisa'.",
        "📌 Kartu Tips Hari Ini:\nJika terlalu banyak hal, pilih satu yang paling kecil dan mudah diselesaikan sebagai awal.",
    ]
    await query.edit_message_text(random.choice(tips), reply_markup=cards_menu())

async def card_idea(query):
    ideas = [
        "💡 Kartu Inspirasi:\nTuliskan satu ide atau kalimat yang tiba-tiba muncul hari ini, tidak perlu lengkap, cukup nyata.",
        "💡 Kartu Inspirasi:\nBayangkan jika hari ini difoto, apa yang akan kamu ambil? Pikirkan secara singkat.",
    ]
    await query.edit_message_text(random.choice(ideas), reply_markup=cards_menu())

async def card_self(query):
    texts = [
        "❤️ Kartu Perhatian Diri:\nKamu tidak harus selalu kuat, kadang berkata 'sedikit lelah' juga tidak apa-apa.",
        "❤️ Kartu Perhatian Diri:\nCoba ucapkan pada diri sendiri 'terima kasih sudah bertahan sampai sekarang', meski hari ini belum sempurna.",
    ]
    await query.edit_message_text(random.choice(texts), reply_markup=cards_menu())

async def card_goal(query):
    texts = [
        "⭐ Kartu Tujuan Kecil:\nHari ini cukup selesaikan satu hal 'kecil dan spesifik', misal: rapikan satu halaman, tulis satu paragraf, berjalan 5 menit.",
        "⭐ Kartu Tujuan Kecil:\nPikirkan satu tujuan kecil yang bisa selesai dalam 10 menit, setelah selesai beri pujian kecil pada diri sendiri.",
    ]
    await query.edit_message_text(random.choice(texts), reply_markup=cards_menu())

# ========= Main =========
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("about", about_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot berjalan...")
    app.run_polling()
