#=============== In The Name Of God ===============#
# Source Name: Ultra Self Creator
# Source Version: 2.0.0
# Developer: @IVGalaxy
# © 2024 Ultra Self LLC. All rights reserved.
#==================== Import ======================#
from colorama import Fore
from pyrogram import Client, filters, idle, errors
from pyrogram.types import *
from functools import wraps
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import subprocess
import html
import zipfile
import pymysql
import shutil
import signal
import re
import os
import time
#==================== Config =====================#
Admin = 8360575945 # Admin ID
Token = "8245180326:AAE8r6t9kh4CkEYHYlzjegHQF4Kr3lrtnEU" # Bot Token
API_ID = 37892224 # API ID
API_HASH = "16809da472988f2febce216912ae7be0" # API HASH
Channel_ID = "TelBlack_Source" # Channel Username
Channel_Help = "TelBlack_Source" # Channel Help Username
Helper_ID = "TelBlack_Source" # Helper Username
DBName = "gajmwv_selfff" # Database Name
DBUser = "gajmwv_selfff" # Database User
DBPass = "111111" # Database Password
HelperDBName = "gajmwv_helperrr" # Helper Database Name
HelperDBUser = "gajmwv_helperrr" # Helper Database User
HelperDBPass = "111111" # Helper Database Password
CardNumber = "6037701213986919" # Card Number
CardName = "امیرعلی میرزایی" # Card Name
#==================== Create =====================#
if not os.path.isdir("sessions"):
    os.mkdir("sessions")
if not os.path.isdir("selfs"):
    os.mkdir("selfs")
if not os.path.isdir("cards"):
    os.mkdir("cards")
#===================== App =======================#
app = Client("Bot", api_id=API_ID, api_hash=API_HASH, bot_token=Token)

scheduler = AsyncIOScheduler()
scheduler.start()

temp_Client = {}
lock = asyncio.Lock()

#==================== Database Functions =====================#
def get_data(query):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass, cursorclass=pymysql.cursors.DictCursor) as connect:
        db = connect.cursor()
        db.execute(query)
        result = db.fetchone()
        return result

def get_datas(query):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass) as connect:
        db = connect.cursor()
        db.execute(query)
        result = db.fetchall()
        return result

def update_data(query):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass) as connect:
        db = connect.cursor()
        db.execute(query)
        connect.commit()

def helper_getdata(query):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=HelperDBName, user=HelperDBUser, password=HelperDBPass) as connect:
        db = connect.cursor()
        db.execute(query)
        result = db.fetchone()
        return result

def helper_updata(query):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=HelperDBName, user=HelperDBUser, password=HelperDBPass) as connect:
        db = connect.cursor()
        db.execute(query)
        connect.commit()

#==================== Card Functions =====================#
def add_card(user_id, card_number, bank_name=None):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass) as connect:
        db = connect.cursor()
        if bank_name:
            db.execute(f"INSERT INTO cards(user_id, card_number, bank_name, verified) VALUES({user_id}, '{card_number}', '{bank_name}', 'pending')")
        else:
            db.execute(f"INSERT INTO cards(user_id, card_number, verified) VALUES({user_id}, '{card_number}', 'pending')")
        connect.commit()

def get_user_cards(user_id):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass, cursorclass=pymysql.cursors.DictCursor) as connect:
        db = connect.cursor()
        db.execute(f"SELECT * FROM cards WHERE user_id = '{user_id}' AND verified = 'verified' ORDER BY id DESC")
        result = db.fetchall()
        return result

def get_user_all_cards(user_id):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass, cursorclass=pymysql.cursors.DictCursor) as connect:
        db = connect.cursor()
        db.execute(f"SELECT * FROM cards WHERE user_id = '{user_id}' ORDER BY id DESC")
        result = db.fetchall()
        return result

def get_pending_cards():
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass, cursorclass=pymysql.cursors.DictCursor) as connect:
        db = connect.cursor()
        db.execute("SELECT * FROM cards WHERE verified = 'pending'")
        result = db.fetchall()
        return result

def update_card_status(card_id, status, bank_name=None):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass) as connect:
        db = connect.cursor()
        if bank_name:
            db.execute(f"UPDATE cards SET verified = '{status}', bank_name = '{bank_name}' WHERE id = '{card_id}'")
        else:
            db.execute(f"UPDATE cards SET verified = '{status}' WHERE id = '{card_id}'")
        connect.commit()

def delete_card(card_id):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass) as connect:
        db = connect.cursor()
        db.execute(f"DELETE FROM cards WHERE id = '{card_id}'")
        connect.commit()

def get_card_by_number(user_id, card_number):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock", database=DBName, user=DBUser, password=DBPass, cursorclass=pymysql.cursors.DictCursor) as connect:
        db = connect.cursor()
        db.execute(f"SELECT * FROM cards WHERE user_id = '{user_id}' AND card_number = '{card_number}' LIMIT 1")
        result = db.fetchone()
        return result

def get_card_by_id(card_id):
    with pymysql.connect(host="localhost", port=3307, unix_socket="/home/a1201324/mysql.sock, database=DBName, user=DBUser, password=DBPass, cursorclass=pymysql.cursors.DictCursor) as connect:
        db = connect.cursor()
        db.execute(f"SELECT * FROM cards WHERE id = '{card_id}' LIMIT 1")
        result = db.fetchone()
        return result

#==================== Admin Functions =====================#
def add_admin(user_id):
    if helper_getdata(f"SELECT * FROM adminlist WHERE id = '{user_id}' LIMIT 1") is None:
        helper_updata(f"INSERT INTO adminlist(id) VALUES({user_id})")

def delete_admin(user_id):
    if helper_getdata(f"SELECT * FROM adminlist WHERE id = '{user_id}' LIMIT 1") is not None:
        helper_updata(f"DELETE FROM adminlist WHERE id = '{user_id}' LIMIT 1")

#==================== Database Initialization =====================#
update_data("""
CREATE TABLE IF NOT EXISTS bot(
status varchar(10) DEFAULT 'ON'
) default charset=utf8mb4;
""")

update_data("""
CREATE TABLE IF NOT EXISTS user(
id bigint PRIMARY KEY,
step varchar(150) DEFAULT 'none',
phone varchar(150) DEFAULT NULL,
expir bigint DEFAULT '0',
account varchar(50) DEFAULT 'unverified',
self varchar(50) DEFAULT 'inactive',
pid bigint DEFAULT NULL
) default charset=utf8mb4;
""")

update_data("""
CREATE TABLE IF NOT EXISTS cards(
id INT AUTO_INCREMENT PRIMARY KEY,
user_id bigint NOT NULL,
card_number varchar(20) NOT NULL,
bank_name varchar(50) DEFAULT NULL,
verified varchar(10) DEFAULT 'pending',
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
) default charset=utf8mb4;
""")

update_data("""
CREATE TABLE IF NOT EXISTS settings(
id INT AUTO_INCREMENT PRIMARY KEY,
setting_key VARCHAR(100) NOT NULL UNIQUE,
setting_value TEXT NOT NULL,
description VARCHAR(255) DEFAULT NULL,
updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) default charset=utf8mb4;
""")

update_data("""
CREATE TABLE IF NOT EXISTS block(
id bigint PRIMARY KEY
) default charset=utf8mb4;
""")

helper_updata("""
CREATE TABLE IF NOT EXISTS ownerlist(
id bigint PRIMARY KEY
) default charset=utf8mb4;
""")

helper_updata("""
CREATE TABLE IF NOT EXISTS adminlist(
id bigint PRIMARY KEY
) default charset=utf8mb4;
""")

bot = get_data("SELECT * FROM bot")
if bot is None:
    update_data("INSERT INTO bot() VALUES()")

OwnerUser = helper_getdata(f"SELECT * FROM ownerlist WHERE id = '{Admin}' LIMIT 1")
if OwnerUser is None:
    helper_updata(f"INSERT INTO ownerlist(id) VALUES({Admin})")

AdminUser = helper_getdata(f"SELECT * FROM adminlist WHERE id = '{Admin}' LIMIT 1")
if AdminUser is None:
    helper_updata(f"INSERT INTO adminlist(id) VALUES({Admin})")


default_settings = [
    ("start_message", "**\nسلام [ {user_link} ],  به ربات خرید دستیار تلگرام خوش آمدید.\n\nتوی این ربات میتونید از خرید، نصب دستیار بهره ببرید.\n\nلطفا اگر سوالی دارید از بخش پشتیبانی ، با پشتیبان ها در ارتباط باشید یا در گروه پشتیبانی ما عضو شوید.\n\n\n **", "پیام استارت ربات"),
    ("price_message", "**\nنرخ ربات دستیار عبارت است از :\n\n» 1 ماهه : ( `{price_1month}` تومان )\n\n» 2 ماهه : ( `{price_2month}` تومان )\n\n» 3 ماهه : ( `{price_3month}` تومان )\n\n» 4 ماهه : ( `{price_4month}` تومان )\n\n» 5 ماهه : ( `{price_5month}` تومان )\n\n» 6 ماهه : ( `{price_6month}` تومان )\n\n\n(⚠️) توجه داشته باشید که ربات دستیار روی شماره های ایران توصیه میشود و در صورت نصب روی شماره های خارج از کشور، ما مسئولیتی در مورد مسدود شدن اکانت نداریم.\n\n\nدر صورتی که میخواهید به صورت ارزی پرداخت کنید از پشتیبانی درخواست ولت کنید.\n‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌\n‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌\n**", "پیام نرخ‌ها"),
    ("whatself_message", "**\nسلف به رباتی گفته میشه که روی اکانت شما نصب میشه و امکانات خاصی رو در اختیارتون میزاره ، لازم به ذکر هست که نصب شدن بر روی اکانت شما به معنی وارد شدن ربات به اکانت شما هست ( به دلیل دستور گرفتن و انجام فعالیت ها )\nاز جمله امکاناتی که در اختیار شما قرار میدهد شامل موارد زیر است:\n\n❈ گذاشتن ساعت با فونت های مختلف بر روی بیو ، اسم\n❈ قابلیت تنظیم حالت خوانده شدن خودکار پیام ها\n❈ تنظیم حالت پاسخ خودکار\n❈ پیام انیمیشنی\n❈ منشی هوشمند\n❈ دریافت پنل و تنظیمات اکانت هوشمند\n❈ دو زبانه بودن دستورات و جواب ها\n❈ تغییر نام و کاور فایل ها\n❈ اعلان پیام ادیت و حذف شده در پیوی\n❈ ذخیره پروفایل های جدید و اعلان حذف پروفایل مخاطبین\n\nو امکاناتی دیگر که میتوانید با مراجعه به بخش راهنما آن ها را ببینید و مطالعه کنید!\n\n❈ لازم به ذکر است که امکاناتی که در بالا گفته شده تنها ذره ای از امکانات سلف میباشد .\n**", "پیام توضیح سلف"),
    ("price_1month", "75000", "قیمت 1 ماهه"),
    ("price_2month", "150000", "قیمت 2 ماهه"),
    ("price_3month", "220000", "قیمت 3 ماهه"),
    ("price_4month", "275000", "قیمت 4 ماهه"),
    ("price_5month", "340000", "قیمت 5 ماهه"),
    ("price_6month", "390000", "قیمت 6 ماهه"),
    ("card_number", CardNumber, "شماره کارت"),
    ("card_name", CardName, "نام صاحب کارت"),
]

# وارد کردن تنظیمات پیش‌فرض
for key, value, description in default_settings:
    if get_data(f"SELECT * FROM settings WHERE setting_key = '{key}'") is None:
        update_data(f"INSERT INTO settings(setting_key, setting_value, description) VALUES('{key}', '{value}', '{description}')")

#==================== Utility Functions =====================#
def checker(func):
    @wraps(func)
    async def wrapper(c, m, *args, **kwargs):
        chat_id = m.chat.id if hasattr(m, "chat") else m.from_user.id
        bot = get_data("SELECT * FROM bot")
        block = get_data(f"SELECT * FROM block WHERE id = '{chat_id}' LIMIT 1")

        if block is not None and chat_id != Admin:
            return
        
        try:
            chat = await app.get_chat(Channel_ID)
            channel_name = chat.title
            await app.get_chat_member(Channel_ID, chat_id)
        except errors.UserNotParticipant:
            await app.send_message(chat_id, "**• برای استفاده از خدمات ما ابتدا باید در کانال ما عضو باشید، بعد از این که عضو شدید روی دکمه عضو شدم کلیک کنید.**", reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=f"( {channel_name} )", url=f"https://t.me/{Channel_ID}")
                    ],
                    [
                        InlineKeyboardButton(text="عضو شدم ( ✔️ )", callback_data="check_membership")
                    ]
                ]
            ))
            return
        except errors.ChatAdminRequired:
            if chat_id == Admin:
                await app.send_message(Admin, "**• ابتدا ربات را در کانال ادمین کرده سپس ربات را [ /start ] کنید.**")
            return

        if bot["status"] == "OFF" and chat_id != Admin:
            await app.send_message(chat_id, "**درحال حاظر ربات خاموش میباشد، بعدا مجدد اقدام نمایید.**")
            return
        
        return await func(c, m, *args, **kwargs)
    return wrapper

