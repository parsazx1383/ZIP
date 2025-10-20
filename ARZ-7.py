from telegram.helpers import escape_markdown
import requests
from datetime import datetime, timedelta 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, InlineQueryHandler, ChatMemberHandler
import nest_asyncio
import asyncio
import pytz
import logging
import re
from io import BytesIO
import sqlite3
import json
from typing import Dict, List, Any

nest_asyncio.apply()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
API_URL = "https://api.fast-creat.ir/nobitex/v2?apikey=8011183959:reYVhtb0314COpc@Api_ManagerRoBot"
BOT_TOKEN = "8230534981:AAFdbTbdoFRhGqvuEPLIDlUffhtQwvvyUOI"
ADMINS = [7472446130]

# بقیه کد شما بدون تغییر...  # ایدی ادمین چند تا هم میتونید بزارید
# برای چندتا باید اینجوری بزارید
# ADMINS = [00000, 00000, 00000]
crypto_data_cache = {}
last_update_time = None
user_sessions = {}

IRAN_TZ = pytz.timezone('Asia/Tehran')

EMOJIS = {
    "home": "🏠", "search": "🔍", "up": "📈", "down": "📉", "stable": "➡️",
    "info": "ℹ️", "money": "💵", "clock": "🕒", "error": "❌", "warning": "⚠️",
    "group": "👥", "inline": "🔎", "channel": "📢", "settings": "⚙️",
    "check": "✅", "trash": "🗑️", "users": "👥", "stats": "📊",
    "admin": "👑", "ban": "🚫", "unban": "✅", "back": "🔙", "next": "➡️",
    "previous": "⬅️", "message": "💬"
}

CUSTOM_CRYPTO = {
    "STARS": {
        "name": "استارز (Starz)",
        "irr": "0",
        "usdt": "0.015",
        "dayChange": "0"
    }
}

