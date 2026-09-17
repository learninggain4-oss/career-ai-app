import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Career AI App", page_icon="🚀")
st.title("🚀 Career AI App - My Portfolio")

tab1, tab2, tab3 = st.tabs(["Career Advice", "Dashboard", "Job Matcher"])

# TAB 1 - App
with tab1:
    st.header("Career Advice App")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, max_value=100, value=22)
    if st.button("Get Advice"):
        if age < 0: advice = "Invalid"
        elif age < 18: advice = "Too young to work, but perfect for learning!"
        elif age < 25: advice = "Perfect age for internship & skill building!"
        elif age < 40: advice = "Best time for full-time job & career growth!"
        else: advice = "Great experience, try leadership roles!"

        st.success(f"Hello {name}, {advice}")
        # Save
        with open("users.txt", "a", encoding="utf-8") as f:
            f.write(f"{name},{age},{advice}\n")

# TAB 2 - Dashboard
with tab2:
    st.header("AI Dashboard")
    try:
        data = []
        with open("users.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(",", 2)
                if len(parts) >= 2:
                    data.append({"name": parts[0], "age": int(parts[1])})
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.metric("Total Users", len(df))
            st.metric("Average Age", f"{df['age'].mean():.1f}")

            young = len(df[df['age'] < 25])
            exp = len(df[df['age'] >= 25])
            fig, ax = plt.subplots()
            ax.bar(["Young (<25)", "Experienced"], [young, exp])
            ax.set_title("Users")
            st.pyplot(fig)
        else:
            st.info("No users yet, go to Tab 1")
    except:
        st.warning("users.txt not found")

# TAB 3 - Job Matcher
with tab3:
    st.header("AI Job Matcher")
    job_keywords = ["python", "pandas", "matplotlib", "git", "github", "automation", "data analysis", "file handling"]
    st.write(f"Required: {', '.join(job_keywords)}")
    my_skills = st.text_input("Your skills (comma separated)", "python, git, pandas")
    if st.button("Check Match"):
        matched = [s for s in job_keywords if s in my_skills.lower()]
        score = (len(matched)/len(job_keywords))*100
        st.write(f"Matched: {matched}")
        st.progress(int(score))
        st.write(f"**Score: {score:.1f}%**")
        if score >= 70:
            st.success("Ready to apply! 🔥")
        else:
            missing = [s for s in job_keywords if s not in my_skills.lower()]
            st.warning(f"Learn next: {missing}")