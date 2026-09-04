import os
import asyncio

from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from .config import BOT_TOKEN


app = FastAPI(title="Cracker World")


async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "👋 Welcome to Cracker World!\n\n"
        "Your bot is online successfully! 🚀"
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text(
        "🛠 Help\n\n"
        "/start - Start the bot\n"
        "/help - Show help"
    )


def create_bot():
    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not configured."
        )

    bot = Application.builder().token(BOT_TOKEN).build()

    bot.add_handler(
        CommandHandler("start", start_command)
    )

    bot.add_handler(
        CommandHandler("help", help_command)
    )

    return bot


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


async def run_bot():
    bot = create_bot()

    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await bot.updater.stop()
        await bot.stop()
        await bot.shutdown()


async def main():
    await run_bot()


if __name__ == "__main__":
    import uvicorn

    port = int(
        os.getenv("PORT", "8000")
    )

    asyncio.create_task(run_bot())

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port
    )
