import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- 1. CONFIGURATION ---
TOKEN = "8685665586:AAEN8p9Hv0mzCHyC1HQQtZfC_3M9cP-ar1U"
FILE_LINK = "https://t.me/+N9dirzW9dCE3ZDY1"

CHANNELS = [
    {"id": -1002738654837, "link": "https://t.me/+eDHBE5FJ06hhNTE1"},
    {"id": -1003891879213, "link": "https://t.me/+gvHlB8CHkiYyNWU1"},
    {"id": -1003863147385, "link": "https://t.me/+068-brtYHko4ZDI1"},
    {"id": -1003855670834, "link": "https://t.me/+Q2JvbMtOFFwyNGE9"},
]

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 2. TIMER LOGIC ---
async def delete_message_job(context: ContextTypes.DEFAULT_TYPE):
    """This is the 'alarm clock' function that deletes the message"""
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.chat_id, message_id=job.data)
        logging.info(f"Deleted expired link message in chat {job.chat_id}")
    except Exception as e:
        logging.error(f"Could not delete message: {e}")

# --- 3. MEMBERSHIP CHECK ---
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

# --- 4. BOT HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    missing = await check_membership(user_id, context)

    if not missing:
        await send_expiring_link(update.message.chat_id, context)
    else:
        keyboard = [[InlineKeyboardButton("Join Channel", url=c['link'])] for c in missing]
        keyboard.append([InlineKeyboardButton("🔄 Verify & Download", callback_data="check")])
        await update.message.reply_text("👋 Join our channels to get the link:", reply_markup=InlineKeyboardMarkup(keyboard))

async def send_expiring_link(chat_id, context):
    """Sends the link and schedules it to be deleted in 5 minutes"""
    keyboard = [[InlineKeyboardButton("🚀 Download File Now", url=FILE_LINK)]]
    
    # 1. Send the message with the warning
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text="✅ **Access Granted!**\n\n⚠️ **WARNING:** This link will self-destruct in **5 minutes** for security. Download it now!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )
    
    # 2. Set the 'alarm' to delete this specific message ID in 300 seconds (5 minutes)
    context.job_queue.run_once(delete_message_job, 300, chat_id=chat_id, data=msg.message_id)

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    missing = await check_membership(user_id, context)

    if not missing:
        await query.edit_message_text("✅ Success! Checking your download link...")
        await send_expiring_link(user_id, context)
    else:
        # Re-show join buttons if still missing
        keyboard = [[InlineKeyboardButton("Join Channel", url=c['link'])] for c in missing]
        keyboard.append([InlineKeyboardButton("🔄 Try Again", callback_data="check")])
        await query.edit_message_text("⚠️ You still need to join all channels!", reply_markup=InlineKeyboardMarkup(keyboard))

if __name__ == '__main__':
    # Use .job_queue() to enable the timer feature
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_button, pattern="check"))
    
    print("Auto-Delete Bot is running...")
    app.run_polling()
