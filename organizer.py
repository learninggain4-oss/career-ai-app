import os
import shutil

# Ninte practice folder thanne organize cheyyam
folder = "E:/python_practice"
print(f"Scanning: {folder}")

# Ethu file evide pokanam
rules = {
    "Images": [".png", ".jpg", ".jpeg"],
    "PythonFiles": [".py"],
    "TextReports": [".txt"],
    "Data": [".csv", ".xlsx"]
}

for file in os.listdir(folder):
    path = os.path.join(folder, file)
    if os.path.isfile(path):
        ext = os.path.splitext(file)[1].lower()
        for target, exts in rules.items():
            if ext in exts:
                dest_folder = os.path.join(folder, target)
                os.makedirs(dest_folder, exist_ok=True)
                shutil.move(path, os.path.join(dest_folder, file))
                print(f"Moved {file} -> {target}")
                break

print("\n✅ Organization Done! Automation success.")
