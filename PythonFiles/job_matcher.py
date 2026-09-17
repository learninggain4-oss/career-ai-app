# job_matcher.py - Ninte Job kittanulla AI tool
print("--- AI Job Matcher ---")

# Oru sample Job Description
job_description = """
We need Python developer with skills: python, pandas, git, github, 
data analysis, automation, file handling
"""

print(f"Job: {job_description}")

my_skills = input("\nNinte skills entha? (comma vechu): ").lower()
# Eg: python, git, file handling

job_keywords = ["python", "pandas", "matplotlib", "git", "github", "automation", "data analysis", "file handling"]

matched = []
for skill in job_keywords:
    if skill in my_skills:
        matched.append(skill)

score = (len(matched) / len(job_keywords)) * 100

print(f"\n--- Result ---")
print(f"Matched Skills: {matched}")
print(f"Match Score: {score:.1f}%")

if score >= 70:
    print("🔥 Ready to apply! Strong match")
elif score >= 40:
    print("👍 Nalla progress, pandas/github okke koodi add cheyy")
else:
    print("💪 Skills kooduthal add cheyyanam, nammal padippikkam")

# Missing skills
missing = [s for s in job_keywords if s not in my_skills]
print(f"Learn next: {missing}")

# Save report
with open("job_report.txt", "w", encoding="utf-8") as f:
    f.write(f"Score: {score}%\nMatched: {matched}\nMissing: {missing}\n")
print("\nReport saved as job_report.txt")