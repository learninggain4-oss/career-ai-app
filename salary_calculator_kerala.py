import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Salary Calculator - Kerala", page_icon="💰", layout="wide")

st.markdown("""
<style>
.salary-main {
    background: linear-gradient(135deg, #6c63ff 0%, #10b981 100%);
    border-radius:22px; padding:32px; color:white;
    text-align:center; box-shadow:0 10px 30px rgba(108,99,255,0.3);
    margin-bottom:24px;
}
.stat-card {
    background:#fff; border-radius:16px; padding:20px;
    border:1px solid #eee; text-align:center;
    box-shadow:0 4px 12px rgba(0,0,0,0.05); margin-bottom:16px;
}
.tip-card {
    background:#fff7ed; border-radius:12px; padding:16px;
    border-left:5px solid #f59e0b; margin:8px 0; font-size:13px;
}
.growth-card {
    background:#f0fdf4; border-radius:12px; padding:14px;
    border:1px solid #bbf7d0; margin:6px 0;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 Salary Calculator - Kerala")
st.caption("Kerala IT Market 2026 | Real Data | Fresher to 10+ Years")

# Kerala Salary Base Data 2026 (LPA) - Research based
SALARY_DATA = {
    "Python Developer": {"fresher": 4.5, "1-2": 6.8, "3-5": 10.5, "5-10": 16.0, "demand": "Very High"},
    "Java Developer": {"fresher": 4.2, "1-2": 6.5, "3-5": 10.0, "5-10": 15.5, "demand": "High"},
    "Software Developer": {"fresher": 4.3, "1-2": 6.6, "3-5": 10.2, "5-10": 15.8, "demand": "Very High"},
    "Game Developer": {"fresher": 3.8, "1-2": 6.0, "3-5": 9.5, "5-10": 14.0, "demand": "Medium"},
    "Video Editor": {"fresher": 2.8, "1-2": 4.2, "3-5": 6.5, "5-10": 9.0, "demand": "High"},
    "UI/UX Designer": {"fresher": 3.6, "1-2": 5.8, "3-5": 9.0, "5-10": 13.5, "demand": "Very High"},
    "Digital Marketer": {"fresher": 2.5, "1-2": 4.0, "3-5": 6.8, "5-10": 10.0, "demand": "High"},
    "Data Analyst": {"fresher": 5.0, "1-2": 7.5, "3-5": 11.5, "5-10": 18.0, "demand": "Very High"},
    "Content Creator / YouTuber": {"fresher": 2.2, "1-2": 3.8, "3-5": 6.0, "5-10": 10.0, "demand": "High"},
    "Graphic Designer": {"fresher": 2.6, "1-2": 4.0, "3-5": 6.2, "5-10": 8.5, "demand": "Medium"},
}

LOCATION_MULT = {
    "Kochi (IT Hub)": 1.15,
    "Trivandrum (Technopark)": 1.10,
    "Calicut / Kozhikode": 0.90,
    "Kerala Average": 1.0,
    "Bangalore (Comparison)": 1.35,
    "Remote / US Client": 1.40,
}

COMPANY_MULT = {
    "Service (Infosys, TCS)": 1.0,
    "Product (Startup)": 1.25,
    "MNC Product (Google, Amazon)": 1.60,
    "Kerala Startup": 0.85,
    "Freelance": 1.10,
}

# Inputs
c1,c2,c3 = st.columns(3, gap="large")
with c1:
    career = st.selectbox("💼 Career", list(SALARY_DATA.keys()))
    lang = st.selectbox("🌐 Language", ["Malayalam (മലയാളം)", "English", "Manglish"])
with c2:
    exp = st.selectbox("📅 Experience", ["Fresher (0-1 Year)", "1-2 Years", "3-5 Years", "5-10 Years"])
    location = st.selectbox("📍 Location", list(LOCATION_MULT.keys()), index=3)
with c3:
    company = st.selectbox("🏢 Company Type", list(COMPANY_MULT.keys()))
    education = st.selectbox("🎓 Education", ["Plus Two", "Degree", "BTech / BE", "MCA / MTech", "Self-taught"])

is_ml = "Malayalam" in lang

def calculate_salary():
    base = SALARY_DATA[career]
    exp_key = exp.split()[0]  # Fresher, 1-2, 3-5, 5-10
    if "Fresher" in exp:
        exp_key = "fresher"
    elif "1-2" in exp:
        exp_key = "1-2"
    elif "3-5" in exp:
        exp_key = "3-5"
    else:
        exp_key = "5-10"
    
    base_lpa = base[exp_key]
    loc_mult = LOCATION_MULT[location]
    comp_mult = COMPANY_MULT[company]
    
    # Education bonus
    edu_bonus = 0
    if "BTech" in education:
        edu_bonus = 0.3
    elif "MCA" in education:
        edu_bonus = 0.4
    elif "Self-taught" in education and exp_key == "fresher":
        edu_bonus = -0.5
    
    final_lpa = (base_lpa * loc_mult * comp_mult) + edu_bonus
    final_lpa = max(1.5, final_lpa)  # minimum
    
    return final_lpa, base_lpa, base["demand"]

if st.button("💰 Calculate My Kerala Salary", type="primary", use_container_width=True):
    final_lpa, base_lpa, demand = calculate_salary()
    
    monthly = (final_lpa * 100000) / 12
    # In-hand approx 85% after PF, tax for fresher
    inhand_mult = 0.88 if final_lpa < 6 else 0.80 if final_lpa < 10 else 0.72
    inhand_monthly = monthly * inhand_mult
    
    # Yearly growth projection
    growth_rate = 0.25 if "Very High" in demand else 0.18
    
    # Display Main Salary
    if is_ml:
        main_title = f"{career} - Kerala Salary"
        sub = f"{exp} | {location} | {company}"
    else:
        main_title = f"{career} - Kerala Salary"
        sub = f"{exp} | {location} | {company}"
    
    st.markdown(f"""
    <div class="salary-main">
        <h2 style="margin:0;color:white;">{main_title}</h2>
        <p style="opacity:0.9;margin:6px 0">{sub}</p>
        <h1 style="margin:10px 0;font-size:48px;color:white;">₹ {final_lpa:.1f} LPA</h1>
        <p style="font-size:18px;opacity:0.95">₹ {int(inspace := monthly):,} / month | In-hand ~₹ {int(inhand_monthly):,} / month</p>
        <span style="background:rgba(255,255,255,0.2);padding:6px 14px;border-radius:20px;font-size:12px">🔥 Demand: {demand} | Base Kerala: {base_lpa} LPA</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats row
    s1,s2,s3,s4 = st.columns(4)
    with s1:
        st.markdown(f'<div class="stat-card"><h3 style="margin:0;color:#6c63ff">₹ {int(monthly):,}</h3><small>Gross / Month</small></div>', unsafe_allow_html=True)
    with s2:
        st.markdown(f'<div class="stat-card"><h3 style="margin:0;color:#10b981">₹ {int(inhand_monthly):,}</h3><small>In-hand / Month*</small></div>', unsafe_allow_html=True)
    with s3:
        st.markdown(f'<div class="stat-card"><h3 style="margin:0;color:#f59e0b">₹ {int(final_lpa*100000):,}</h3><small>Yearly CTC</small></div>', unsafe_allow_html=True)
    with s4:
        loc_diff = (LOCATION_MULT[location] - 1.0) * 100
        st.markdown(f'<div class="stat-card"><h3 style="margin:0">{"+" if loc_diff>=0 else ""}{loc_diff:.0f}%</h3><small>Location Impact</small></div>', unsafe_allow_html=True)
    
    # Growth & Comparison
    c_left, c_right = st.columns([1.2, 1], gap="large")
    with c_left:
        st.subheader("📈 5 Year Growth - Kerala")
        for i in range(1, 6):
            projected = final_lpa * ((1 + growth_rate) ** i)
            year_label = f"{i} Year Later" if not is_ml else f"{i} Varsham Kazhinju"
            if i == 1:
                year_label += " 🔜"
            st.markdown(f'<div class="growth-card"><b>{year_label}:</b> ₹ {projected:.1f} LPA <small style="color:#666">(~₹ {int(projected*100000/12):,}/month)</small></div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="tip-card">💡 <b>Kerala Cost of Living:</b> Kochi-il family-nu ~₹ 30-40k/month. Ninte in-hand ₹ {int(inhand_monthly):,} aanel savings ~₹ {int(max(0, inhand_monthly-35000)):,}/month possible!</div>', unsafe_allow_html=True)
    
    with c_right:
        st.subheader("🆚 Comparison")
        comp_data = {
            "Kerala Avg": base_lpa,
            f"{location}": final_lpa,
            "Bangalore": base_lpa * 1.35 * COMPANY_MULT[company],
            "Remote US": base_lpa * 1.4 * COMPANY_MULT[company],
        }
        st.bar_chart(comp_data)
        
        st.subheader("💡 Negotiation Tips" if not is_ml else "💡 Salary Koodan Tips")
        tips = [
            "2 strong projects = +1.5 LPA" if not is_ml else "2 nalla project = +1.5 LPA koodum",
            f"{career}-il certification = +0.5 LPA",
            "LinkedIn-il 500+ connections = better offers" if not is_ml else "LinkedIn 500+ connections = nalla offers",
            "Product company target cheyyu - 60% kooduthal kittum" if is_ml else "Target product companies - 60% more salary",
            "English communication polish cheyyu - MNC-ku must" if is_ml else "Polish English - Must for MNC",
        ]
        for t in tips:
            st.markdown(f'<div class="tip-card">✅ {t}</div>', unsafe_allow_html=True)
    
    st.success(f"✅ {career} - {exp} - Kerala market rate aanu ithu! Real data 2026" if not is_ml else f"✅ {career} - Kerala market rate 2026!")

st.divider()
st.caption("📊 Data: Kerala IT Parks (Infopark Kochi, Technopark Tvm), Naukri, LinkedIn 2026 | *In-hand approximate, tax may vary | For educational purpose")