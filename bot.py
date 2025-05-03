from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Tugmalar ro'yxati
BUTTONS = {
    "🎓 Ta'lim xizmati": "Tugma 1 matni",
    "🚌 Avtobus xizmati": "Tugma 2 matni",
    "🏨 Yotoqxona xizmati": "Tugma 3 matni",
    "📞 Bog'lanish": "Tugma 4 matni",
}


# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(k, callback_data=k)] for k in BUTTONS]
    await update.message.reply_text(
        "Iltimos, birini tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Inline tugma handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not context.user_data.get("phone_number"):
        # Raqam so'rash
        contact_button = KeyboardButton("📱 Raqam yuborish", request_contact=True)
        contact_keyboard = ReplyKeyboardMarkup(
            [[contact_button]], resize_keyboard=True, one_time_keyboard=True
        )
        await query.message.reply_text(
            "Iltimos, avval telefon raqamingizni yuboring:",
            reply_markup=contact_keyboard
        )
        return

    # Agar raqam bor bo‘lsa tugma ishlaydi
    text = BUTTONS.get(query.data, "Topilmadi.")
    await query.edit_message_text(text)

# Raqam qabul qilganda
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        context.user_data["phone_number"] = contact.phone_number

        # "Tugmalarni tanlash" tugmasi
        select_buttons = [
            [KeyboardButton("🧩 Tugmalarni tanlash")]
        ]
        reply_markup = ReplyKeyboardMarkup(select_buttons, resize_keyboard=True, one_time_keyboard=True)

        await update.message.reply_text(
            "✅ Raqamingiz qabul qilindi.\n\nTugmalarni tanlash uchun pastdagi tugmani bosing.",
            reply_markup=reply_markup
        )

# "Tugmalarni tanlash" tugmasi bosilganda
async def show_buttons_again(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🧩 Tugmalarni tanlash":
        keyboard = [[InlineKeyboardButton(k, callback_data=k)] for k in BUTTONS]
        await update.message.reply_text(
            "Iltimos, birini tanlang:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token("7580446562:AAF6GnQlh_9cCZ5SnXOTUZ83FRphYUuaUxA").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🧩 Tugmalarni tanlash"), show_buttons_again))

    app.run_polling()
