# dashboard.py - Data Science + Visualization
import pandas as pd
import matplotlib.pyplot as plt

print("--- AI Dashboard ---")

# users.txt read cheyyam
try:
    # nammude file-il comma advice-yilum undu, athukond first 2 column mathram edukkum
    data = []
    with open("users.txt", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",", 2) # 2 thavana mathram split
            if len(parts) >= 2:
                name = parts[0]
                age = int(parts[1])
                data.append({"name": name, "age": age})

    df = pd.DataFrame(data)
    print(df)
    print(f"\nTotal: {len(df)}, Average Age: {df['age'].mean():.1f}")

    # Graph
    young = len(df[df['age'] < 25])
    exp = len(df[df['age'] >= 25])

    plt.bar(["Young (<25)", "Experienced (25+)"], [young, exp])
    plt.title("Career App Users")
    plt.ylabel("Count")
    plt.savefig("chart.png")
    print("\nChart saved as chart.png! Check VS Code left side.")

except Exception as e:
    print(f"Error: {e}")
    print("Make sure users.txt undu, app.py run cheythu.")