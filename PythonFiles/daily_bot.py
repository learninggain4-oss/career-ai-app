import time
import os
import shutil
from datetime import datetime

def organize():
    folder = "E:/python_practice"
    print(f"{datetime.now()} - Auto organizing...")
    # same logic
    rules = { "Images": [".png",".jpg"], "PythonFiles": [".py"], "TextReports": [".txt"] }
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path) and not file.startswith("daily_bot"):
            ext = os.path.splitext(file)[1].lower()
            for target, exts in rules.items():
                if ext in exts:
                    dest = os.path.join(folder, target)
                    os.makedirs(dest, exist_ok=True)
                    try:
                        shutil.move(path, os.path.join(dest, file))
                        print(f"Moved {file}")
                    except: pass
                    break

print("Bot started - will run every day 2:44 AM. Keep this window open.")
while True:
    now = datetime.now()
    if now.hour == 3 and now.minute == 49:
        organize()
        time.sleep(60) # 1 min wait to avoid repeat
    time.sleep(30)