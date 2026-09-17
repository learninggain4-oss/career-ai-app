# analyzer.py - Ninte first Data Science tool
print("--- Career App Data Report ---")

try:
    with open("users.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines:
        print("No data yet!")
        exit()

    ages = []
    for line in lines:
        parts = line.split(",") # name,age,advice
        age = int(parts[1])
        ages.append(age)

    total_users = len(lines)
    avg_age = sum(ages) / total_users
    young = len([a for a in ages if a < 25])
    experienced = total_users - young

    print(f"Total users: {total_users}")
    print(f"Average age: {avg_age:.1f}")
    print(f"Young (<25): {young} per")
    print(f"Experienced (25+): {experienced} per")
    print("\nIthu thanne aanu Automation + Data Analysis!")

except FileNotFoundError:
    print("users.txt illa, app.py run cheythu users add cheyy")