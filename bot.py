import logging
import os
import threading

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from telegram import (
    Update,
    MenuButtonWebApp,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config import (
    BOT_TOKEN,
    ADMIN_ID,
    DEVELOPER_NAME,
    DEVELOPER_USERNAME,
    MAINTENANCE_MODE,
)

from utils.keyboards import (
    main_menu,
    pdf_menu,
    image_menu,
    qr_menu,
    audio_menu,
    file_menu,
    developer_menu,
    help_menu,
    admin_menu,
)

from handlers.pdf import (
    start_text_to_pdf,
    start_image_to_pdf as start_pdf_image_to_pdf,
    start_merge_pdf,
    start_split_pdf,
    start_pdf_to_image,
    start_pdf_to_text,
    start_protect_pdf,
    handle_pdf_text,
    handle_image_to_pdf as handle_pdf_image,
    handle_pdf_document,
    handle_protect_password,
    done_pdf,
    done_merge_pdf,
)

from handlers.image import (
    start_resize_image,
    start_compress_image,
    start_convert_image,
    start_image_to_pdf,
    start_image_info,
    handle_image,
    handle_image_text,
    handle_convert_format,
    done_image_to_pdf,
)

from handlers.qr import (
    start_qr_text,
    start_qr_url,
    start_qr_wifi,
    start_qr_contact,
    start_qr_email,
    start_qr_phone,
    start_qr_scan,
    start_qr_to_pdf,
    handle_qr_text,
    handle_qr_image,
)

from handlers.audio import (
    start_text_to_voice,
    start_voice_changer,
    start_audio_cutter,
    start_audio_converter,
    start_volume_changer,
    start_audio_info,
    handle_audio_text,
    handle_audio_file,
    handle_audio_format,
    handle_volume_text,
    handle_cut_text,
)

from handlers.file import (
    start_create_zip,
    start_extract_zip,
    start_file_converter,
    start_file_info,
    handle_file_document,
    done_create_zip,
)


# =========================================================
# LOGGING
# =========================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


# =========================================================
# FASTAPI / RENDER WEB SERVER
# =========================================================

web_app = FastAPI()


@web_app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta
    name="viewport"
    content="width=device-width, initial-scale=1.0"
>

<title>CRACKER WORLD | MASTERMIND</title>

<style>

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html,
body {
    width: 100%;
    height: 100%;
}

body {
    overflow: hidden;
    background: #020303;
    color: #d7ffe8;
    font-family:
        "Courier New",
        Courier,
        monospace;
}

/* =====================================================
   BACKGROUND
   ===================================================== */

body::before {
    content: "";
    position: fixed;
    inset: 0;

    background:
        linear-gradient(
            rgba(0, 255, 120, 0.025) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(0, 255, 120, 0.025) 1px,
            transparent 1px
        );

    background-size: 45px 45px;

    animation:
        gridMove 12s linear infinite;

    pointer-events: none;
}

@keyframes gridMove {
    from {
        transform: translateY(0);
    }

    to {
        transform: translateY(45px);
    }
}

/* =====================================================
   SCANLINES
   ===================================================== */

.scanlines {
    position: fixed;
    inset: 0;

    pointer-events: none;

    background:
        repeating-linear-gradient(
            to bottom,
            rgba(255,255,255,0.025) 0px,
            rgba(255,255,255,0.025) 1px,
            transparent 2px,
            transparent 5px
        );

    opacity: 0.35;

    z-index: 20;
}

/* =====================================================
   MAIN
   ===================================================== */

.wrapper {
    position: relative;

    width: 100%;
    height: 100vh;

    display: flex;
    align-items: center;
    justify-content: center;

    padding: 20px;
}

.panel {
    position: relative;

    width: min(720px, 100%);

    padding: 38px 30px;

    border: 1px solid rgba(0,255,120,0.22);

    background:
        linear-gradient(
            145deg,
            rgba(0,20,12,0.88),
            rgba(2,5,5,0.96)
        );

    box-shadow:
        0 0 25px rgba(0,255,120,0.06),
        inset 0 0 35px rgba(0,255,120,0.025);

    backdrop-filter: blur(10px);

    overflow: hidden;
}

.panel::before {
    content: "";

    position: absolute;

    top: 0;
    left: -100%;

    width: 60%;
    height: 100%;

    background:
        linear-gradient(
            90deg,
            transparent,
            rgba(0,255,120,0.06),
            transparent
        );

    animation: sweep 5s linear infinite;
}

@keyframes sweep {
    0% {
        left: -100%;
    }

    100% {
        left: 160%;
    }
}

/* =====================================================
   TOP DECORATION
   ===================================================== */

.top-line {
    color: rgba(0,255,120,0.45);

    font-size: 11px;

    letter-spacing: 3px;

    margin-bottom: 22px;

    text-align: center;
}

/* =====================================================
   LOGO
   ===================================================== */

.logo {
    position: relative;

    text-align: center;

    font-family:
        "Courier New",
        monospace;

    font-size:
        clamp(27px, 7vw, 58px);

    font-weight: 900;

    letter-spacing:
        clamp(4px, 1.8vw, 11px);

    color: #dffff0;

    text-shadow:
        0 0 5px rgba(0,255,120,0.65),
        0 0 18px rgba(0,255,120,0.30);

    animation:
        logoPulse 2.5s ease-in-out infinite;
}

@keyframes logoPulse {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0.78;
    }
}

