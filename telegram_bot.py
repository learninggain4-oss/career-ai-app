import telebot
import os
import shutil
import time

# PUTHIYA TOKEN IVide - GitHub-il push cheyyaruth!
TOKEN = "8621404692:AAGmsx1P6QeapisDJc59-XoflC4pHzwoB9Y"
FOLDER = "E:/python_practice"

bot = telebot.TeleBot(TOKEN)

# Organize cheyyenda rules
RULES = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "PythonFiles": [".py"],
    "TextReports": [".txt", ".csv"],
}

@bot.message_handler(commands=['start', 'help'])
def start(msg):
    bot.reply_to(msg,
        "Hi! Njan ready aanu 🚀\n\n"
        "Commands:\n"
        "/organize - Files organize cheyyam\n"
        "/list - Folder-il enthu undu ennu nokkam\n"
        "/help - Ithu kanam"
    )

@bot.message_handler(commands=['organize'])
def organize_files(msg):
    bot.reply_to(msg, "Organizing... ⏳")
    moved = 0
    try:
        for file in os.listdir(FOLDER):
            file_path = os.path.join(FOLDER, file)
            if os.path.isfile(file_path):
                # telegram_bot.py thanne move aakaruth
                if "telegram_bot" in file:
                    continue
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
        bot.reply_to(msg, f"Done! {moved} files organized ✅")
    except Exception as e:
        bot.reply_to(msg, f"Error: {e}")

@bot.message_handler(commands=['list'])
def list_files(msg):
    try:
        files = os.listdir(FOLDER)
        # Folders ozhichu 20 files mathram kanikkam
        only_files = [f for f in files if os.path.isfile(os.path.join(FOLDER, f))][:15]
        if not only_files:
            bot.reply_to(msg, "Folder clean aanu! Organize cheyyan onnum illa 👌")
        else:
            bot.reply_to(msg, "Root-il ulla files:\n" + "\n".join(only_files))
    except Exception as e:
        bot.reply_to(msg, f"Error: {e}")

# Ithu aanu "hello" fix - eth text ayachalum reply tharum
@bot.message_handler(func=lambda message: True)
def echo_all(msg):
    text = msg.text.lower()
    if "hello" in text or "hi" in text or "hey" in text:
        bot.reply_to(msg, "Hello da! 😊 /organize adikku, njan clean cheyyam")
    elif "thanks" in text or "thank" in text:
        bot.reply_to(msg, "Welcome bro! 🙏")
    else:
        bot.reply_to(msg, f"Nee paranjathu: {msg.text}\n\nEnikku manassilayilla. Use cheyy: /organize, /list, /start")

print("Bot started... Telegram-il /start adikku")
# Timeout varanda irikkan loop
while True:
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=30)
    except Exception as e:
        print(f"Connection lost, retrying in 5 sec... {e}")
        time.sleep(5)