class GroupManager:
    def __init__(self, db_name="bot_database.db"):
        self.db_name = db_name
        self.init_group_database()
    
    def init_group_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY,
                group_title TEXT,
                group_username TEXT,
                is_active INTEGER DEFAULT 0,
                install_date TEXT,
                admin_user_id INTEGER,
                message_count INTEGER DEFAULT 0,
                last_activity TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_group(self, group_id: int, group_title: str, group_username: str, admin_user_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO groups 
            (group_id, group_title, group_username, is_active, install_date, admin_user_id, last_activity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (group_id, group_title, group_username, 0, 
              datetime.now(IRAN_TZ).isoformat(), admin_user_id, 
              datetime.now(IRAN_TZ).isoformat()))
        
        conn.commit()
        conn.close()
    
    def activate_group(self, group_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE groups SET is_active = 1, install_date = ?
            WHERE group_id = ?
        ''', (datetime.now(IRAN_TZ).isoformat(), group_id))
        
        conn.commit()
        conn.close()
    
    def deactivate_group(self, group_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE groups SET is_active = 0 WHERE group_id = ?', (group_id,))
        
        conn.commit()
        conn.close()    
    
    def get_group(self, group_id: int) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM groups WHERE group_id = ?', (group_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'group_id': result[0],
                'group_title': result[1],
                'group_username': result[2],
                'is_active': result[3],
                'install_date': result[4],
                'admin_user_id': result[5],
                'message_count': result[6],
                'last_activity': result[7]
            }
        return None
    
    def get_all_groups(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM groups ORDER BY install_date DESC')
        
        groups = []
        for row in cursor.fetchall():
            groups.append({
                'group_id': row[0],
                'group_title': row[1],
                'group_username': row[2],
                'is_active': row[3],
                'install_date': row[4],
                'admin_user_id': row[5],
                'message_count': row[6],
                'last_activity': row[7]
            })
        
        conn.close()
        return groups
    
    def update_group_activity(self, group_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE groups SET last_activity = ?, message_count = message_count + 1 
            WHERE group_id = ?
        ''', (datetime.now(IRAN_TZ).isoformat(), group_id))
        
        conn.commit()
        conn.close()

group_manager = GroupManager()

class DatabaseManager:
    def __init__(self, db_name="bot_database.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                join_date TEXT,
                message_count INTEGER DEFAULT 0,
                is_banned INTEGER DEFAULT 0,
                last_activity TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chat_id INTEGER,
                message_text TEXT,
                timestamp TEXT,
                message_type TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS required_chats (
                chat_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                chat_type TEXT NOT NULL,  -- 'channel' یا 'group'
                added_by INTEGER,
                added_at TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_user(self, user_id: int, username: str, first_name: str, last_name: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (user_id, username, first_name, last_name, join_date, last_activity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name, 
              datetime.now(IRAN_TZ).isoformat(), datetime.now(IRAN_TZ).isoformat()))
        
        conn.commit()
        conn.close()
    
    def update_user_activity(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET last_activity = ?, message_count = message_count + 1 
            WHERE user_id = ?
        ''', (datetime.now(IRAN_TZ).isoformat(), user_id))
        
        conn.commit()
        conn.close()
    
    def log_message(self, user_id: int, chat_id: int, message_text: str, message_type: str):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (user_id, chat_id, message_text, timestamp, message_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, chat_id, message_text, datetime.now(IRAN_TZ).isoformat(), message_type))
        
        conn.commit()
        conn.close()
    
    def ban_user(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET is_banned = 1 WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    def unban_user(self, user_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('UPDATE users SET is_banned = 0 WHERE user_id = ?', (user_id,))
        
        conn.commit()
        conn.close()
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.*, COUNT(m.message_id) as total_messages
            FROM users u
            LEFT JOIN messages m ON u.user_id = m.user_id
            WHERE u.user_id = ?
            GROUP BY u.user_id
        ''', (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'user_id': result[0],
                'username': result[1],
                'first_name': result[2],
                'last_name': result[3],
                'join_date': result[4],
                'message_count': result[5],
                'is_banned': result[6],
                'last_activity': result[7],
                'total_messages': result[8]
            }
        return None
    
    def get_all_users(self, limit: int = 1000) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT u.*, COUNT(m.message_id) as total_messages
            FROM users u
            LEFT JOIN messages m ON u.user_id = m.user_id
            GROUP BY u.user_id
            ORDER BY u.join_date DESC
            LIMIT ?
        ''', (limit,))
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'user_id': row[0],
                'username': row[1],
                'first_name': row[2],
                'last_name': row[3],
                'join_date': row[4],
                'message_count': row[5],
                'is_banned': row[6],
                'last_activity': row[7],
                'total_messages': row[8]
            })
        
        conn.close()
        return users
    
    def get_bot_stats(self) -> Dict[str, Any]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        week_ago = (datetime.now(IRAN_TZ) - timedelta(days=7)).isoformat()
        cursor.execute('SELECT COUNT(*) FROM users WHERE last_activity > ?', (week_ago,))
        active_users = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM messages')
        total_messages = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM users WHERE is_banned = 1')
        banned_users = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_messages': total_messages,
            'banned_users': banned_users
        }
    
    def add_required_chat(self, chat_id: int, username: str, chat_type: str, added_by: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO required_chats (chat_id, username, chat_type, added_by, added_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (chat_id, username, chat_type, added_by, datetime.now(IRAN_TZ).isoformat()))
        
        conn.commit()
        conn.close()
    
    def remove_required_chat(self, chat_id: int):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM required_chats WHERE chat_id = ?', (chat_id,))
        
        conn.commit()
        conn.close()
    
    def get_all_required_chats(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM required_chats')
        chats = []
        for row in cursor.fetchall():
            chats.append({
                'chat_id': row[0],
                'username': row[1],
                'chat_type': row[2],
                'added_by': row[3],
                'added_at': row[4]
            })
        
        conn.close()
        return chats

db = DatabaseManager()

def get_required_chats() -> List[Dict[str, Any]]:
    try:
        return db.get_all_required_chats()
    except Exception as e:
        logger.error(f"Error fetching required chats: {str(e)}")
        return []

async def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    return user_id in ADMINS

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, context):
        await update.message.reply_text(f"{EMOJIS['error']} دسترسی denied!")
        return

    if update.message.reply_to_message:
        message_to_broadcast = update.message.reply_to_message
        original_message_id = update.message.reply_to_message.message_id
    else:
        if len(context.args) == 0:
            await update.message.reply_text(
                f"{EMOJIS['info']} روش استفاده:\n\n"
                f"• ریپلای روی یک پیام و ارسال: <code>/broadcast</code>\n"
                f"• یا ارسال مستقیم: <code>/broadcast متن پیام</code>",
                parse_mode='HTML'
            )
            return
        
        message_text = ' '.join(context.args)
        message_to_broadcast = message_text
        original_message_id = None
    
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJIS['check']} بله، ارسال کن", callback_data=f"confirm_broadcast_{original_message_id}"),
            InlineKeyboardButton(f"{EMOJIS['error']} لغو", callback_data="cancel_broadcast")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{EMOJIS['warning']} <b>آیا مطمئن هستید که می‌خواهید این پیام را به همه کاربران ارسال کنید؟</b>\n\n"
        f"این عمل قابل بازگشت نیست!",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    
    if original_message_id:
        context.user_data['broadcast_message'] = message_to_broadcast
    else:
        context.user_data['broadcast_message_text'] = message_to_broadcast

async def forward_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, context):
        await update.message.reply_text(f"{EMOJIS['error']} دسترسی denied!")
        return
    
    if not update.message.reply_to_message:
        await update.message.reply_text(
            f"{EMOJIS['info']} لطفاً روی پیامی که می‌خواهید فوروارد همگانی کنید ریپلای کنید و دستور زیر را ارسال کنید:\n"
            f"<code>/forward</code>",
            parse_mode='HTML'
        )
        return
    
    message_to_forward = update.message.reply_to_message
    original_message_id = update.message.reply_to_message.message_id
    
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJIS['check']} بله، فوروارد کن", callback_data=f"confirm_forward_{original_message_id}"),
            InlineKeyboardButton(f"{EMOJIS['error']} لغو", callback_data="cancel_broadcast")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"{EMOJIS['warning']} <b>آیا مطمئن هستید که می‌خواهید این پیام را به همه کاربران فوروارد کنید؟</b>\n\n"
        f"این عمل قابل بازگشت نیست!",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    context.user_data['forward_message'] = message_to_forward

async def execute_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE, message_type: str):
    query = update.callback_query
    await query.answer()
    
    users = db.get_all_users()
    total_users = len(users)
    successful_sends = 0
    failed_sends = 0
    
    progress_message = await query.edit_message_text(
        f"{EMOJIS['clock']} <b>در حال ارسال پیام همگانی...</b>\n\n"
        f"✅ ارسال موفق: 0\n"
        f"❌ ارسال ناموفق: 0\n"
        f"📊 پیشرفت: 0/{total_users}",
        parse_mode='HTML'
    )
    
    for i, user in enumerate(users):
        try:
            if message_type == "broadcast":
                if 'broadcast_message' in context.user_data:
                    await context.bot.copy_message(
                        chat_id=user['user_id'],
                        from_chat_id=update.effective_chat.id,
                        message_id=context.user_data['broadcast_message'].message_id
                    )
                else:
                    await context.bot.send_message(
                        chat_id=user['user_id'],
                        text=context.user_data['broadcast_message_text']
                    )
            elif message_type == "forward":
                await context.bot.forward_message(
                    chat_id=user['user_id'],
                    from_chat_id=update.effective_chat.id,
                    message_id=context.user_data['forward_message'].message_id
                )
            
            successful_sends += 1
        except Exception as e:
            failed_sends += 1
            logger.error(f"Error sending to user {user['user_id']}: {e}")
        
        if i % 10 == 0 or i == total_users - 1:
            progress_percentage = (i + 1) / total_users * 100
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=progress_message.message_id,
                text=f"{EMOJIS['clock']} <b>در حال ارسال پیام همگانی...</b>\n\n"
                     f"✅ ارسال موفق: {successful_sends}\n"
                     f"❌ ارسال ناموفق: {failed_sends}\n"
                     f"📊 پیشرفت: {i+1}/{total_users} ({progress_percentage:.1f}%)",
                parse_mode='HTML'
            )
    
    result_text = f"""
{EMOJIS['check']} <b>ارسال همگانی تکمیل شد!</b>

📊 <b>نتایج:</b>
• کاربران کل: {total_users}
• ارسال موفق: {successful_sends}
• ارسال ناموفق: {failed_sends}
• درصد موفقیت: {(successful_sends/total_users*100) if total_users > 0 else 0:.1f}%

🕒 زمان اتمام: {datetime.now(IRAN_TZ).strftime('%Y-%m-%d %H:%M:%S')}
"""

    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['back']} بازگشت به پنل", callback_data="admin_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=progress_message.message_id,
        text=result_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )
    
    if 'broadcast_message' in context.user_data:
        del context.user_data['broadcast_message']
    if 'broadcast_message_text' in context.user_data:
        del context.user_data['broadcast_message_text']
    if 'forward_message' in context.user_data:
        del context.user_data['forward_message']

async def check_bot_admin_status(group_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        bot_member = await context.bot.get_chat_member(group_id, context.bot.id)
        return bot_member.status in ['administrator', 'creator']
    except Exception as e:
        logger.error(f"Error checking bot admin status: {e}")
        return False

async def handle_bot_promoted(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member:
        chat_member = update.my_chat_member
        new_status = chat_member.new_chat_member.status
        old_status = chat_member.old_chat_member.status
        
        if (new_status in ['administrator', 'creator'] and 
            old_status not in ['administrator', 'creator']):
            
            group = chat_member.chat
            user = chat_member.from_user
            
            group_manager.add_group(
                group_id=group.id,
                group_title=group.title,
                group_username=group.username,
                admin_user_id=user.id
            )
            
            welcome_text = f"""
{EMOJIS['group']} <b>سلام! ممنون که منو ادمین کردید</b>

🤖 برای <b>فعال‌سازی ربات</b> و شروع استفاده از امکانات، لطفاً دستور زیر را ارسال کنید:

<code>نصب ربات</code>

✅ پس از نصب، می‌توانید از امکانات زیر استفاده کنید:
• دریافت قیمت ارز با ارسال <code>.btc</code> یا <code>.اتریوم</code>
• محاسبه قیمت مقادیر خاص: <code>.2 btc</code> یا <code>.0.5 تتر</code>
• جستجوی ارزهای مختلف

🔧 <b>نکات مهم:</b>
• برای استفاده از نقطه (.) قبل از نام ارز استفاده کنید
• قیمت‌ها هر 5 دقیقه خودکار آپدیت می‌شوند
"""

            keyboard = [
                [InlineKeyboardButton("🎯 فعال‌سازی ربات", callback_data="install_bot")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                await context.bot.send_message(
                    chat_id=group.id,
                    text=welcome_text,
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
            except Exception as e:
                logger.error(f"Error sending welcome message: {e}")

async def handle_group_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.new_chat_members:
        for member in update.message.new_chat_members:
            if member.id == context.bot.id:
                await asyncio.sleep(2)
                
                group = update.effective_chat
                user = update.effective_user
                
                try:
                    bot_member = await context.bot.get_chat_member(group.id, context.bot.id)
                    
                    group_manager.add_group(
                        group_id=group.id,
                        group_title=group.title,
                        group_username=group.username,
                        admin_user_id=user.id
                    )
                    
                    if bot_member.status in ['administrator', 'creator']:
                        welcome_text = f"""
{EMOJIS['group']} <b>سلام! ممنون که منو به گروه اضافه کردید</b>

🤖 ربات با موفقیت ادمین شد! برای <b>فعال‌سازی</b> دستور زیر را ارسال کنید:

<code>نصب ربات</code>

✅ پس از نصب، می‌توانید از امکانات ربات استفاده کنید.
"""
                    else:
                        welcome_text = f"""
{EMOJIS['group']} <b>سلام! ممنون که منو به گروه اضافه کردید</b>

⚠️ لطفاً ربات را ادمین گروه کنید تا بتواند کار کند.

✅ پس از ادمین کردن، دستور زیر را ارسال کنید:
<code>نصب ربات</code>
"""

                    keyboard = [
                        [InlineKeyboardButton("🎯 فعال‌سازی ربات", callback_data="install_bot")]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    await update.message.reply_text(
                        welcome_text,
                        reply_markup=reply_markup,
                        parse_mode='HTML'
                    )
                    
                except Exception as e:
                    logger.error(f"Error checking bot status: {e}")
                    welcome_text = f"""
{EMOJIS['group']} <b>سلام! ممنون که منو به گروه اضافه کردید</b>

🤖 لطفاً ربات را ادمین کرده و سپس دستور زیر را ارسال کنید:
<code>نصب ربات</code>
"""
                    await update.message.reply_text(welcome_text, parse_mode='HTML')
                return

async def install_bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ['group', 'supergroup']:
        await update.message.reply_text(f"{EMOJIS['error']} این دستور فقط در گروه‌ها قابل استفاده است!")
        return
    
    group_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    try:
        member = await context.bot.get_chat_member(group_id, user_id)
        if member.status not in ['administrator', 'creator']:
            await update.message.reply_text(
                f"{EMOJIS['error']} فقط ادمین‌های گروه می‌توانند ربات را نصب کنند!"
            )
            return
    except Exception as e:
        logger.error(f"Error checking admin status: {e}")
        await update.message.reply_text(f"{EMOJIS['error']} خطا در بررسی وضعیت ادمین!")
        return
    
    is_bot_admin = await check_bot_admin_status(group_id, context)
    if not is_bot_admin:
        await update.message.reply_text(
            f"{EMOJIS['error']} لطفاً ابتدا ربات را ادمین گروه کنید سپس دوباره تلاش کنید!"
        )
        return
    
    group_manager.activate_group(group_id)
    
    success_text = f"""
{EMOJIS['check']} <b>ربات با موفقیت فعال شد!</b>

✅ اکنون می‌توانید از امکانات ربات استفاده کنید:

<code>.btc</code> - قیمت بیت‌کوین
<code>.اتریوم</code> - قیمت اتریوم  
<code>.2 btc</code> - قیمت 2 بیت‌کوین
<code>.0.5 تتر</code> - قیمت 0.5 تتر

📚 <b>راهنما:</b>
• همیشه از نقطه (.) قبل از دستور استفاده کنید
• می‌توانید از نام فارسی یا انگلیسی ارزها استفاده کنید
• برای محاسبه قیمت مقادیر خاص، عدد و نام ارز را بنویسید

💬 برای راهنمایی بیشتر به پیوی ربات مراجعه کنید: @{context.bot.username}
"""
    
    await update.message.reply_text(success_text, parse_mode='HTML')

async def install_bot_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.message.chat.type not in ['group', 'supergroup']:
        await query.edit_message_text(f"{EMOJIS['error']} این دکمه فقط در گروه‌ها کار می‌کند!")
        return
    
    update.message = query.message
    await install_bot_command(update, context)

async def check_group_activation(update: Update, context: ContextTypes.DEFAULT_TYPE, next_handler):
    if update.effective_chat.type in ['group', 'supergroup']:
        group_id = update.effective_chat.id
        group_info = group_manager.get_group(group_id)
        
        if not group_info or not group_info['is_active']:
            if update.message and update.message.text and 'نصب' in update.message.text:
                await install_bot_command(update, context)
            else:
                if update.message:
                    await update.message.reply_text(
                        f"{EMOJIS['warning']} <b>ربات در این گروه فعال نیست!</b>\n\n"
                        f"لطفاً برای فعال‌سازی دستور زیر را ارسال کنید:\n"
                        f"<code>نصب ربات</code>",
                        parse_mode='HTML'
                    )
            return
    
    await next_handler(update, context)

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, context):
        if hasattr(update, 'message') and update.message:
            await update.message.reply_text(f"{EMOJIS['error']} دسترسی denied!")
        return
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['stats']} آمار ربات", callback_data="admin_stats")],
        [InlineKeyboardButton(f"{EMOJIS['users']} مدیریت کاربران", callback_data="admin_users_1")],
        [InlineKeyboardButton(f"{EMOJIS['group']} مدیریت گروه‌ها", callback_data="admin_groups_1")],
        [InlineKeyboardButton(f"{EMOJIS['channel']} مدیریت چت‌های اجباری", callback_data="admin_chats")], 
        [InlineKeyboardButton(f"{EMOJIS['message']} پیام همگانی", callback_data="broadcast_options")],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = f"{EMOJIS['admin']} <b>پنل مدیریت ادمین</b>\n\nلطفاً یکی از گزینه‌ها را انتخاب کنید:"
    
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    elif hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.edit_message_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

async def broadcast_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['message']} ارسال پیام همگانی", callback_data="broadcast_help")],
        [InlineKeyboardButton(f"{EMOJIS['message']} فوروارد همگانی", callback_data="forward_help")],
        [InlineKeyboardButton(f"{EMOJIS['back']} بازگشت", callback_data="admin_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{EMOJIS['message']} <b>گزینه‌های پیام همگانی</b>\n\n"
        f"لطفاً یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def show_groups_list(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 1):
    query = update.callback_query
    if query:
        await query.answer()
    
    groups = group_manager.get_all_groups()
    groups_per_page = 8
    total_pages = (len(groups) + groups_per_page - 1) // groups_per_page
    
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    start_idx = (page - 1) * groups_per_page
    end_idx = start_idx + groups_per_page
    page_groups = groups[start_idx:end_idx]
    
    message_text = f"{EMOJIS['group']} <b>لیست گروه‌ها (صفحه {page} از {total_pages})</b>\n\n"
    
    if not page_groups:
        message_text += "هیچ گروهی یافت نشد."
    else:
        for i, group in enumerate(page_groups, start=1):
            group_number = start_idx + i
            status = "✅" if group['is_active'] else "🚫"
            username = f"@{group['group_username']}" if group['group_username'] else "بدون یوزرنیم"
            message_text += f"{group_number}. {status} {group['group_title']} ({username})\n"
            message_text += f"   📊 پیام‌ها: {group['message_count']} | 🆔: {group['group_id']}\n\n"
    
    keyboard = []
    for i, group in enumerate(page_groups):
        group_number = start_idx + i + 1
        btn_text = f"{group_number}. {group['group_title'][:12]}..."
        keyboard.append([InlineKeyboardButton(
            f"{btn_text} {'✅' if group['is_active'] else '🚫'}",
            callback_data=f"group_detail_{group['group_id']}"
        )])
    
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(
            f"{EMOJIS['previous']} قبلی", 
            callback_data=f"admin_groups_{page-1}"
        ))
    
    pagination_buttons.append(InlineKeyboardButton(
        f"{EMOJIS['back']} بازگشت", 
        callback_data="admin_back"
    ))
    
    if page < total_pages:
        pagination_buttons.append(InlineKeyboardButton(
            f"{EMOJIS['next']} بعدی", 
            callback_data=f"admin_groups_{page+1}"
        ))
    
    if pagination_buttons:
        keyboard.append(pagination_buttons)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

async def show_bot_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """نمایش آمار ربات"""
    query = update.callback_query
    await query.answer()
    
    stats = db.get_bot_stats()
    
    message_text = f"""
{EMOJIS['stats']} <b>آمار کلی ربات:</b>

👥 <b>تعداد کاربران:</b>
• کل کاربران: {stats['total_users']}
• کاربران فعال: {stats['active_users']}
• کاربران بن شده: {stats['banned_users']}

💬 <b>آمار پیام‌ها:</b>
• کل پیام‌ها: {stats['total_messages']}

🕒 <b>وضعیت سیستم:</b>
• ارزهای ذخیره شده: {len(crypto_data_cache)}
• آخرین بروزرسانی: {last_update_time.strftime('%H:%M:%S') if last_update_time else 'نامعلوم'}
"""
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['back']} بازگشت", callback_data="admin_back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def show_users_list(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 1):
    query = update.callback_query
    if query:
        await query.answer()
    
    users = db.get_all_users()
    users_per_page = 10
    total_pages = (len(users) + users_per_page - 1) // users_per_page
    
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    start_idx = (page - 1) * users_per_page
    end_idx = start_idx + users_per_page
    page_users = users[start_idx:end_idx]
    
    message_text = f"{EMOJIS['users']} <b>لیست کاربران (صفحه {page} از {total_pages})</b>\n\n"
    
    if not page_users:
        message_text += "هیچ کاربری یافت نشد."
    else:
        for i, user in enumerate(page_users, start=1):
            user_number = start_idx + i
            status = "🚫" if user['is_banned'] else "✅"
            username = f"@{user['username']}" if user['username'] else "بدون یوزرنیم"
            message_text += f"{user_number}. {status} {user['first_name']} {user['last_name'] or ''} ({username})\n"
            message_text += f"   📊 پیام‌ها: {user['total_messages']} | 🆔: {user['user_id']}\n\n"
    
    keyboard = []
    for i, user in enumerate(page_users):
        user_number = start_idx + i + 1
        btn_text = f"{user_number}. {user['first_name']}"
        if len(btn_text) > 15:
            btn_text = btn_text[:12] + "..."
        keyboard.append([InlineKeyboardButton(
            f"{btn_text} {'🚫' if user['is_banned'] else '✅'}",
            callback_data=f"user_detail_{user['user_id']}"
        )])
    
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(
            f"{EMOJIS['previous']} قبلی", 
            callback_data=f"admin_users_{page-1}"
        ))
    
    pagination_buttons.append(InlineKeyboardButton(
        f"{EMOJIS['back']} بازگشت", 
        callback_data="admin_back"
    ))
    
    if page < total_pages:
        pagination_buttons.append(InlineKeyboardButton(
            f"{EMOJIS['next']} بعدی", 
            callback_data=f"admin_users_{page+1}"
        ))
    
    if pagination_buttons:
        keyboard.append(pagination_buttons)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query:
        await query.edit_message_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    else:
        await update.message.reply_text(
            message_text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )

async def show_user_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int):
    query = update.callback_query
    await query.answer()
    
    user_stats = db.get_user_stats(user_id)
    
    if not user_stats:
        await query.edit_message_text(f"{EMOJIS['error']} کاربر یافت نشد!")
        return
    
    join_date = datetime.fromisoformat(user_stats['join_date']).strftime('%Y-%m-%d %H:%M:%S')
    last_activity = datetime.fromisoformat(user_stats['last_activity']).strftime('%Y-%m-%d %H:%M:%S') if user_stats['last_activity'] else 'نامعلوم'
    
    message_text = f"""
{EMOJIS['info']} <b>جزئیات کاربر</b>

👤 <b>اطلاعات کاربر:</b>
• نام: {user_stats['first_name']} {user_stats['last_name'] or ''}
• یوزرنیم: @{user_stats['username'] or 'بدون یوزرنیم'}
• آیدی: <code>{user_stats['user_id']}</code>

📊 <b>آمار فعالیت:</b>
• تاریخ عضویت: {join_date}
• آخرین فعالیت: {last_activity}
• تعداد پیام‌ها: {user_stats['total_messages']}

🔒 <b>وضعیت:</b> {'🚫 بن شده' if user_stats['is_banned'] else '✅ فعال'}
"""
    keyboard = []
    if user_stats['is_banned']:
        keyboard.append([InlineKeyboardButton(
            f"{EMOJIS['unban']} آنبن کردن کاربر", 
            callback_data=f"user_unban_{user_id}"
        )])
    else:
        keyboard.append([InlineKeyboardButton(
            f"{EMOJIS['ban']} بن کردن کاربر", 
            callback_data=f"user_ban_{user_id}"
        )])
    
    keyboard.append([
        InlineKeyboardButton(f"{EMOJIS['back']} بازگشت", callback_data=f"admin_users_1"),
        InlineKeyboardButton(f"{EMOJIS['users']} لیست کاربران", callback_data="admin_users_1")
    ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_admin(update, context):
        await update.message.reply_text(f"{EMOJIS['error']} شما دسترسی لازم برای این کار را ندارید.")
        return
    
    try:
        bot_info = await context.bot.get_me()
        stats = db.get_bot_stats()
        active_percentage = (stats['active_users'] / stats['total_users'] * 100) if stats['total_users'] > 0 else 0
        avg_messages_per_user = (stats['total_messages'] / stats['total_users']) if stats['total_users'] > 0 else 0
        
        message_text = f"""
{EMOJIS['stats']} <b>آمار پیشرفته ربات</b>

🤖 <b>اطلاعات ربات:</b>
• نام: {bot_info.first_name}
• یوزرنیم: @{bot_info.username}
• آیدی: <code>{bot_info.id}</code>

👥 <b>آمار کاربران:</b>
• کل کاربران: <code>{stats['total_users']:,}</code>
• کاربران فعال (7 روز): <code>{stats['active_users']:,}</code>
• درصد فعال: <code>{active_percentage:.1f}%</code>
• کاربران بن شده: <code>{stats['banned_users']:,}</code>

💬 <b>آمار پیام‌ها:</b>
• کل پیام‌ها: <code>{stats['total_messages']:,}</code>
• میانگین پیام per کاربر: <code>{avg_messages_per_user:.1f}</code>

📊 <b>وضعیت سیستم:</b>
• ارزهای ذخیره شده: <code>{len(crypto_data_cache)}</code>
• آخرین بروزرسانی: {last_update_time.strftime('%Y-%m-%d %H:%M:%S') if last_update_time else 'نامعلوم'}

🕒 <b>زمان سیستم:</b>
• زمان فعلی: {datetime.now(IRAN_TZ).strftime('%Y-%m-%d %H:%M:%S')}
• منطقه زمانی: Asia/Tehran
"""
        if update.message:
            await update.message.reply_text(message_text, parse_mode='HTML')
        elif update.callback_query:
            await update.callback_query.edit_message_text(message_text, parse_mode='HTML')
            
    except Exception as e:
        error_msg = f"{EMOJIS['error']} خطا در دریافت آمار: {str(e)}"
        if update.message:
            await update.message.reply_text(error_msg)
        elif update.callback_query:
            await update.callback_query.edit_message_text(error_msg)

async def manage_user_ban(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: int, action: str):
    query = update.callback_query
    await query.answer()
    
    if action == "ban":
        db.ban_user(user_id)
        action_text = "بن شد"
        emoji = EMOJIS['ban']
        callback_data = "admin_users_1"
    else:
        db.unban_user(user_id)
        action_text = "آنبن شد"
        emoji = EMOJIS['unban']
        callback_data = "admin_users_1"
    
    user_stats = db.get_user_stats(user_id)
    
    keyboard = [
        [InlineKeyboardButton(f"{EMOJIS['back']} بازگشت به لیست کاربران", callback_data=callback_data)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{emoji} <b>کاربر با موفقیت {action_text}</b>\n\n"
        f"👤 کاربر: {user_stats['first_name']} {user_stats['last_name'] or ''}\n"
        f"🆔 آیدی: <code>{user_id}</code>",
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def broadcast_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        f"{EMOJIS['info']} <b>راهنمای ارسال پیام همگانی</b>\n\n"
        f"برای ارسال پیام به همه کاربران:\n"
        f"1. پیام مورد نظر را بنویسید یا روی یک پیام ریپلای کنید\n"
        f"2. دستور <code>/broadcast</code> را وارد کنید\n"
        f"3. تأیید کنید تا پیام برای همه ارسال شود\n\n"
        f"{EMOJIS['back']} برای بازگشت به پنل، دکمه زیر را فشار دهید:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{EMOJIS['back']} بازگشت", callback_data="admin_back")]
        ]),
        parse_mode='HTML'
    )

async def forward_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        f"{EMOJIS['info']} <b>راهنمای فوروارد همگانی</b>\n\n"
        f"برای فوروارد پیام به همه کاربران:\n"
        f"1. روی پیام مورد نظر ریپلای کنید\n"
        f"2. دستور <code>/forward</code> را وارد کنید\n"
        f"3. تأیید کنید تا پیام برای همه فوروارد شود\n\n"
        f"{EMOJIS['back']} برای بازگشت به پنل، دکمه زیر را فشار دهید:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{EMOJIS['back']} بازگشت", callback_data="admin_back")]
        ]),
        parse_mode='HTML'
    )

async def admin_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    try:
        if data == "admin_stats":
            await show_bot_stats(update, context)
        elif data == "admin_back":
            await admin_panel(update, context)
        elif data.startswith("admin_users_"):
            page = int(data.split("_")[2])
            await show_users_list(update, context, page)
        elif data.startswith("admin_groups_"):
            page = int(data.split("_")[2])
            await show_groups_list(update, context, page)
        elif data.startswith("admin_chats"):
            page = int(data.split("_")[2]) if len(data.split("_")) > 2 else 1
            await show_required_chats_list(update, context, page)
        elif data.startswith("user_detail_"):
            user_id = int(data.split("_")[2])
            await show_user_detail(update, context, user_id)
        elif data.startswith("confirm_broadcast_"):
            await execute_broadcast(update, context, "broadcast")
        elif data.startswith("confirm_forward_"):
            await execute_broadcast(update, context, "forward")
        elif data == "cancel_broadcast":
            await query.edit_message_text(
                f"{EMOJIS['info']} ارسال همگانی لغو شد.",
                parse_mode='HTML'
            )
        elif data == "broadcast_help":
            await broadcast_help(update, context)
        elif data == "forward_help":
            await forward_help(update, context)
        elif data.startswith("user_ban_"):
            user_id = int(data.split("_")[2])
            await manage_user_ban(update, context, user_id, "ban")
        elif data.startswith("user_unban_"):
            user_id = int(data.split("_")[2])
            await manage_user_ban(update, context, user_id, "unban")
        elif data == "add_chat":
            await prompt_add_chat(update, context)
        elif data.startswith("remove_chat_"):
            chat_id = int(data.split("_")[2])
            await remove_chat(update, context, chat_id)
        elif data == "admin_panel":
            await admin_panel(update, context)
        elif data == "install_bot":
            await install_bot_button(update, context)
    except Exception as e:
        logger.error(f"Error in admin_button_handler: {e}")
        await query.edit_message_text(
            f"{EMOJIS['error']} خطایی رخ داد! لطفاً دوباره تلاش کنید.",
            parse_mode='HTML'
        )

async def check_user_membership(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        chats = get_required_chats()
        if not chats: 
            return True
        
        for chat in chats:
            try:
                chat_member = await context.bot.get_chat_member(chat["chat_id"], user_id)
                if chat_member.status in ['left', 'kicked']:
                    return False
            except Exception as e:
                logger.error(f"Error checking membership for chat {chat['chat_id']}: {e}")
                continue
                
        return True
    except Exception as e:
        logger.error(f"Error checking membership for user {user_id}: {e}")
        return False

def create_join_keyboard():
    chats = get_required_chats()
    if not chats:
        return None
    
    buttons = []
    for chat in chats:
        buttons.append([InlineKeyboardButton(f"عضویت در {chat['username']}", url=f"https://t.me/{chat['username'][1:]}")])
    
    buttons.append([InlineKeyboardButton("✅ بررسی عضویت", callback_data="check_membership")])
    
    return InlineKeyboardMarkup(buttons)

async def show_required_chats_list(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 1):
    query = update.callback_query
    await query.answer()
    
    chats = db.get_all_required_chats()
    chats_per_page = 8
    total_pages = (len(chats) + chats_per_page - 1) // chats_per_page
    
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages
    
    start_idx = (page - 1) * chats_per_page
    end_idx = start_idx + chats_per_page
    page_chats = chats[start_idx:end_idx]
    
    message_text = f"{EMOJIS['channel']} <b>لیست چت‌های جوین اجباری (صفحه {page} از {total_pages})</b>\n\n"
    
    if not page_chats:
        message_text += "هیچ چت اجباری یافت نشد."
    else:
        for i, chat in enumerate(page_chats, start=1):
            chat_number = start_idx + i
            chat_type = "کانال" if chat['chat_type'] == 'channel' else "گروه"
            message_text += f"{chat_number}. {chat['username']} ({chat_type})\n"
            message_text += f"   🆔: {chat['chat_id']}\n"
            message_text += f"   🕒 اضافه شده در: {datetime.fromisoformat(chat['added_at']).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    keyboard = []
    for i, chat in enumerate(page_chats):
        chat_number = start_idx + i + 1
        chat_type = "کانال" if chat['chat_type'] == 'channel' else "گروه"
        btn_text = f"{chat_number}. {chat['username']} ({chat_type})"
        if len(btn_text) > 15:
            btn_text = btn_text[:12] + "..."
        keyboard.append([InlineKeyboardButton(
            btn_text,
            callback_data=f"remove_chat_{chat['chat_id']}"
        )])
    
    keyboard.append([InlineKeyboardButton(f"{EMOJIS['channel']} اضافه کردن چت", callback_data="add_chat")])
    
    pagination_buttons = []
    if page > 1:
        pagination_buttons.append(InlineKeyboardButton(
            f"{EMOJIS['previous']} قبلی", 
            callback_data=f"admin_chats_{page-1}"
        ))
    
    pagination_buttons.append(InlineKeyboardButton(
        f"{EMOJIS['back']} بازگشت", 
        callback_data="admin_back"
    ))
    
    if page < total_pages:
        pagination_buttons.append(InlineKeyboardButton(
            f"{EMOJIS['next']} بعدی", 
            callback_data=f"admin_chats_{page+1}"
        ))
    
    if pagination_buttons:
        keyboard.append(pagination_buttons)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def prompt_add_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        f"{EMOJIS['channel']} <b>اضافه کردن چت جدید</b>\n\n"
        f"لطفاً اطلاعات چت (کانال یا گروه) را در قالب زیر وارد کنید:\n"
        f"<code>@ChatUsername ChatID Type</code>\n\n"
        f"مثال برای کانال: <code>@MyChannel -1001234567890 channel</code>\n"
        f"مثال برای گروه: <code>@MyGroup -1009876543210 group</code>\n\n"
        f"{EMOJIS['info']} برای دریافت آیدی چت، ربات را به کانال یا گروه اضافه کنید و دستور /id را اجرا کنید.",
        parse_mode='HTML'
    )
    context.user_data['awaiting_chat_info'] = True

async def remove_chat(update: Update, context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    query = update.callback_query
    await query.answer()
    
    chat = next((c for c in db.get_all_required_chats() if c['chat_id'] == chat_id), None)
    
    if not chat:
        await query.edit_message_text(
            f"{EMOJIS['error']} چت یافت نشد!",
            parse_mode='HTML'
        )
        return
    
    db.remove_required_chat(chat_id)
    
    chat_type = "کانال" if chat['chat_type'] == 'channel' else "گروه"
    await query.edit_message_text(
        f"{EMOJIS['check']} چت {chat['username']} ({chat_type}) با موفقیت حذف شد!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{EMOJIS['back']} بازگشت", callback_data="admin_chats")]
        ]),
        parse_mode='HTML'
    )

async def handle_chat_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Processing chat info: {update.message.text} by user {update.effective_user.id}")
    
    if not await is_user_admin(update, context):
        logger.warning(f"User {update.effective_user.id} is not admin")
        await update.message.reply_text(
            f"{EMOJIS['error']} شما دسترسی لازم برای این کار را ندارید.",
            parse_mode='HTML'
        )
        return
    
    text = update.message.text
    match = re.match(r'^@(\w+)\s+(-?\d+)\s+(channel|group)$', text)
    
    if not match:
        logger.error(f"Invalid format: {text}")
        await update.message.reply_text(
            f"{EMOJIS['error']} فرمت اشتباه است. مثال:\n@ChannelUsername -1001234567890 channel",
            parse_mode='HTML'
        )
        return
    
    username, chat_id, chat_type = match.groups()
    logger.info(f"Parsed: username=@{username}, chat_id={chat_id}, chat_type={chat_type}")
    
    try:
        chat = await context.bot.get_chat(chat_id)
        if not chat:
            logger.error(f"Chat not found for chat_id={chat_id}")
            await update.message.reply_text(
                f"{EMOJIS['error']} چت با آیدی {chat_id} یافت نشد یا ربات دسترسی ندارد.",
                parse_mode='HTML'
            )
            return
        
        if chat.id != int(chat_id):
            logger.error(f"Chat ID mismatch: expected {chat_id}, got {chat.id}")
            await update.message.reply_text(
                f"{EMOJIS['error']} آیدی چت اشتباه است.",
                parse_mode='HTML'
            )
            return
        
        if chat_type == 'channel' and chat.type != 'channel':
            logger.error(f"Chat type mismatch: expected channel, got {chat.type}")
            await update.message.reply_text(
                f"{EMOJIS['error']} چت با آیدی {chat_id} یک کانال نیست.",
                parse_mode='HTML'
            )
            return
        
        if chat_type == 'group' and chat.type not in ['group', 'supergroup']:
            logger.error(f"Chat type mismatch: expected group/supergroup, got {chat.type}")
            await update.message.reply_text(
                f"{EMOJIS['error']} چت با آیدی {chat_id} یک گروه نیست.",
                parse_mode='HTML'
            )
            return
        
    except Exception as e:
        logger.error(f"Error checking chat {chat_id}: {str(e)}")
        await update.message.reply_text(
            f"{EMOJIS['error']} خطا در بررسی چت: {str(e)}",
            parse_mode='HTML'
        )
        return
    
    try:
        db.add_required_chat(int(chat_id), f"@{username}", chat_type, update.effective_user.id)
        logger.info(f"Chat added: @{username} ({chat_type}) by user {update.effective_user.id}")
        await update.message.reply_text(
            f"{EMOJIS['check']} چت @{username} ({chat_type}) با موفقیت به لیست جوین اجباری اضافه شد.",
            parse_mode='HTML'
        )
    except Exception as e:
        logger.error(f"Error adding chat to database: {str(e)}")
        await update.message.reply_text(
            f"{EMOJIS['error']} خطا در افزودن چت به دیتابیس: {str(e)}",
            parse_mode='HTML'
        )

async def check_membership_wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, next_handler):
    logger.info(f"Checking membership for user {update.effective_user.id}")
    user_id = update.effective_user.id
    user_stats = db.get_user_stats(user_id)
    
    if user_stats and user_stats['is_banned']:
        logger.warning(f"User {user_id} is banned")
        if update.message:
            await update.message.reply_text(
                f"{EMOJIS['error']} <b>شما از استفاده از این ربات محروم شده‌اید.</b>\n\n"
                f"در صورت اعتراض به این تصمیم، با پشتیبانی تماس بگیرید.",
                parse_mode='HTML'
            )
        elif update.callback_query:
            await update.callback_query.message.reply_text(
                f"{EMOJIS['error']} <b>شما از استفاده از این ربات محروم شده‌اید.</b>",
                parse_mode='HTML'
            )
        return
    
    if await is_user_admin(update, context):
        logger.info(f"User {user_id} is admin, skipping membership check")
        await next_handler(update, context)
        return
    
    if not await check_user_membership(user_id, context):
        logger.info(f"User {user_id} is not a member of required chats")
        message_text = f"""
{EMOJIS['warning']} <b>برای استفاده از ربات باید در چت‌های زیر عضو شوید:</b>

"""
        chats = get_required_chats() 
        if not chats:
            logger.warning("No required chats found in database")
            message_text += "هیچ چت اجباری تنظیم نشده است.\n"
        else:
            for chat in chats:
                chat_type = "کانال" if chat['chat_type'] == 'channel' else "گروه"
                message_text += f"• {chat['username']} ({chat_type})\n"
        
        message_text += f"\n{EMOJIS['info']} پس از عضویت، روی دکمه «بررسی عضویت» کلیک کنید."
        
        if update.message:
            await update.message.reply_text(
                message_text,
                reply_markup=create_join_keyboard(),
                parse_mode='HTML'
            )
        elif update.callback_query:
            await update.callback_query.message.reply_text(
                message_text,
                reply_markup=create_join_keyboard(),
                parse_mode='HTML'
            )
        return
    
    logger.info(f"User {user_id} passed membership check")
    await next_handler(update, context)

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if await check_user_membership(user_id, context):
        await query.message.edit_text(
            f"{EMOJIS['check']} <b>تبریک! شما در کانال‌ها عضو هستید. اکنون می‌توانید از ربات استفاده کنید.</b>",
            parse_mode='HTML'
        )
    else:
        await query.message.edit_text(
            f"{EMOJIS['warning']} <b>شما هنوز در برخی کانال‌ها عضو نشده‌اید. لطفاً در تمام کانال‌ها عضو شوید و سپس بررسی کنید.</b>",
            reply_markup=create_join_keyboard(),
            parse_mode='HTML'
        )

async def get_chart_image(symbol):
    try:
        chart_symbol = symbol
        url = f"https://api.fast-creat.ir/chart?apikey=8011183959:elxwqkXMZABd0P9@Api_ManagerRoBot&symbol={chart_symbol}&id=@arzdigigitalbot&type=1"
        
        response = requests.get(url, timeout=50)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') and data.get('status') == 'successfully':
                return data['result']['image']
        
        return None
    except Exception as e:
        logger.error(f"Error fetching chart for {symbol}: {e}")
        return None

async def download_chart_image(chart_url):
    try:
        response = requests.get(chart_url, timeout=50)
        if response.status_code == 200:
            return BytesIO(response.content)
        return None
    except Exception as e:
        logger.error(f"Error downloading chart image: {e}")
        return None

async def create_initial_price_message(crypto, symbol):
    if crypto['irr'] == "0" or crypto['usdt'] == "0":
        return None

    if crypto['dayChange'] and float(crypto['dayChange']) < 0:
        change_icon = EMOJIS['down']
    elif crypto['dayChange'] and float(crypto['dayChange']) > 0:
        change_icon = EMOJIS['up']
    else:
        change_icon = EMOJIS['stable']

    message = f"🏠 <b>{crypto['name']}</b> ({symbol})\n\n"
    message += f"💰 قیمت تومان: <code>{format_price(crypto['irr'])}</code> تومان\n"
    message += f"💵 قیمت دلار: <code>{format_price(crypto['usdt'], is_usdt=True)}</code> USDT\n"
    if crypto['dayChange']:
        message += f"{change_icon} تغییر 24h: <code>{float(crypto['dayChange']):+.2f}%</code>\n"
    message += f"\n🕒 در حال دریافت چارت..."
    
    return message

async def create_final_price_message(crypto, symbol, chart_available=True):
    if crypto['irr'] == "0" or crypto['usdt'] == "0":
        return None

    if crypto['dayChange'] and float(crypto['dayChange']) < 0:
        change_icon = EMOJIS['down']
    elif crypto['dayChange'] and float(crypto['dayChange']) > 0:
        change_icon = EMOJIS['up']
    else:
        change_icon = EMOJIS['stable']

    message = f"🏠 <b>{crypto['name']}</b> ({symbol})\n\n"
    message += f"💰 قیمت تومان: <code>{format_price(crypto['irr'])}</code> تومان\n"
    message += f"💵 قیمت دلار: <code>{format_price(crypto['usdt'], is_usdt=True)}</code> USDT\n"
    if crypto['dayChange']:
        message += f"{change_icon} تغییر 24h: <code>{float(crypto['dayChange']):+.2f}%</code>\n"
    
    if chart_available:
        message += f"\n📊 چارت {symbol} به پیام اضافه شد"
    else:
        message += f"\n{EMOJIS['warning']} چارت {symbol} در دسترس نیست"
    
    message += f"\n🕒 آخرین بروزرسانی: {datetime.now(IRAN_TZ).strftime('%H:%M:%S')}"
    
    return message

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ['group', 'supergroup']:
        await update.message.reply_text(
            f"{EMOJIS['info']} برای استفاده از ربات در گروه، از نقطه قبل از نام ارزها استفاده کنید.\n"
            f"مثال: `.btc` یا `.2 اتریوم`\n\n"
            f"برای راهنمایی کامل به پیوی ربات مراجعه کنید: @{context.bot.username}",
            parse_mode='HTML'
        )
        return

    user = update.effective_user
    user_stats = db.get_user_stats(user.id)
    
    if user_stats and user_stats['is_banned']:
        await update.message.reply_text(
            f"{EMOJIS['error']} <b>شما از استفاده از این ربات محروم شده‌اید.</b>\n\n"
            f"در صورت اعتراض به این تصمیم، با پشتیبانی تماس بگیرید.",
            parse_mode='HTML'
        )
        return
    
    db.add_user(
        user.id, 
        user.username, 
        user.first_name, 
        user.last_name or ""
    )
    db.log_message(user.id, update.effective_chat.id, "/start", "command")
    
    keyboard = [
        [
            InlineKeyboardButton(f"{EMOJIS['group']} افزودن به گروه", url=f"https://t.me/{context.bot.username}?startgroup=true"),
            InlineKeyboardButton(f"{EMOJIS['inline']} استفاده در چت", switch_inline_query="")
        ]
    ]
    
    if await is_user_admin(update, context):
        keyboard.append([InlineKeyboardButton(f"{EMOJIS['admin']} پنل مدیریت", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = f"""
{EMOJIS['home']} <b>به ربات قیمت ارزهای دیجیتال خوش آمدید!</b>

{user.first_name} عزیز، این ربات به شما امکان می‌دهد:
• مشاهده قیمت لحظه‌ای ارزهای دیجیتال
• جستجوی ارزهای خاص
• <b>محاسبه قیمت مقادیر خاص (مثلاً 2 بیت‌کوین یا 0.5 اتریوم)</b>

✨ <b>راهنمای استفاده اینلاین:</b>
فقط کافی است در هر چتی @{context.bot.username} را تایپ کرده و نام ارز مورد نظر را وارد کنید.

✨ <b>راهنمای محاسبه مقدار خاص:</b>
- در پیوی: <code>2 btc</code> یا <code>0.5 اتریوم</code>
- در گروه: <code>.2 btc</code> یا <code>.0.5 تتر</code>

(قیمت‌ها هر ۵ دقیقه خودکار بروزرسانی می‌شوند)
برای استفاده ربات در گروه کافیه رباتو ادمین کنید و برای گرفتن قیمت کافیه یه نقطه . پشت اسم ارز بزارید
"""

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='HTML'
    )

async def calculate_irr_price(usdt_price):
    try:
        if crypto_data_cache and 'USDT' in crypto_data_cache:
            usdt_to_irr = float(crypto_data_cache['USDT']['irr'])
            irr_price = float(usdt_price) * usdt_to_irr
            return str(irr_price)
        return "0"
    except Exception as e:
        logger.error(f"Error calculating IRR price: {e}")
        return "0"

async def get_crypto_data():
    try:
        response = requests.get(API_URL, timeout=10)
        data = response.json()
        if data.get('ok') and data.get('code') == 200:
            result = data['result']
            result.update(CUSTOM_CRYPTO)
            return result
        return None
    except Exception as e:
        logger.error(f"Error fetching data: {e}")
        return None

async def update_crypto_cache(context: ContextTypes.DEFAULT_TYPE = None):
    global crypto_data_cache, last_update_time
    data = await get_crypto_data()
    if data:
        crypto_data_cache = data
        
        if 'STARS' in crypto_data_cache:
            stars_usdt_price = crypto_data_cache['STARS']['usdt']
            stars_irr_price = await calculate_irr_price(stars_usdt_price)
            crypto_data_cache['STARS']['irr'] = stars_irr_price
        
        last_update_time = datetime.now(IRAN_TZ)
        return True
    return False

def format_price(price, is_usdt=False):
    try:
        price_num = float(price)
        if price_num == 0:
            return "0"
        elif price_num >= 1000:
            return f"{price_num:,.0f}"
        elif price_num >= 1:
            return f"{price_num:,.2f}"
        else:
            formatted = f"{price_num:.8f}"
            return formatted.rstrip('0').rstrip('.') if '.' in formatted else formatted
    except:
        return price

def create_amount_message(crypto, symbol, amount):
    if crypto['irr'] == "0" or crypto['usdt'] == "0":
        return None

    try:
        amount_num = float(amount)
        irr_price = float(crypto['irr']) * amount_num
        usdt_price = float(crypto['usdt']) * amount_num

        if crypto['dayChange'] and float(crypto['dayChange']) < 0:
            change_icon = EMOJIS['down']
        elif crypto['dayChange'] and float(crypto['dayChange']) > 0:
            change_icon = EMOJIS['up']
        else:
            change_icon = EMOJIS['stable']

        message = f"🧮 <b>محاسبه قیمت {amount} {crypto['name']}</b> ({symbol})\n\n"
        message += f"💰 قیمت تومان: <code>{format_price(irr_price)}</code> تومان\n"
        message += f"💵 قیمت دلار: <code>{format_price(usdt_price, is_usdt=True)}</code> USDT\n"
        message += f"📊 قیمت واحد: <code>{format_price(crypto['irr'])}</code> تومان\n"
        if crypto['dayChange']:
            message += f"{change_icon} تغییر 24h: <code>{float(crypto['dayChange']):+.2f}%</code>\n"
        message += f"\n🕒 آخرین بروزرسانی: {datetime.now(IRAN_TZ).strftime('%H:%M:%S')}"
        
        return message
    except ValueError:
        return None

def parse_amount_message(text):
    text = text.lower().replace('هزار تومن', '1000 تومان').replace('تومن', 'تومن')
    patterns_conversion = [
        r'^(?:تبدیل\s+)?(\d+\.?\d*)\s+([^\d\s]+)\s+(?:به\s+)?([^\d\s]+)$', 
        r'^(?:تبدیل\s+)?(\d+\.?\d*)\s+([\w\s]+)\s+(?:به\s+)?([\w\s]+)$',  
        r'^(?:تبدیل\s+)?([^\d\s]+)\s+(?:به\s+)?([^\d\s]+)$',       
        r'^(?:تبدیل\s+)?([\w\s]+)\s+(?:به\s+)?([\w\s]+)$',        
    ]
    
    for pattern in patterns_conversion:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) == 3:
                amount = match.group(1)
                source_input = match.group(2).strip()
                target_input = match.group(3).strip()
                return amount, source_input, target_input
            else:
                source_input = match.group(1).strip()
                target_input = match.group(2).strip()
                return None, source_input, target_input
    
    patterns_single = [
        r'^(\d+\.?\d*)\s+([\w\s]+)$', 
        r'^([\w\s]+)$',               
    ]
    
    for pattern in patterns_single:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            if len(match.groups()) == 2:
                amount = match.group(1)
                crypto_input = match.group(2).strip()
                return amount, crypto_input, None
            else:
                crypto_input = match.group(1).strip()
                return None, crypto_input, None
    
    return None, None, None

async def search_crypto(update: Update, context: ContextTypes.DEFAULT_TYPE, user_input=None):
    if not user_input:
        if update.message:
            user_input = update.message.text.strip()
        else:
            return None, None

    if not crypto_data_cache:
        if not await update_crypto_cache():
            if update.message:
                await update.message.reply_text(f"{EMOJIS['error']} خطا در دریافت داده از API. لطفاً بعداً تلاش کنید.")
            return None, None

    user_input = user_input.strip().upper()
    found_crypto = None
    found_symbol = None
    
    for symbol, crypto in crypto_data_cache.items():
        name_upper = crypto['name'].upper()
        if (user_input == symbol or
            user_input == name_upper or
            user_input in name_upper or
            user_input.replace(' ', '') in name_upper.replace(' ', '')):
            found_crypto = crypto
            found_symbol = symbol
            break
    
    if not found_crypto:
        stars_keywords = ['STARS', 'STARZ', 'استارز', 'استار']
        if any(keyword in user_input for keyword in stars_keywords):
            if 'STARS' in crypto_data_cache:
                found_crypto = crypto_data_cache['STARS']
                found_symbol = 'STARS'
    
    if not found_crypto and 'تومن' in user_input.lower():
        found_symbol = 'IRR'
        found_crypto = {'name': 'تومن', 'irr': '1', 'usdt': str(1 / float(crypto_data_cache['USDT']['irr']))}

    return found_crypto, found_symbol

async def convert_currency(amount: float, source_currency: str, target_currency: str) -> dict:
    try:
        source_crypto, source_symbol = await search_crypto(None, None, source_currency)
        target_crypto, target_symbol = await search_crypto(None, None, target_currency)
        
        if not source_crypto or not target_crypto:
            return {"error": f"ارز {source_currency} یا {target_currency} یافت نشد."}
        
        if source_symbol == "IRR":
            if "USDT" not in crypto_data_cache:
                return {"error": "داده‌های تتر در دسترس نیست."}
            usdt_irr = float(crypto_data_cache["USDT"]["irr"]) 
            target_irr = float(target_crypto["irr"]) 
            if target_irr == 0:
                return {"error": f"قیمت {target_currency} در دسترس نیست."}
            converted_amount = amount / target_irr 
            source_name = "تومن"
            target_name = target_crypto['name']
        elif target_symbol == "IRR":
            source_irr = float(source_crypto["irr"])
            if source_irr == 0:
                return {"error": f"قیمت {source_currency} در دسترس نیست."}
            converted_amount = amount * source_irr 
            source_name = source_crypto['name']
            target_name = "تومن"
        else:
            source_usdt = float(source_crypto["usdt"])
            target_usdt = float(target_crypto["usdt"])
            if source_usdt == 0 or target_usdt == 0:
                return {"error": f"قیمت برای {source_currency} یا {target_currency} در دسترس نیست."}
            converted_amount = (amount * source_usdt) / target_usdt
            source_name = source_crypto['name']
            target_name = target_crypto['name']
        
        return {
            "converted_amount": converted_amount,
            "source_currency": source_symbol,
            "target_currency": target_symbol,
            "source_name": source_name,
            "target_name": target_name
        }
    except Exception as e:
        logger.error(f"Error in convert_currency: {e}")
        return {"error": f"خطا در تبدیل ارز: {str(e)}"}

def create_conversion_message(conversion_result, amount):
    if "error" in conversion_result:
        return (
            f"{EMOJIS['error']} <b>خطا در تبدیل</b>\n\n"
            f"⚠️ {conversion_result['error']}\n"
            f"لطفاً نام ارز یا مقدار را بررسی کنید و دوباره امتحان کنید."
        )
    
    converted_amount = conversion_result['converted_amount']
    source_name = conversion_result['source_name']
    target_name = conversion_result['target_name']
    
    message = (
        f"{EMOJIS['money']} <b>نتیجه تبدیل ارز</b>\n\n"
        f"💸 <b>{format_price(amount)} {source_name}</b> برابر است با:\n"
        f"<code>{format_price(converted_amount)}</code> <b>{target_name}</b>\n\n"
        f"{EMOJIS['clock']} به‌روزرسانی: {datetime.now(IRAN_TZ).strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    return message

async def display_crypto_info(update: Update, context: ContextTypes.DEFAULT_TYPE, crypto, symbol):
    if crypto['irr'] == "0" or crypto['usdt'] == "0":
        await update.message.reply_text(f"{EMOJIS['warning']} ارز {crypto['name']} ({symbol}) در حال حاضر قیمتی ندارد.")
        return

    initial_message = await create_initial_price_message(crypto, symbol)
    
    if not initial_message:
        await update.message.reply_text(f"{EMOJIS['warning']} ارز {crypto['name']} ({symbol}) در حال حاضر قیمتی ندارد.")
        return

    sent_message = await update.message.reply_text(initial_message, parse_mode='HTML')
    db.update_user_activity(update.effective_user.id)
    db.log_message(update.effective_user.id, update.effective_chat.id, f"Search: {symbol}", "search")
    
    chart_url = await get_chart_image(symbol)
    
    if chart_url:
        chart_file = await download_chart_image(chart_url)
        
        if chart_file:
            final_message = await create_final_price_message(crypto, symbol, chart_available=True)
            
            await context.bot.edit_message_media(
                chat_id=update.effective_chat.id,
                message_id=sent_message.message_id,
                media=InputMediaPhoto(
                    media=chart_file,
                    caption=final_message,
                    parse_mode='HTML'
                )
            )
        else:
            final_message = await create_final_price_message(crypto, symbol, chart_available=False)
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=sent_message.message_id,
                text=final_message,
                parse_mode='HTML'
            )
    else:
        final_message = await create_final_price_message(crypto, symbol, chart_available=False)
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=sent_message.message_id,
            text=final_message,
            parse_mode='HTML'
        )

async def display_amount_info(update: Update, context: ContextTypes.DEFAULT_TYPE, crypto, symbol, amount):
    if crypto['irr'] == "0" or crypto['usdt'] == "0":
        await update.message.reply_text(f"{EMOJIS['warning']} ارز {crypto['name']} ({symbol}) در حال حاضر قیمتی ندارد.")
        return

    message = create_amount_message(crypto, symbol, amount)
    if not message:
        await update.message.reply_text(f"{EMOJIS['error']} خطا در محاسبه قیمت.")
        return

    sent_message = await update.message.reply_text(message, parse_mode='HTML')
    db.update_user_activity(update.effective_user.id)
    db.log_message(update.effective_user.id, update.effective_chat.id, f"Calculate: {amount} {symbol}", "calculation")
    
    chart_url = await get_chart_image(symbol)
    
    if chart_url:
        chart_file = await download_chart_image(chart_url)
        
        if chart_file:
            await context.bot.edit_message_media(
                chat_id=update.effective_chat.id,
                message_id=sent_message.message_id,
                media=InputMediaPhoto(
                    media=chart_file,
                    caption=message,
                    parse_mode='HTML'
                )
            )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    chat_type = update.effective_chat.type
    user_stats = db.get_user_stats(user_id)
    
    if user_stats and user_stats['is_banned']:
        await update.message.reply_text(
            f"{EMOJIS['error']} <b>دسترسی مسدود</b>\n\n"
            f"شما از استفاده از این ربات محروم شده‌اید. برای اطلاعات بیشتر با پشتیبانی تماس بگیرید.",
            parse_mode='HTML'
        )
        return
    
    if chat_type in ['group', 'supergroup']:
        group_manager.update_group_activity(update.effective_chat.id)
    
    db.log_message(user_id, update.effective_chat.id, text, "message")
    db.update_user_activity(user_id)
    
    if not text.startswith('/'):
        user_input = text.strip() 
        
        if user_input:
            amount_str, source_input, target_input = parse_amount_message(user_input)
            
            if source_input:
                if target_input:
                    amount = float(amount_str) if amount_str else 1.0 
                    conversion_result = await convert_currency(amount, source_input, target_input)
                    message = create_conversion_message(conversion_result, amount)
                    await update.message.reply_text(message, parse_mode='HTML')
                    db.log_message(user_id, update.effective_chat.id, f"Convert: {amount} {source_input} to {target_input}", "conversion")
                else:
                    amount = amount_str
                    found_crypto, found_symbol = await search_crypto(update, context, source_input)
                    
                    if found_crypto:
                        if amount:
                            await display_amount_info(update, context, found_crypto, found_symbol, amount)
                        else:
                            await display_crypto_info(update, context, found_crypto, found_symbol)

async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.inline_query.from_user.id
    user_stats = db.get_user_stats(user_id)
    if user_stats and user_stats['is_banned']:
        await update.inline_query.answer([], cache_time=1)
        return
    
    query = update.inline_query.query.strip()
    results = []
    
    if not crypto_data_cache:
        if not await update_crypto_cache():
            return
    
    if not query:
        top_cryptos = list(crypto_data_cache.items())[:10]
        
        for i, (symbol, crypto) in enumerate(top_cryptos):
            price = format_price(crypto['irr'])
            change = crypto['dayChange']
            
            if change and float(change) < 0:
                change_icon = EMOJIS['down']
            elif change and float(change) > 0:
                change_icon = EMOJIS['up']
            else:
                change_icon = EMOJIS['stable']
                
            title = f"{crypto['name']} ({symbol})"
            description = f"{price} تومان | {change_icon} {change if change else '0'}%"
            
            message_text = f"{EMOJIS['info']} <b>{crypto['name']}</b> ({symbol}):\n\n"
            message_text += f"{EMOJIS['money']} قیمت تومان: <code>{price}</code> تومان\n"
            message_text += f"💵 قیمت دلار: <code>{format_price(crypto['usdt'], is_usdt=True)}</code> USDT\n"
            if change:
                message_text += f"{change_icon} تغییر 24h: <code>{float(change):+.2f}%</code>\n"
            
            if last_update_time:
                message_text += f"\n{EMOJIS['clock']} آخرین بروزرسانی: {last_update_time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            results.append(
                InlineQueryResultArticle(
                    id=str(i),
                    title=title,
                    description=description,
                    input_message_content=InputTextMessageContent(
                        message_text, parse_mode='HTML'
                    )
                )
            )
    else:
        query = query.upper()
        found_items = []
        
        for symbol, crypto in crypto_data_cache.items():
            if (query in symbol or 
                query in crypto['name'].upper()):
                found_items.append((symbol, crypto))
        
        found_items = found_items[:20]
        
        for i, (symbol, crypto) in enumerate(found_items):
            price = format_price(crypto['irr'])
            change = crypto['dayChange']
            
            if change and float(change) < 0:
                change_icon = EMOJIS['down']
            elif change and float(change) > 0:
                change_icon = EMOJIS['up']
            else:
                change_icon = EMOJIS['stable']
                
            title = f"{crypto['name']} ({symbol})"
            description = f"{price} تومان | {change_icon} {change if change else '0'}%"
            
            message_text = f"{EMOJIS['info']} <b>{crypto['name']}</b> ({symbol}):\n\n"
            message_text += f"{EMOJIS['money']} قیمت تومان: <code>{price}</code> تومان\n"
            message_text += f"💵 قیمت دلار: <code>{format_price(crypto['usdt'], is_usdt=True)}</code> USDT\n"
            if change:
                message_text += f"{change_icon} تغییر 24h: <code>{float(change):+.2f}%</code>\n"
            
            if last_update_time:
                message_text += f"\n{EMOJIS['clock']} آخرین بروزرسانی: {last_update_time.strftime('%Y-%m-%d %H:%M:%S')}"
            
            results.append(
                InlineQueryResultArticle(
                    id=str(i),
                    title=title,
                    description=description,
                    input_message_content=InputTextMessageContent(
                        message_text, parse_mode='HTML'
                    )
                )
            )
    
    await update.inline_query.answer(results, cache_time=1)

async def update_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await update_crypto_cache():
        await update.message.reply_text(
            f"{EMOJIS['check']} قیمت‌ها با موفقیت بروزرسانی شدند!\n"
            f"آخرین بروزرسانی: {datetime.now(IRAN_TZ).strftime('%H:%M:%S')}"
        )
    else:
        await update.message.reply_text(f"{EMOJIS['error']} خطا در بروزرسانی قیمت‌ها!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ['group', 'supergroup']:
        await update.message.reply_text(
            f"{EMOJIS['info']} برای راهنمایی کامل به پیوی ربات مراجعه کنید: @{context.bot.username}",
            parse_mode='HTML'
        )
        return
    
    help_text = f"""
{EMOJIS['info']} <b>راهنمای استفاده از ربات</b>

<b>در پیوی ربات:</b>
• فقط نام ارز را تایپ کنید (مثلاً: btc یا bitcoin)
• برای محاسبه مقدار خاص: <code>2 btc</code> یا <code>0.5 اتریوم</code>

<b>در گروه‌ها:</b>
• از نقطه قبل از نام ارز استفاده کنید (مثلاً: <code>.btc</code> یا <code>.اتریوم</code>)
• برای محاسبه مقدار خاص: <code>.2 btc</code> یا <code>.0.5 تتر</code>

<b>استفاده اینلاین:</b>
• در هر چتی: <code>@{context.bot.username} btc</code>
• یا از طریق آیکون اینلاین در کنار باکس تایپ

<b>دستورات موجود:</b>
/start - شروع ربات
/help - این راهنما
/update - بروزرسانی قیمت‌ها

{EMOJIS['warning']} <b>توجه:</b>
• قیمت‌ها هر 5 دقیقه خودکار بروز می‌شوند
• برای دریافت قیمت لحظه‌ای از دستور /update استفاده کنید
"""
    
    await update.message.reply_text(help_text, parse_mode='HTML')

async def start_with_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_membership_wrapper(update, context, start)

async def help_with_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_membership_wrapper(update, context, help_command)

async def update_with_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_membership_wrapper(update, context, update_prices)

async def admin_with_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await admin_panel(update, context)

async def handle_message_with_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_membership_wrapper(update, context, handle_message)

async def cleanup_temp_data():
    try:
        current_time = datetime.now(IRAN_TZ)
        expired_sessions = []
        
        for user_id, session_data in user_sessions.items():
            if 'last_activity' in session_data:
                last_activity = session_data['last_activity']
                if (current_time - last_activity) > timedelta(hours=24):
                    expired_sessions.append(user_id)
        
        for user_id in expired_sessions:
            del user_sessions[user_id]
        
        logger.info(f"پاک‌سازی sessions: {len(expired_sessions)} session منقضی شده")
        
    except Exception as e:
        logger.error(f"خطا در پاک‌سازی داده‌ها: {e}")

async def initialize_bot():
    print("🔍 در حال بررسی سلامت سیستم...")
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            print("✅ اتصال به API موفق")
        else:
            print("⚠️  مشکل در اتصال به API")
    except Exception as e:
        print(f"❌ خطا در اتصال به API: {e}")
    
    try:
        stats = db.get_bot_stats()
        print(f"✅ دیتابیس سالم - کاربران: {stats['total_users']}")
    except Exception as e:
        print(f"❌ مشکل در دیتابیس: {e}")
   
    if await update_crypto_cache():
        print(f"✅ داده‌های ارزها بارگذاری شد ({len(crypto_data_cache)} ارز)")
    else:
        print("❌ خطا در بارگذاری داده‌های ارزها")
    
    print("🚀 ربات آماده است!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"خطا در هنگام پردازش آپدیت: {context.error}")
    
    try:
        if update and update.effective_user:
            error_msg = f"""
{EMOJIS['error']} <b>خطای سیستمی رخ داد</b>

🆔 کاربر: {update.effective_user.id}
📝 متن: {update.effective_message.text if update.effective_message else 'N/A'}
🔧 خطا: {str(context.error)[:1000]}
"""
           
            if ADMINS:
                await context.bot.send_message(
                    chat_id=ADMINS[0],
                    text=error_msg,
                    parse_mode='HTML'
                )
    except Exception as e:
        logger.error(f"خطا در ارسال گزارش خطا: {e}")

async def shutdown_bot():
    """خاموش کردن تمیز ربات"""
    print("🛑 در حال خاموش کردن ربات...")
    print("✅ ربات با موفقیت متوقف شد")

async def main_async():
    """تابع اصلی به صورت async"""
    await initialize_bot()
    
    try:
        from telegram.request import HTTPXRequest
        
        PROXY_CONFIG = {
            'proxy_url': 'socks5://Shooka-Koopa.xhivar-nokian.rang-mavar-zhos.info:2040',
        }
        
        request = HTTPXRequest(
            **PROXY_CONFIG,
            connect_timeout=60,
            read_timeout=60,
            write_timeout=60
        )
        
        application = Application.builder() \
            .token(BOT_TOKEN) \
            .request(request) \
            .build()

        # اضافه کردن handlerها
        application.add_handler(CommandHandler("start", start_with_membership))
        application.add_handler(CommandHandler("help", help_with_membership))
        application.add_handler(CommandHandler("update", update_with_membership))
        application.add_handler(CommandHandler("admin", admin_with_membership))
        application.add_handler(CommandHandler("stats", stats_command))        
        application.add_handler(CommandHandler("broadcast", broadcast_message))
        application.add_handler(CommandHandler("forward", forward_broadcast))
        application.add_handler(CallbackQueryHandler(broadcast_options, pattern="^broadcast_options$"))
        application.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^confirm_broadcast_"))
        application.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^confirm_forward_"))
        application.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^cancel_broadcast$"))
        application.add_handler(CallbackQueryHandler(broadcast_help, pattern="^broadcast_help$"))
        application.add_handler(CallbackQueryHandler(forward_help, pattern="^forward_help$"))
        application.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^admin_"))
        application.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^user_"))
        application.add_handler(CallbackQueryHandler(check_membership, pattern="^check_membership$"))
        application.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^add_chat$"))
        application.add_handler(CallbackQueryHandler(admin_button_handler, pattern="^remove_chat_"))
        application.add_handler(CallbackQueryHandler(install_bot_button, pattern="^install_bot$"))
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND & filters.Regex(r'^@\w+\s+-?\d+\s+(channel|group)$'),
            handle_chat_info
        ))
        
        application.add_handler(ChatMemberHandler(handle_bot_promoted, ChatMemberHandler.MY_CHAT_MEMBER))
        application.add_handler(MessageHandler(
            filters.ChatType.GROUPS & filters.StatusUpdate.NEW_CHAT_MEMBERS,
            handle_group_add
        ))
        application.add_handler(MessageHandler(
            filters.ChatType.GROUPS & filters.TEXT & filters.Regex(r'نصب ربات'),
            install_bot_command
        ))
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            lambda update, context: check_group_activation(update, context, handle_message)
        ))
        
        application.add_handler(InlineQueryHandler(inline_query))
        application.add_error_handler(error_handler)

        # راه‌اندازی job queue
        job_queue = application.job_queue
        job_queue.run_repeating(
            lambda context: asyncio.create_task(update_crypto_cache(context)), 
            interval=300,
            first=10
        )
        job_queue.run_repeating(
            lambda context: asyncio.create_task(cleanup_temp_data()), 
            interval=3600,
            first=30
        )

        print("🤖 ربات در حال راه‌اندازی...")
        print("=" * 50)
        print("🤖 ربات قیمت ارزهای دیجیتال در حال راه‌اندازی...")
        print(f"🕒 زمان شروع: {datetime.now(IRAN_TZ).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💾 وضعیت دیتابیس: فعال")
        print(f"📊 تعداد ارزهای پشتیبانی شده: {len(crypto_data_cache)}")
        print(f"👑 ادمین‌ها: {ADMINS}")
        print("=" * 50)
        
        await application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"خطای جدی در راه‌اندازی ربات: {e}")
        print(f"❌ خطای بحرانی: {e}")

def main():
    """تابع اصلی"""
    asyncio.run(main_async())

if __name__ == "__main__":
    main()