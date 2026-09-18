import streamlit as st

st.set_page_config(page_title="Portfolio Builder PRO", page_icon="🎨", layout="wide")

st.markdown("""
<style>
.portfolio-preview { border: 2px solid #e5e7eb; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.08); }
.skill-pill { background:#6c63ff; color:white; padding:6px 14px; border-radius:20px; font-size:12px; margin:4px; display:inline-block; }
.project-card { background:#f9fafb; border-radius:12px; padding:16px; border:1px solid #eee; margin-bottom:12px; }
</style>
""", unsafe_allow_html=True)

st.title("🎨 Portfolio Builder - Kerala Edition")
st.caption("No coding needed | 2 min-il portfolio website | Download as HTML")

c1,c2 = st.columns([1, 1.2], gap="large")

with c1:
    st.subheader("📝 Your Details")
    name = st.text_input("Full Name", "Arjun Krishna")
    role = st.text_input("Role / Title", "Python Developer | Game Developer")
    about = st.text_area("About You", "Passionate developer from Kerala. Love building games and Python apps. 2 projects completed.", height=80)
    
    col_a, col_b = st.columns(2)
    with col_a:
        email = st.text_input("Email", "arjun@example.com")
        github = st.text_input("GitHub", "github.com/arjun")
    with col_b:
        linkedin = st.text_input("LinkedIn", "linkedin.com/in/arjun")
        youtube = st.text_input("YouTube / Website", "youtube.com/@arjun")

    skills_raw = st.text_input("Skills (comma)", "Python, Unity, Video Editing, JavaScript, UI/UX")
    skills = [s.strip() for s in skills_raw.split(",") if s.strip()]

    st.divider()
    st.subheader("🚀 Projects (3 max)")
    
    projects = []
    for i in range(1, 4):
        with st.expander(f"Project {i}", expanded=(i==1)):
            p_title = st.text_input(f"Title {i}", f"My Awesome Project {i}" if i==1 else "", key=f"pt{i}")
            p_desc = st.text_area(f"Description {i}", f"A cool project built with {skills[0] if skills else 'tech'}.", key=f"pd{i}", height=70)
            p_tech = st.text_input(f"Tech Used {i}", "Python, Streamlit" if i==1 else "", key=f"pte{i}")
            p_link = st.text_input(f"Link {i}", "https://github.com" if i==1 else "", key=f"pl{i}")
            if p_title:
                projects.append({"title": p_title, "desc": p_desc, "tech": p_tech, "link": p_link})

    theme = st.selectbox("Theme", ["Modern Purple (Tech)", "Kerala Green (Fresh)", "YouTube Red (Creative)", "Dark Minimal"])

themes = {
    "Modern Purple (Tech)": {"primary": "#6c63ff", "bg": "#f5f5ff", "accent": "#10b981"},
    "Kerala Green (Fresh)": {"primary": "#059669", "bg": "#f0fdf4", "accent": "#f59e0b"},
    "YouTube Red (Creative)": {"primary": "#ef4444", "bg": "#fef2f2", "accent": "#6c63ff"},
    "Dark Minimal": {"primary": "#111827", "bg": "#f9fafb", "accent": "#6b7280"},
}
colors = themes[theme]

def generate_html():
    skill_html = "".join([f'<span style="background:{colors["primary"]};color:white;padding:6px 14px;border-radius:20px;font-size:12px;margin:4px;display:inline-block">{s}</span>' for s in skills])
    
    proj_html = ""
    for p in projects:
        proj_html += f"""
        <div style="background:#f9fafb;border-radius:12px;padding:18px;border:1px solid #eee;margin-bottom:16px;border-left:5px solid {colors['primary']}">
            <h3 style="margin:0 0 6px 0;color:{colors['primary']}">{p['title']}</h3>
            <p style="margin:0 0 8px 0;color:#555;font-size:14px">{p['desc']}</p>
            <small style="color:#888">Tech: {p['tech']}</small><br>
            <a href="{p['link']}" target="_blank" style="color:{colors['primary']};font-weight:600;font-size:13px">View Project -></a>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} - {role}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
body {{ font-family:Inter,sans-serif; margin:0; background:{colors['bg']}; }}
.hero {{ background:{colors['primary']}; color:white; padding:60px 20px; text-align:center; }}
.container {{ max-width:900px; margin:-30px auto 0; background:white; border-radius:20px; padding:30px; box-shadow:0 10px 30px rgba(0,0,0,0.1); }}
.btn {{ background:{colors['primary']}; color:white; padding:10px 20px; border-radius:10px; text-decoration:none; display:inline-block; margin:6px; font-weight:600; }}
</style></head>
<body>
<div class="hero"><h1>{name}</h1><p>{role}</p><p style="font-size:14px;max-width:600px;margin:15px auto 0;opacity:0.85">{about}</p></div>
<div class="container">
<h2>Skills</h2><div>{skill_html}</div>
<h2 style="margin-top:30px">Projects</h2>{proj_html}
<h2 style="margin-top:30px">Contact</h2><p>{email}</p>
<a href="https://{github}" class="btn">GitHub</a>
<a href="https://{linkedin}" class="btn">LinkedIn</a>
<a href="https://{youtube}" class="btn">YouTube</a>
<br><br><a href="mailto:{email}" class="btn" style="background:{colors['accent']}">Hire Me</a>
</div>
<div style="text-align:center;padding:30px;color:#888;font-size:12px">Made with Love in Kerala | {name} 2026</div>
</body></html>
"""
    return html

with c2:
    st.subheader("Live Preview")
    preview_skills = "".join([f'<span class="skill-pill" style="background:{colors["primary"]}">{s}</span>' for s in skills[:6]])
    preview_projects = "".join([f'<div class="project-card"><b>{p["title"]}</b><br><small>{p["desc"][:60]}...</small></div>' for p in projects[:2]])
    
    st.markdown(f"""
    <div class="portfolio-preview">
        <div style="background:{colors['primary']};color:white;padding:30px;text-align:center">
            <h2 style="margin:0;color:white">{name}</h2>
            <p style="margin:5px 0;opacity:0.9">{role}</p>
            <small style="opacity:0.8">{about[:80]}...</small>
        </div>
        <div style="padding:20px;background:white">
            <b>Skills:</b><br>{preview_skills}
            <br><br><b>Projects:</b>{preview_projects}
            <br><b>{email}</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    html_content = generate_html()
    
    st.download_button(
        label="Download Portfolio (HTML)",
        data=html_content,
        file_name=f"{name.lower().replace(' ','_')}_portfolio.html",
        mime="text/html",
        type="primary",
        use_container_width=True
    )
    
    st.info("Tip: HTML download cheythu GitHub-il upload cheythal free website! yourname.github.io")

with st.sidebar:
    st.header("Free Hosting")
    st.markdown("""
    **Portfolio live aakkan:**
    1. Download HTML
    2. github.com -> New Repo -> yourname.github.io
    3. HTML upload
    4. Link: https://yourname.github.io - LIVE!
    """)

st.caption("Portfolio Builder PRO | No Coding | Kerala Edition")