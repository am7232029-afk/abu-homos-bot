import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN") or ""

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
    for doc in doctors:
        name = doc.get("name","").lower()
        spec = doc.get("specialty","").lower()
        addr = doc.get("address","").lower()
        if text in name or text in spec or text in addr or text in "دكتور":
            results.append(doc)
        # كمان لو كتب تخصص بس
        if text.replace("دكتور","").strip() in spec:
            if doc not in results:
                results.append(doc)
    return results

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا بيك في بوت دكاترة أبو شوشة 👨‍⚕️\nاكتب التخصص مثلا: دكتور اسنان، دكتور اطفال، دكتور عيون")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.message.text
    res = search_doctors(q)
    if not res:
        all_specs = sorted(set([d.get('specialty','') for d in load_doctors()]))
        await update.message.reply_text(f"مفيش نتيجة لـ '{q}'\nالتخصصات المتاحة عندنا: {', '.join(all_specs)}")
        return
    msg = f"لقيت {len(res)} دكتور لطلبك '{q}':\n\n"
    for d in res[:10]:
        phone = d.get('phone','')
        if not phone or "000000" in phone:
            phone = "غير متوفر حاليا"
        msg += f"👨‍⚕️ {d.get('name')}\n🔹 {d.get('specialty')} - {d.get('address')}\n📞 {phone}\n⏰ {d.get('hours','')}\n\n"
    await update.message.reply_text(msg)

def main():
    if not TOKEN or len(TOKEN) < 20:
        print("مفيش توكن! ضيفه في Secrets باسم BOT_TOKEN")
        return
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
