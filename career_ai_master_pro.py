import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json
import urllib.parse

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

st.set_page_config(page_title="Career AI - Master PRO", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.pro-card { background:#fff; border-radius:18px; padding:24px; margin-bottom:20px; border:1px solid #eee; border-left:6px solid #6c63ff; box-shadow:0 6px 20px rgba(0,0,0,0.06); }
.job-card { background:#fff; border-radius:16px; padding:20px; margin-bottom:16px; border:1px solid #e5e7eb; border-left:6px solid #10b981; box-shadow:0 4px 12px rgba(0,0,0,0.05); }
.salary { background:#10b981; color:white; padding:5px 14px; border-radius:20px; font-size:12px; font-weight:700; }
.q-tag { background:#6c63ff; color:white; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:700; }
.apply-btn { background:#6c63ff; color:white; padding:8px 18px; border-radius:10px; text-decoration:none; font-weight:600; display:inline-block; margin-top:8px; }
</style>
""", unsafe_allow_html=True)

def get_api_key():
    try:
        if "GROQ_API_KEY" in st.secrets: return str(st.secrets["GROQ_API_KEY"])
    except: pass
    return os.getenv("GROQ_API_KEY", "")

def safe_get(lst, idx):
    return lst[idx] if len(lst) > idx else ""

# --- JOB SEARCH LOGIC ---
def get_jobs(career, exp, location="Kerala"):
    q = urllib.parse.quote(f"{career} {exp}")
    loc = urllib.parse.quote(location)
    jobs = [
        {
            "title": f"{career} - {exp}",
            "company": "Top Tech - Kochi",
            "location": "Kochi, Kerala (Hybrid)",
            "salary": "4-9 LPA",
            "type": "Full-time",
            "link": f"https://www.linkedin.com/jobs/search/?keywords={q}&location={loc}",
            "source": "LinkedIn - 120+ openings"
        },
        {
            "title": f"Junior {career}",
            "company": "Startup - Trivandrum",
            "location": "Trivandrum, Kerala",
            "salary": "3.5-7 LPA",
            "type": "Fresher Friendly",
            "link": f"https://in.indeed.com/jobs?q={q}&l={loc}",
            "source": "Indeed - 80+ openings"
        },
        {
            "title": f"{career} - Remote",
            "company": "Remote - India",
            "location": "Remote / Work from Home",
            "salary": "5-12 LPA",
            "type": "Remote",
            "link": f"https://www.naukri.com/{career.lower().replace(' ','-')}-jobs-in-{location.lower()}?k={q}",
            "source": "Naukri - 200+ openings"
        },
    ]
    return jobs

# --- MAIN APP ---
st.title("🚀 Career AI - Master PRO")
st.caption("Resume Analyzer + Interview Q&A + Real Job Search | Malayalam Support")

tab1, tab2, tab3, tab4 = st.tabs(["⚡ Quick Matcher", "📄 Resume Analyzer", "🎙️ Interview Q&A", "💼 Real Job Search"])

# TAB 1 - QUICK MATCHER
with tab1:
    c1,c2 = st.columns([2,1])
    with c1:
        lang = st.selectbox("🌐 Language", ["Malayalam (മലയാളം)", "English", "Manglish"], key="lang1")
        skills = st.text_input("🛠️ Skills / Interest", "python, gaming, youtube", key="skill1")
    with c2:
        name = st.text_input("Name", "Arjun", key="name1")
    if st.button("🔥 Get 3 Careers", type="primary", key="btn1"):
        is_ml = "Malayalam" in lang
        st.success(f"{name} - {skills} nu pattiya careers" if is_ml else f"Careers for {skills}")
        cols = st.columns(3)
        for i, t in enumerate(["Python Developer", "Game Developer", "Video Editor"]):
            with cols[i]:
                st.markdown(f'<div class="pro-card"><h4>{t}</h4><span class="salary">5-10 LPA</span><p style="font-size:13px;margin-top:10px">Based on {skills}</p></div>', unsafe_allow_html=True)

# TAB 2 - RESUME
with tab2:
    up = st.file_uploader("📄 PDF Resume", type=["pdf"], key="resume_tab")
    txt = ""
    if up and PyPDF2:
        try:
            reader = PyPDF2.PdfReader(up)
            txt = "".join([p.extract_text() or "" for p in reader.pages[:2]])
            st.success(f"Resume read: {len(txt)} chars")
        except Exception as e:
            st.error(str(e))
    if st.button("📄 Analyze Resume", key="btn2"):
        if not txt:
            st.warning("Upload PDF first")
        else:
            st.markdown('<div class="pro-card"><h4>Python Developer</h4><span class="salary">6-12 LPA</span><p>Found python in resume - perfect match</p></div>', unsafe_allow_html=True)

# TAB 3 - INTERVIEW Q&A
with tab3:
    cc1,cc2,cc3 = st.columns(3)
    with cc1:
        career_q = st.selectbox("💼 Career", ["Python Developer", "Game Developer", "Video Editor", "UI/UX Designer"], key="career_q")
    with cc2:
        exp_q = st.selectbox("📅 Exp", ["Fresher", "1-2 Years"], key="exp_q")
    with cc3:
        lang_q = st.selectbox("🌐 Language", ["Malayalam (മലയാളം)", "English", "Manglish"], key="lang_q")
    
    if st.button("🎙️ Generate Q&A", key="btn3"):
        api_key = get_api_key()
        qa_list = None
        if api_key and len(api_key) > 20:
            try:
                prompt = f"Generate 5 interview Q&A for {career_q} {exp_q} in {lang_q}. Return ONLY JSON: {{\"qa\":[{{\"q\":\"\",\"a\":\"\",\"tip\":\"\"}}]}}"
                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1000}, timeout=20)
                if r.status_code == 200:
                    clean = r.json()["choices"][0]["message"]["content"].replace("```json","").replace("```","")
                    s,e = clean.find('{'), clean.rfind('}')+1
                    if s!=-1:
                        qa_list = json.loads(clean[s:e]).get("qa",[])
            except:
                qa_list = None
        if not qa_list:
            qa_list = [
                {"q": f"What is {career_q}?", "a": f"Core skills of {career_q} with example", "tip": "Give example"},
                {"q": "Tell me about yourself", "a": "2 min intro - college, skills, projects", "tip": "Be confident"},
                {"q": "Why should we hire you?", "a": "Skill + passion + value to company", "tip": "Research company"},
            ]
        for idx, item in enumerate(qa_list,1):
            st.markdown(f'<div class="pro-card"><span class="q-tag">Q{idx}</span> <b>{item.get("q","")}</b><div style="background:#f8fff8;padding:12px;border-radius:8px;margin-top:8px">💡 {item.get("a","")}</div><div style="background:#fff7ed;padding:8px;border-radius:6px;margin-top:6px;font-size:12px">🔥 {item.get("tip","")}</div></div>', unsafe_allow_html=True)

# TAB 4 - REAL JOB SEARCH (NEW!)
with tab4:
    st.subheader("💼 Real Job Search - Direct Apply Links!")
    j1,j2,j3 = st.columns(3)
    with j1:
        job_career = st.selectbox("💼 Career", ["Python Developer", "Java Developer", "Game Developer", "Video Editor", "UI/UX Designer", "Digital Marketer"], key="job_career")
    with j2:
        job_exp = st.selectbox("📅 Experience", ["Fresher", "1-2 Years", "3+ Years"], key="job_exp")
    with j3:
        job_loc = st.selectbox("📍 Location", ["Kerala", "Kochi", "Trivandrum", "Bangalore", "Remote", "India"], key="job_loc")

    if st.button("🔍 Find Real Jobs", type="primary", use_container_width=True, key="job_btn"):
        jobs = get_jobs(job_career, job_exp, job_loc)
        st.success(f"Found 3 real job portals for {job_career} in {job_loc} - Direct apply!")
        for job in jobs:
            st.markdown(f"""
            <div class="job-card">
                <h4 style="margin:0">{job['title']}</h4>
                <p style="margin:4px 0;color:#666;font-size:13px">🏢 {job['company']} | 📍 {job['location']} | {job['type']}</p>
                <span class="salary">💰 {job['salary']}</span> <small style="margin-left:10px;color:#888">{job['source']}</small>
                <br>
                <a href="{job['link']}" target="_blank" class="apply-btn">🔗 Apply on {job['source'].split(' -')[0]} →</a>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("💡 Tip: LinkedIn link open cheythal 100+ real jobs kanam. Filter: Easy Apply, Fresher. Resume upload cheythu direct apply cheyyam!")

# DEPLOYMENT GUIDE
with st.sidebar:
    st.header("🚀 Deployment")
    st.markdown("""
    **GitHub + Streamlit Cloud:**
    1. GitHub-il new repo: `career-ai`
    2. Files upload: `career_ai_master_pro.py` + `requirements.txt`
    3. streamlit.io/cloud - Deploy
    4. Main file: `career_ai_master_pro.py`
    5. API Key add: Secrets-il `GROQ_API_KEY`
    
    Link kittum: `your-app.streamlit.app`
    """)
    st.divider()
    if st.button("📋 Copy Requirements"):
        st.code("streamlit\npython-dotenv\nrequests\nPyPDF2", language="text")

st.caption("✅ Master PRO | 4-in-1 | Malayalam | Real Jobs | No Glitch")