/* =====================================================
   GLITCH
   ===================================================== */

.logo::before,
.logo::after {
    content: attr(data-text);

    position: absolute;

    left: 50%;
    top: 0;

    transform: translateX(-50%);

    width: 100%;

    pointer-events: none;
}

.logo::before {
    color: rgba(255,40,80,0.65);

    clip-path:
        inset(0 0 60% 0);

    animation: glitchOne 3.2s infinite;
}

.logo::after {
    color: rgba(0,220,255,0.55);

    clip-path:
        inset(62% 0 0 0);

    animation: glitchTwo 2.7s infinite;
}

@keyframes glitchOne {

    0%,
    88%,
    100% {
        transform:
            translateX(-50%);
    }

    90% {
        transform:
            translateX(
                calc(-50% - 5px)
            );
    }

    92% {
        transform:
            translateX(
                calc(-50% + 4px)
            );
    }
}

@keyframes glitchTwo {

    0%,
    82%,
    100% {
        transform:
            translateX(-50%);
    }

    84% {
        transform:
            translateX(
                calc(-50% + 6px)
            );
    }

    86% {
        transform:
            translateX(
                calc(-50% - 4px)
            );
    }
}

/* =====================================================
   MASTERMIND
   ===================================================== */

.mastermind {
    margin-top: 15px;

    text-align: center;

    font-size:
        clamp(12px, 3vw, 17px);

    letter-spacing:
        clamp(5px, 2vw, 12px);

    color: #82ffb5;

    text-shadow:
        0 0 8px rgba(0,255,120,0.65),
        0 0 18px rgba(0,255,120,0.25);

    animation:
        mastermindGlow 2s ease-in-out infinite;
}

@keyframes mastermindGlow {

    0%,
    100% {
        opacity: 0.65;
    }

    50% {
        opacity: 1;
    }
}

.signature {
    text-align: center;

    margin-top: 8px;

    color: rgba(180,255,210,0.35);

    font-size: 9px;

    letter-spacing: 3px;
}

/* =====================================================
   TERMINAL
   ===================================================== */

.terminal {
    margin-top: 32px;

    border:
        1px solid rgba(0,255,120,0.13);

    background:
        rgba(0,0,0,0.45);

    padding: 19px;

    min-height: 180px;

    box-shadow:
        inset 0 0 25px rgba(0,255,120,0.025);
}

.terminal-header {
    display: flex;

    align-items: center;

    gap: 7px;

    margin-bottom: 16px;

    color:
        rgba(190,255,215,0.38);

    font-size: 10px;

    letter-spacing: 2px;
}

.dot {
    width: 7px;
    height: 7px;

    border-radius: 50%;

    background: #65ff9a;

    box-shadow:
        0 0 10px rgba(0,255,120,0.8);

    animation:
        dotPulse 1s infinite;
}

