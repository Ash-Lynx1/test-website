const TelegramBot = require('node-telegram-bot-api');
const express = require('express');
const axios = require('axios');
const app = express();

// === CONFIGURATION ===
const TOKEN = '8110670496:AAGuWTvGAjrnC_a012YF5_cq2I3rXF_dE5U';
const PORT = process.env.PORT || 3000;

// Initialize Telegram Bot
const bot = new TelegramBot(TOKEN, { polling: true });

// Handle /start command
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(
    chatId,
    `🎵 Welcome to the YouTube Downloader Bot!\n\nSend:\n• /song or /play [YouTube URL] → to download audio\n• /video [YouTube URL] → to download video\n\nPowered by APIs-Keith ❤️`
  );
});

// Helper function to extract YouTube URL from message
function extractYouTubeUrl(text) {
  const urlMatch = text.match(
    /(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([^\s&]+)/
  );
  return urlMatch ? `https://youtu.be/${urlMatch[1]}` : null;
}

// Command: /song or /play
bot.onText(/\/(song|play)\s(.+)/, async (msg, match) => {
  const chatId = msg.chat.id;
  const inputUrl = match[2];
  const youtubeUrl = extractYouTubeUrl(inputUrl);
  
  if (!youtubeUrl) {
    return bot.sendMessage(chatId, "❌ Please provide a valid YouTube URL.");
  }
  
  try {
    bot.sendMessage(chatId, "🎵 Fetching audio... ⏳");
    
    const response = await axios.get('https://apis-keith.vercel.app/download/audio', {
      params: { url: youtubeUrl }
    });
    
    const data = response.data;
    
    if (data.success && data.data?.download) {
      await bot.sendAudio(chatId, data.data.download, {
        title: data.data.title || 'Unknown Title',
        performer: data.data.artist || 'Unknown Artist',
        caption: `🎧 ${data.data.title}\n\n📥 Audio downloaded via @YourBotName`
      });
    } else {
      await bot.sendMessage(chatId, "❌ Failed to fetch audio. Please try again.");
    }
  } catch (error) {
    console.error("Audio error:", error.message);
    await bot.sendMessage(chatId, "⚠️ Failed to process audio. Invalid link or service down.");
  }
});

// Command: /video
bot.onText(/\/video\s(.+)/, async (msg, match) => {
  const chatId = msg.chat.id;
  const inputUrl = match[1];
  const youtubeUrl = extractYouTubeUrl(inputUrl);
  
  if (!youtubeUrl) {
    return bot.sendMessage(chatId, "❌ Please provide a valid YouTube URL.");
  }
  
  try {
    bot.sendMessage(chatId, "🎥 Fetching video... ⏳");
    
    const response = await axios.get('https://apis-keith.vercel.app/download/video', {
      params: { url: youtubeUrl }
    });
    
    const data = response.data;
    
    if (data.success && data.data?.download) {
      await bot.sendVideo(chatId, data.data.download, {
        caption: `🎬 ${data.data.title}\n\n📥 Video downloaded via @YourBotName`
      });
    } else {
      await bot.sendMessage(chatId, "❌ Failed to fetch video. Please try again.");
    }
  } catch (error) {
    console.error("Video error:", error.message);
    await bot.sendMessage(chatId, "⚠️ Failed to process video. Invalid link or service down.");
  }
});

// Fallback for unmatched commands or messages
bot.on('message', (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text;
  
  if (text && !text.startsWith('/')) {
    bot.sendMessage(
      chatId,
      "❗ Send a command:\n• `/play [YouTube URL]`\n• `/song [YouTube URL]`\n• `/video [YouTube URL]`"
    );
  }
});

// === EXPRESS SERVER (Required for Render) ===
app.get('/', (req, res) => {
  res.send('Bot is running...');
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});