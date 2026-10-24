import logging
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logger = logging.getLogger("Bot2")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    name = user.first_name if user else "គ្នាយើង"
    await update.message.reply_text(
        f"សួស្តី {name}! ខ្ញុំជា Bot ទី ២ របស់អ្នក! 🤖✨\n"
        "ប្រព័ន្ធដំណើរការបានយ៉ាងរលូន។"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    await update.message.reply_text(f"Bot 2 ទទួលបានសារ៖ {update.message.text}")

def build_bot2_app(token: str) -> Application:
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app
