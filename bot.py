from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes

TOKEN = "8699235554:AAGiov_E9AewZf3Z0bO-t90MPE7bYSeqUrI"

# Foydalanauvchilarni ma'lumotlarini saqlash
user_data = {}


# START
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["➕ Yig'indi","➖ Ayirma"],
        ["✖️ Ko'paytma","➗ Bo'lish"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)

    user_data[update.effective_user.id] = {}

    await update.message.reply_text("Amalni tanlang:",reply_markup=reply_markup)

# Xabarni boshqarish
async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    #Amalni tanlash
    if text in ["➕ Yig'indi","➖ Ayirma","✖️ Ko'paytma","➗ Bo'lish"]:
        user_data[user_id]["operation"] = text
        user_data[user_id]["step"] = "a"
        await update.message.reply_text("a ni kiriting:")

    # a ni kiritish
    elif user_data.get(user_id,{}).get("step") == "a":
        try:
            user_data[user_id]["a"] = float(text)
            user_data[user_id]["step"] = "b"
            await update.message.reply_text("b ni kiriting (son):")
        except ValueError:
            await update.message_reply_text("Iltimos,son kiriting!")
    
    # b ni qabul qilsih hisoblash
    elif user_data.get(user_id,{}).get("step") == "b":
        try:
            
            a = user_data[user_id]["a"]
            b = float(text)
            op = user_data[user_id]["operation"]
            
            # Hisoblash
            if op == "➕ Yig'indi":
                result = a + b
                beldi = "➕"
            elif op == "➖ Ayirma":
                result = a - b
                belgi = "➖"
            elif op == "✖️ Ko'paytma":
                result = a * b
                belgi = "✖️"
            elif op == "➗ Bo'lish":
                if b == 0:
                    await update.message.reply_text("Xato!Nolga bo'lish mumkin emas!")
                    return 
                result = a / b
                belgi = "➗"
                
            # Natijani chiqarish
            await update.message.reply_text(f"{a} {belgi} {b} = {result}")
            
            # Qayta ishga tushurish (yangi amal uchun)
            user_data[user_id] = {}
            keyboard = [
                ["➕ Yig'indi", "➖ Ayirma"],
                ["✖️ Ko'paytma", "➗ Bo'lish"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Yangi amal kiriting:",reply_markup=reply_markup)
        except ValueError:
            await update.message.reply_text("Iltimos,son kiriting!")
        except Exception as e:
            await update.message.reply_text(f"Xatolik yuz berdi {e}")
            
    else:
        # hech qanday amal tanlanmagan bo'lsa
        await update.message.reply_text("Iltimos,avval amalni tanlang:")
            

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))

print("Bot ishga tushdi...🤖 😎")
app.run_polling()