from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8699235554:AAGiov_E9AewZf3Z0bO-t90MPE7bYSeqUrI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Men Abror botman 😎 🤖")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot ishlayapti...")
app.run_polling()