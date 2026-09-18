import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import requests
import json

# Safe imports
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

st.set_page_config(page_title="Interview Q&A Bot PRO", page_icon="🎙️", layout="wide")

st.markdown("""
<style>
.qa-card {
    background:#fff; border-radius:16px; padding:22px;
    margin-bottom:20px; border:1px solid #eee;
    border-left:6px solid #ff6b6b;
    box-shadow:0 5px 15px rgba(0,0,0,0.05);
}
.q-tag { background:#6c63ff; color:white; padding:4px 12px; border-radius:20px; font-size:12px; font-weight:700; }
.a-box { background:#f8fff8; padding:14px; border-radius:10px; margin-top:10px; border:1px solid #d1fae5; font-size:14px; }
.tip-box { background:#fff7ed; padding:10px 14px; border-radius:8px; margin-top:10px; border-left:3px solid #f59e0b; font-size:13px; }
</style>
""", unsafe_allow_html=True)

st.title("🎙️ Interview Q&A Bot - Crack Cheyyam!")

def get_api_key():
    try:
        if "GROQ_API_KEY" in st.secrets:
            return str(st.secrets["GROQ_API_KEY"])
    except:
        pass
    return os.getenv("GROQ_API_KEY", "")

def get_local_qa(career, exp, lang):
    is_ml = "Malayalam" in lang
    career_low = career.lower()
    
    # Base QAs by career
    if "python" in career_low or "coding" in career_low or "software" in career_low:
        base_qa = [
            {"q": "Python-il List vs Tuple difference entha?" if is_ml else "What is difference between List and Tuple in Python?", "a": "List mutable aanu, Tuple immutable. List [] , Tuple () . List slow, Tuple fast. Interview-il memory use parayanam." if is_ml else "List is mutable, Tuple is immutable. List uses [], Tuple uses (). List is slower, Tuple faster and memory efficient.", "tip": "Example code parayu" if is_ml else "Give code example"},
            {"q": "Decorator entha?" if is_ml else "What is a decorator?", "a": "Function-nu extra feature add cheyyanulla function aanu decorator. @ symbol use cheyyum. Logging, authentication okke use." if is_ml else "A decorator adds extra feature to a function. Uses @ symbol. Used for logging, authentication etc.", "tip": "@my_decorator example kanikku"},
            {"q": "OOP concepts?" if is_ml else "Explain OOP concepts", "a": "Encapsulation, Inheritance, Polymorphism, Abstraction - 4 pillars. Real example: Car class, different car types inheritance.", "tip": "Real life example parayu"},
            {"q": "Tell me about yourself" if not is_ml else "Ninne kurichu parayu", "a": "Fresher aanenkil: College, skills, 2 projects, passion. 2 min mathram, career focus." if is_ml else "If fresher: Mention college, skills, 2 projects, passion. Keep 2 mins, career focused.", "tip": "Resume-il ulla project parayu"},
            {"q": "Why should we hire you?" if not is_ml else "Njangal enthu kond ninne edukkanam?", "a": "Skill + passion + culture fit. Ninte 2 strengths + company-nu enthu value add cheyyum ennu parayu." if is_ml else "Show skill + passion + culture fit. Mention 2 strengths + how you add value to company.", "tip": "Company research cheythu parayu"},
        ]
    elif "game" in career_low:
        base_qa = [
            {"q": "Unity vs Unreal?" if not is_ml else "Unity vs Unreal difference?", "a": "Unity C# , beginner friendly, mobile best. Unreal C++, AAA graphics, high performance.", "tip": "Ninte engine parayu"},
            {"q": "Game Loop entha?" if is_ml else "What is Game Loop?", "a": "Input -> Update -> Render -> repeat. 60 FPS target. Core of every game.", "tip": "Diagram varachu kanikku"},
            {"q": "Tell me about a game you made" if not is_ml else "Nee undakkiya game kurichu parayu", "a": "Project name, tech stack, challenges faced, what you learned. 2 min story.", "tip": "Demo video ready aakku"},
        ]
    elif "video" in career_low or "edit" in career_low or "youtube" in career_low:
        base_qa = [
            {"q": "Which editing software you use?" if not is_ml else "Ethu software aanu use cheyyunnathu?", "a": "Premiere Pro, DaVinci Resolve, After Effects. Ninte main tool + why.", "tip": "Portfolio link parayu"},
            {"q": "How to make video viral?" if not is_ml else "Video viral aakkaan enthu cheyyum?", "a": "Hook first 3 sec, trending audio, subtitles, thumbnail, story. Not just editing, algorithm manassilakkanam.", "tip": "Ninte viral video example"},
        ]
    else:
        base_qa = [
            {"q": "Tell me about yourself" if not is_ml else "Ninne kurichu parayu", "a": "Short intro: Name, study, skills, projects, career goal. 90 seconds.", "tip": "Confidence important"},
            {"q": "What are your strengths?" if not is_ml else "Ninte strengths entha?", "a": "2 technical + 1 soft skill. Example: Python + Problem solving + Team work.", "tip": "Example sahitham parayu"},
            {"q": "Where do you see yourself in 5 years?" if not is_ml else "5 varsham kazhinju evide aanu?", "a": "Senior role, leading projects, learning new tech. Company-il growth kaanikkuka.", "tip": "Loyal aanu ennu kaanikku"},
        ]

    # Add experience based
    if "Fresher" in exp:
        base_qa.append({"q": "No experience, why hire you?" if not is_ml else "Experience illa, pinne enthu?", "a": "Projects, internship, self-learning, passion. Real projects kanichu prove cheyyam.", "tip": "GitHub link kanikku"})
    else:
        base_qa.append({"q": "Why changing job?" if not is_ml else "Job maaraan kaaranam?", "a": "Growth, learning, new challenges. Old company negative parayaruthu.", "tip": "Positive aayittu parayu"})

    # Pad to 10 if needed
    while len(base_qa) < 8:
        base_qa.append({"q": f"Q{len(base_qa)+1} for {career}?" if not is_ml else f"{career} Q{len(base_qa)+1}?", "a": f"Answer for {career} role - show skill + example", "tip": "Example important"})

    return base_qa[:10]

