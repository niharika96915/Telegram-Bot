from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()
# API KEYS - Load from environment variables
TELEGRAM_TOKEN = os.getenv("8696211547:AAETJgTgWZkYrUQ5KAreu7Kc86O0hEMtYKA")
OPENAI_API_KEY = os.getenv("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")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("8696211547:AAETJgTgWZkYrUQ5KAreu7Kc86O0hEMtYKA")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# 🔹 Function to call AI API
async def generate_caption(user_input):
    prompt = f"Generate 3 engaging social media captions for: {user_input}"

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    return response.choices[0].message.content


# 🔹 Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! Send me a topic + tone and I'll generate captions ✨"
    )


# 🔹 Handle user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    captions = await generate_caption(user_text)

    await update.message.reply_text(captions)


# 🔹 Run bot
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()