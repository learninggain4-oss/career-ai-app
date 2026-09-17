import os
from dotenv import load_dotenv
load_dotenv() #.env file-il ninnu token edukkum

import telebot
import shutil
import time
import threading
from flask import Flask

# SAFE - Token.env-il ninnu, GitHub-il pokilla
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN.env-il illa!.env file check cheyy")

FOLDER = os.getenv("LOCAL_FOLDER") or "E:/python_practice"

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running 24/7! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

bot = telebot.TeleBot(TOKEN)

# Move aakarutha important files
IGNORE_FILES = [
    "requirements.txt", "README.md", "telegram_bot.py",
    "streamlit_app.py", ".gitignore", ".env", "app.py"
]

RULES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "PythonFiles": [".py"],
    "TextReports": [".txt", ".csv"],
}

@bot.message_handler(commands=['start', 'help'])
def start(msg):
    bot.reply_to(msg,
        "Hi! Njan ready aanu 🚀 24/7 SAFE mode\n\n"
        "/organize - Files organize cheyyam\n"
        "/list - Root files nokkam\n"
        "/help - Help"
    )

@bot.message_handler(commands=['organize'])
def organize_files(msg):
    bot.reply_to(msg, "Organizing... ⏳")
    moved = 0
    try:
        if not os.path.exists(FOLDER):
            bot.reply_to(msg, "Njan ippo Render cloud-il aanu, laptop files ivide illa 😉")
            return

        for file in os.listdir(FOLDER):
            if file in IGNORE_FILES:
                continue
            if "telegram" in file.lower():
                continue

            file_path = os.path.join(FOLDER, file)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file)[1].lower()
                for target_folder, exts in RULES.items():
                    if ext in exts:
                        dest_folder = os.path.join(FOLDER, target_folder)
                        os.makedirs(dest_folder, exist_ok=True)
                        try:
                            shutil.move(file_path, os.path.join(dest_folder, file))
                            moved += 1
                        except:
                            pass
                        break

        if moved == 0:
            bot.reply_to(msg, "Already clean aanu! 👌 0 files")
        else:
            bot.reply_to(msg, f"Done! {moved} files organized ✅")
    except Exception as e:
        bot.reply_to(msg, f"Error: {e}")

@bot.message_handler(commands=['list'])
def list_files(msg):
    try:
        if not os.path.exists(FOLDER):
            bot.reply_to(msg, "Cloud-il aanu, local files illa")
            return
        files = os.listdir(FOLDER)
        only_files = [f for f in files if os.path.isfile(os.path.join(FOLDER, f))][:20]
        if not only_files:
            bot.reply_to(msg, "Folder clean aanu! 👌")
        else:
            bot.reply_to(msg, "Root files:\n" + "\n".join(only_files))
    except Exception as e:
        bot.reply_to(msg, f"Error: {e}")

@bot.message_handler(func=lambda message: True)
def echo_all(msg):
    txt = msg.text.lower()
    if "hello" in txt or "hi" in txt or "hey" in txt:
        bot.reply_to(msg, "Hello da! 😊 /organize adikku")
    elif "thanks" in txt:
        bot.reply_to(msg, "Welcome! 🙏")
    else:
        bot.reply_to(msg, f"Got it: {msg.text}\nUse: /organize, /list, /start")

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("Bot + Flask started... 24/7 SAFE mode")
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=30)
        except Exception as e:
            print(f"Retry in 5 sec... {e}")
            time.sleep(5)