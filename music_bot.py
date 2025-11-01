"""
Simple Telegram Music Bot (Python)

Features:
- Search YouTube for a query (using youtube-search-python)
- Download audio (pytube) and send as mp3 to user
- Uses BOT_TOKEN from environment or .env file

USAGE:
- Install dependencies from requirements.txt
- Edit the .env file or set environment variable BOT_TOKEN before running
- Run: python music_bot.py
"""

import os
import time
import tempfile
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from youtubesearchpython import VideosSearch
from pytube import YouTube

BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    # try load from .env
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == "BOT_TOKEN":
                    BOT_TOKEN = v.strip().strip('"').strip("'")
                    break

if not BOT_TOKEN:
    raise RuntimeError("Bot token not found. Set BOT_TOKEN env var or put BOT_TOKEN=... in .env file")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("नमस्ते! मुझे गाना का नाम भेजो और मैं ऑडियो भेज दूँगा।")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("गाना खोजने के लिए गाना का नाम टाइप करें। उदाहरण: Shape of You")

async def get_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    user_id = update.effective_user.id if update.effective_user else int(time.time())
    await update.message.reply_text(f"🔎 '{query}' के लिए खोज रहा हूँ...")

    try:
        videos = VideosSearch(query, limit=1).result()
    except Exception as e:
        await update.message.reply_text("सर्च करते समय त्रुटि हुई। बाद में फिर कोशिश करें।")
        return

    results = videos.get("result") or []
    if not results:
        await update.message.reply_text("❌ कोई परिणाम नहीं मिला।")
        return

    first = results[0]
    url = first.get("link")
    title = first.get("title", "audio")

    await update.message.reply_text(f"🎧 डाउनलोड कर रहा हूँ: {title}")

    # create a safe temporary filename
    tmp_dir = Path(tempfile.gettempdir())
    filename = tmp_dir / f"song_{user_id}_{int(time.time())}.mp3"

    try:
        yt = YouTube(url)
        # select audio-only stream
        stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if not stream:
            await update.message.reply_text("ऑडियो स्ट्रीम उपलब्ध नहीं है।")
            return

        out_file = stream.download(filename=str(filename))
        # Ensure file exists
        if not Path(out_file).exists():
            await update.message.reply_text("डाउनलोड में समस्या हुई।")
            return

        # Send the audio file
        with open(out_file, "rb") as f:
            await update.message.reply_audio(audio=f, title=title)

    except Exception as e:
        await update.message.reply_text("डाउनलोड में त्रुटि आई — संभवतः यह वीडियो region-restricted या age-restricted है।")
    finally:
        # cleanup
        try:
            if filename.exists():
                filename.unlink()
        except Exception:
            pass

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_music))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
