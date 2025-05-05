from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import os

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN environment variable not set.")

# Tugmalar ro'yxati
BUTTONS = {
    "🎓 Ta'lim xizmati": "Tugma 1 matni",
    "🚌 Avtobus xizmati": "Tugma 2 matni",
    "🏨 Yotoqxona xizmati": "Tugma 3 matni",
    "📞 Bog'lanish": "Tugma 4 matni",
}

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.set_my_commands([
        BotCommand("menu", "📋 Xizmatlar menyusi")
    ])
    await update.message.reply_text("Assalomu alaykum! Pastdagi menyudan foydalaning.")

# /menu komandasi
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(k, callback_data=k)] for k in BUTTONS]
    await update.message.reply_text(
        "Iltimos, birini tanlang:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Inline tugma bosilganda
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not context.user_data.get("phone_number"):
        contact_button = KeyboardButton("📱 Raqam yuborish", request_contact=True)
        contact_keyboard = ReplyKeyboardMarkup(
            [[contact_button]], resize_keyboard=True, one_time_keyboard=True
        )
        await query.message.reply_text(
            "Iltimos, avval telefon raqamingizni yuboring:",
            reply_markup=contact_keyboard
        )
        return

    text = BUTTONS.get(query.data, "Topilmadi.")
    await query.edit_message_text(text)

# Telefon raqami qabul qilganda
async def contact_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:
        context.user_data["phone_number"] = contact.phone_number
        await update.message.reply_text(
            "✅ Raqamingiz qabul qilindi. Endi menyudan foydalanishingiz mumkin.",
            reply_markup=ReplyKeyboardRemove()
        )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.CONTACT, contact_handler))

    app.run_polling(drop_pending_updates=True)
