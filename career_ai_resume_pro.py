import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json

# PyPDF2 import - fixed for VSCode
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

st.set_page_config(page_title="Resume Analyzer PRO", page_icon="📄", layout="wide")

st.markdown("""
<style>
.pro-card { background:#fff; border-radius:18px; padding:26px; margin-bottom:28px; border:1px solid #eee; border-left:6px solid #6c63ff; box-shadow:0 6px 20px rgba(0,0,0,0.06); }
.salary { background:#10b981; color:white; padding:5px 14px; border-radius:20px; font-size:13px; font-weight:700; }
.step { background:#f5f5ff; padding:10px 14px; border-radius:10px; margin:8px 0; font-size:14px; border-left:3px solid #6c63ff; }
</style>
""", unsafe_allow_html=True)

st.title("📄 Resume Analyzer PRO - Pattiyathu Mathram!")

def get_api_key():
    try:
        if "GROQ_API_KEY" in st.secrets: return str(st.secrets["GROQ_API_KEY"])
    except: pass
    return os.getenv("GROQ_API_KEY", "")

def safe_rm(rm_list, index):
    if len(rm_list) > index:
        return rm_list[index]
    return ""

def get_relevant_from_text(text, lang):
    t = text.lower()
    is_ml = "Malayalam" in lang
    mapping = {
        "python": {"title_en": "Python Developer", "title_ml": "പൈത്തൺ ഡെവലപ്പർ", "sal": "6-12 LPA"},
        "java": {"title_en": "Java Developer", "title_ml": "ജാവ ഡെവലപ്പർ", "sal": "5-11 LPA"},
        "coding": {"title_en": "Software Developer", "title_ml": "സോഫ്റ്റ്‌വെയർ ഡെവലപ്പർ", "sal": "6-12 LPA"},
        "game": {"title_en": "Game Developer", "title_ml": "ഗെയിം ഡെവലപ്പർ", "sal": "5-15 LPA"},
        "youtube": {"title_en": "Video Editor / YouTuber", "title_ml": "വീഡിയോ എഡിറ്റർ", "sal": "4-8 LPA"},
        "edit": {"title_en": "Video Editor", "title_ml": "വീഡിയോ എഡിറ്റർ", "sal": "4-8 LPA"},
        "design": {"title_en": "UI/UX Designer", "title_ml": "ഡിസൈനർ", "sal": "5-10 LPA"},
        "marketing": {"title_en": "Digital Marketer", "title_ml": "ഡിജിറ്റൽ മാർക്കറ്റർ", "sal": "4-9 LPA"},
    }
    found = []
    for k,v in mapping.items():
        if k in t:
            title = v["title_ml"] if is_ml else v["title_en"]
            why_text = f"Resume-il {k} skill und, athinu pattiyathu" if is_ml else f"Found {k} skill in resume - perfect match"
            road = ["30 days: Skill polish", "2 projects build", "Apply jobs"] if not is_ml else ["30 ദിവസം: Skill polish", "2 പ്രോജക്റ്റ്", "ജോലിക്ക് അപേക്ഷ"]
            found.append({
                "title": title, "salary": v["sal"], "demand": "High",
                "why_good": why_text,
                "roadmap": road,
                "top_skills": [k.title(), "Portfolio", "Communication"]
            })
    if not found:
        found = [{"title": "General Skill Expert", "salary": "4-10 LPA", "demand": "High", "why_good": "Resume based career", "roadmap": ["Learn advanced", "Build portfolio", "Apply"], "top_skills": ["Resume Skill"]}]
    return found[:3]

c1,c2 = st.columns([2,1], gap="large")
with c1:
    lang = st.selectbox("🌐 Language", ["Malayalam (മലയാളം)", "English", "Manglish"])
with c2:
    name = st.text_input("Name", "Arjun")

uploaded = st.file_uploader("📄 PDF Resume Upload Cheyyu", type=["pdf"])
resume_text = ""

if uploaded:
    if PyPDF2 is None:
        st.error("❌ PyPDF2 install cheythittilla! Terminal-il: pip install PyPDF2")
    else:
        try:
            reader = PyPDF2.PdfReader(uploaded)
            resume_text = "".join([p.extract_text() or "" for p in reader.pages[:3]])
            st.success(f"✅ Resume vaayichu! {len(resume_text)} chars")
            with st.expander("Resume-il enthu undu?"):
                st.write(resume_text[:2000])
        except Exception as e:
            st.error(f"PDF read error: {e}")

if st.button("🔥 Analyze & Get Pattiya Careers", type="primary", use_container_width=True):
    if not resume_text:
        st.warning("⚠️ First PDF upload cheyyu!")
    else:
        with st.spinner("Resume analyze cheyyunnu..."):
            api_key = get_api_key().strip()
            careers = None

            if api_key and len(api_key) > 20:
                try:
                    lang_rule = "pure Malayalam script only" if "Malayalam" in lang else "English only"
                    prompt = f"Read this resume and give ONLY 3 careers directly related to skills in resume. No unrelated careers. Return ONLY JSON: {{\"careers\": [{{\"title\":\"\",\"salary\":\"\",\"demand\":\"High\",\"why_good\":\"\",\"roadmap\":[\"s1\",\"s2\",\"s3\"],\"top_skills\":[]}}]}} Resume: {resume_text[:1200]} Language: {lang_rule}"
                    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                        json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "max_tokens": 800, "temperature": 0.3}, timeout=25)
                    if r.status_code == 200:
                        txt = r.json()["choices"][0]["message"]["content"]
                        clean = txt.replace("```json","").replace("```","")
                        s,e = clean.find('{'), clean.rfind('}')+1
                        if s!=-1:
                            j = json.loads(clean[s:e])
                            careers = j.get("careers", [])[:3]
                except:
                    careers = None

            if not careers:
                careers = get_relevant_from_text(resume_text, lang)

            st.divider()
            st.subheader(f"💼 {name} - Resume-nu pattiya 3 careers")

            cols = st.columns(3, gap="large")
            for i, car in enumerate(careers[:3]):
                with cols[i%3]:
                    rm = car.get('roadmap', [])
                    r1 = safe_rm(rm, 0)
                    r2 = safe_rm(rm, 1)
                    r3 = safe_rm(rm, 2)
                    skills_str = ", ".join(car.get('top_skills',[]))
                    title = car.get('title','')
                    salary = car.get('salary','')
                    demand = car.get('demand','High')
                    why = car.get('why_good','')
                    
                    html_code = f"""
                    <div class="pro-card">
                        <h4 style="margin:0 0 10px 0;">{title}</h4>
                        <span class="salary">💰 {salary}</span> <small>🔥 {demand}</small>
                        <p style="margin:14px 0; font-size:14px; color:#444;">{why}</p>
                        <b style="font-size:12px;">Roadmap</b>
                        <div class="step">1️⃣ {r1}</div>
                        <div class="step">2️⃣ {r2}</div>
                        <div class="step">3️⃣ {r3}</div>
                        <div style="margin-top:12px; font-size:11px; color:#888;">🛠️ {skills_str}</div>
                    </div>
                    """
                    st.markdown(html_code, unsafe_allow_html=True)

            st.success("✅ Ithu resume-il ulla skill-nu mathram pattiyathu aanu!")

st.caption("✅ Fixed - No Import Error | No Quote Clash")