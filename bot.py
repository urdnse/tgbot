import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
TOKEN = "8685665586:AAEN8p9Hv0mzCHyC1HQQtZfC_3M9cP-ar1U"
ADMIN_ID = 7447549373  # Replace with YOUR numeric Telegram ID (Get it from @userinfobot)

# List your 4 channels
CHANNELS = [
    {"id": -1002738654837, "link": "https://t.me/+eDHBE5FJ06hhNTE1"},
    {"id": -1003891879213, "link": "https://t.me/+gvHlB8CHkiYyNWU1"},
    {"id": -1003863147385, "link": "https://t.me/+068-brtYHko4ZDI1"},
    {"id": -1003855670834, "link": "https://t.me/+Q2JvbMtOFFwyNGE9"},
]

# We will store the File ID in this variable while the bot is running
CURRENT_FILE_ID = BQACAgUAAxkBAAMCaZvfA-wehdSHmXPkHiGCYZQrEv0AAuUYAAIXktlU5V1WYH7J0lg6BA 

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

async def check_membership(user_id, context):
    not_joined = []
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel['id'], user_id=user_id)
            if member.status in ['left', 'kicked']:
                not_joined.append(channel)
        except Exception:
            not_joined.append(channel) 
    return not_joined

# --- ADMIN FEATURE: SET NEW FILE ---
async def handle_admin_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CURRENT_FILE_ID
    # Only the admin can change the file
    if update.effective_user.id == ADMIN_ID:
        if update.message.document:
            CURRENT_FILE_ID = update.message.document.file_id
        elif update.message.video:
            CURRENT_FILE_ID = update.message.video.file_id
        
        await update.message.reply_text(f"✅ **Success!** New file set.\n\nFile ID: `{CURRENT_FILE_ID}`\nAll new users will receive this file now.")
    else:
        await update.message.reply_text("❌ You are not the admin.")

# --- USER FEATURES ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CURRENT_FILE_ID:
        await update.message.reply_text("The admin hasn't set a file yet. Please wait.")
        return

    user_id = update.effective_user.id
    missing = await check_membership(user_id, context)

    if not missing:
        await update.message.reply_text("✅ Access Granted! Sending file...")
        await update.message.reply_document(document=CURRENT_FILE_ID)
    else:
        keyboard = [[InlineKeyboardButton("Join " + c['link'].split('/')[-1], url=c['link'])] for c in missing]
        keyboard.append([InlineKeyboardButton("🔄 Try Again", callback_data="check")])
        await update.message.reply_text(
            "❌ Please join our channels to get the file:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    missing = await check_membership(user_id, context)

    if not missing:
        await query.edit_message_text("✅ Verification successful! Sending file...")
        await context.bot.send_document(chat_id=user_id, document=CURRENT_FILE_ID)
    else:
        keyboard = [[InlineKeyboardButton("Join " + c['link'].split('/')[-1], url=c['link'])] for c in missing]
        keyboard.append([InlineKeyboardButton("🔄 Try Again", callback_data="check")])
        await query.edit_message_text("⚠️ Join ALL channels first!", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    
    # This handler listens for files sent by the Admin
    app.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO, handle_admin_file))
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_button, pattern="check"))
    
    print("Bot is running...")

    app.run_polling()
