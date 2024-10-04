import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from transformers import pipeline

# Load environment variables
load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")

# Check if TELEGRAM_API_KEY is set
if not TELEGRAM_API_KEY:
    print("TELEGRAM_API_KEY is not set")
    exit(1)

# Load pre-trained summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_API_KEY)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply("Welcome! I'm a summarization bot developed by Sunny Kumar(kgpian). Send me a long text, and I'll summarize it for you.")

@dp.message_handler()
async def summarize_text(message: types.Message):
    try:
        # Check if the message is long enough to summarize
        if len(message.text.split()) < 30:
            await message.reply("Please provide a longer text (at least 30 words) for summarization.")
            return

        # Send typing action
        await bot.send_chat_action(message.chat.id, action="typing")
        
        # Generate summary
        summary = summarizer(message.text, max_length=150, min_length=30, do_sample=False)
        
        # Send the summary
        await message.reply(summary[0]['summary_text'])
    
    except Exception as err:
        await message.reply(f"Oops, something went wrong:\n\n{err}")

if __name__ == '__main__':
    print("Starting summarization bot")
    executor.start_polling(dp, skip_updates=True)