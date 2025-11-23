import logging
import os
import random

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

# ========= 配置 =========
BOT_TOKEN = os.getenv("BOT_TOKEN")        # Railway 环境变量
EXTERNAL_URL = "https://t.me/gamee"         # 外部小游戏资源

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# ========= 主菜单 =========
def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("⚔ 今日冒险任务", callback_data="quest_task"),
        ],
        [
            InlineKeyboardButton("✨ 随机装备生成", callback_data="item_generate"),
            InlineKeyboardButton("🧱 随机关卡挑战", callback_data="level_challenge"),
        ],
        [
            InlineKeyboardButton("🎲 掷骰子", callback_data="dice"),
        ],
        [
            InlineKeyboardButton("🔗 冒险小游戏资源（Poki）", url=EXTERNAL_URL),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# ========= 指令 =========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "⚔ 欢迎来到 FunQuest 冒险任务工具 Bot！\n\n"
        "这里你可以体验轻量冒险玩法：\n"
        "• ⚔ 今日冒险任务\n"
        "• ✨ 随机装备生成（文字版）\n"
        "• 🧱 随机关卡挑战\n"
        "• 🎲 冒险骰子\n"
        "• 🔗 外部冒险小游戏资源（Poki）\n\n"
        "本机器人完全安全、无任何敏感内容。开始冒险吧！"
    )
    await update.message.reply_text(text, reply_markup=main_menu())


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📝 使用帮助\n\n"
        "/start 打开主菜单\n\n"
        "机器人提供轻量冒险任务与工具功能，无任何敏感内容，可投放广告。"
    )
    await update.message.reply_text(text)


# ========= 回调处理 =========
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action = query.data

    if action == "quest_task":
        await handle_quest_task(query)
    elif action == "item_generate":
        await handle_item_generate(query)
    elif action == "level_challenge":
        await handle_level_challenge(query)
    elif action == "dice":
        await handle_dice(query)
    else:
        await query.edit_message_text(
            "未知指令，请使用 /start 回到主菜单。",
            reply_markup=main_menu()
        )


# ========= 功能 1：今日冒险任务 =========
async def handle_quest_task(query):
    tasks = [
        "⚔ 执行“森林巡逻”任务：在现实中完成 10 次深呼吸，保持冷静。",
        "🛡 保卫村庄：整理桌面 2 分钟，模拟建立防线！",
        "🔍 探索废墟：找出身边一个“旧物品”观察 10 秒。",
        "📜 接受神秘试炼：记录今天你想完成的一个小目标。",
        "🐾 野外探索：走动 30 秒，活动身体。",
    ]

    await query.edit_message_text(
        "⚔ 今日冒险任务：\n\n" + random.choice(tasks),
        reply_markup=main_menu()
    )


# ========= 功能 2：随机装备生成（文字 RPG 风格） =========
async def handle_item_generate(query):
    prefixes = ["远古的", "闪光的", "失落的", "神秘的", "轻便的", "强化的"]
    types = ["长剑", "魔杖", "皮甲", "护符", "短弓", "铁盾", "水晶戒"]
    suffixes = ["力量", "智慧", "敏捷", "守护", "幸运", "能量"]

    item = f"{random.choice(prefixes)}{random.choice(types)}（+{random.choice(suffixes)}）"

    await query.edit_message_text(
        f"✨ 随机装备：\n\n👉 {item}\n\n快去挑战关卡吧！",
        reply_markup=main_menu()
    )


# ========= 功能 3：随机关卡挑战 =========
async def handle_level_challenge(query):
    challenges = [
        "🧱 关卡：迷雾森林\n任务：在 20 秒内找到一个绿色物品。",
        "🕳 关卡：遗迹深处\n任务：模仿怪物吼叫 3 秒（在心里也可以 😆）。",
        "🔥 关卡：火山边缘\n任务：伸展身体 3 次，充满能量！",
        "❄ 关卡：冰晶洞窟\n任务：保持安静 10 秒。",
        "🌪 关卡：风暴高塔\n任务：随便做一个“胜利动作”！",
    ]

    await query.edit_message_text(
        "🧱 当前关卡挑战：\n\n" + random.choice(challenges),
        reply_markup=main_menu()
    )


# ========= 功能 4：冒险骰子 =========
async def handle_dice(query):
    point = random.randint(1, 6)
    await query.edit_message_text(
        f"🎲 冒险骰子掷出：{point} 点！\n\n再次掷骰子开启新事件吧！",
        reply_markup=main_menu()
    )


# ========= 主入口 =========
def main():
    if not BOT_TOKEN:
        raise RuntimeError("❌ BOT_TOKEN 环境变量未设置！")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(callback_handler))

    app.run_polling()


if __name__ == "__main__":
    main()
