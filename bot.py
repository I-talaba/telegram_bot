from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler,MessageHandler,filters,ContextTypes

TOKEN = "8699235554:AAGiov_E9AewZf3Z0bO-t90MPE7bYSeqUrI"
# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["➕ Yig'indi","➖ Ayirma"],
        ["✖️ Ko'paytma","➗ Bo'lish"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    
    await update.message.reply_text("Amalni tanlang:🤖",reply_markup=reply_markup)
    
# Tugmalarni ishlashi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "➕ Yig'indi":
        await update.message.reply_text("a + b ni hisoblayman.")
    elif text == "➖ Ayirma":
        await update.message.reply_text("a - b ni hisoblayman.")
    elif text == "✖️ Ko'paytma":
        await update.message.reply_text("a * b ni hisoblayman.")
    elif text == "➗ Bo'lish":
        await update.message.reply_text("a / b ni hisoblayman.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~ filters.COMMAND,handle_message))
print("Bot ishlayapti...")
app.run_polling()