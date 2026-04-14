import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

TOKEN = os.getenv("TOKEN")

app_flask = Flask(__name__)

# Flask route (Render uchun)
@app_flask.route("/")
def home():
    return "Bot ishlayapti!"

# Telegram bot
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Yig‘indi", callback_data="add")],
        [InlineKeyboardButton("➖ Ayirma", callback_data="sub")],
        [InlineKeyboardButton("✖️ Ko‘paytma", callback_data="mul")],
        [InlineKeyboardButton("➗ Bo‘lish", callback_data="div")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Amalni tanlang:", reply_markup=reply_markup)

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    user_data[user_id] = {}

    if query.data == "add":
        user_data[user_id]["operation"] = "+"
    elif query.data == "sub":
        user_data[user_id]["operation"] = "-"
    elif query.data == "mul":
        user_data[user_id]["operation"] = "*"
    elif query.data == "div":
        user_data[user_id]["operation"] = "/"

    user_data[user_id]["step"] = "a"

    await query.message.reply_text("a ni kiriting:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    try:
        if user_data.get(user_id, {}).get("step") == "a":
            user_data[user_id]["a"] = int(text)
            user_data[user_id]["step"] = "b"
            await update.message.reply_text("b ni kiriting:")

        elif user_data.get(user_id, {}).get("step") == "b":
            a = user_data[user_id]["a"]
            b = int(text)
            op = user_data[user_id]["operation"]

            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "*":
                result = a * b
            elif op == "/":
                if b == 0:
                    await update.message.reply_text("0 ga bo‘lish mumkin emas!")
                    return
                result = a / b

            await update.message.reply_text(f"Natija: {result}")
            user_data.pop(user_id, None)

        else:
            await update.message.reply_text("Iltimos, avval amal tanlang /start")

    except:
        await update.message.reply_text("Iltimos, son kiriting!")

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_click))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot ishlayapti...")
    app.run_polling()

# Thread orqali botni ishga tushiramiz
threading.Thread(target=run_bot).start()

# Flask port (Render uchun)
port = int(os.environ.get("PORT", 10000))
app_flask.run(host="0.0.0.0", port=port)