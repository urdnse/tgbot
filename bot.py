import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- 1. CONFIGURATION ---
TOKEN = "8685665586:AAEN8p9Hv0mzCHyC1HQQtZfC_3M9cP-ar1U"

# List your 4 channels here
CHANNELS = [
    {"id": -1002738654837, "link": "https://t.me/+eDHBE5FJ06hhNTE1"},
    {"id": -1003891879213, "link": "https://t.me/+gvHlB8CHkiYyNWU1"},
    {"id": -1003863147385, "link": "https://t.me/+068-brtYHko4ZDI1"},
    {"id": -1003855670834, "link": "https://t.me/+Q2JvbMtOFFwyNGE9"},
]

# --- YOUR CUSTOM MESSAGE ---
# This is the message the user sees AFTER they join all channels
FINAL_SUCCESS_MESSAGE = (
    "☠️ 𝐑𝐈𝐌𝐎𝐗 𝐅𝐅 𝐄𝐗𝐂𝐋𝐔𝐒𝐈𝐕𝐄 ☠️"

"⚙️Vᴇʀsɪᴏɴ:-  𝙾𝙱52"

📄𝐕𝐏𝐇𝐎𝐍𝐄 𝐎𝐒 𝐀𝐋𝐋 𝐅𝐈𝐋𝐄𝐒 👉 📥Dᴏᴡɴʟᴏᴀᴅ 👈 
➖➖➖➖➖➖➖➖➖➖➖➖➖
📄𝐅𝐅 𝐀𝐏𝐊 𝐇𝐄𝐑𝐄 👉 📥Dᴏᴡɴʟᴏᴀᴅ 👈
➖➖➖➖➖➖➖➖➖➖➖➖➖
📄𝐌𝐓 𝐌𝐀𝐍𝐆𝐄𝐑 𝐇𝐄𝐑𝐄 👉 📥Dᴏᴡɴʟᴏᴀᴅ 👈
➖➖➖➖➖➖➖➖➖➖➖➖➖
📄𝐕𝐏𝐇𝐎𝐍𝐄 𝐎𝐒 𝐋𝐈𝐍𝐊 𝐇𝐄𝐑𝐄 👉 📥Dᴏᴡɴʟᴏᴀᴅ 👈
➖➖➖➖➖➖➖➖➖➖➖➖➖
🎥 𝐒𝐞𝐭𝐮𝐩:- 👉 📥 WATCH 👈 
➖➖➖➖➖➖➖➖➖➖➖➖➖
✈️𝐅𝐞𝐞𝐝𝐛𝐚𝐜𝐤 👉  🩵 @urdnse 👈
➖➖➖➖➖➖➖➖➖➖➖➖➖
💸💸💸💸💸💸🗂🗂🗂🗂



              🔔  𝐖𝐀𝐑𝐍𝐈𝐍𝐆 🔔
      𝐃𝐎𝐍'𝐓 𝐔𝐒𝐄 𝐘𝐎𝐔𝐑 𝐌𝐀𝐈𝐍 𝐈𝐃
         𝐎𝐍𝐋𝐘 𝐔𝐒𝐄 𝐒𝐄𝐂𝐎𝐍𝐃 𝐈𝐃

                𝙳𝙰𝚃𝙴 --) 23/02/2026



Dear Telegram Team,
Educational IL2CPP/game dev tutorials  
• Open-source tools sharing
#research #android #security
https://telegra.ph/ᴅɪꜱᴄʟᴀɪᴍᴇʀ-11-25-17"
    "⚠️ *This message will disappear in 5 minutes.*"
)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 2. TIMER LOGIC ---
async def delete_message_job(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.chat_id, message_id=job.data)
    except Exception as e:
        logging.error(f"Message already deleted or not found: {e}")

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

# --- 4. SUCCESS HANDLER ---
async def send_approved_message(chat_id, context):
    """Sends ONLY the custom message with no links/buttons"""
    
    # Send the plain text message
    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=FINAL_SUCCESS_MESSAGE,
        parse_mode='Markdown'
    )
    
    # Set the 5-minute auto-delete (300 seconds)
    context.job_queue.run_once(delete_message_job, 300, chat_id=chat_id, data=msg.message_id)

# --- 5. MAIN BOT LOGIC ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    missing = await check_membership(user_id, context)

    if not missing:
        # User already joined, send the message directly
        await send_approved_message(user_id, context)
    else:
        # Show join buttons
        keyboard = [[InlineKeyboardButton("Join Channel", url=c['link'])] for c in missing]
        keyboard.append([InlineKeyboardButton("🔄 Verify Membership", callback_data="check")])
        await update.message.reply_text(
            "👋 Welcome! To see the hidden content, join our channels first:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    missing = await check_membership(user_id, context)

    if not missing:
        # 1. Answer the click
        await query.answer("✅ Verified!")
        # 2. Delete the 'Join' message so it looks cleaner
        await query.delete_message()
        # 3. Send your custom text-only message
        await send_approved_message(user_id, context)
    else:
        # Still missing channels
        await query.answer("❌ You are still missing some channels!", show_alert=True)

if __name__ == '__main__':
    # Initialize with Job Queue for the timer
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_button, pattern="check"))
    
    print("Text-only Bot is running...")
    app.run_polling()