async def expirdec(user_id):
    user = get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1")
    user_expir = user["expir"]
    if user_expir > 0:
        user_upexpir = user_expir - 1
        update_data(f"UPDATE user SET expir = '{user_upexpir}' WHERE id = '{user_id}' LIMIT 1")
    else:
        job = scheduler.get_job(str(user_id))
        if job:
            scheduler.remove_job(str(user_id))
        if user_id != Admin:
            delete_admin(user_id)
        if os.path.isdir(f"selfs/self-{user_id}"):
            pid = user["pid"]
            try:
                os.kill(pid, signal.SIGKILL)
            except:
                pass
            await asyncio.sleep(1)
            try:
                shutil.rmtree(f"selfs/self-{user_id}")
            except:
                pass
        if os.path.isfile(f"sessions/{user_id}.session"):
            try:
                async with Client(f"sessions/{user_id}") as user_client:
                    await user_client.log_out()
            except:
                pass
            if os.path.isfile(f"sessions/{user_id}.session"):
                os.remove(f"sessions/{user_id}.session")
        if os.path.isfile(f"sessions/{user_id}.session-journal"):
            os.remove(f"sessions/{user_id}.session-journal")
        await app.send_message(user_id, "**انقضای سلف شما** به پایان رسید، شما میتوانید از بخش **خرید اشتراک**، **سلف خود را تمدید کنید.**")
        update_data(f"UPDATE user SET self = 'inactive' WHERE id = '{user_id}' LIMIT 1")
        update_data(f"UPDATE user SET pid = NULL WHERE id = '{user_id}' LIMIT 1")

async def setscheduler(user_id):
    job = scheduler.get_job(str(user_id))
    if not job:
        scheduler.add_job(expirdec, "interval", hours=24, args=[user_id], id=str(user_id))

def detect_bank(card_number):
    prefix = card_number[:6]
    if prefix.startswith("6037"):
        return "بانک کشاورزی"
    elif prefix.startswith("5892"):
        return "بانک سپه"
    elif prefix.startswith("6276"):
        return "بانک صادرات"
    elif prefix.startswith("6273"):
        return "بانک صادرات"
    elif prefix.startswith("6278"):
        return "بانک اقتصاد نوین"
    elif prefix.startswith("6280"):
        return "بانک پارسیان"
    elif prefix.startswith("6393"):
        return "بانک سامان"
    elif prefix.startswith("6395"):
        return "بانک سامان"
    elif prefix.startswith("6362"):
        return "بانک آینده"
    elif prefix.startswith("5029"):
        return "بانک پاسارگاد"
    elif prefix.startswith("6037"):
        return "بانک کشاورزی"
    elif prefix.startswith("6062"):
        return "بانک ملی"
    elif prefix.startswith("6104"):
        return "بانک ملت"
    elif prefix.startswith("6221"):
        return "بانک توسعه صادرات"
    else:
        return "نامشخص"

#==================== Settings Functions =====================#
def get_setting(key, default=None):
    result = get_data(f"SELECT setting_value FROM settings WHERE setting_key = '{key}'")
    return result["setting_value"] if result else default

def update_setting(key, value):
    update_data(f"UPDATE settings SET setting_value = '{value}' WHERE setting_key = '{key}'")

def get_all_settings():
    return get_datas("SELECT * FROM settings ORDER BY id")

def get_prices():
    return {
        "1month": get_setting("price_1month", "75000"),
        "2month": get_setting("price_2month", "150000"),
        "3month": get_setting("price_3month", "220000"),
        "4month": get_setting("price_4month", "275000"),
        "5month": get_setting("price_5month", "340000"),
        "6month": get_setting("price_6month", "390000"),
    }

def get_main_keyboard(user_id):
    user = get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1")
    expir = user["expir"] if user else 0
    
    keyboard = [
        [InlineKeyboardButton(text="پشتیبانی 👨‍💻", callback_data="Support")],
        [InlineKeyboardButton(text="راهنما 🗒️", url=f"https://t.me/{Channel_Help}"),
         InlineKeyboardButton(text="دستیار چیست؟ 🧐", callback_data="WhatSelf")],
        [InlineKeyboardButton(text=f"انقضا : ( {expir} روز )", callback_data="ExpiryStatus")],
        [InlineKeyboardButton(text="خرید اشتراک 💵", callback_data="BuySub"),
         InlineKeyboardButton(text="احراز هویت ✔️", callback_data="AccVerify")]
    ]
    
    # دکمه خرید/تمدید با کد
    if expir > 0:
        keyboard.append(
            [InlineKeyboardButton(text="تمدید با کد 💵", callback_data="BuyCode")]
        )
    else:
        keyboard.append(
            [InlineKeyboardButton(text="خرید با کد 💶", callback_data="BuyCode")]
        )
    
    # اگر کاربر ادمین است
    if str(user_id) == str(Admin):
        keyboard.append(
            [InlineKeyboardButton(text="مدیریت 🎈", callback_data="AdminPanel")]
        )
    
    # دکمه نرخ برای همه کاربران
    keyboard.append(
        [InlineKeyboardButton(text="نرخ 💎", callback_data="Price")]
    )
    
    # اگر کاربر انقضا دارد (expir > 0)
    if expir > 0:
        keyboard.extend([
            [InlineKeyboardButton(text="ورود / نصب ⏏️", callback_data="InstallSelf"),
             InlineKeyboardButton(text="تغییر زبان 🇬🇧", callback_data="ChangeLang")],
            [InlineKeyboardButton(text="وضعیت ⚙️", callback_data="SelfStatus")],
            [InlineKeyboardButton(text="زبان : ( فارسی 🇮🇷 )", callback_data="text")]
        ])
    
    keyboard.append(
        [InlineKeyboardButton(text="کانال ما 📢", url=f"https://t.me/{Channel_ID}")]
    )
    
    return InlineKeyboardMarkup(keyboard)

AdminPanelKeyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="آمار 📊", callback_data="AdminStats")],
        [InlineKeyboardButton(text="ارسال همگانی ✉️", callback_data="AdminBroadcast"),
         InlineKeyboardButton(text="فوروارد همگانی ✉️", callback_data="AdminForward")],
        [InlineKeyboardButton(text="بلاک کاربر 🚫", callback_data="AdminBlock"),
         InlineKeyboardButton(text="آنبلاک کاربر ✅️", callback_data="AdminUnblock")],
        [InlineKeyboardButton(text="افزودن انقضا ➕", callback_data="AdminAddExpiry"),
         InlineKeyboardButton(text="کسر انقضا ➖", callback_data="AdminDeductExpiry")],
        [InlineKeyboardButton(text="فعال کردن سلف 🔵", callback_data="AdminActivateSelf"),
         InlineKeyboardButton(text="غیرفعال کردن سلف 🔴", callback_data="AdminDeactivateSelf")],
        [InlineKeyboardButton(text="روشن کردن ربات 🔵", callback_data="AdminTurnOn"),
         InlineKeyboardButton(text="خاموش کردن ربات 🔴", callback_data="AdminTurnOff")],
        [InlineKeyboardButton(text="تنظیمات ⚙️", callback_data="AdminSettings")],  # دکمه جدید
        [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="Back")]
    ]
)

# اضافه کردن کیبورد تنظیمات
AdminSettingsKeyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="تغییر متن استارت 📝", callback_data="EditStartMessage")],
        [InlineKeyboardButton(text="تغییر متن نرخ 💰", callback_data="EditPriceMessage")],
        [InlineKeyboardButton(text="تغییر متن سلف 🤖", callback_data="EditSelfMessage")],
        [InlineKeyboardButton(text="تغییر قیمت‌ها 📊", callback_data="EditPrices")],
        [InlineKeyboardButton(text="تغییر اطلاعات کارت 💳", callback_data="EditCardInfo")],
        [InlineKeyboardButton(text="مشاهده تنظیمات 👁️", callback_data="ViewSettings")],
        [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]
    ]
)

#==================== Handlers =====================#
@app.on_message(filters.private, group=-1)
async def update(c, m):
    user = get_data(f"SELECT * FROM user WHERE id = '{m.chat.id}' LIMIT 1")
    if user is None:
        update_data(f"INSERT INTO user(id) VALUES({m.chat.id})")


@app.on_message(filters.private&filters.command("start"))
@checker
async def start_handler(c, m):
    keyboard = get_main_keyboard(m.chat.id)
    user_link = f'<a href="tg://user?id={m.chat.id}">{html.escape(m.chat.first_name)}</a>'
    start_message = get_setting("start_message").format(user_link=user_link)
    await app.send_message(m.chat.id, start_message, reply_markup=keyboard)
    update_data(f"UPDATE user SET step = 'none' WHERE id = '{m.chat.id}' LIMIT 1")
    async with lock:
        if m.chat.id in temp_Client:
            del temp_Client[m.chat.id]
    
    journal_file = f"sessions/{m.chat.id}.session-journal"
    if os.path.isfile(journal_file):
        os.remove(journal_file)


@app.on_callback_query()
@checker
async def callback_handler(c, call):
    global temp_Client
    user = get_data(f"SELECT * FROM user WHERE id = '{call.from_user.id}' LIMIT 1")
    phone_number = user["phone"] if user else None
    expir = user["expir"] if user else 0
    chat_id = call.from_user.id
    m_id = call.message.id
    data = call.data
    username = f"@{call.from_user.username}" if call.from_user.username else "وجود ندارد"

    if data == "BuySub" or data == "Back2":
        if user["phone"] is None:
            await app.delete_messages(chat_id, m_id)
            await app.send_message(chat_id, "**لطفا با استفاده از دکمه زیر شماره موبایل خود را به اشتراک بگذارید.**", reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(text="اشتراک گذاری شماره", request_contact=True)
                    ]
                ],resize_keyboard=True
            ))
            update_data(f"UPDATE user SET step = 'contact' WHERE id = '{call.from_user.id}' LIMIT 1")
        else:
            user_cards = get_user_cards(call.from_user.id)
            if user_cards:
                keyboard_buttons = []
                for card in user_cards:
                    card_number = card["card_number"]
                    bank_name = card["bank_name"] if card["bank_name"] else "نامشخص"
                    masked_card = f"{card_number[:4]} - - - - - - {card_number[-4:]}"
                    keyboard_buttons.append([
                        InlineKeyboardButton(text=masked_card, callback_data=f"SelectCardForPayment-{card['id']}")
                    ])
                keyboard_buttons.append([InlineKeyboardButton(text="(🔙) بازگشت", callback_data="Back")])
                
                await app.edit_message_text(chat_id, m_id,
                                           "**• لطفا انتخاب کنید برای پرداخت از کدام کارت احراز شده ی خود میخواهید استفاده کنید.**",
                                           reply_markup=InlineKeyboardMarkup(keyboard_buttons))
                update_data(f"UPDATE user SET step = 'none' WHERE id = '{call.from_user.id}' LIMIT 1")
            else:
                await app.edit_message_text(chat_id, m_id,
                                           "**• برای خرید باید ابتدا احراز هویت کنید.**",
                                           reply_markup=InlineKeyboardMarkup([
                                               [InlineKeyboardButton(text="احراز هویت ✔️", callback_data="AccVerify")]
                                           ]))
                update_data(f"UPDATE user SET step = 'none' WHERE id = '{call.from_user.id}' LIMIT 1")

