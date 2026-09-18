import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Career AI - Pro", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.pro-card {
    background: #fff; border-radius: 18px; padding: 26px;
    margin-bottom: 24px; border: 1px solid #eee;
    border-left: 6px solid #6c63ff;
    box-shadow: 0 6px 20px rgba(0,0,0,0.06);
}
.salary { background: #10b981; color: white; padding: 5px 14px; border-radius: 20px; font-size: 13px; font-weight: 700; }
.step { background: #f5f5ff; padding: 10px 14px; border-radius: 10px; margin: 7px 0; font-size: 14px; border-left: 3px solid #6c63ff; }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Career AI - Pro Coach")

def get_api_key():
    try:
        if "GROQ_API_KEY" in st.secrets: return str(st.secrets["GROQ_API_KEY"])
    except: pass
    return os.getenv("GROQ_API_KEY", "")

# Pattiya career mathram kodukkunna function
def get_relevant_careers(skills_text, lang):
    text = skills_text.lower()
    is_ml = "Malayalam" in lang

    # Skill base mapping - vendathathu varilla
    all_careers = {
        "coding": {"en": "Python Developer", "ml": "പൈത്തൺ ഡെവലപ്പർ", "sal": "6-12 LPA", "why_en": "Perfect for your coding skill", "why_ml": "നിന്റെ കോഡിംഗ് കഴിവിന് പറ്റിയത്", "road": ["Python basics 30 days", "2 projects", "Apply jobs"] if not is_ml else ["Python basics 30 ദിവസം", "2 പ്രോജക്റ്റ്", "ജോലിക്ക് അപേക്ഷ"], "skills": ["Python", "DSA", "Git"]},
        "gaming": {"en": "Game Developer", "ml": "ഗെയിം ഡെവലപ്പർ", "sal": "5-15 LPA", "why_en": "Gaming + coding combo", "why_ml": "ഗെയിമിംഗ് + കോഡിംഗ് കോമ്പോ", "road": ["Unity basics", "1 mini game", "Portfolio"] if not is_ml else ["Unity basics", "1 ചെറിയ ഗെയിം", "Portfolio"], "skills": ["Unity", "C#", "Design"]},
        "youtube": {"en": "Video Editor / YouTuber", "ml": "വീഡിയോ എഡിറ്റർ", "sal": "4-8 LPA", "why_en": "Your youtube editing is trending", "why_ml": "YouTube എഡിറ്റിംഗ് ട്രെൻഡിംഗ് ആണ്", "road": ["Premiere Pro", "30 videos", "Freelance"] if not is_ml else ["Premiere Pro", "30 വീഡിയോ", "Freelance"], "skills": ["Premiere", "Editing", "YouTube"]},
        "editing": {"en": "Video Editor", "ml": "വീഡിയോ എഡിറ്റർ", "sal": "4-8 LPA", "why_en": "Editing skill is high demand", "why_ml": "എഡിറ്റിംഗ് നല്ല ഡിമാൻഡ് ആണ്", "road": ["Premiere + After Effects", "Portfolio", "Clients"] if not is_ml else ["Premiere + After Effects", "Portfolio", "Clients"], "skills": ["Premiere", "After Effects", "Reels"]},
        "design": {"en": "UI/UX Designer", "ml": "ഡിസൈനർ", "sal": "5-10 LPA", "why_en": "Design skill perfect match", "why_ml": "ഡിസൈൻ കഴിവിന് പറ്റിയത്", "road": ["Figma basics", "5 designs", "Apply"], "skills": ["Figma", "UI/UX", "Portfolio"]},
        "marketing": {"en": "Digital Marketer", "ml": "ഡിജിറ്റൽ മാർക്കറ്റർ", "sal": "4-9 LPA", "why_en": "Marketing is high demand", "why_ml": "മാർക്കറ്റിംഗ് നല്ല ഡിമാൻഡ്", "road": ["SEO + Ads", "1 campaign", "Freelance"], "skills": ["SEO", "Ads", "Analytics"]},
    }

    matched = []
    for key, data in all_careers.items():
        if key in text:
            matched.append(data)

    # Oru match polum illa enkil - user entha type cheythathu athu mathram
    if not matched:
        return [{
            "title": skills_text.title() + (" Expert" if not is_ml else " എക്സ്പെർട്ട്"),
            "salary": "4-10 LPA", "demand": "High",
            "why_good": f"Your skill {skills_text} is in demand" if not is_ml else f"{skills_text} നല്ല ഡിമാൻഡ് ഉള്ള skill ആണ്",
            "roadmap": ["Learn advanced", "Build portfolio", "Apply"], "top_skills": [skills_text, "Portfolio", "Communication"]
        }]

    # Pattiyathu mathram - max 3
    result = []
    for m in matched[:3]:
        result.append({
            "title": m["ml"] if is_ml else m["en"],
            "salary": m["sal"], "demand": "High",
            "why_good": m["why_ml"] if is_ml else m["why_en"],
            "roadmap": m["road"], "top_skills": m["skills"]
        })
    return result

# --- UI ---
c1,c2,c3 = st.columns(3, gap="large")
with c1: name = st.text_input("Name", "Arjun")
with c2: age2 = st.number_input("Age", 18, 40, 22)
with c3: language = st.selectbox("🌐 Language", ["Malayalam (മലയാളം)", "English", "Manglish"])

skills = st.text_input("Skills (1 line) - ex: coding gaming youtube", "coding gaming youtube editing")

if st.button("Get Advice 🔥", type="primary", use_container_width=True):
    if not skills.strip():
        st.warning("Skills enter cheyyu!")
    else:
        api_key = get_api_key().strip()
        final_careers = None

        # Try Groq - pattiyathu mathram chodikkum
        if api_key and len(api_key) > 20:
            try:
                lang_rule = "pure Malayalam script only" if "Malayalam" in language else "English only"
                prompt = f"Skills: {skills}. Give ONLY 3 careers directly related to these skills, no unrelated careers. Return ONLY JSON: {{\"careers\": [{{\"title\":\"\",\"salary\":\"\",\"demand\":\"High\",\"why_good\":\"\",\"roadmap\":[\"s1\",\"s2\",\"s3\"],\"top_skills\":[]}}]}} Language: {lang_rule}"
                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "max_tokens": 700, "temperature": 0.3},
                    timeout=20)
                if r.status_code == 200:
                    txt = r.json()["choices"][0]["message"]["content"]
                    clean = txt.replace("```json","").replace("```","")
                    s,e = clean.find('{'), clean.rfind('}')+1
                    data = json.loads(clean[s:e])
                    if "careers" in data and len(data["careers"])>0:
                        final_careers = data["careers"][:3] # pattiyathu 3 ennam mathram
            except:
                final_careers = None

        # API fail / unwanted varumbol - local relevant mathram
        if not final_careers:
            final_careers = get_relevant_careers(skills, language)

        # --- DISPLAY - Pattiyathu mathram ---
        st.divider()
        st.subheader(f"💼 {name} - {skills} nu pattiya careers")
        cols = st.columns(3, gap="large")
        for i, car in enumerate(final_careers):
            with cols[i % 3]:
                rm = car.get('roadmap', [])
                st.markdown(f"""
                <div class="pro-card">
                    <h4 style="margin:0 0 10px 0;">{car.get('title')}</h4>
                    <span class="salary">💰 {car.get('salary')}</span> <small>🔥 {car.get('demand')}</small>
                    <p style="margin:14px 0; font-size:14px; color:#444;">{car.get('why_good')}</p>
                    <b style="font-size:12px;">🗺️ Roadmap</b>
                    <div class="step">1️⃣ {rm[0] if len(rm)>0 else ''}</div>
                    <div class="step">2️⃣ {rm[1] if len(rm)>1 else ''}</div>
                    <div class="step">3️⃣ {rm[2] if len(rm)>2 else ''}</div>
                    <div style="margin-top:12px; font-size:11px; color:#888;">🛠️ {', '.join(car.get('top_skills',[]))}</div>
                </div>
                """, unsafe_allow_html=True)