@keyframes dotPulse {

    0%,
    100% {
        opacity: 0.35;
    }

    50% {
        opacity: 1;
    }
}

.terminal-line {
    font-size:
        clamp(10px, 2.5vw, 13px);

    line-height: 2;

    color:
        rgba(190,255,215,0.68);

    white-space: nowrap;
}

.terminal-line .prompt {
    color: #55ff91;
}

.status {
    float: right;

    color: #6cffaa;
}

/* =====================================================
   PROGRESS
   ===================================================== */

.progress-area {
    margin-top: 26px;
}

.progress-info {
    display: flex;

    justify-content: space-between;

    font-size: 10px;

    color:
        rgba(190,255,215,0.4);

    margin-bottom: 9px;

    letter-spacing: 1px;
}

.progress-bar {
    width: 100%;
    height: 5px;

    background:
        rgba(0,255,120,0.08);

    overflow: hidden;

    border-radius: 10px;
}

.progress-fill {
    width: 0%;

    height: 100%;

    background:
        linear-gradient(
            90deg,
            #1aff75,
            #9cffc2
        );

    box-shadow:
        0 0 12px rgba(0,255,120,0.8);

    animation:
        progress 6s ease-out forwards;
}

@keyframes progress {
    0% {
        width: 0%;
    }

    25% {
        width: 32%;
    }

    50% {
        width: 58%;
    }

    75% {
        width: 82%;
    }

    100% {
        width: 100%;
    }
}

/* =====================================================
   FINAL STATUS
   ===================================================== */

.final-status {
    margin-top: 28px;

    text-align: center;

    font-size:
        clamp(12px, 3vw, 16px);

    letter-spacing: 4px;

    color: #76ffad;

    text-shadow:
        0 0 12px rgba(0,255,120,0.65);

    opacity: 0;

    animation:
        finalAppear 0.8s ease-out 6s forwards;
}

@keyframes finalAppear {
    to {
        opacity: 1;
    }
}

.status-symbol {
    display: inline-block;

    margin-right: 8px;

    animation:
        statusBlink 1.2s infinite;
}

@keyframes statusBlink {

    0%,
    100% {
        opacity: 0.45;
    }

    50% {
        opacity: 1;
    }
}

/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    margin-top: 24px;

    text-align: center;

    color:
        rgba(190,255,215,0.22);

    font-size: 9px;

    letter-spacing: 2px;
}

/* =====================================================
   MOBILE
   ===================================================== */

@media (max-width: 500px) {

    .panel {
        padding:
            30px 18px;
    }

    .terminal {
        padding: 14px;
    }

    .terminal-line {
        font-size: 9px;
    }

    .status {
        font-size: 8px;
    }
}

</style>
</head>

<body>

<div class="scanlines"></div>

<div class="wrapper">

    <main class="panel">

        <div class="top-line">
            // SECURE CONNECTION // INITIALIZATION PROTOCOL
        </div>

        <div
            class="logo"
            data-text="CRACKER WORLD"
        >
            CRACKER WORLD
        </div>

        <div class="mastermind">
            M A S T E R M I N D
        </div>

        <div class="signature">
            SYSTEM ARCHITECT
        </div>

        <section class="terminal">

            <div class="terminal-header">
                <span class="dot"></span>
                CRACKER-WORLD://BOOT_SEQUENCE
            </div>

            <div class="terminal-line">
                <span class="prompt">&gt;</span>
                establishing connection...
                <span
                    class="status"
                    id="s1"
                >
                    WAIT
                </span>
            </div>

            <div class="terminal-line">
                <span class="prompt">&gt;</span>
                waking service...
                <span
                    class="status"
                    id="s2"
                >
                    WAIT
                </span>
            </div>

            <div class="terminal-line">
                <span class="prompt">&gt;</span>
                loading modules...
                <span
                    class="status"
                    id="s3"
                >
                    WAIT
                </span>
            </div>

            <div class="terminal-line">
                <span class="prompt">&gt;</span>
                telegram gateway...
                <span
                    class="status"
                    id="s4"
                >
                    WAIT
                </span>
            </div>

            <div class="terminal-line">
                <span class="prompt">&gt;</span>
                system status...
                <span
                    class="status"
                    id="s5"
                >
                    WAIT
                </span>
            </div>

        </section>

        <div class="progress-area">

            <div class="progress-info">
                <span id="progressText">
                    INITIALIZING
                </span>

                <span id="percent">
                    0%
                </span>
            </div>

            <div class="progress-bar">
                <div
                    class="progress-fill"
                    id="progressFill"
                ></div>
            </div>

        </div>

        <div class="final-status">
            <span class="status-symbol">◉</span>
            SYSTEM ONLINE
        </div>

        <div class="footer">
            POWERED BY MASTERMIND · CRACKER WORLD
        </div>

    </main>

