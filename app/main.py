import os

from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from .config import BOT_TOKEN
from .tools import TOOLS


app = FastAPI(title="Cracker World")

telegram_app = None


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "👋 Welcome to Cracker World!\n\n"
        "Your bot is online! 🚀\n\n"
        "Use /tools to see available tools."
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🛠 Help\n\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/tools - Show all tools\n\n"
        "Example:\n"
        "/calc 25*4"
    )


async def tools_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    message = "🛠 CRACKER WORLD TOOLS\n\n"

    for index, (tool_id, tool_data) in enumerate(
        TOOLS.items(),
        start=1
    ):
        tool_name = tool_data[0]

        message += (
            f"{index}. {tool_name}\n"
            f"   /{tool_id}\n\n"
        )

    message += (
        "💡 Example:\n"
        "/calc 25*4+10\n\n"
        "More tools will be added soon! 🚀"
    )

    await update.message.reply_text(message)


async def tool_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    command = update.message.text.split()[0]
    tool_id = command.lstrip("/")

    if tool_id not in TOOLS:
        await update.message.reply_text(
            "❌ Unknown tool.\n"
            "Use /tools to see available tools."
        )
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            f"🛠 {TOOLS[tool_id][0]}\n\n"
            f"Use:\n/{tool_id} <your text>"
        )
        return

    function = TOOLS[tool_id][1]

    try:
        result = function(text)

        await update.message.reply_text(
            str(result)
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Tool error: {error}"
        )


def create_bot():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not configured."
        )

    bot = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    bot.add_handler(
        CommandHandler("start", start_command)
    )

    bot.add_handler(
        CommandHandler("help", help_command)
    )

    bot.add_handler(
        CommandHandler("tools", tools_command)
    )

    for tool_id in TOOLS:
        bot.add_handler(
            CommandHandler(
                tool_id,
                tool_command
            )
        )

    return bot


@app.on_event("startup")
async def startup():
    global telegram_app

    telegram_app = create_bot()

    await telegram_app.initialize()
    await telegram_app.start()
    await telegram_app.updater.start_polling()


@app.on_event("shutdown")
async def shutdown():
    global telegram_app

    if telegram_app:
        await telegram_app.updater.stop()
        await telegram_app.stop()
        await telegram_app.shutdown()


@app.get("/")
async def home():
    return {
        "status": "online",
        "bot": "Cracker World"
    }


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }


if __name__ == "__main__":
    import uvicorn

    port = int(
        os.getenv("PORT", "10000")
    )

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port
    )
