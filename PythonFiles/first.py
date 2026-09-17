name = input("Enter your name:")
age = int(input("Enter Your Age:"))
dream = "Ai App Developer"

print(f"Hello {name}!")

if age <18:
    print("You are too young to work, but you can start learning now and prepare for your future career.")
elif age >18 and age < 25:
    print("Perfect age to Start your career, you can start learning and working on your dream.")
else:
    print (f"{age} is a great age to start your career, {name}! Experience + Ai skill = Job Success.")
    print ("You can storngly Portfolio your skills and experience to get your dream job.")
#Bonus automation logic
if "ai" in dream.lower():
   print("Dream set ! AI App Developer is a great career choice. Start learning Ai and work on your dream. ")
