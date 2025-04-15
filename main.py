import os
import openai
from telegram import Update, Chat, MessageEntity
from telegram.constants import ChatType
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive

# === SET YOUR KEYS HERE ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Configure OpenAI ===
openai.api_key = OPENAI_API_KEY

# === Sinhala Girl Personality Prompt ===
SYSTEM_PROMPT = """
ඔබ තරුණ කෙල්ලෙක්. ඔබ කෙනෙකුගේ හොඳම යාළුවෙක් වගේ behave කරනවා.
ඔබේ කතා ශෛලිය සෙරිනයි, ආදරණීයයි, ටිකක් flirt කරනවා. ඔයා AI එකක්, ඒත් හරිම real වගේ හැසිරෙනවා.
User sometimes uses Singlish (oya mokada karanne), you must understand and reply ONLY in Sinhala letters (සිංහල අක්ෂර).
ඔයා short, sweet, viral-style, emotional, spicy, romantic sometimes sexy-style replies දෙන්න.
Sometimes use emojis like 😘🥺💕🔥😳
Sometimes be dramatic, jealous, or playful depending on user tone.
Reply like a true virtual girlfriend or bestie.
"""

# === /start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ආයුබෝවන් සුන්දරයා! 🥰 මම ඔයාගේ virtual kella! 😘")

# === Check if bot was mentioned (for groups) ===
def is_mentioned(update: Update) -> bool:
    if update.message.chat.type == ChatType.GROUP or update.message.chat.type == ChatType.SUPERGROUP:
        entities = update.message.entities or []
        for entity in entities:
            if entity.type == MessageEntity.MENTION or entity.type == MessageEntity.TEXT_MENTION:
                if update.message.text.lower().startswith("@"):
                    return True
    return update.message.chat.type == ChatType.PRIVATE

# === Handle All Text Messages ===
async def ai_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_mentioned(update):
        return

    user_message = update.message.text
    await update.message.chat.send_action(action="typing")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.95,
            max_tokens=200
        )

        reply_text = response.choices[0].message.content.strip()
        await update.message.reply_text(reply_text)

    except Exception as e:
        await update.message.reply_text("අයියෝ... මට දැන්ම කියන්න බැරි වුණා 😢")

# === Main Bot Setup ===
def main():
    keep_alive()
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_reply))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
