import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 *Welcome to YouTube Downloader Bot!*\n\n"
        "🎵 `/play <YouTube URL>` – Download audio\n"
        "🎬 `/video <YouTube URL>` – Download video\n\n"
        "_Send a valid YouTube URL to begin._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

# /play or /song command
async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a YouTube link.\nExample: /play https://youtu.be/...")
        return

    url = context.args[0]
    await update.message.reply_text("🎧 Processing audio...")

    try:
        res = requests.get(f"https://apis-keith.vercel.app/download/audio?url={url}")
        res.raise_for_status()
        data = res.json()
        audio_url = data.get("url")

        if audio_url:
            await update.message.reply_audio(audio=audio_url, caption="✅ Here is your audio!")
        else:
            await update.message.reply_text("❌ Failed to get audio.")
    except Exception as e:
        logging.error(f"Audio Error: {e}")
        await update.message.reply_text("⚠️ Error downloading audio.")

# /video command
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please provide a YouTube link.\nExample: /video https://youtu.be/...")
        return

    url = context.args[0]
    await update.message.reply_text("📥 Processing video...")

    try:
        res = requests.get(f"https://apis-keith.vercel.app/download/video?url={url}")
        res.raise_for_status()
        data = res.json()
        video_url = data.get("url")

        if video_url:
            await update.message.reply_video(video=video_url, caption="✅ Here is your video!")
        else:
            await update.message.reply_text("❌ Failed to get video.")
    except Exception as e:
        logging.error(f"Video Error: {e}")
        await update.message.reply_text("⚠️ Error downloading video.")

# Run bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["play", "song"], handle_audio))
    app.add_handler(CommandHandler("video", handle_video))
    app.run_polling()

if __name__ == "__main__":
    main()