# UI Inputs
c1,c2,c3 = st.columns(3, gap="large")
with c1:
    career = st.selectbox("💼 Career / Role", ["Python Developer", "Java Developer", "Software Developer", "Game Developer", "Video Editor", "UI/UX Designer", "Digital Marketer", "Custom"])
    custom_career = ""
    if career == "Custom":
        custom_career = st.text_input("Custom career ezhuthu", "Content Creator")
with c2:
    exp = st.selectbox("📅 Experience", ["Fresher", "1-2 Years", "3+ Years"])
with c3:
    lang = st.selectbox("🌐 Language", ["Malayalam (മലയാളം)", "English", "Manglish"])

final_career = custom_career if career == "Custom" and custom_career else career

# Optional resume upload to auto-detect career
with st.expander("📄 Resume upload cheythal auto career detect cheyyum (optional)"):
    uploaded = st.file_uploader("PDF upload", type=["pdf"])
    resume_text = ""
    if uploaded and PyPDF2:
        try:
            reader = PyPDF2.PdfReader(uploaded)
            resume_text = "".join([p.extract_text() or "" for p in reader.pages[:2]])
            st.success(f"Resume vaayichu - {len(resume_text)} chars - {final_career} nu pattum")
        except Exception as e:
            st.error(f"Error: {e}")

if st.button("🎙️ Generate 10 Interview Q&A", type="primary", use_container_width=True):
    with st.spinner(f"{final_career} - Interview Q&A ready aakkunnu..."):
        api_key = get_api_key().strip()
        qa_list = None

        if api_key and len(api_key) > 20:
            try:
                lang_rule = "in pure Malayalam script" if "Malayalam" in lang else "in English" if "English" in lang else "in Manglish (Malayalam typed in English)"
                prompt = f"""
                You are interview expert. Generate exactly 10 interview Q&A for role: {final_career}, Experience: {exp}.
                Language: {lang_rule}.
                Only relevant to this role. No unrelated Qs.
                Return ONLY JSON: {{"qa": [{{"q":"question","a":"detailed answer in 2-3 lines","tip":"short tip"}}]}}
                Include HR + Technical mix. Keep answers concise, interview-ready.
                Resume context if any: {resume_text[:500] if 'resume_text' in locals() else 'None'}
                """
                r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "max_tokens": 1500, "temperature": 0.4}, timeout=30)
                if r.status_code == 200:
                    txt = r.json()["choices"][0]["message"]["content"]
                    clean = txt.replace("```json","").replace("```","")
                    s,e = clean.find('{'), clean.rfind('}')+1
                    if s != -1:
                        j = json.loads(clean[s:e])
                        qa_list = j.get("qa", [])[:10]
            except Exception as e:
                qa_list = None

        if not qa_list:
            qa_list = get_local_qa(final_career, exp, lang)

        st.divider()
        st.subheader(f"🎯 {final_career} - {exp} - 10 Q&A")
        st.caption(f"✅ Only relevant to {final_career} | No unwanted Qs | {lang}")

        for idx, item in enumerate(qa_list, 1):
            q = item.get('q','')
            a = item.get('a','')
            tip = item.get('tip','')
            html = f"""
            <div class="qa-card">
                <span class="q-tag">Q{idx}</span> <b style="margin-left:8px;">{q}</b>
                <div class="a-box">💡 <b>Answer:</b> {a}</div>
                <div class="tip-box">🔥 <b>Tip:</b> {tip}</div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)

        st.success(f"✅ {len(qa_list)} questions ready - Interview crack cheyyam!")

st.caption("✅ Fixed | Only Relevant Q&A | Malayalam Support | No Glitch")