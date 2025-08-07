import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🟢 /play or /song handler
async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please send a YouTube link.\n\nExample:\n`/play https://youtu.be/abc123`", parse_mode="Markdown")
        return

    url = context.args[0]
    await update.message.reply_text("🎧 Downloading audio...")

    api_url = f"https://apis-keith.vercel.app/download/audio?url={url}"
    try:
        res = requests.get(api_url).json()
        if 'url' in res:
            await update.message.reply_audio(audio=res['url'], caption="🎵 Here is your audio!")
        else:
            await update.message.reply_text("❌ Failed to get audio. Try another link.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

# 🟢 /video handler
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Please send a YouTube link.\n\nExample:\n`/video https://youtu.be/abc123`", parse_mode="Markdown")
        return

    url = context.args[0]
    await update.message.reply_text("📥 Downloading video...")

    api_url = f"https://apis-keith.vercel.app/download/video?url={url}"
    try:
        res = requests.get(api_url).json()
        if 'url' in res:
            await update.message.reply_video(video=res['url'], caption="🎬 Here is your video!")
        else:
            await update.message.reply_text("❌ Failed to get video. Try another link.")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

# 🟢 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 *Welcome to Keith Downloader Bot!*\n\n"
        "🎧 `/play <YouTube link>` – Download audio\n"
        "🎬 `/video <YouTube link>` – Download video\n\n"
        "_Send a valid YouTube URL to get started._"
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

# 🔁 Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["play", "song"], download_audio))
    app.add_handler(CommandHandler("video", download_video))
    app.run_polling()

if __name__ == "__main__":
    main()