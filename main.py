import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

def load_doctors():
    try:
        with open("doctors.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def search_doctors(text):
    doctors = load_doctors()
    text = text.lower().strip()
    results = []
    for d in doctors:
        if text in d.get("اسم","").lower() or text in d.get("تخصص","").lower():
            results.append(d)
    return results

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا بيك في مساعد أبوحمص الطبي 🏥\nاكتب اسم الدكتور أو التخصص")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    results = search_doctors(query)
    if not results:
        await update.message.reply_text(f"مالقيتش '{query}' جرب: باطنة، اسنان، اطفال")
        return
    msg = f"لقيت {len(results)} دكتور:\n\n"
    for d in results[:10]:
        msg += f"👨‍⚕️ {d.get('اسم','')}\n📌 {d.get('تخصص','')} - {d.get('عنوان','')}\n📞 {d.get('رقم','')}\n\n"
    await update.message.reply_text(msg)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