</div>

<script>

const statuses = [
    document.getElementById("s1"),
    document.getElementById("s2"),
    document.getElementById("s3"),
    document.getElementById("s4"),
    document.getElementById("s5")
];

const messages = [
    "CONNECTING",
    "WAKING",
    "LOADED",
    "CONNECTED",
    "ONLINE"
];

const progressText =
    document.getElementById("progressText");

const percent =
    document.getElementById("percent");

const progressFill =
    document.getElementById("progressFill");


let current = 0;

function activateNext() {

    if (current >= statuses.length) {
        progressText.textContent =
            "SYSTEM READY";

        percent.textContent =
            "100%";

        return;
    }

    statuses[current].textContent =
        messages[current];

    statuses[current].style.color =
        "#72ffad";

    current++;

    setTimeout(
        activateNext,
        1100
    );
}

activateNext();


let progress = 0;

const progressTimer =
    setInterval(() => {

        progress += 1;

        if (progress >= 100) {

            progress = 100;

            clearInterval(
                progressTimer
            );

            progressText.textContent =
                "SYSTEM READY";
        }

        percent.textContent =
            progress + "%";

        progressFill.style.width =
            progress + "%";

    }, 60);


/* =====================================================
   RANDOM GLITCH EFFECT
   ===================================================== */

const logo =
    document.querySelector(".logo");

setInterval(() => {

    if (Math.random() > 0.7) {

        logo.style.transform =
            "translateX(" +
            (Math.random() * 4 - 2) +
            "px)";

        setTimeout(() => {

            logo.style.transform =
                "translateX(0)";

        }, 80);
    }

}, 700);

</script>

