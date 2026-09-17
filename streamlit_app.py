import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd

st.set_page_config(page_title="Career AI - AI Powered", page_icon="🚀")
st.title("🚀 Career AI - Now with Real AI!")

tab1, tab2 = st.tabs(["📊 Career Matcher", "🤖 AI Career Coach"])

with tab1:
    st.header("Simple Matcher")
    interest = st.selectbox("Interest", ["Coding", "Design", "Gaming", "Marketing"])
    if st.button("Get Career"):
        if interest == "Coding":
            st.success("Go for Software Developer / Python Developer!")
        elif interest == "Design":
            st.success("UI/UX Designer / Graphic Designer!")
        elif interest == "Gaming":
            st.success("Game Developer / Game Tester!")
        else:
            st.success("Digital Marketing Specialist!")

with tab2:
    st.header("🤖 AI Career Coach - Ask Anything!")
    st.write("Real AI will give you personalized advice")

    name = st.text_input("Your Name", "Arjun")
    age = st.number_input("Age", 18, 40, 22)
    skills = st.text_area("Your Skills & Likes", "I like coding, gaming and YouTube editing")

    if st.button("Get AI Advice 🔥"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            st.error("GROQ_API_KEY.env-il illa! groq.com-il ninnu eduthu.env-il add cheyy")
        else:
            try:
                from groq import Groq
                client = Groq(api_key=api_key)

                prompt = f"I am {name}, {age} years old. My skills: {skills}. Give me 3 best career paths in Kerala/India with salary and roadmap in Manglish mix (Malayalam+English)."

                with st.spinner("AI thinking... 🧠"):
                    chat = client.chat.completions.create(
                        messages=[{"role": "user", "content": prompt}],
                        model="llama-3.3-70b-versatile",
                    )
                    st.success("AI Advice:")
                    st.write(chat.choices[0].message.content)
                    st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")