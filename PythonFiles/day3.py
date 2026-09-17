# Lesson 3 - Loops
skills = ["Python", "Git", "Pandas", "FastAPI", "AI Basics"]
dream = "AI App Developer"

print(f"{dream} aavan vendi padikkanullathu:")

# for loop
for i, skill in enumerate(skills, start=1):
    print(f"{i}. {skill} - Learning...")

# Bonus: range() vechu countdown
print("\nNext 7 days plan:")
for day in range(1, 8):
    print(f"Day {day}: Code cheyyum!")