# در تابع callback_handler، قسمت SelectCardForPayment را به‌روزرسانی کنید:
    elif data.startswith("SelectCardForPayment-"):
        card_id = data.split("-")[1]
        card = get_card_by_id(card_id)
        if card:
            update_data(f"UPDATE user SET step = 'select_subscription-{card_id}' WHERE id = '{call.from_user.id}' LIMIT 1")
        
        # دریافت قیمت‌ها از تنظیمات
            prices = get_prices()
        
            await app.edit_message_text(chat_id, m_id,
                                   "**• لطفا از گزینه های زیر انتخاب کنید میخواهید دستیار را برای چند ماه خریداری کنید:**",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text=f"(1) ماه معادل {prices['1month']} تومان", callback_data=f"Sub-30-{prices['1month']}")],
                                       [InlineKeyboardButton(text=f"(2) ماه معادل {prices['2month']} تومان", callback_data=f"Sub-60-{prices['2month']}")],
                                       [InlineKeyboardButton(text=f"(3) ماه معادل {prices['3month']} تومان", callback_data=f"Sub-90-{prices['3month']}")],
                                       [InlineKeyboardButton(text=f"(4) ماه معادل {prices['4month']} تومان", callback_data=f"Sub-120-{prices['4month']}")],
                                       [InlineKeyboardButton(text=f"(5) ماه معادل {prices['5month']} تومان", callback_data=f"Sub-150-{prices['5month']}")],
                                       [InlineKeyboardButton(text=f"(6) ماه معادل {prices['6month']} تومان", callback_data=f"Sub-180-{prices['6month']}")],
                                       [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="BuySub")]
                                   ]))

    elif data.startswith("Sub-"):
        params = data.split("-")
        expir_count = params[1]
        cost = params[2]
        card_id = user["step"].split("-")[1]
        card = get_card_by_id(card_id)
    
        if card:
            card_number = card["card_number"]
            masked_card = f"{card_number[:4]} - - - - - - {card_number[-4:]}"
        
        # استفاده از شماره کارت و نام از تنظیمات
            bot_card_number = get_setting("card_number")
            bot_card_name = get_setting("card_name")
        
            await app.edit_message_text(chat_id, m_id, f"**• لطفا مبلغ ( `{cost}` تومان ) رو با کارتی که احراز هویت و انتخاب کردید یعنی [ `{card_number}` ] به کارت زیر واریز کنید و فیش واریز خود را همینجا ارسال کنید.\n\n[ `{bot_card_number}` ]\nبه نام : {bot_card_name}\n\n• ربات آماده دریافت فیش واریزی شماست :**")
        
            update_data(f"UPDATE user SET step = 'payment_receipt-{expir_count}-{cost}-{card_id}' WHERE id = '{call.from_user.id}' LIMIT 1")

    elif data == "Price":
        prices = get_prices()
        price_message = get_setting("price_message").format(
            price_1month=prices["1month"],
            price_2month=prices["2month"],
            price_3month=prices["3month"],
            price_4month=prices["4month"],
            price_5month=prices["5month"],
            price_6month=prices["6month"]
        )
        await app.edit_message_text(chat_id, m_id, price_message, 
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="Back")]
                               ]))
        update_data(f"UPDATE user SET step = 'none' WHERE id = '{call.from_user.id}' LIMIT 1")

    elif data == "AccVerify":
    # تغییر: فقط کارت‌های تایید شده را بگیرید
        user_cards = get_user_cards(call.from_user.id)  # این تابع already کارت‌های verified را برمی‌گرداند
    
        if user_cards:
            cards_text = "**• به منوی احراز هویت خوش آمدید:\n\nکارت های احراز شده : **\n"
            for idx, card in enumerate(user_cards, 1):
                card_number = card["card_number"]
                bank_name = card["bank_name"] if card["bank_name"] else "نامشخص"
                masked_card = f"{card_number[:4]} - - - - - - {card_number[-4:]}"
                cards_text += f"**{idx} - {bank_name} [ {card_number} ]**\n"
        
            keyboard_buttons = []
            keyboard_buttons.append(
                [InlineKeyboardButton(text="کارت جدید ➕", callback_data="AddNewCard"),
                InlineKeyboardButton(text="حذف کارت ➖", callback_data="DeleteCard")])
            keyboard_buttons.append(
                [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="Back")])
        
            await app.edit_message_text(chat_id, m_id, cards_text, 
                                   reply_markup=InlineKeyboardMarkup(keyboard_buttons))
        else:
            await app.edit_message_text(chat_id, m_id, 
                                   "**• به منوی احراز هویت خوش آمدید ، لطفا انتخاب کنید:**",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="➕ کارت جدید", callback_data="AddNewCard"),
                                       InlineKeyboardButton(text="حذف کارت ➖", callback_data="DeleteCard")],
                                       [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="Back")]
                                   ]))
        update_data(f"UPDATE user SET step = 'none' WHERE id = '{call.from_user.id}' LIMIT 1")

    elif data == "AddNewCard":
        await app.edit_message_text(chat_id, m_id, """**• به بخش احراز هویت خوش آمدید.  برای احراز هویت از کارت خود ( حتما کارتی که با آن میخواهید پرداخت انجام دهید ) عکس بگیرید و ارسال کنید.  
• اسم و فامیل شما روی کارت باید کاملا مشخص باشد و عکس کارت داخل برنامه قابل قبول نمیباشد...

• نکات :
1) شماره کارت و نام صاحب کارت کاملا مشخص باشد.
2) لطفا تاریخ اعتبار و Cvv2 کارت خود را بپوشانید!
3) فقط با کارتی که احراز هویت میکنید میتوانید خرید انجام بدید و اگر با کارت دیگری اقدام کنید تراکنش ناموفق میشود و هزینه از سمت خودِ بانک به شما بازگشت داده میشود.
4) در صورتی که توانایی ارسال عکس از کارت را ندارید تنها راه حل ارسال عکس از کارت ملی یا شناسنامه صاحب کارت است.

لطفا عکس از کارتی که میخواهید با آن خرید انجام دهید ارسال کنید...**""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AccVerify")]
        ]))
        update_data(f"UPDATE user SET step = 'card_photo' WHERE id = '{call.from_user.id}' LIMIT 1")

    elif data == "DeleteCard":
        user_cards = get_user_all_cards(call.from_user.id)
    
    # فیلتر کردن: فقط کارت‌های تایید شده
        verified_cards = [card for card in user_cards if card["verified"] == "verified"]
    
        if verified_cards:
            keyboard_buttons = []
            for card in verified_cards:
                card_number = card["card_number"]
                masked_card = f"{card_number[:4]} - - - - - - {card_number[-4:]}"
                keyboard_buttons.append([
                    InlineKeyboardButton(text=masked_card, callback_data=f"SelectCard-{card['id']}")
                ])
            keyboard_buttons.append([InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AccVerify")])
        
            await app.edit_message_text(chat_id, m_id,
                                   "**• لطفا انتخاب کنید میخواهید کدام کارت خود را حذف کنید.**",
                                   reply_markup=InlineKeyboardMarkup(keyboard_buttons))
        else:
            await app.answer_callback_query(call.id, text="• هیچ کارت احراز هویت شده ای برای حذف ندارید •", show_alert=True)

    elif data.startswith("SelectCard-"):
        card_id = data.split("-")[1]
        card = get_card_by_id(card_id)
        if card:
            card_number = card["card_number"]
            masked_card = f"{card_number[:4]} - - - - - - {card_number[-4:]}"
            await app.edit_message_text(chat_id, m_id,
                                       f"**• آیا مطمئن هستید که میخواهید کارت [ `{masked_card}` ] را حذف کنید؟**",
                                       reply_markup=InlineKeyboardMarkup([
                                           [InlineKeyboardButton(text="بله", callback_data=f"ConfirmDelete-{card_id}"),
                                            InlineKeyboardButton(text="خیر", callback_data="AccVerify")]
                                       ]))

    elif data.startswith("ConfirmDelete-"):
        card_id = data.split("-")[1]
        card = get_card_by_id(card_id)
        if card:
            card_number = card["card_number"]
            bank_name = card["bank_name"] if card["bank_name"] else "نامشخص"
            masked_card = f"{card_number[:4]} - - - - - - {card_number[-4:]}"
            delete_card(card_id)
            await app.edit_message_text(chat_id, m_id,
                                       f"**• کارت ( `{bank_name}` - `{card_number}` ) با موفقیت حذف شد.**",
                                       reply_markup=InlineKeyboardMarkup([
                                           [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AccVerify")]
                                       ]))

    elif data == "WhatSelf":
        whatself_message = get_setting("whatself_message")
        await app.edit_message_text(chat_id, m_id, whatself_message, 
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="Back")]
                               ]))
        update_data(f"UPDATE user SET step = 'none' WHERE id = '{call.from_user.id}' LIMIT 1")

    elif data == "Support":
        await app.edit_message_text(chat_id, m_id, "**• شما با موفقیت به پشتیبانی متصل شدید!\nلطفا دقت کنید که توی پشتیبانی اسپم ندید و از دستورات سلف توی پشتیبانی استفاده نکنید، اکنون میتوانید پیام خود را ارسال کنید.**", reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="لغو اتصال 💥", callback_data="Back")
                ]
            ]
        ))
        update_data(f"UPDATE user SET step = 'support' WHERE id = '{call.from_user.id}' LIMIT 1")
    
    # در تابع callback_handler، بعد از هندلرهای موجود این موارد را اضافه کنید:

    elif data == "AdminSettings":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id,
                                   "**مدیر گرامی، به بخش تنظیمات خوش آمدید.\nلطفا گزینه مورد نظر را انتخاب کنید:**",
                                   reply_markup=AdminSettingsKeyboard)
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")

    elif data == "EditStartMessage":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            current_message = get_setting("start_message")
            await app.edit_message_text(chat_id, m_id,
                                   f"**متن فعلی پیام استارت:**\n\n{current_message}\n\n**لطفا متن جدید را ارسال کنید:**\n\n**نکته:** برای نمایش نام کاربر میتوانید از `{{user_link}}` استفاده کنید.",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                                   ]))
            update_data(f"UPDATE user SET step = 'edit_start_message' WHERE id = '{chat_id}' LIMIT 1")

    elif data == "EditPriceMessage":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            current_message = get_setting("price_message")
            await app.edit_message_text(chat_id, m_id,
                                   f"**متن فعلی پیام نرخ:**\n\n{current_message}\n\n**لطفا متن جدید را ارسال کنید:**\n\n**نکته:** برای نمایش قیمت‌ها میتوانید از متغیرهای زیر استفاده کنید:\n- `{{price_1month}}`\n- `{{price_2month}}`\n- `{{price_3month}}`\n- `{{price_4month}}`\n- `{{price_5month}}`\n- `{{price_6month}}`",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                                   ]))
            update_data(f"UPDATE user SET step = 'edit_price_message' WHERE id = '{chat_id}' LIMIT 1")

    elif data == "EditSelfMessage":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            current_message = get_setting("whatself_message")
            await app.edit_message_text(chat_id, m_id,
                                   f"**متن فعلی توضیح سلف:**\n\n{current_message}\n\n**لطفا متن جدید را ارسال کنید:**",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                                   ]))
            update_data(f"UPDATE user SET step = 'edit_self_message' WHERE id = '{chat_id}' LIMIT 1")

    elif data == "EditPrices":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            prices = get_prices()
            prices_text = "**قیمت‌های فعلی:**\n\n"
            prices_text += f"» 1 ماهه: {prices['1month']} تومان\n"
            prices_text += f"» 2 ماهه: {prices['2month']} تومان\n"
            prices_text += f"» 3 ماهه: {prices['3month']} تومان\n"
            prices_text += f"» 4 ماهه: {prices['4month']} تومان\n"
            prices_text += f"» 5 ماهه: {prices['5month']} تومان\n"
            prices_text += f"» 6 ماهه: {prices['6month']} تومان\n\n"
            prices_text += "**لطفا قیمت‌های جدید را به ترتیب زیر ارسال کنید (هر قیمت در یک خط):**\n\n"
            prices_text += "```\nقیمت 1 ماهه\nقیمت 2 ماهه\nقیمت 3 ماهه\nقیمت 4 ماهه\nقیمت 5 ماهه\nقیمت 6 ماهه\n```\n\n"
            prices_text += "**مثال:**\n```\n75000\n140000\n210000\n280000\n350000\n420000\n```"
    
            await app.edit_message_text(chat_id, m_id, prices_text,
                               reply_markup=InlineKeyboardMarkup([
                                   [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                               ]))
            update_data(f"UPDATE user SET step = 'edit_all_prices' WHERE id = '{chat_id}' LIMIT 1")

    elif data == "EditCardInfo":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            current_card = get_setting("card_number")
            current_name = get_setting("card_name")
        
            await app.edit_message_text(chat_id, m_id,
                                   f"**اطلاعات فعلی کارت:**\n\n**شماره کارت:** `{current_card}`\n**نام صاحب کارت:** {current_name}\n\n**لطفا گزینه مورد نظر را انتخاب کنید:**",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="تغییر شماره کارت", callback_data="EditCardNumber")],
                                       [InlineKeyboardButton(text="تغییر نام صاحب کارت", callback_data="EditCardName")],
                                       [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                                   ]))

    elif data == "EditCardNumber":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            current_card = get_setting("card_number")
            await app.edit_message_text(chat_id, m_id,
                                   f"**شماره کارت فعلی:** `{current_card}`\n\n**لطفا شماره کارت جدید را وارد کنید:**",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="EditCardInfo")]
                                   ]))
            update_data(f"UPDATE user SET step = 'edit_card_number' WHERE id = '{chat_id}' LIMIT 1")

    elif data == "EditCardName":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            current_name = get_setting("card_name")
            await app.edit_message_text(chat_id, m_id,
                                   f"**نام صاحب کارت فعلی:** {current_name}\n\n**لطفا نام جدید را وارد کنید:**",
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="EditCardInfo")]
                                   ]))
            update_data(f"UPDATE user SET step = 'edit_card_name' WHERE id = '{chat_id}' LIMIT 1")

    elif data == "ViewSettings":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            settings = get_all_settings()
            settings_text = "**تنظیمات فعلی ربات:**\n\n"
            for setting in settings:
                key = setting[1]
                value = setting[2][:50] + "..." if len(str(setting[2])) > 50 else setting[2]
                desc = setting[3]
                settings_text += f"**{desc}:**\n`{key}` = `{value}`\n\n"
        
            await app.edit_message_text(chat_id, m_id, settings_text,
                                   reply_markup=InlineKeyboardMarkup([
                                       [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                                   ]))
    
    elif data == "InstallSelf":
        if user["expir"] > 0:
            session_exists = os.path.isfile(f"sessions/{chat_id}.session") or os.path.isfile(f"sessions/{chat_id}.session-journal")
        
            if session_exists:
                await app.answer_callback_query(call.id, text="• سلف شما فعال است •", show_alert=True)
            else:
                await app.edit_message_text(chat_id, m_id,
                                        "**برای نصب سلف لطفا شماره تلفن خود را با دکمه زیر به اشتراک بگذارید:**",
                                        reply_markup=ReplyKeyboardMarkup(
                                            [[KeyboardButton(text="اشتراک گذاری شماره", request_contact=True)]],
                                            resize_keyboard=True
                                           ))
                update_data(f"UPDATE user SET step = 'install_self_contact' WHERE id = '{call.from_user.id}' LIMIT 1")
        else:
            await app.send_message(chat_id, m_id, "**شما انقضا ندارید.**")
    
    elif data == "ExpiryStatus":
        await app.answer_callback_query(call.id, text=f"انقضای شما : ( {expir} روز )", show_alert=True)

    elif data == "AdminPanel":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id, "**مدیر گرامی، به پنل ربات سلف ساز تلگرام خوش آمدید.\nاکنون ربات کاملا در اختیار شماست، در صورتی که آشنایی با پنل مدیریت یا کارکرد ربات ندارید، بخش « راهنما » را بخوانید.**", reply_markup=AdminPanelKeyboard)
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
            async with lock:
                if chat_id in temp_Client:
                    del temp_Client[chat_id]
        else:
            await app.answer_callback_query(call.id, text="**شما دسترسی به بخش مدیریت ندارید.**", show_alert=True)
    
    elif data == "AdminStats":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            botinfo = await app.get_me()
            allusers = get_datas("SELECT COUNT(id) FROM user")[0][0]
            allblocks = get_datas("SELECT COUNT(id) FROM block")[0][0]
            pending_cards = len(get_pending_cards())
            
            await app.edit_message_text(chat_id, m_id, f"""
            • تعداد کل کاربران ربات : **[ {allusers} ]**
            • تعداد کاربران بلاک شده :  **[ {allblocks} ]**
            • تعداد کارت های در انتضار تایید : **[ {pending_cards} ]**
            
            • نام ربات : **( {botinfo.first_name} )**
            • آیدی عددی ربات : **( `{botinfo.id}` )**
            • آیدی ربات : **( @{botinfo.username} )**
            """, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
    
    elif data == "AdminBroadcast":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id, f"**پیام خود را جهت ارسال همگانی، ارسال کنید.**\n\n• با ارسال پیام در این بخش، پیام شما برای تمامی کاربران ربات **ارسال** میشود.", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'admin_broadcast' WHERE id = '{chat_id}' LIMIT 1")
    
    elif data == "AdminForward":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id, f"**پیام خود را جهت فوروارد همگانی ارسال کنید.**\n\n• با ارسال پیام در این بخش، پیام شما برای تمامی کاربران ربات **فوروارد** میشود.", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'admin_forward' WHERE id = '{chat_id}' LIMIT 1")
    
    elif data == "AdminBlock":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id, "**آیدی عددی کاربر را جهت مسدود از ربات ارسال کنید:**", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'admin_block' WHERE id = '{chat_id}' LIMIT 1")
    
    elif data == "AdminUnblock":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id, "**آیدی عددی کاربر را جهت پاک کردن از لیست مسدود ها ارسال کنید:**", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'admin_unblock' WHERE id = '{chat_id}' LIMIT 1")
    
    elif data == "AdminAddExpiry":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id, "**• آیدی عددی کاربر را جهت افزایش انقضا ارسال کنید:**", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'admin_add_expiry1' WHERE id = '{chat_id}' LIMIT 1")
    
    elif data == "AdminDeductExpiry":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id, "**• آیدی عددی کاربر را جهت کسر انقضا ارسال کنید:**", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'admin_deduct_expiry1' WHERE id = '{chat_id}' LIMIT 1")
    
    elif data == "AdminActivateSelf":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id, "**آیدی عددی کاربر را جهت فعالسازی سلف ارسال کنید:**", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'admin_activate_self' WHERE id = '{chat_id}' LIMIT 1")
    
    elif data == "AdminDeactivateSelf":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            await app.edit_message_text(chat_id, m_id, "**آیدی عددی کاربر را جهت غیرفعال سازی سلف ارسال کنید:**", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'admin_deactivate_self' WHERE id = '{chat_id}' LIMIT 1")
    
    elif data == "AdminTurnOn":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            bot = get_data("SELECT * FROM bot")
            if bot["status"] != "ON":
                await app.edit_message_text(chat_id, m_id, "**• ربات روشن شد.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
                update_data(f"UPDATE bot SET status = 'ON' LIMIT 1")
            else:
                await app.answer_callback_query(call.id, text="**• ربات روشن بوده است.**", show_alert=True)
    
    elif data == "AdminTurnOff":
        if call.from_user.id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{call.from_user.id}' LIMIT 1") is not None:
            bot = get_data("SELECT * FROM bot")
            if bot["status"] != "OFF":
                await app.edit_message_text(chat_id, m_id, "**• ربات خاموش شد.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
                update_data(f"UPDATE bot SET status = 'OFF' LIMIT 1")
            else:
                await app.answer_callback_query(call.id, text="**• ربات خاموش بوده است.**", show_alert=True)
    
    elif data.startswith("AdminVerifyCard-"):
        params = data.split("-")
        user_id = int(params[1])
        card_number = params[2]
    
        bank_name = detect_bank(card_number)
        card = get_card_by_number(user_id, card_number)
    
        if card:
            update_card_status(card["id"], "verified", bank_name)
    
    # اصلاح: استفاده از call به جای m
        user_info = await app.get_users(user_id)
        username = f"@{user_info.username}" if user_info.username else "ندارد"
    
        await app.edit_message_text(call.message.chat.id, call.message.id, 
                               f"""**• درخواست احراز هویت از طرف ( {html.escape(user_info.first_name)} - {username} - {user_id} )
• شماره کارت : [ {card_number} ]

به دستور ( {call.from_user.id} ) تایید شد.**""")
    
        await app.send_message(user_id, f"**• درخواست احراز هویت کارت ( `{card_number}` ) تایید شد.\nشما هم اکنون میتوانید از بخش خرید / تمدید اشتراک ، خرید خود را انجام دهید.**")

    elif data.startswith("AdminRejectCard-"):
        params = data.split("-")
        user_id = int(params[1])
        card_number = params[2]
    
        card = get_card_by_number(user_id, card_number)
        if card:
            update_card_status(card["id"], "rejected")
    
    # اصلاح: استفاده از call به جای m
        user_info = await app.get_users(user_id)
        username = f"@{user_info.username}" if user_info.username else "ندارد"
    
        await app.edit_message_text(call.message.chat.id, call.message.id, 
                               f"""**• درخواست احراز هویت از طرف ( {html.escape(user_info.first_name)} - {username} - {user_id} )
• شماره کارت : [ {card_number} ]

به دستور ( {call.from_user.id} ) رد شد.**""")
    
        await app.send_message(user_id, f"**• درخواست احراز هویت کارت ( {card_number} ) به دلیل اشتباه بودن، رد شد.\nشما میتوانید مجددا برای احراز هویت با رعایت شرایط، درخواست دهید.**")

    elif data.startswith("AdminIncompleteCard-"):
        params = data.split("-")
        user_id = int(params[1])
        card_number = params[2]
    
        card = get_card_by_number(user_id, card_number)
        if card:
            update_card_status(card["id"], "rejected")
    
    # اصلاح: استفاده از call به جای m
        user_info = await app.get_users(user_id)
        username = f"@{user_info.username}" if user_info.username else "ندارد"
    
        await app.edit_message_text(call.message.chat.id, call.message.id, 
                               f"""**• درخواست احراز هویت از طرف ( {html.escape(user_info.first_name)} - {username} - {user_id} )
• شماره کارت : [ {card_number} ]

به دستور ( {call.from_user.id} ) رد شد.**""")
    
        await app.send_message(user_id, f"**• درخواست احراز هویت کارت ( {card_number} ) به دلیل ناقص بودن ، رد شد.\nشما میتوانید مجددا برای احراز هویت با رعایت شرایط، درخواست دهید.**")
    
    elif data.startswith("AdminApprovePayment-"):
        params = data.split("-")
        user_id = int(params[1])
        expir_count = int(params[2])
        cost = params[3]
        transaction_id = params[4]
        
        user_data = get_data(f"SELECT expir FROM user WHERE id = '{user_id}' LIMIT 1")
        old_expir = user_data["expir"] if user_data else 0
        new_expir = old_expir + expir_count
        
        update_data(f"UPDATE user SET expir = '{new_expir}' WHERE id = '{user_id}' LIMIT 1")
        
        await app.edit_message_text(Admin, m_id, f"**پرداخت کاربر [ `{user_id}` ] تایید شد.\n\n• شناسه تراکنش : [ `{transaction_id}` ]\n• انقضای جدید کاربر : [ `{new_expir} روز` ]**")
        
        await app.send_message(user_id, f"**پرداخت شما تایید شد.**\n\n•شناسه تراکنش : **[ {transaction_id} ]**\n• انقضای سلف شما ( **{expir_count}** ) روز اضافه گردید.\n\n**انقضای قبلی شما : ( `{old_expir}` ) روز\n\n• انقضای جدید : ( `{new_expir}` ) روز**")
    
    elif data.startswith("AdminRejectPayment-"):
        params = data.split("-")
        user_id = int(params[1])
        transaction_id = params[2]
        
        await app.edit_message_text(Admin, m_id,f"**• پرداخت کاربر [ `{user_id}` ] رد شد.**")
        
        await app.edit_message_text(user_id, f"**پرداخت شما رد گردید.\n\n•شناسه تراکنش : [ `{transaction_id}` ]\n• افزایش انقضای شما به دلیل ارسال فیش واربزی اشتباه رد شده و درخواست شما لغو گردید.\n• در صورتی که غکر میکنید اشتباه شده است، شناسه تراکنش را به پشتیبانی ارسال کرده و با پشتیان ها در ارتباط باشید.**")
    
    elif data.startswith("AdminBlockPayment-"):
        user_id = int(data.split("-")[1])
        
        update_data(f"INSERT INTO block(id) VALUES({user_id})")
        
        await app.edit_message_text(Admin, m_id, f"**• کاربر [ `{user_id}` ] از ربات مسدود شد.**")
        
        await app.send_message(user_id, f"**شما به دلیل نقض قوانین از ربات مسدود شده اید.\n• با پشتیبان ها در ارتباط باشید.**")
    
    elif data.startswith("Reply-"):
        user_id = int(data.split("-")[1])  # استخراج آیدی کاربر
        user_info = await app.get_users(user_id)
        await app.send_message(
            Admin,
            f"**• پیام خود را جهت پاسخ به کاربر [ {html.escape(user_info.first_name)} ] ارسال کنید:**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            )
        )
        update_data(f"UPDATE user SET step = 'ureply-{user_id}' WHERE id = '{Admin}' LIMIT 1")

    elif data.startswith("Block-"):
        user_id = int(data.split("-")[1])  # استخراج آیدی کاربر
        user_info = await app.get_users(user_id)
        block = get_data(f"SELECT * FROM block WHERE id = '{user_id}' LIMIT 1")
        if block is None:
            await app.send_message(user_id, "**شما به دلیل نقض قوانین از ربات مسدود شدید.**")
            await app.send_message(Admin, f"**• کاربر [ {html.escape(user_info.first_name)} ] از ربات مسدود شد.**")
            update_data(f"INSERT INTO block(id) VALUES({user_id})")
        else:
            await app.send_message(Admin, f"**• کاربر [ {html.escape(user_info.first_name)} ] از قبل بلاک بوده است.**")

    elif data == "Back":
        keyboard = get_main_keyboard(call.from_user.id)
        await app.edit_message_text(chat_id, m_id, f"**‌ ‌ ‌ ‌ \nبه منوی اصلی بازگشتید.\n\nلطفا اگر سوالی دارید از بخش پشتیبانی ، با پشتیبان ها در ارتباط باشید.\n\n‌ ‌ ‌ ‌ ‌ ‌ ‌ لطفا انتخاب کنید:**\n\n", reply_markup=keyboard)
        update_data(f"UPDATE user SET step = 'none' WHERE id = '{call.from_user.id}' LIMIT 1")
        async with lock:
            if chat_id in temp_Client:
                del temp_Client[chat_id]
    
    elif data == "text":
        await app.answer_callback_query(call.id, text="• دکمه نمایش است •", show_alert=True)


@app.on_message(filters.contact)
@checker
async def contact_handler(c, m):
    user = get_data(f"SELECT * FROM user WHERE id = '{m.chat.id}' LIMIT 1")
    if user["step"] == "contact":
        phone_number = str(m.contact.phone_number)
        if not phone_number.startswith("+"):
            phone_number = f"+{phone_number}"
        contact_id = m.contact.user_id
        if m.contact and m.chat.id == contact_id:
            mess = await app.send_message(m.chat.id, "**• شماره شما با موفقیت ذخیره شد.\nاکنون میتوانید از بخش خرید استفاده کنید.\n\nربات رو مجددا [ /start ] کنید.**", reply_markup=ReplyKeyboardRemove())
            update_data(f"UPDATE user SET phone = '{phone_number}' WHERE id = '{m.chat.id}' LIMIT 1")
            
        else:
            await app.send_message(m.chat.id, "**• با استفاده از دکمه « اشتراک گذاری شماره » شماره تلفن را ارسال نمایید.**")
            
    elif user["step"] == "install_self_contact":
        phone_number = str(m.contact.phone_number)
        if not phone_number.startswith("+"):
            phone_number = f"+{phone_number}"
        contact_id = m.contact.user_id
        
        if m.contact and m.chat.id == contact_id:
            update_data(f"UPDATE user SET phone = '{phone_number}' WHERE id = '{m.chat.id}' LIMIT 1")
            await app.send_message(m.chat.id, "**شماره شما ثبت شد.**",
                                 reply_markup=ReplyKeyboardRemove())
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{m.chat.id}' LIMIT 1")
            
        else:
            await app.send_message(m.chat.id, "**• با استفاده از دکمه « اشتراک گذاری شماره » شماره تلفن را ارسال نمایید.**")


@app.on_message(filters.private)
@checker
async def message_handler(c, m):
    global temp_Client
    user = get_data(f"SELECT * FROM user WHERE id = '{m.chat.id}' LIMIT 1")
    username = f"@{m.from_user.username}" if m.from_user.username else "وجود ندارد"
    expir = user["expir"] if user else 0
    chat_id = m.chat.id
    text = m.text
    m_id = m.id

    if user["step"] == "card_photo":
        if m.photo:
            photo_path = await m.download(file_name=f"cards/{chat_id}_{int(time.time())}.jpg")
            update_data(f"UPDATE user SET step = 'card_number-{photo_path}-{m_id}' WHERE id = '{m.chat.id}' LIMIT 1")
            
            await app.send_message(chat_id,
                                 "**• لطفا شماره کارت خود را به صورت اعداد انگلیسی ارسال کنید.\nدر صورتی که منصرف شدید ربات را مجدد [ /start ] کنید.**")
        else:
            await app.send_message(chat_id, "**• فقط ارسال عکس مجاز است.**")

    elif user["step"].startswith("card_number-"):
        if text and text.isdigit() and len(text) == 16:
            parts = user["step"].split("-", 2)
            photo_path = parts[1]
            photo_message_id = parts[2] if len(parts) > 2 else None
        
            card_number = text.strip()
    
            add_card(chat_id, card_number)
    
            if photo_message_id:
                try:
                    forwarded_photo_msg = await app.forward_messages(
                        from_chat_id=chat_id,
                        chat_id=Admin,
                        message_ids=int(photo_message_id)
                    )
                
                    await app.send_message(
                        Admin,
                        f"""**• درخواست احراز هویت از طرف ( {html.escape(m.chat.first_name)} - @{m.from_user.username if m.from_user.username else 'ندارد'} - {m.chat.id} )
شماره کارت : [ {card_number} ]**""",  # تغییر m به message
                        reply_to_message_id=forwarded_photo_msg.id,
                        reply_markup=InlineKeyboardMarkup([
                            [
                                InlineKeyboardButton(text="تایید (✅)", callback_data=f"AdminVerifyCard-{chat_id}-{card_number}")
                            ],
                            [
                                InlineKeyboardButton(text="اشتباه (❌)", callback_data=f"AdminRejectCard-{chat_id}-{card_number}"),
                                InlineKeyboardButton(text="کامل نیست (❌)", callback_data=f"AdminIncompleteCard-{chat_id}-{card_number}")
                            ]
                        ])
                    )
                except Exception as e:
                    await app.send_message(
                        Admin,
                        f"""**• درخواست احراز هویت از طرف ({html.escape(m.chat.first_name)} - @{m.from_user.username if m.from_user.username else 'ندارد'} - {m.chat.id})
شماره کارت : [ {card_number} ]**""",  # تغییر m به message
                        reply_markup=InlineKeyboardMarkup([
                            [
                                InlineKeyboardButton(text="تایید (✅)", callback_data=f"AdminVerifyCard-{chat_id}-{card_number}"),
                                InlineKeyboardButton(text="اشتباه (❌)", callback_data=f"AdminRejectCard-{chat_id}-{card_number}"),
                                InlineKeyboardButton(text="کامل نیست (❌)", callback_data=f"AdminIncompleteCard-{chat_id}-{card_number}")
                            ]
                        ])
                    )
            else:
                await app.send_message(
                    Admin,
                    f"""**• درخواست احراز هویت از طرف ({html.escape(m.chat.first_name)} - @{m.from_user.username if m.from_user.username else 'ندارد'} - {m.chat.id})
شماره کارت : [ {card_number} ]**""",  # تغییر m به message
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton(text="تایید (✅)", callback_data=f"AdminVerifyCard-{chat_id}-{card_number}"),
                            InlineKeyboardButton(text="اشتباه (❌)", callback_data=f"AdminRejectCard-{chat_id}-{card_number}"),
                            InlineKeyboardButton(text="کامل نیست (❌)", callback_data=f"AdminIncompleteCard-{chat_id}-{card_number}")
                        ]
                    ])
                )
    
            await app.send_message(chat_id,
                            """**• درخواست احراز هویت شما برای پشتیبانی ارسال شد و در اولین فرصت تایید خواهد شد ، لطفا صبور باشید.

لطفا برای تایید کارت به پشتیبانی پیام ارسال نفرمایید و درخواست احرازهویتتون رو اسپم نکنید ، در صورت مشاهده این کار یک روز با تاخیر تایید میشود.**""")
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{m.chat.id}' LIMIT 1")  # تغییر m به message
        else:
            await app.send_message(chat_id, "**شماره کارت باید 16 رقم باشد.**\n• در صورتی که منصرف شدید ربات رو مجددا [ /start ] کنید.**")

    elif user["step"].startswith("payment_receipt-"):
        if m.photo:
            params = user["step"].split("-")
            expir_count = params[1]
            cost = params[2]
            card_id = params[3]
            
            card = get_card_by_id(card_id)
            card_number = card["card_number"] if card else "نامشخص"
            
            mess = await app.forward_messages(from_chat_id=chat_id, chat_id=Admin, message_ids=m_id)
            
            transaction_id = str(int(time.time()))[-11:]
            
            await app.send_message(Admin,
                                 f"""**• درخواست خرید اشتراک از طرف ( {html.escape(m.chat.first_name)} - @{m.from_user.username if m.from_user.username else 'ندارد'} - {m.chat.id} )
اشتراک انتخاب شده : ( `{cost} تومان - {expir_count} روز` )
کارت خرید : ( `{card_number}` )**""",
                                 reply_to_message_id=mess.id,
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton(text="تایید (✅)", callback_data=f"AdminApprovePayment-{chat_id}-{expir_count}-{cost}-{transaction_id}"),
                                      InlineKeyboardButton(text="مسدود (❌)", callback_data=f"AdminBlockPayment-{chat_id}"),
                                      InlineKeyboardButton(text="رد (❌)", callback_data=f"AdminRejectPayment-{chat_id}-{transaction_id}")]
                                 ]))
            
            await app.send_message(chat_id,
                                 f"""**فیش واریزی شما ارسال شد.
• شناسه تراکنش: [ `{transaction_id}` ]
منتظر تایید فیش توسط مدیر باشید.**""")
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{m.chat.id}' LIMIT 1")
        else:
            await app.send_message(chat_id, "**فقط عکس فیش واریزی را ارسال کنید.**")

    elif user["step"] == "support":
        mess = await app.forward_messages(from_chat_id=chat_id, chat_id=Admin, message_ids=m_id)
        await app.send_message(Admin, f"""**
• پیام جدید از طرف ( {html.escape(m.chat.first_name)} - `{m.chat.id}` - {username} )**\n
""", reply_to_message_id=mess.id, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("پاسخ (✅)", callback_data=f"Reply-{m.chat.id}"),
                InlineKeyboardButton("مسدود (❌)", callback_data=f"Block-{m.chat.id}")
            ]
        ]
    ))
        await app.send_message(chat_id, "**• پیام شما به پشتیبانی ارسال شد.\nلطفا در بخش پشتیبانی اسپم نکنید و از دستورات استفاده نکنید به پیام شما در اسرع وقت پاسخ داده خواهد شد.**", reply_to_message_id=m_id)
    
    # در تابع message_handler، بعد از هندلرهای موجود این موارد را اضافه کنید:

    elif user["step"] == "edit_start_message":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            update_setting("start_message", text)
            await app.send_message(chat_id, "**✅ متن پیام استارت با موفقیت به‌روزرسانی شد.**",
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                             ]))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")

    elif user["step"] == "edit_price_message":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            update_setting("price_message", text)
            await app.send_message(chat_id, "**✅ متن پیام نرخ با موفقیت به‌روزرسانی شد.**",
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                             ]))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")

    elif user["step"] == "edit_self_message":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            update_setting("whatself_message", text)
            await app.send_message(chat_id, "**✅ متن توضیح سلف با موفقیت به‌روزرسانی شد.**",
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                             ]))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")

    elif user["step"] == "edit_all_prices":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
        # تقسیم متن به خطوط
            lines = text.strip().split('\n')
        
        # بررسی تعداد خطوط
            if len(lines) != 6:
                await app.send_message(chat_id, "**خطا: باید دقیقا 6 قیمت (هر قیمت در یک خط) وارد کنید.**\n\n**فرمت صحیح:**\n```\nقیمت 1 ماهه\nقیمت 2 ماهه\nقیمت 3 ماهه\nقیمت 4 ماهه\nقیمت 5 ماهه\nقیمت 6 ماهه\n```",
                                reply_markup=InlineKeyboardMarkup([
                                    [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                                ]))
                return
        
        # تعریف کلیدهای قیمت‌ها
            price_keys = ['1month', '2month', '3month', '4month', '5month', '6month']
            price_names = {
                '1month': '1 ماهه',
                '2month': '2 ماهه', 
                '3month': '3 ماهه',
                '4month': '4 ماهه',
                '5month': '5 ماهه',
                '6month': '6 ماهه'
            }
        
        # بررسی اعتبار هر قیمت
            valid_prices = []
            errors = []
        
            for i, line in enumerate(lines):
                price_text = line.strip()
                if not price_text.isdigit():
                    errors.append(f"قیمت {price_names[price_keys[i]]} باید عدد باشد: {price_text}")
                else:
                    valid_prices.append((price_keys[i], price_text))
        
        # اگر خطا وجود دارد
            if errors:
                error_text = "**خطا در ورود قیمت‌ها:**\n\n"
                for error in errors:
                    error_text += f"• {error}\n"
                error_text += "\n**لطفا مجددا تلاش کنید.**"
            
                await app.send_message(chat_id, error_text,
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                                ]))
                update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
                return
        
        # ذخیره قیمت‌های جدید
            success_text = "**✅ قیمت‌ها با موفقیت به‌روزرسانی شد:**\n\n"
            for key, price in valid_prices:
                update_setting(f"price_{key}", price)
                success_text += f"**{price_names[key]}:** {price} تومان\n"
        
            success_text += "\n**تغییرات ذخیره شدند.**"
        
            await app.send_message(chat_id, success_text,
                            reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                            ]))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")

    elif user["step"] == "edit_card_number":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            if text.replace(" ", "").isdigit() and len(text.replace(" ", "")) >= 16:
                update_setting("card_number", text.replace(" ", ""))
                await app.send_message(chat_id, f"**✅ شماره کارت با موفقیت به `{text}` به‌روزرسانی شد.**",
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                                 ]))
                update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
            else:
                await app.send_message(chat_id, "**شماره کارت نامعتبر است. لطفا یک شماره کارت معتبر وارد کنید.**")

    elif user["step"] == "edit_card_name":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            update_setting("card_name", text)
            await app.send_message(chat_id, f"**✅ نام صاحب کارت با موفقیت به `{text}` به‌روزرسانی شد.**",
                             reply_markup=InlineKeyboardMarkup([
                                 [InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminSettings")]
                             ]))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
    
    elif user["step"] == "admin_broadcast":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            mess = await app.send_message(chat_id, "**• ارسال پیام شما درحال انجام است، لطفا صبور باشید.**")
            users = get_datas(f"SELECT id FROM user")
            for user in users:
                await app.copy_message(from_chat_id=chat_id, chat_id=user[0], message_id=m_id)
                await asyncio.sleep(0.1)
            await app.edit_message_text(chat_id, mess.id, "**• پیام شما به تمامی کاربران ارسال شد.**", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
    
    elif user["step"] == "admin_forward":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            mess = await app.send_message(chat_id, "**• فوروارد پیام شما درحال انجام است، لطفا صبور باشید.**")
            users = get_datas(f"SELECT id FROM user")
            for user in users:
                await app.forward_messages(from_chat_id=chat_id, chat_id=user[0], message_ids=m_id)
                await asyncio.sleep(0.1)
            await app.edit_message_text(chat_id, mess.id, "**• پیام شما به تمامی کاربران فوروارد شد.**", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
            ))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
    
    elif user["step"] == "admin_block":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            if text.isdigit():
                user_id = int(text.strip())
                if get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1") is not None:
                    block = get_data(f"SELECT * FROM block WHERE id = '{user_id}' LIMIT 1")
                    if block is None:
                        await app.send_message(user_id, f"**شما به دلیل نقض قوانین از ربات مسدود شدید.\n• با پشتیان ها در ارتباط باشید.**")
                        await app.send_message(chat_id, f"**کاربر [ `{user_id}` ] از ربات مسدود شد.**", reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                        ))
                        update_data(f"INSERT INTO block(id) VALUES({user_id})")
                    else:
                        await app.send_message(chat_id, f"**کاربر [ `{user_id}` ] از ربات مسدود شد.**", reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                        ))
                else:
                    await app.send_message(chat_id, "**کاربر پیدا نشد.\n• ابتدا آیدی کاربر را بررسی کرده و از ربات بخواهید ربات را [ /start ] کند.**", reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                    ))
            else:
                await app.send_message(chat_id, "**فقط ارسال عدد مجاز است.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
    
    elif user["step"] == "admin_unblock":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            if text.isdigit():
                user_id = int(text.strip())
                if get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1") is not None:
                    block = get_data(f"SELECT * FROM block WHERE id = '{user_id}' LIMIT 1")
                    if block is not None:
                        await app.send_message(user_id, f"**شما توسط مدیر از لیست سیاه ربات خارج شدید.\n• اکنون میتوانید از ربات استفاده کنید.**")
                        await app.send_message(chat_id, f"**کاربر [ `{user_id}` ] از لیست سیاه خارج شد.**", reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                        ))
                        update_data(f"DELETE FROM block WHERE id = '{user_id}' LIMIT 1")
                    else:
                        await app.send_message(chat_id, f"**کاربر [ `{user_id}` ] در لیست سیاه وجود ندارد.**", reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                        ))
                else:
                    await app.send_message(chat_id, "**کاربر پیدا نشد.\n•ابتدا آیدی ربات را بررسی کرده و از کاربر بخواهید ربات را [ /start ] کند.**", reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                    ))
            else:
                await app.send_message(chat_id, "**فقط ارسال عدد مجاز است.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
    
    elif user["step"] == "admin_add_expiry1":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            if text.isdigit():
                user_id = int(text.strip())
                if get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1") is not None:
                    await app.send_message(chat_id, "**• آیدی عددی کاربر را جهت افزایش انقضا ارسال کنید.**", reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                    ))
                    update_data(f"UPDATE user SET step = 'admin_add_expiry2-{user_id}' WHERE id = '{chat_id}' LIMIT 1")
                else:
                    await app.send_message(chat_id, f"**کاربر پیدا نشد.\n• ابتدا آیدی کاربر را بررسی کرده و از کاربر بخواهید ربات را [ /start ] کند.**", reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                    ))
            else:
                await app.send_message(chat_id, "**فقط ارسال عدد مجاز است.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
    
    elif user["step"].startswith("admin_add_expiry2"):
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            if text.isdigit():
                user_id = int(user["step"].split("-")[1])
                count = int(text.strip())
                user_expir = get_data(f"SELECT expir FROM user WHERE id = '{user_id}' LIMIT 1")
                user_upexpir = int(user_expir["expir"]) + int(count)
                update_data(f"UPDATE user SET expir = '{user_upexpir}' WHERE id = '{user_id}' LIMIT 1")
                
                await app.send_message(user_id, f"**افزایش انقضا برای شما انجام شد.\n• ( `{count}` روز ) به انقضای شما اضافه گردید.\n\n• انقضای جدید شما : ( {user_upexpir} روز )\n")
                
                await app.send_message(chat_id, f"**افزایش انقضا برای کاربر [ `{user_id}` ] انجام شد.\n\n• انقضای اضافه شده: ( `{count}` روز )\n• انقضای جدید کاربر : ( `{user_upexpir}` روز )**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
                update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
            else:
                await app.send_message(chat_id, "**فقط ارسال عدد مجاز است.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
    
    elif user["step"] == "admin_deduct_expiry1":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            if text.isdigit():
                user_id = int(text.strip())
                if get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1") is not None:
                    await app.send_message(chat_id, "**زمان انقضای موردنظر را برای کاهش ارسال کنید:**", reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                    ))
                    update_data(f"UPDATE user SET step = 'admin_deduct_expiry2-{user_id}' WHERE id = '{chat_id}' LIMIT 1")
                else:
                    await app.send_message(chat_id, f"**کاربر پیدا نشد.\n• ابتدا آیدی کاربر را بررسی کرده و از کاربر بخواهید ربات را [ /start ] کند.**", reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                    ))
            else:
                await app.send_message(chat_id, "**فقط ارسال عدد مجاز است.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
    
    elif user["step"].startswith("admin_deduct_expiry2"):
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            if text.isdigit():
                user_id = int(user["step"].split("-")[1])
                count = int(text.strip())
                user_expir = get_data(f"SELECT expir FROM user WHERE id = '{user_id}' LIMIT 1")
                user_upexpir = int(user_expir["expir"]) - int(count)
                update_data(f"UPDATE user SET expir = '{user_upexpir}' WHERE id = '{user_id}' LIMIT 1")
                
                await app.send_message(user_id, f"**کسر انقضا برای شما انجام شد.\n\nانقضای جدید شما : ( `{user_upexpir}` روز )\n\n• انقضای کسر شده ؛ ( `{count}` روز )**")
                
                await app.send_message(chat_id, f"**کسر انقضا برای کاربر [ `{user_id}` ] انجام شد.\n\n• انقضای کسر شده: ( `{count}` روز )\n• انقضای جدید کاربر : ( `{user_upexpir}` روز )**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
                update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
            else:
                await app.send_message(chat_id, "**فقط ارسال عدد مجاز است.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
    
    elif user["step"] == "admin_activate_self":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            if text.isdigit():
                user_id = int(text.strip())
                if get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1") is not None:
                    if os.path.isfile(f"sessions/{user_id}.session-journal"):
                        user_data = get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1")
                        if user_data["self"] != "active":
                            mess = await app.send_message(chat_id, f"**• اشتراک سلف برای کاربر [ `{user_id}` ] درحال فعالسازی است، لطفا صبور باشید.**")
                            process = subprocess.Popen(["python3", "self.py", str(user_id), str(API_ID), API_HASH, Helper_ID], cwd=f"selfs/self-{user_id}")
                            await asyncio.sleep(10)
                            if process.poll() is None:
                                await app.edit_message_text(chat_id, mess.id, f"**• ربات سلف با موفقیت برای کاربر [ `{user_id}` ] فعال شد.**", reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                                ))
                                update_data(f"UPDATE user SET self = 'active' WHERE id = '{user_id}' LIMIT 1")
                                update_data(f"UPDATE user SET pid = '{process.pid}' WHERE id = '{user_id}' LIMIT 1")
                                add_admin(user_id)
                                await setscheduler(user_id)
                                await app.send_message(user_id, f"**• اشتراک سلف توسط مدیریت برای شما فعال شد.\nاکنون مجاز به استفاده از ربات دستیار میباشید.**")
                            else:
                                await app.edit_message_text(chat_id, mess.id, f"**فعالسازی سلف برای کاربر [ `{user_id}` ] با خطا مواجه شد.**", reply_markup=InlineKeyboardMarkup(
                                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                                ))
                        else:
                            await app.send_message(chat_id, f"**اشتراک سلف برای کاربر [ `{user_id}` ] غیرفعال بوده است.**", reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                            ))
                    else:
                        await app.send_message(chat_id, f"**کاربر [ `{user_id}` ] اشتراک فعالی ندارد.**", reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                        ))
                else:
                    await app.send_message(chat_id, "**کاربر یافت نشد، ابتدا از کاربر بخواهید ربات را [ /start ] کند.**", reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                    ))
            else:
                await app.send_message(chat_id, "**فقط ارسال عدد مجاز است.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
    
    elif user["step"] == "admin_deactivate_self":
        if chat_id == Admin or helper_getdata(f"SELECT * FROM adminlist WHERE id = '{chat_id}' LIMIT 1") is not None:
            if text.isdigit():
                user_id = int(text.strip())
                if get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1") is not None:
                    if os.path.isfile(f"sessions/{user_id}.session-journal"):
                        user_data = get_data(f"SELECT * FROM user WHERE id = '{user_id}' LIMIT 1")
                        if user_data["self"] != "inactive":
                            mess = await app.send_message(chat_id, "**• درحال پردازش، لطفا صبور باشید.**")
                            try:
                                os.kill(user_data["pid"], signal.SIGKILL)
                            except:
                                pass
                            await app.edit_message_text(chat_id, mess.id, f"**• ربات سلف برای کاربر [ `{user_id}` ] غیرفعال شد.**", reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                            ))
                            update_data(f"UPDATE user SET self = 'inactive' WHERE id = '{user_id}' LIMIT 1")
                            if user_id != Admin:
                                delete_admin(user_id)
                            job = scheduler.get_job(str(user_id))
                            if job:
                                scheduler.remove_job(str(user_id))
                            await app.send_message(user_id, f"**کاربر [ `{user_id}` ] سلف شما به دلایلی غیرفعال شد، لطفا با پشتیبان ها در ارتباط باشید.**")
                        else:
                            await app.send_message(chat_id, f"**ربات سلف از قبل برای کاربر [ `{user_id}` ] غیرفعال بوده است.**", reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                            ))
                    else:
                        await app.send_message(chat_id, f"**کاربر [ `{user_id}` ] انقضای فعالی ندارد.**", reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                        ))
                else:
                    await app.send_message(chat_id, "**کاربر یافت نشد، ابتدا از کاربر بخواهید ربات را [ /start ] کند.**", reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                    ))
            else:
                await app.send_message(chat_id, "**فقط ارسال عدد مجاز است.**", reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
                ))
            update_data(f"UPDATE user SET step = 'none' WHERE id = '{chat_id}' LIMIT 1")
            
    elif user["step"].startswith("ureply-"):
        user_id = int(user["step"].split("-")[1])
        mess = await app.copy_message(from_chat_id=Admin, chat_id=user_id, message_id=m_id)
        await app.send_message(user_id, "**• کاربر گرامی، پاسخ شما از پشتیبانی دریافت شد.**", reply_to_message_id=mess.id)
        await app.send_message(Admin, "**• پیام شما برای کاربر ارسال شد.**", reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="(🔙) بازگشت", callback_data="AdminPanel")]]
        ))
        update_data(f"UPDATE user SET step = 'none' WHERE id = '{Admin}' LIMIT 1")


#================== Run ===================#
app.start()
print(Fore.YELLOW + "Ultra Self Bot v2.0.0 Started...")
print(Fore.GREEN + f"Bot is running as: @{(app.get_me()).username}")
print(Fore.CYAN + "Press Ctrl+C to stop the bot")
idle()
app.stop()