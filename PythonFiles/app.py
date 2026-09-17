def save_user(name, age, advice):
    with open("users.txt", "a", encoding="utf-8") as f:
        f.write(f"{name},{age},{advice}\n")
    print(f"Saved {name} to users.txt!")

def career_advisor(name,age):
    if age < 18:
        return "Too young to work, but perfect to start learning!"
    elif age < 25:
        return "Perfect age to start! Build projects now."
    else:
        return f"{age} is a great age! Experience + AI = Job Success."

def greet(name):
    return f"Hello {name}! Ninte AI App ready aanu."

# App start
print("--- Sadhoo's Career AI App ---")
while True:
    name = input("\nEnter your name (exit = close): ")
    if name.lower() == "exit":
        print("App closed. Data saved in users.txt!")
        break
    
    try:
        age = int(input(f"Hi {name}, age entha? "))
        advice = career_advisor(name, age)
        print(f"\n>> {greet(name)}")
        print(f">> Advice: {advice}")
        save_user(name, age, advice)  # <-- puthiyathu
    except ValueError:
        print("Age number aayi adikkanam! Eg: 24")
      