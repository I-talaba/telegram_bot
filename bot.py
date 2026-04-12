"""Bu telegram bot da ishlaydigan kalkulyator dasturi.pip install python-telegram-bot==22.7"""

from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder,CommandHandler,MessageHandler,filters,ContextTypes

TOKEN = "BU_YERGA_TOKEN_JOYLANG"

# Foydalanauvchilarni ma'lumotlarini saqlash
user_data = {}


# START
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Foydalanuvchilarni ma'lumotlarini tozalash
    user_data[user_id] = {}

    keyboard = [
        ["➕ Yig'indi","➖ Ayirma"],
        ["✖️ Ko'paytma","➗ Bo'lish"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard,resize_keyboard=True)


    await update.message.reply_text("Amalni tanlang:",reply_markup=reply_markup)

# Xabarni boshqarish
async def handle_message(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    # Nuhim: Agar foydalanuvchi user_data da bo'lmasa,yaratish
    if user_id not in user_data:
        user_data[user_id] = {}
        await update.message.reply_text("Iltimos,avval /start tugmasini bosing.")
        return


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
                belgi = "➕"
                amal = "Yig'indi"
            elif op == "➖ Ayirma":
                result = a - b
                belgi = "➖"
                amal = "Ayirma"
            elif op == "✖️ Ko'paytma":
                result = a * b
                belgi = "✖️"
                amal = "Ko'paytma"
            elif op == "➗ Bo'lish":
                if b == 0:
                    await update.message.reply_text("Xato!Nolga bo'lish mumkin emas!")
                    # Qayta boshlash
                    user_data[user_id] = {}
                    return
                result = a / b
                belgi = "➗"
                amal = "Bo'lish"
            else:
                await update.message.teply_text("❌ Xato!Amal tanlanmagan! ")
                return

            # Natijani chiqarish
            javob = f"📋 {amal} amal natijasi: \n"
            javob += f"{a} {belgi} {b} = {result}"
            await update.message.reply_text(javob)


            # Qayta ishga tushurish (yangi amal uchun) ma'lumotlarni tozalash
            user_data[user_id] = {}
            # Yana amla tanlash uchun
            keyboard = [
                ["➕ Yig'indi", "➖ Ayirma"],
                ["✖️ Ko'paytma", "➗ Bo'lish"]
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text("Yangi amal kiriting yoki /start bosing:",reply_markup=reply_markup)

        except ValueError:
            await update.message.reply_text("Iltimos,son kiriting!")
        except Exception as e:
            await update.message.reply_text(f"Xatolik yuz berdi {e}")

    else:
        # hech qanday amal tanlanmagan bo'lsa
        await update.message.reply_text("Iltimos,avval amallardan birini tanlang yoki /start bosing:")
        # tugmalarni ko'rsatish
        keyboard = [
            ["➕ Yig'indi", "➖ Ayirma"],
            ["✖️ Ko'paytma", "➗ Bo'lish"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text("Amal:", reply_markup=reply_markup)

if __name__ == "__main__":

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle_message))
    print("Bot ishga tushdi...🤖 😎")
    app.run_polling()