</body>
</html>
"""


@web_app.get("/health")
async def health():
    return {
        "status": "healthy",
    }


def start_web_server():
    port = int(
        os.environ.get(
            "PORT",
            "10000",
        )
    )

    logger.info(
        "Starting web server on port %s",
        port,
    )

    uvicorn.run(
        web_app,
        host="0.0.0.0",
        port=port,
        log_level="warning",
    )


# =========================================================
# TELEGRAM MENU BUTTON
# =========================================================

async def setup_menu_button(application):
    try:

        await application.bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="🚀 On Bot",
                web_app=WebAppInfo(
                    url="https://cracker-world.onrender.com/"
                ),
            )
        )

        logger.info(
            "Telegram menu button configured: 🚀 On Bot"
        )

    except Exception:

        logger.exception(
            "Failed to configure Telegram menu button."
        )


# =========================================================
# START
# =========================================================

async def start_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    if MAINTENANCE_MODE:

        await update.message.reply_text(
            "🔧 <b>Bot Maintenance Mode</b>\n\n"
            "এখন bot maintenance-এ আছে। "
            "একটু পরে আবার চেষ্টা করো।",
            parse_mode="HTML",
        )

        return

    text = (
        "👋 <b>Welcome to All-in-One Telegram Bot!</b>\n\n"
        "এক জায়গা থেকে PDF, Image, QR, Audio "
        "এবং File tools ব্যবহার করতে পারবে।\n\n"
        "নিচের menu থেকে একটি option select করো।"
    )

    await update.message.reply_text(
        text,
        parse_mode="HTML",
        reply_markup=main_menu(),
    )


# =========================================================
# HOME
# =========================================================

async def home_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    if update.callback_query:

        query = update.callback_query

        await query.answer()

        await query.edit_message_text(
            "🏠 <b>Main Menu</b>\n\n"
            "একটি tool select করো।",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )

    elif update.message:

        await update.message.reply_text(
            "🏠 <b>Main Menu</b>\n\n"
            "একটি tool select করো।",
            parse_mode="HTML",
            reply_markup=main_menu(),
        )


# =========================================================
# PDF CALLBACK
# =========================================================

async def pdf_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query
    data = query.data

    if data == "pdf_menu":

        await query.answer()

        context.user_data.clear()

        await query.edit_message_text(
            "📄 <b>PDF Tools</b>\n\n"
            "একটি PDF tool select করো।",
            parse_mode="HTML",
            reply_markup=pdf_menu(),
        )

        return

    if data == "text_to_pdf":
        await start_text_to_pdf(
            update,
            context,
        )
        return

    if data == "pdf_image_to_pdf":
        await start_pdf_image_to_pdf(
            update,
            context,
        )
        return

    if data == "merge_pdf":
        await start_merge_pdf(
            update,
            context,
        )
        return

    if data == "split_pdf":
        await start_split_pdf(
            update,
            context,
        )
        return

    if data == "pdf_to_image":
        await start_pdf_to_image(
            update,
            context,
        )
        return

    if data == "pdf_to_text":
        await start_pdf_to_text(
            update,
            context,
        )
        return

    if data == "protect_pdf":
        await start_protect_pdf(
            update,
            context,
        )
        return


# =========================================================
# IMAGE CALLBACK
# =========================================================

async def image_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query
    data = query.data

    if data == "image_menu":

        await query.answer()

        context.user_data.clear()

        await query.edit_message_text(
            "🖼️ <b>Image Tools</b>\n\n"
            "একটি image tool select করো।",
            parse_mode="HTML",
            reply_markup=image_menu(),
        )

        return

    if data == "resize_image":
        await start_resize_image(
            update,
            context,
        )
        return

    if data == "compress_image":
        await start_compress_image(
            update,
            context,
        )
        return

    if data == "convert_image":
        await start_convert_image(
            update,
            context,
        )
        return

    if data == "image_to_pdf":
        await start_image_to_pdf(
            update,
            context,
        )
        return

    if data == "image_info":
        await start_image_info(
            update,
            context,
        )
        return


async def image_format_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query
    data = query.data

    formats = {
        "convert_jpg": "jpg",
        "convert_png": "png",
        "convert_webp": "webp",
        "convert_bmp": "bmp",
    }

    output_format = formats.get(data)

    if not output_format:

        await query.answer(
            "Invalid image format.",
            show_alert=True,
        )

        return

    await handle_convert_format(
        update,
        context,
        output_format,
    )


# =========================================================
# QR CALLBACK
# =========================================================

async def qr_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query
    data = query.data

    if data == "qr_menu":

        await query.answer()

        context.user_data.clear()

        await query.edit_message_text(
            "🔳 <b>QR Tools</b>\n\n"
            "একটি QR tool select করো।",
            parse_mode="HTML",
            reply_markup=qr_menu(),
        )

        return

    if data == "qr_text":
        await start_qr_text(
            update,
            context,
        )
        return

    if data == "qr_url":
        await start_qr_url(
            update,
            context,
        )
        return

    if data == "qr_wifi":
        await start_qr_wifi(
            update,
            context,
        )
        return

    if data == "qr_contact":
        await start_qr_contact(
            update,
            context,
        )
        return

    if data == "qr_email":
        await start_qr_email(
            update,
            context,
        )
        return

    if data == "qr_phone":
        await start_qr_phone(
            update,
            context,
        )
        return

    if data == "qr_scan":
        await start_qr_scan(
            update,
            context,
        )
        return

    if data == "qr_to_pdf":
        await start_qr_to_pdf(
            update,
            context,
        )
        return


# =========================================================
# AUDIO CALLBACK
# =========================================================

async def audio_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query
    data = query.data

    if data == "audio_menu":

        await query.answer()

        context.user_data.clear()

        await query.edit_message_text(
            "🎙️ <b>Audio Tools</b>\n\n"
            "একটি audio tool select করো।",
            parse_mode="HTML",
            reply_markup=audio_menu(),
        )

        return

    if data == "text_to_voice":
        await start_text_to_voice(
            update,
            context,
        )
        return

    if data == "voice_changer":
        await start_voice_changer(
            update,
            context,
        )
        return

    if data == "audio_cutter":
        await start_audio_cutter(
            update,
            context,
        )
        return

    if data == "audio_converter":
        await start_audio_converter(
            update,
            context,
        )
        return

    if data == "volume_changer":
        await start_volume_changer(
            update,
            context,
        )
        return

    if data == "audio_info":
        await start_audio_info(
            update,
            context,
        )
        return


async def audio_format_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query
    data = query.data

    formats = {
        "audio_mp3": "mp3",
        "audio_wav": "wav",
        "audio_ogg": "ogg",
        "audio_m4a": "m4a",
        "audio_flac": "flac",
    }

    output_format = formats.get(data)

    if not output_format:

        await query.answer(
            "Invalid audio format.",
            show_alert=True,
        )

        return

    await handle_audio_format(
        update,
        context,
        output_format,
    )


# =========================================================
# FILE CALLBACK
# =========================================================

async def file_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query
    data = query.data

    if data == "file_menu":

        await query.answer()

        context.user_data.clear()

        await query.edit_message_text(
            "🛠️ <b>File Tools</b>\n\n"
            "একটি file tool select করো।",
            parse_mode="HTML",
            reply_markup=file_menu(),
        )

        return

    if data == "create_zip":
        await start_create_zip(
            update,
            context,
        )
        return

    if data == "extract_zip":
        await start_extract_zip(
            update,
            context,
        )
        return

    if data == "file_converter":
        await start_file_converter(
            update,
            context,
        )
        return

    if data == "file_info":
        await start_file_info(
            update,
            context,
        )
        return


# =========================================================
# DEVELOPER
# =========================================================

async def developer_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    context.user_data.clear()

    await query.edit_message_text(
        "👨‍💻 <b>Developer</b>\n\n"
        f"Name: <b>{DEVELOPER_NAME}</b>\n"
        f"Telegram: <b>{DEVELOPER_USERNAME}</b>",
        parse_mode="HTML",
        reply_markup=developer_menu(
            DEVELOPER_USERNAME
        ),
    )


# =========================================================
# HELP
# =========================================================

async def help_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    context.user_data.clear()

    await query.edit_message_text(
        "ℹ️ <b>Help</b>\n\n"
        "📄 PDF Tools — PDF তৈরি ও process\n"
        "🖼️ Image Tools — resize, compress, convert\n"
        "🔳 QR Tools — QR generate ও scan\n"
        "🎙️ Audio Tools — voice ও audio processing\n"
        "🛠️ File Tools — ZIP ও file information\n\n"
        "কোনো tool ব্যবহার করতে Main Menu "
        "থেকে option select করো।",
        parse_mode="HTML",
        reply_markup=help_menu(),
    )


# =========================================================
# ADMIN
# =========================================================

async def admin_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.effective_user:
        return

    if update.effective_user.id != ADMIN_ID:

        await update.message.reply_text(
            "⛔ এই command শুধু admin-এর জন্য।"
        )

        return

    await update.message.reply_text(
        "🛠️ <b>Admin Panel</b>\n\n"
        "একটি option select করো।",
        parse_mode="HTML",
        reply_markup=admin_menu(),
    )


async def admin_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    if not update.effective_user:
        return

    if update.effective_user.id != ADMIN_ID:

        await query.answer(
            "⛔ Admin only.",
            show_alert=True,
        )

        return

    await query.answer()

    data = query.data

    messages = {
        "admin_statistics": (
            "📊 <b>Statistics</b>\n\n"
            "Database system বর্তমানে active নেই।"
        ),
        "admin_users": (
            "👥 <b>Users</b>\n\n"
            "Database system বর্তমানে active নেই।"
        ),
        "admin_broadcast": (
            "📢 <b>Broadcast</b>\n\n"
            "Database system বর্তমানে active নেই।"
        ),
        "admin_ban": (
            "🚫 <b>Ban</b>\n\n"
            "Database system বর্তমানে active নেই।"
        ),
        "admin_unban": (
            "✅ <b>Unban</b>\n\n"
            "Database system বর্তমানে active নেই।"
        ),
        "admin_maintenance": (
            "🔧 <b>Maintenance</b>\n\n"
            "বর্তমানে config.py থেকে "
            "maintenance mode control করা হয়।"
        ),
    }

    message = messages.get(data)

    if message:

        await query.edit_message_text(
            message,
            parse_mode="HTML",
            reply_markup=admin_menu(),
        )


# =========================================================
# TEXT HANDLER
# =========================================================

async def text_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    data = context.user_data

    if data.get("pdf_action") == "text_to_pdf":

        await handle_pdf_text(
            update,
            context,
        )

        return

    if (
        data.get("pdf_action") == "protect"
        and data.get("protect_waiting_password")
    ):

        await handle_protect_password(
            update,
            context,
        )

        return

    if (
        data.get("image_action") == "resize"
        and data.get("image_waiting_dimensions")
    ):

        await handle_image_text(
            update,
            context,
        )

        return

    if data.get("qr_action"):

        await handle_qr_text(
            update,
            context,
        )

        return

    if data.get("audio_action") == "text_to_voice":

        await handle_audio_text(
            update,
            context,
        )

        return

    if data.get("audio_waiting_volume"):

        await handle_volume_text(
            update,
            context,
        )

        return

    if data.get("audio_waiting_cut"):

        await handle_cut_text(
            update,
            context,
        )

        return

    await update.message.reply_text(
        "ℹ️ কোনো active tool নেই।\n\n"
        "/start দিয়ে Main Menu খুলো।"
    )


# =========================================================
# PHOTO HANDLER
# =========================================================

async def photo_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    data = context.user_data

    if data.get("pdf_action") == "image_to_pdf":

        await handle_pdf_image(
            update,
            context,
        )

        return

    if data.get("image_action"):

        await handle_image(
            update,
            context,
        )

        return

    if data.get("qr_action") == "scan":

        await handle_qr_image(
            update,
            context,
        )

        return


# =========================================================
# DOCUMENT HANDLER
# =========================================================

async def document_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    data = context.user_data

    if data.get("pdf_action") in {
        "merge",
        "split",
        "pdf_to_text",
        "pdf_to_image",
        "protect",
    }:

        await handle_pdf_document(
            update,
            context,
        )

        return

    if data.get("qr_action") == "scan":

        await handle_qr_image(
            update,
            context,
        )

        return

    if data.get("audio_action") in {
        "voice_changer",
        "cutter",
        "converter",
        "volume",
        "info",
    }:

        await handle_audio_file(
            update,
            context,
        )

        return

    if data.get("file_action") in {
        "create_zip",
        "extract_zip",
        "file_info",
    }:

        await handle_file_document(
            update,
            context,
        )

        return


# =========================================================
# AUDIO
# =========================================================

async def audio_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    await handle_audio_file(
        update,
        context,
    )


async def voice_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    if not update.message:
        return

    await handle_audio_file(
        update,
        context,
    )


# =========================================================
# DONE
# =========================================================

async def done_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    data = context.user_data

    if data.get("pdf_action") == "image_to_pdf":

        await done_pdf(
            update,
            context,
        )

        return

    if data.get("pdf_action") == "merge":

        await done_merge_pdf(
            update,
            context,
        )

        return

    if data.get("image_action") == "image_to_pdf":

        await done_image_to_pdf(
            update,
            context,
        )

        return

    if data.get("file_action") == "create_zip":

        await done_create_zip(
            update,
            context,
        )

        return

    await update.message.reply_text(
        "ℹ️ কোনো active multi-file operation নেই।"
    )


# =========================================================
# CANCEL
# =========================================================

async def cancel_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    context.user_data.clear()

    await update.message.reply_text(
        "❌ Current operation cancelled.\n\n"
        "🏠 Main Menu:",
        reply_markup=main_menu(),
    )


# =========================================================
# ERROR HANDLER
# =========================================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):

    logger.error(
        "Unhandled exception:",
        exc_info=context.error,
    )


# =========================================================
# MAIN
# =========================================================

def main():

    if not BOT_TOKEN:

        raise RuntimeError(
            "BOT_TOKEN environment variable is missing."
        )

    # -----------------------------------------------------
    # Render Web Server
    # -----------------------------------------------------

    web_thread = threading.Thread(
        target=start_web_server,
        daemon=True,
    )

    web_thread.start()

    logger.info(
        "Render web server started."
    )

    # -----------------------------------------------------
    # Telegram Application
    # -----------------------------------------------------

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(setup_menu_button)
        .build()
    )

    # -----------------------------------------------------
    # Commands
    # -----------------------------------------------------

    application.add_handler(
        CommandHandler(
            "start",
            start_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "done",
            done_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "cancel",
            cancel_command,
        )
    )

    application.add_handler(
        CommandHandler(
            "admin",
            admin_command,
        )
    )

    # -----------------------------------------------------
    # HOME
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            home_command,
            pattern=r"^home$",
        )
    )

    # -----------------------------------------------------
    # PDF
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            pdf_callback,
            pattern=(
                r"^(pdf_menu|text_to_pdf|"
                r"pdf_image_to_pdf|merge_pdf|split_pdf|"
                r"pdf_to_image|pdf_to_text|protect_pdf)$"
            ),
        )
    )

    # -----------------------------------------------------
    # IMAGE
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            image_callback,
            pattern=(
                r"^(image_menu|resize_image|"
                r"compress_image|convert_image|"
                r"image_to_pdf|image_info)$"
            ),
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            image_format_callback,
            pattern=r"^convert_(jpg|png|webp|bmp)$",
        )
    )

    # -----------------------------------------------------
    # QR
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            qr_callback,
            pattern=(
                r"^(qr_menu|qr_text|qr_url|qr_wifi|"
                r"qr_contact|qr_email|qr_phone|"
                r"qr_scan|qr_to_pdf)$"
            ),
        )
    )

    # -----------------------------------------------------
    # AUDIO
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            audio_callback,
            pattern=(
                r"^(audio_menu|text_to_voice|"
                r"voice_changer|audio_cutter|"
                r"audio_converter|volume_changer|"
                r"audio_info)$"
            ),
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            audio_format_callback,
            pattern=r"^audio_(mp3|wav|ogg|m4a|flac)$",
        )
    )

    # -----------------------------------------------------
    # FILE
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            file_callback,
            pattern=(
                r"^(file_menu|create_zip|extract_zip|"
                r"file_converter|file_info)$"
            ),
        )
    )

    # -----------------------------------------------------
    # DEVELOPER / HELP
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            developer_callback,
            pattern=r"^developer$",
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            help_callback,
            pattern=r"^help$",
        )
    )

    # -----------------------------------------------------
    # ADMIN
    # -----------------------------------------------------

    application.add_handler(
        CallbackQueryHandler(
            admin_callback,
            pattern=r"^admin_",
        )
    )

    # -----------------------------------------------------
    # PHOTO
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            photo_handler,
        )
    )

    # -----------------------------------------------------
    # DOCUMENT
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.Document.ALL,
            document_handler,
        )
    )

    # -----------------------------------------------------
    # AUDIO
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.AUDIO,
            audio_handler,
        )
    )

    # -----------------------------------------------------
    # VOICE
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.VOICE,
            voice_handler,
        )
    )

    # -----------------------------------------------------
    # TEXT
    # -----------------------------------------------------

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler,
        )
    )

    # -----------------------------------------------------
    # ERROR
    # -----------------------------------------------------

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "Telegram bot is starting..."
    )

    # -----------------------------------------------------
    # POLLING
    # -----------------------------------------------------

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()
