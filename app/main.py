```python
import os

from fastapi import FastAPI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from .config import BOT_TOKEN
from .tools import TOOLS as OLD_TOOLS
from .free_tools import FREE_TOOLS
from .keyboards import tools_keyboard, category_keyboard


# =========================================================
# TOOL REGISTRY
# =========================================================

# Keep all existing tools
# and add the new free/offline tools.
TOOLS = {
    **OLD_TOOLS,
    **FREE_TOOLS,
}


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(title="Cracker World")

telegram_app = None


# =========================================================
# START
# =========================================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    await update.message.reply_text(
        "👋 Welcome to Cracker World!\n\n"
        "🚀 Your bot is online!\n\n"
        "🆓 Free offline tools are available.\n\n"
        "🛠 Use /tools to open the tools menu."
    )


# =========================================================
# HELP
# =========================================================

async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    await update.message.reply_text(
        "🛠 Cracker World Help\n\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/tools - Open tools menu\n\n"
        f"🧰 Available tools: {len(TOOLS)}"
    )


# =========================================================
# TOOLS MENU
# =========================================================

async def tools_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    await update.message.reply_text(
        "🛠 CRACKER WORLD TOOLS\n\n"
        f"🧰 Total tools: {len(TOOLS)}\n\n"
        "👇 Select a category:",
        reply_markup=tools_keyboard(),
    )


# =========================================================
# CATEGORY BUTTON
# =========================================================

async def category_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    data = query.data or ""

    if not data.startswith("category:"):
        return

    category_name = data.split(":", 1)[1]

    await query.edit_message_text(
        f"📂 {category_name}\n\n"
        "👇 Select a tool:",
        reply_markup=category_keyboard(category_name),
    )


# =========================================================
# BACK TO TOOLS
# =========================================================

async def back_to_tools(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    await query.edit_message_text(
        "🛠 CRACKER WORLD TOOLS\n\n"
        f"🧰 Total tools: {len(TOOLS)}\n\n"
        "👇 Select a category:",
        reply_markup=tools_keyboard(),
    )


# =========================================================
# TOOL BUTTON
# =========================================================

async def tool_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    if not query:
        return

    await query.answer()

    data = query.data or ""

    if not data.startswith("tool:"):
        return

    tool_id = data.split(":", 1)[1]

    if tool_id not in TOOLS:
        await query.edit_message_text(
            "❌ Tool not found."
        )
        return

    tool_name = TOOLS[tool_id][0]

    await query.edit_message_text(
        f"🛠 {tool_name}\n\n"
        f"Use this command:\n"
        f"/{tool_id} <your text>\n\n"
        f"Example:\n"
        f"/{tool_id} hello"
    )


# =========================================================
# TOOL COMMAND
# =========================================================

async def tool_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    if not update.message:
        return

    message_text = update.message.text or ""

    if not message_text:
        return

    command = message_text.split()[0]

    tool_id = command.lstrip("/").split("@")[0].lower()

    if tool_id not in TOOLS:
        await update.message.reply_text(
            "❌ Unknown tool.\n\n"
            "Use /tools to see available tools."
        )
        return

    text = " ".join(context.args)

    if not text:
        await update.message.reply_text(
            f"🛠 {TOOLS[tool_id][0]}\n\n"
            f"Usage:\n"
            f"/{tool_id} <your text>"
        )
        return

    function = TOOLS[tool_id][1]

    try:
        result = function(text)

        # Telegram messages have a practical size limit.
        # Prevent very large tool results from causing errors.
        result_text = str(result)

        if len(result_text) > 4000:
            result_text = result_text[:3990] + "\n\n…"

        await update.message.reply_text(
            result_text
        )

    except Exception:
        await update.message.reply_text(
            "❌ Something went wrong while running this tool."
        )


# =========================================================
# CREATE BOT
# =========================================================

def create_bot():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN is not configured."
        )

    bot = (
        Application
        .builder()
        .token(BOT_TOKEN)
        .build()
    )

    # -----------------------------------------------------
    # BASIC COMMANDS
    # -----------------------------------------------------

    bot.add_handler(
        CommandHandler(
            "start",
            start_command
        )
    )

    bot.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )

    bot.add_handler(
        CommandHandler(
            "tools",
            tools_command
        )
    )

    # -----------------------------------------------------
    # CATEGORY CALLBACK
    # -----------------------------------------------------

    bot.add_handler(
        CallbackQueryHandler(
            category_button,
            pattern=r"^category:"
        )
    )

    # -----------------------------------------------------
    # BACK BUTTON
    # -----------------------------------------------------

    bot.add_handler(
        CallbackQueryHandler(
            back_to_tools,
            pattern=r"^back:tools$"
        )
    )

    # -----------------------------------------------------
    # TOOL BUTTON
    # -----------------------------------------------------

    bot.add_handler(
        CallbackQueryHandler(
            tool_button,
            pattern=r"^tool:"
        )
    )

    # -----------------------------------------------------
    # REGISTER ALL TOOLS
    # -----------------------------------------------------

    for tool_id in TOOLS:

        bot.add_handler(
            CommandHandler(
                tool_id,
                tool_command
            )
        )

    return bot


# =========================================================
# FASTAPI STARTUP
# =========================================================

@app.on_event("startup")
async def startup():

    global telegram_app

    telegram_app = create_bot()

    await telegram_app.initialize()

    await telegram_app.start()

    await telegram_app.updater.start_polling()


# =========================================================
# FASTAPI SHUTDOWN
# =========================================================

@app.on_event("shutdown")
async def shutdown():

    global telegram_app

    if telegram_app:

        await telegram_app.updater.stop()

        await telegram_app.stop()

        await telegram_app.shutdown()


# =========================================================
# HOME
# =========================================================

@app.get("/")
async def home():

    return {
        "status": "online",
        "bot": "Cracker World",
        "tools": len(TOOLS),
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
async def health():

    return {
        "status": "ok"
    }


# =========================================================
# LOCAL RUN
# =========================================================

if __name__ == "__main__":

    import uvicorn

    port = int(
        os.getenv(
            "PORT",
            "10000"
        )
    )

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port
    )
```
