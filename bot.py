import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- 1. CONFIGURATION ---
TOKEN = "8685665586:AAEN8p9Hv0mzCHyC1HQQtZfC_3M9cP-ar1U"

# Paste your Mediafire, Catbox, or Google Drive link here
FILE_LINK = "https://www.mediafire.com/your-file-link"

# List your 4 channels
CHANNELS = [
    {"id": -1002738654837, "link": "https://t.me/+eDHBE5FJ06hhNTE1"},
    {"id": -1003891879213, "link": "https://t.me/+gvHlB8CHkiYyNWU1"},
    {"id": -1003863147385, "link": "https://t.me/+068-brtYHko4ZDI1"},
    {"id": -1003855670834, "link": "https://t.me/+Q2JvbMtOFFwyNGE9"},
]
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 2. MEMBERSHIP CHECK ---
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

# --- 3. BOT LOGIC ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    missing = await check_membership(user_id, context)

    if not missing:
        # Create a "Download" button that opens the link
        keyboard = [[InlineKeyboardButton("🚀 Download File Now", url=FILE_LINK)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "✅ Access Granted! Click the button below to download your file:",
            reply_markup=reply_markup
        )
    else:
        # Create join buttons
        keyboard = [[InlineKeyboardButton("Join Channel", url=c['link'])] for c in missing]
        keyboard.append([InlineKeyboardButton("🔄 Verify & Download", callback_data="check")])
        
        await update.message.reply_text(
            "👋 Welcome! You must join our channels to get the download link:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    missing = await check_membership(user_id, context)

    if not missing:
        keyboard = [[InlineKeyboardButton("🚀 Download File Now", url=FILE_LINK)]]
        await query.edit_message_text(
            "✅ Success! You can now download the file:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        keyboard = [[InlineKeyboardButton("Join Channel", url=c['link'])] for c in missing]
        keyboard.append([InlineKeyboardButton("🔄 Try Again", callback_data="check")])
        await query.edit_message_text("⚠️ You still need to join all channels!", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_button, pattern="check"))
    
    print("Link Bot is running...")
    app.run_polling()
