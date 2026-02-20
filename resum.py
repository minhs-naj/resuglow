import streamlit as st
import pdfplumber
from groq import Groq
import json, re

GROQ_API_KEY ="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"
st.set_page_config(page_title="ResuGlow", page_icon="✨", layout="wide")

# ── Embed OriginTech font as base64 ──────────────────────────────
ORIGINTECH_B64 = "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"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Montserrat:wght@300;400;500;600&family=Share+Tech+Mono&display=swap');

@font-face {{
    font-family: 'OriginTech';
    src: url('data:font/truetype;base64,{ORIGINTECH_B64}') format('truetype');
    font-weight: normal;
    font-style: normal;
}}

*, *::before, *::after {{ box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: #080808 !important;
    color: #e8e0d0 !important;
}}

#MainMenu, footer, header, [data-testid="stToolbar"] {{ visibility: hidden !important; }}
[data-testid="stDecoration"] {{ display: none !important; }}

body, .stMarkdown, .stText, p, label, div {{
    font-family: 'Montserrat', sans-serif !important;
    font-weight: 300;
    letter-spacing: 0.02em;
}}

::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-track {{ background: #111; }}
::-webkit-scrollbar-thumb {{ background: #D4AF37; border-radius: 2px; }}

[data-testid="stAppViewContainer"]::before {{
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 20%, rgba(212,175,55,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(212,175,55,0.03) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}}

.block-container {{
    max-width: 1400px !important;
    padding: 2rem 3rem !important;
}}

@keyframes goldShimmer {{
    0%, 100% {{ filter: drop-shadow(0 0 12px rgba(212,175,55,0.3)); }}
    50%       {{ filter: drop-shadow(0 0 35px rgba(255,248,220,0.7)) drop-shadow(0 0 70px rgba(212,175,55,0.5)); }}
}}

/* ── SPLASH BUTTON — Share Tech Mono (techy feel) ── */
.splash-btn-wrap button {{
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.4em !important;
    text-transform: uppercase !important;
    background: transparent !important;
    border: 1px solid rgba(212,175,55,0.35) !important;
    color: rgba(212,175,55,0.65) !important;
    padding: 0.7rem 2.5rem !important;
    border-radius: 0 !important;
    transition: all 0.4s ease !important;
    cursor: pointer !important;
    margin-top: 1rem !important;
}}
.splash-btn-wrap button:hover {{
    border-color: #D4AF37 !important;
    color: #D4AF37 !important;
    background: rgba(212,175,55,0.05) !important;
    box-shadow: 0 0 25px rgba(212,175,55,0.2), inset 0 0 25px rgba(212,175,55,0.04) !important;
    letter-spacing: 0.55em !important;
}}

.rg-header {{ text-align: center; padding: 3rem 0 1.5rem; }}
.rg-wordmark {{
    font-family: 'OriginTech', serif !important;
    font-size: clamp(3.5rem, 8vw, 6rem);
    font-weight: normal;
    letter-spacing: 0.25em;
    background: linear-gradient(135deg, #8B6914 0%, #D4AF37 35%, #FFF8DC 55%, #D4AF37 75%, #8B6914 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: goldShimmer 4s ease-in-out infinite;
    display: block;
    line-height: 1;
}}
.rg-tagline {{
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.7rem;
    font-weight: 400;
    letter-spacing: 0.55em;
    color: rgba(212,175,55,0.45);
    text-transform: uppercase;
    margin-top: 0.6rem;
}}
.rg-divider {{
    width: 120px; height: 1px;
    background: linear-gradient(90deg, transparent, #D4AF37, transparent);
    margin: 1.5rem auto;
}}

[data-testid="stRadio"] > div {{
    display: flex !important;
    gap: 1rem !important;
    justify-content: center !important;
    background: transparent !important;
}}
[data-testid="stRadio"] label {{
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: rgba(212,175,55,0.55) !important;
    padding: 0.6rem 1.8rem !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
    border-radius: 0 !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    background: transparent !important;
}}
[data-testid="stRadio"] label:hover {{
    border-color: rgba(212,175,55,0.6) !important;
    color: #D4AF37 !important;
    background: rgba(212,175,55,0.04) !important;
}}

.rg-panel {{
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(212,175,55,0.12);
    border-radius: 2px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    transition: border-color 0.3s ease;
}}
.rg-panel:hover {{ border-color: rgba(212,175,55,0.25); }}
.rg-panel::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #D4AF37, transparent);
    border-radius: 2px 0 0 2px;
}}
.rg-panel-title {{
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.1rem;
    font-weight: 400;
    letter-spacing: 0.2em;
    color: #D4AF37;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
}}
.rg-panel-title::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(212,175,55,0.3), transparent);
}}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] div[data-baseweb="select"] {{
    background: rgba(212,175,55,0.03) !important;
    border: 1px solid rgba(212,175,55,0.15) !important;
    border-radius: 2px !important;
    color: #e8e0d0 !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 300 !important;
    letter-spacing: 0.04em !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {{
    border-color: #D4AF37 !important;
    box-shadow: 0 0 0 1px rgba(212,175,55,0.3), 0 0 20px rgba(212,175,55,0.08) !important;
    outline: none !important;
}}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
[data-testid="stFileUploader"] label {{
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.2em !important;
    text-transform: uppercase !important;
    color: rgba(212,175,55,0.6) !important;
    margin-bottom: 0.4rem !important;
}}
[data-testid="stSelectbox"] [data-baseweb="select"] > div {{
    background: rgba(212,175,55,0.03) !important;
    border: 1px solid rgba(212,175,55,0.15) !important;
    border-radius: 2px !important;
}}
[data-baseweb="popover"] {{
    background: #0f0f0f !important;
    border: 1px solid rgba(212,175,55,0.2) !important;
}}
[data-baseweb="menu"] li {{
    background: #0f0f0f !important;
    color: #e8e0d0 !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.82rem !important;
}}
[data-baseweb="menu"] li:hover {{ background: rgba(212,175,55,0.1) !important; }}

[data-testid="stFileUploader"] section {{
    background: rgba(212,175,55,0.02) !important;
    border: 1px dashed rgba(212,175,55,0.25) !important;
    border-radius: 2px !important;
    transition: all 0.3s ease !important;
}}
[data-testid="stFileUploader"] section:hover {{
    border-color: rgba(212,175,55,0.6) !important;
    background: rgba(212,175,55,0.05) !important;
}}
[data-testid="stFileUploader"] section p {{
    color: rgba(212,175,55,0.5) !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.08em !important;
}}

[data-testid="stExpander"] {{
    background: rgba(212,175,55,0.02) !important;
    border: 1px solid rgba(212,175,55,0.12) !important;
    border-radius: 2px !important;
    margin-bottom: 0.8rem !important;
}}
[data-testid="stExpander"] summary {{
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    color: rgba(212,175,55,0.65) !important;
    padding: 0.9rem 1.2rem !important;
}}
[data-testid="stExpander"] summary:hover {{ color: #D4AF37 !important; background: rgba(212,175,55,0.04) !important; }}
[data-testid="stExpander"] details[open] summary {{ color: #D4AF37 !important; border-bottom: 1px solid rgba(212,175,55,0.12) !important; }}

[data-testid="stButton"] button[kind="primary"] {{
    background: linear-gradient(135deg, #8B6914, #D4AF37, #C9A227) !important;
    border: none !important;
    border-radius: 2px !important;
    color: #080808 !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase !important;
    padding: 0.85rem 3rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(212,175,55,0.25) !important;
    width: 100% !important;
}}
[data-testid="stButton"] button[kind="primary"]:hover {{
    box-shadow: 0 6px 35px rgba(212,175,55,0.5), 0 0 60px rgba(212,175,55,0.15) !important;
    transform: translateY(-1px) !important;
}}

[data-testid="stTabs"] [data-baseweb="tab-list"] {{
    background: transparent !important;
    border-bottom: 1px solid rgba(212,175,55,0.15) !important;
    gap: 0 !important;
}}
[data-testid="stTabs"] [data-baseweb="tab"] {{
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    color: rgba(212,175,55,0.4) !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.18em !important;
    text-transform: uppercase !important;
    padding: 0.8rem 1.5rem !important;
    transition: all 0.3s ease !important;
}}
[data-testid="stTabs"] [aria-selected="true"] {{
    color: #D4AF37 !important;
    border-bottom-color: #D4AF37 !important;
    background: rgba(212,175,55,0.04) !important;
}}

.rg-gauge-row {{ display: flex; gap: 1.5rem; margin: 1.5rem 0; flex-wrap: wrap; }}
.rg-gauge {{
    flex: 1; min-width: 160px;
    background: rgba(212,175,55,0.03);
    border: 1px solid rgba(212,175,55,0.12);
    border-radius: 2px;
    padding: 1.5rem 1.2rem 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease;
}}
.rg-gauge:hover {{ border-color: rgba(212,175,55,0.3); }}
.rg-gauge::before {{
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--gauge-color, #D4AF37), transparent);
}}
.rg-gauge-label {{ font-size: 0.6rem; font-weight: 500; letter-spacing: 0.25em; text-transform: uppercase; color: rgba(212,175,55,0.45); margin-bottom: 0.8rem; }}
.rg-gauge-value {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 3.2rem; font-weight: 300; line-height: 1;
    background: linear-gradient(135deg, #8B6914, #D4AF37, #FFF8DC);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    animation: goldShimmer 4s ease-in-out infinite;
}}
.rg-gauge-unit {{ font-size: 0.85rem; color: rgba(212,175,55,0.4); font-weight: 300; }}
.rg-gauge-bar {{ margin-top: 1rem; height: 3px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; }}
.rg-gauge-fill {{ height: 100%; border-radius: 2px; background: linear-gradient(90deg, #8B6914, #D4AF37); box-shadow: 0 0 8px rgba(212,175,55,0.6); }}
.rg-status-badge {{ display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.4rem 1rem; border-radius: 2px; font-size: 0.65rem; font-weight: 500; letter-spacing: 0.2em; text-transform: uppercase; margin-top: 0.8rem; }}
.rg-status-ready   {{ background: rgba(144,238,144,0.08); border: 1px solid rgba(144,238,144,0.25); color: #90EE90; }}
.rg-status-warning {{ background: rgba(212,175,55,0.08);  border: 1px solid rgba(212,175,55,0.3);  color: #D4AF37; }}
.rg-status-danger  {{ background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.25); color: #ff6b6b; }}

.rg-verdict {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem; font-weight: 300; font-style: italic;
    color: #D4AF37; line-height: 1.5;
    padding: 1.2rem 0;
    border-bottom: 1px solid rgba(212,175,55,0.12);
    margin-bottom: 1rem;
}}
.rg-summary {{ font-size: 0.88rem; color: rgba(232,224,208,0.75); line-height: 1.8; font-weight: 300; }}
.rg-skill-pill {{ display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.35rem 0.9rem; border-radius: 2px; font-size: 0.72rem; font-weight: 500; letter-spacing: 0.08em; margin: 0.25rem; }}
.rg-skill-matched {{ background: rgba(144,238,144,0.07); border: 1px solid rgba(144,238,144,0.2); color: #90EE90; }}
.rg-skill-missing  {{ background: rgba(255,107,107,0.07); border: 1px solid rgba(255,107,107,0.2); color: #ff8080; }}
.rg-point-card {{ padding: 0.9rem 1rem; border-radius: 2px; margin: 0.5rem 0; font-size: 0.83rem; line-height: 1.6; font-weight: 300; }}
.rg-point-best  {{ background: rgba(144,238,144,0.05); border-left: 2px solid #90EE90; color: rgba(232,224,208,0.85); }}
.rg-point-worst {{ background: rgba(255,107,107,0.05); border-left: 2px solid #ff6b6b; color: rgba(232,224,208,0.85); }}
.rg-tip-card {{ padding: 0.9rem 1.1rem; border-radius: 2px; margin: 0.5rem 0; font-size: 0.83rem; line-height: 1.6; font-weight: 300; display: flex; gap: 0.8rem; align-items: flex-start; }}
.rg-tip-improve {{ background: rgba(100,149,237,0.05); border: 1px solid rgba(100,149,237,0.15); color: rgba(232,224,208,0.85); }}
.rg-tip-quick   {{ background: rgba(144,238,144,0.05); border: 1px solid rgba(144,238,144,0.15); color: rgba(232,224,208,0.85); }}
.rg-tip-ats     {{ background: rgba(212,175,55,0.05);  border: 1px solid rgba(212,175,55,0.18);  color: rgba(232,224,208,0.85); }}
.rg-tip-num {{ font-family: 'Cormorant Garamond', serif; font-size: 1.1rem; color: rgba(212,175,55,0.4); min-width: 1.5rem; line-height: 1.4; }}
.rg-note-row {{ display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap; }}
.rg-note {{ flex: 1; min-width: 200px; background: rgba(212,175,55,0.03); border: 1px solid rgba(212,175,55,0.1); border-radius: 2px; padding: 0.9rem 1.1rem; }}
.rg-note-key {{ font-size: 0.6rem; letter-spacing: 0.25em; text-transform: uppercase; color: rgba(212,175,55,0.45); margin-bottom: 0.35rem; }}
.rg-note-val {{ font-size: 0.84rem; color: rgba(232,224,208,0.8); line-height: 1.5; font-weight: 300; }}

.rg-big-percent {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 6rem; font-weight: 300; text-align: center;
    background: linear-gradient(135deg, #8B6914, #D4AF37, #FFF8DC, #D4AF37, #8B6914);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    animation: goldShimmer 4s ease-in-out infinite;
    line-height: 1; padding: 1rem 0 0.5rem;
}}
.rg-big-label {{ text-align: center; font-size: 0.68rem; letter-spacing: 0.3em; text-transform: uppercase; color: rgba(212,175,55,0.5); margin-bottom: 1rem; }}
.rg-enhance-box {{ background: rgba(212,175,55,0.02); border: 1px solid rgba(212,175,55,0.12); border-radius: 2px; padding: 1.4rem; margin: 0.6rem 0; color: rgba(232,224,208,0.85); font-size: 0.87rem; line-height: 1.75; font-weight: 300; transition: border-color 0.3s; }}
.rg-enhance-box:hover {{ border-color: rgba(212,175,55,0.25); }}
.rg-improve-card {{ background: rgba(0,0,0,0.3); border-left: 2px solid #D4AF37; border-radius: 0 2px 2px 0; padding: 1.1rem 1.3rem; margin: 0.7rem 0; }}
.rg-improve-area  {{ font-family: 'Cormorant Garamond', serif; font-size: 1rem; color: #D4AF37; font-weight: 400; letter-spacing: 0.1em; margin-bottom: 0.5rem; }}
.rg-improve-issue {{ font-size: 0.8rem; color: rgba(255,107,107,0.85); margin: 0.3rem 0; line-height: 1.5; }}
.rg-improve-fix   {{ font-size: 0.8rem; color: rgba(144,238,144,0.85); line-height: 1.5; }}
.rg-kw-pill {{ display: inline-block; background: rgba(212,175,55,0.06); border: 1px solid rgba(212,175,55,0.25); border-radius: 2px; padding: 0.4rem 1rem; margin: 0.3rem; color: #D4AF37; font-size: 0.75rem; font-weight: 500; letter-spacing: 0.1em; transition: all 0.2s ease; }}
.rg-kw-pill:hover {{ background: rgba(212,175,55,0.12); border-color: #D4AF37; }}
.rg-skill-item {{ display: flex; align-items: center; gap: 0.5rem; font-size: 0.82rem; padding: 0.3rem 0; color: rgba(232,224,208,0.8); border-bottom: 1px solid rgba(255,255,255,0.04); font-weight: 300; }}
.rg-skill-dot-present {{ color: #90EE90; }}
.rg-skill-dot-partial  {{ color: #FFD700; }}
.rg-skill-dot-missing  {{ color: #ff6b6b; }}
.rg-section-sublabel {{ font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(212,175,55,0.4); margin-bottom: 0.8rem; }}
.splash-wrap {{ display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 85vh; }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# FUNCTIONS
# ══════════════════════════════════════════════════════════════════

def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if page_text:
                text += page_text + "\n"
    return text


def detect_sections(text):
    sections = {"experience": "", "skills": "", "education": "", "other": ""}
    patterns = {
        "experience": r"(experience|work history|employment|career)",
        "skills":     r"(skills|tools|technologies|competencies|expertise)",
        "education":  r"(education|university|degree|academic|qualification)",
    }
    current = "other"
    for line in text.split("\n"):
        for section, pattern in patterns.items():
            if re.search(pattern, line.lower()) and len(line) < 70:
                current = section
                break
        sections[current] += line + "\n"
    return sections


def call_groq(prompt: str, max_tokens: int = 2000) -> dict:
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an expert career coach and elite resume strategist. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.25,
        max_tokens=max_tokens
    )
    return json.loads(response.choices[0].message.content.strip())


def analyze(resume_text, sections, job_desc, field, industry, seniority,
            years_exp, location, salary, job_type, remote,
            education, goal, languages, portfolio, company_info) -> dict:
    prompt = f"""
You are an expert career coach and recruiter. Analyze the resume against the job description.

CANDIDATE PROFILE:
- Field: {field} | Industry: {industry} | Seniority: {seniority}
- Experience: {years_exp} | Job Type: {job_type} | Work Mode: {remote}
- Education: {education} | Career Goal: {goal}
- Location: {location} | Salary Target: {salary}
- Languages: {languages} | Portfolio: {portfolio}
- Company Context: {company_info}

RESUME (first 3000 chars):
{resume_text[:3000]}

JOB DESCRIPTION (first 1500 chars):
{job_desc[:1500]}

Return a JSON object with exactly these keys:
{{
  "match_score": <integer 0-100>,
  "ats_score": <integer 0-100>,
  "verdict": "<one powerful sentence verdict>",
  "summary": "<3 sentence detailed summary>",
  "matched_skills": ["<skill>"],
  "missing_skills": ["<skill>"],
  "best_points": ["<point>", "<point>", "<point>"],
  "worst_points": ["<point>", "<point>", "<point>"],
  "improvements": ["<tip>", "<tip>", "<tip>", "<tip>"],
  "ats_tips": ["<tip>", "<tip>", "<tip>"],
  "quick_wins": ["<win>", "<win>", "<win>"],
  "salary_note": "<one sentence>",
  "location_note": "<one sentence>"
}}
"""
    return call_groq(prompt, max_tokens=2000)


def enhance_resume(resume_text, target_job) -> dict:
    prompt = f"""
You are an elite resume writer and career coach. The candidate targets: "{target_job}"

RESUME:
{resume_text[:3000]}

Return a JSON object:
{{
  "skill_match_percent": <integer 0-100>,
  "skill_match_breakdown": {{
    "present_skills": ["<skill>"],
    "partially_present": ["<skill>"],
    "missing_skills": ["<skill>"]
  }},
  "enhanced_summary": "<rewritten 3-5 sentence professional summary>",
  "enhanced_experience_bullets": ["<bullet>", "<bullet>", "<bullet>"],
  "areas_of_improvement": [
    {{"area": "<name>", "issue": "<what is wrong>", "fix": "<exact fix>"}},
    {{"area": "<name>", "issue": "<what is wrong>", "fix": "<exact fix>"}},
    {{"area": "<name>", "issue": "<what is wrong>", "fix": "<exact fix>"}},
    {{"area": "<name>", "issue": "<what is wrong>", "fix": "<exact fix>"}}
  ],
  "keywords_to_add": ["<kw>", "<kw>", "<kw>", "<kw>", "<kw>", "<kw>"],
  "overall_enhance_tip": "<one powerful overarching advice>"
}}
"""
    return call_groq(prompt, max_tokens=2500)


# ══════════════════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════════════════

def gauge_html(label, value, color="#D4AF37"):
    status_map = [
        (80, "rg-status-ready",   "● Excellent"),
        (60, "rg-status-warning", "◐ Good"),
        (40, "rg-status-warning", "◌ Fair"),
        (0,  "rg-status-danger",  "○ Low"),
    ]
    cls, txt = next((c, t) for threshold, c, t in status_map if value >= threshold)
    return f"""
    <div class="rg-gauge" style="--gauge-color:{color}">
        <div class="rg-gauge-label">{label}</div>
        <div class="rg-gauge-value">{value}<span class="rg-gauge-unit">%</span></div>
        <div class="rg-gauge-bar"><div class="rg-gauge-fill" style="width:{value}%"></div></div>
        <div style="margin-top:0.8rem"><span class="rg-status-badge {cls}">{txt}</span></div>
    </div>"""

def panel(title, icon="◈"):
    return f'<div class="rg-panel-title">{icon} {title}</div>'

def skill_pills(skills, cls):
    return "".join(f'<span class="rg-skill-pill {cls}">{s}</span>' for s in skills)


# ══════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════
if "page" not in st.session_state:
    st.session_state.page = "splash"


# ══════════════════════════════════════════════════════════════════
# SPLASH
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "splash":
    st.markdown("""
    <div class="splash-wrap">
        <div style="text-align:center">
            <div style="font-family:'OriginTech',serif;font-size:clamp(4rem,12vw,9rem);
                        font-weight:normal;letter-spacing:0.3em;
                        background:linear-gradient(135deg,#8B6914,#D4AF37,#FFF8DC,#D4AF37,#8B6914);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;animation:goldShimmer 4s ease-in-out infinite;line-height:1;">
                ResuGlow
            </div>
            <div style="font-size:0.65rem;letter-spacing:0.6em;text-transform:uppercase;
                        color:rgba(212,175,55,0.4);margin-top:1rem;font-family:'Montserrat',sans-serif;">
                Your Career &nbsp;·&nbsp; Illuminated
            </div>
            <div style="width:80px;height:1px;background:linear-gradient(90deg,transparent,#D4AF37,transparent);
                        margin:2rem auto;"></div>
        </div>
    </div>
    <script>
        setTimeout(function() {
            const btn = window.parent.document.querySelector('[data-testid="stButton"] button');
            if (btn) btn.click();
        }, 2800);
    </script>
    """, unsafe_allow_html=True)

    st.markdown('<div class="splash-btn-wrap">', unsafe_allow_html=True)
    if st.button("Get Started", key="auto_enter"):
        st.session_state.page = "app"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "app":

    st.markdown("""
    <div class="rg-header">
        <span class="rg-wordmark">ResuGlow</span>
        <div class="rg-tagline">Your Career &nbsp;·&nbsp; Illuminated</div>
        <div class="rg-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio("", ["Analyzer", "Enhancer"], horizontal=True, label_visibility="collapsed")
    st.markdown("<div style='margin:1.5rem 0'></div>", unsafe_allow_html=True)

    # ════════════════════════════════
    # ANALYZER
    # ════════════════════════════════
    if mode == "Analyzer":
        left, right = st.columns([1.1, 0.9], gap="large")

        with left:
            st.markdown(panel("Primary Inputs"), unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Resume Document", type=["pdf"], key="ana_upload")
            job_desc      = st.text_area("Job Description", height=200, placeholder="Paste the full job posting here...")
            company_info  = st.text_area("Company Context  (optional)", height=80, placeholder="Mission, culture, recent news...")

        with right:
            st.markdown(panel("Professional Profile"), unsafe_allow_html=True)

            with st.expander("Career and Education", expanded=True):
                ca, cb = st.columns(2)
                with ca:
                    field     = st.selectbox("Field of Study", ["Technology","Medicine","Law","Education","Finance","Creative Arts","Science","Marketing","Engineering"])
                    education = st.selectbox("Highest Education", ["High School","Diploma","Bachelor's","Master's","PhD","Professional Degree"])
                    goal      = st.selectbox("Career Goal", ["Get a job","Switch careers","Get promoted","Land internship","Graduate job"])
                with cb:
                    seniority = st.selectbox("Seniority Level", ["Internship","Junior","Mid-Level","Senior","Lead","Manager","Executive"])
                    years_exp = st.selectbox("Years of Experience", ["0 - Student","Less than 1","1-2 years","3-5 years","6-10 years","10+ years"])
                    languages = st.text_input("Languages", placeholder="English, French...")

            with st.expander("Industry and Role"):
                ca, cb = st.columns(2)
                with ca:
                    industry = st.selectbox("Industry", ["Technology","Healthcare","Finance","Legal","Education","Government","Retail","Manufacturing","Media","Consulting","Non-Profit","Startups"])
                    job_type = st.selectbox("Job Type", ["Full-Time","Part-Time","Internship","Contract","Graduate"])
                with cb:
                    remote    = st.selectbox("Work Preference", ["On-site","Hybrid","Fully Remote","No Preference"])
                    portfolio = st.text_input("LinkedIn / Portfolio", placeholder="linkedin.com/in/you")

            with st.expander("Compensation and Location"):
                ca, cb = st.columns(2)
                with ca:
                    location = st.text_input("Location", placeholder="London, UK")
                with cb:
                    salary = st.text_input("Salary Target", placeholder="35,000 / yr")

        st.markdown("<div style='margin:1.5rem 0'></div>", unsafe_allow_html=True)
        _, cta, _ = st.columns([2, 3, 2])
        with cta:
            run = st.button("Illuminate My Resume", type="primary")

        if run:
            if not uploaded_file or not job_desc.strip():
                st.error("Please upload a resume and provide a job description.")
            else:
                with st.spinner("Analyzing your profile..."):
                    resume_text = extract_text(uploaded_file)
                    sections    = detect_sections(resume_text)
                    result      = analyze(resume_text, sections, job_desc,
                                          field, industry, seniority, years_exp,
                                          location, salary, job_type, remote,
                                          education, goal, languages, portfolio, company_info)

                score = result.get("match_score", 0)
                ats   = result.get("ats_score", 0)
                gc    = "#90EE90" if score >= 70 else ("#D4AF37" if score >= 50 else "#ff6b6b")

                st.markdown(f'<div class="rg-gauge-row">{gauge_html("Match Score", score, gc)}{gauge_html("ATS Score", ats, "#D4AF37")}</div>', unsafe_allow_html=True)

                t1, t2, t3, t4 = st.tabs(["Overview", "Skills", "Strengths and Gaps", "Action Plan"])

                with t1:
                    st.markdown(f'<div class="rg-verdict">"{result.get("verdict","")}"</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="rg-summary">{result.get("summary","")}</div>', unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="rg-note-row">
                        <div class="rg-note"><div class="rg-note-key">Salary</div><div class="rg-note-val">{result.get("salary_note","")}</div></div>
                        <div class="rg-note"><div class="rg-note-key">Location</div><div class="rg-note-val">{result.get("location_note","")}</div></div>
                    </div>""", unsafe_allow_html=True)

                with t2:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown('<div class="rg-section-sublabel">Matched Skills</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="line-height:2">{skill_pills(result.get("matched_skills",[]), "rg-skill-matched")}</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown('<div class="rg-section-sublabel">Missing Skills</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="line-height:2">{skill_pills(result.get("missing_skills",[]), "rg-skill-missing")}</div>', unsafe_allow_html=True)

                with t3:
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown('<div class="rg-section-sublabel">Strongest Points</div>', unsafe_allow_html=True)
                        for p in result.get("best_points", []):
                            st.markdown(f'<div class="rg-point-card rg-point-best">▸ {p}</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown('<div class="rg-section-sublabel">Weakest Points</div>', unsafe_allow_html=True)
                        for p in result.get("worst_points", []):
                            st.markdown(f'<div class="rg-point-card rg-point-worst">▸ {p}</div>', unsafe_allow_html=True)

                with t4:
                    st.markdown('<div class="rg-section-sublabel" style="margin-bottom:1rem">Strategic Improvements</div>', unsafe_allow_html=True)
                    for i, tip in enumerate(result.get("improvements", []), 1):
                        st.markdown(f'<div class="rg-tip-card rg-tip-improve"><span class="rg-tip-num">{i:02d}</span><span>{tip}</span></div>', unsafe_allow_html=True)
                    st.markdown('<div class="rg-section-sublabel" style="margin:1.2rem 0 0.8rem">Quick Wins</div>', unsafe_allow_html=True)
                    for w in result.get("quick_wins", []):
                        st.markdown(f'<div class="rg-tip-card rg-tip-quick"><span class="rg-tip-num">▸</span><span>{w}</span></div>', unsafe_allow_html=True)
                    st.markdown('<div class="rg-section-sublabel" style="margin:1.2rem 0 0.8rem">ATS Optimisations</div>', unsafe_allow_html=True)
                    for tip in result.get("ats_tips", []):
                        st.markdown(f'<div class="rg-tip-card rg-tip-ats"><span class="rg-tip-num">◈</span><span>{tip}</span></div>', unsafe_allow_html=True)

    # ════════════════════════════════
    # ENHANCER
    # ════════════════════════════════
    elif mode == "Enhancer":
        left, right = st.columns([1, 1], gap="large")

        with left:
            st.markdown(panel("Upload and Target Role"), unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Resume Document", type=["pdf"], key="enh_upload")
            target_job    = st.text_input("Target Job Title", placeholder="e.g. Senior Data Scientist, Product Manager...")
            st.markdown("<div style='margin:1rem 0'></div>", unsafe_allow_html=True)
            run_enh = st.button("Enhance My Resume", type="primary")

        with right:
            st.markdown(panel("How It Works"), unsafe_allow_html=True)
            st.markdown("""
            <div style="color:rgba(232,224,208,0.55);font-size:0.82rem;line-height:2.4;font-weight:300;">
                <div>◈ &nbsp; Upload your existing resume PDF</div>
                <div>◈ &nbsp; Enter the exact job title you are targeting</div>
                <div>◈ &nbsp; Receive a precise skill-match percentage</div>
                <div>◈ &nbsp; Get an AI-rewritten summary and bullet points</div>
                <div>◈ &nbsp; Discover every gap with an exact fix</div>
            </div>""", unsafe_allow_html=True)

        if run_enh:
            if not uploaded_file:
                st.error("Please upload your resume PDF.")
            elif not target_job.strip():
                st.error("Please enter a target job title.")
            else:
                with st.spinner(f"Analyzing for '{target_job}'..."):
                    resume_text = extract_text(uploaded_file)
                    result      = enhance_resume(resume_text, target_job)

                pct = result.get("skill_match_percent", 0)
                bc  = "#90EE90" if pct >= 70 else ("#D4AF37" if pct >= 45 else "#ff6b6b")

                st.markdown(f"""
                <div class="rg-big-percent">{pct}<span style="font-size:2.5rem">%</span></div>
                <div class="rg-big-label">Skill Match · {target_job}</div>
                <div style="max-width:500px;margin:0 auto 1rem;">
                    <div class="rg-gauge-bar" style="height:5px;">
                        <div class="rg-gauge-fill" style="width:{pct}%;background:linear-gradient(90deg,#8B6914,{bc});"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

                if pct >= 80:   st.success("Outstanding match — you are a compelling candidate for this role.")
                elif pct >= 60: st.warning("Strong foundation — targeted refinements will set you apart.")
                elif pct >= 40: st.warning("Moderate alignment — a focused effort will close the gap.")
                else:           st.error("Significant gaps detected — strategic upskilling recommended.")

                st.markdown("<div style='margin:1rem 0'></div>", unsafe_allow_html=True)

                e1, e2, e3, e4 = st.tabs(["Skill Breakdown", "Enhanced Copy", "Improvement Plan", "Keywords"])

                with e1:
                    bd = result.get("skill_match_breakdown", {})
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown('<div class="rg-section-sublabel">You Have</div>', unsafe_allow_html=True)
                        for s in bd.get("present_skills", []):
                            st.markdown(f'<div class="rg-skill-item"><span class="rg-skill-dot-present">●</span>{s}</div>', unsafe_allow_html=True)
                    with c2:
                        st.markdown('<div class="rg-section-sublabel">Partial</div>', unsafe_allow_html=True)
                        for s in bd.get("partially_present", []):
                            st.markdown(f'<div class="rg-skill-item"><span class="rg-skill-dot-partial">◑</span>{s}</div>', unsafe_allow_html=True)
                    with c3:
                        st.markdown('<div class="rg-section-sublabel">Missing</div>', unsafe_allow_html=True)
                        for s in bd.get("missing_skills", []):
                            st.markdown(f'<div class="rg-skill-item"><span class="rg-skill-dot-missing">●</span>{s}</div>', unsafe_allow_html=True)

                with e2:
                    st.markdown('<div class="rg-section-sublabel" style="margin-bottom:0.8rem">Enhanced Professional Summary</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="rg-enhance-box">{result.get("enhanced_summary","")}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="rg-section-sublabel" style="margin:1.2rem 0 0.8rem">Stronger Experience Bullets</div>', unsafe_allow_html=True)
                    for b in result.get("enhanced_experience_bullets", []):
                        st.markdown(f'<div class="rg-enhance-box">▸ &nbsp;{b}</div>', unsafe_allow_html=True)
                    tip = result.get("overall_enhance_tip", "")
                    if tip:
                        st.markdown(f'<div class="rg-tip-card rg-tip-ats" style="margin-top:1rem"><span class="rg-tip-num">◈</span><span><strong>Pro Tip:</strong> {tip}</span></div>', unsafe_allow_html=True)

                with e3:
                    st.markdown('<div class="rg-section-sublabel" style="margin-bottom:0.8rem">Each card shows the issue and its exact fix</div>', unsafe_allow_html=True)
                    for area in result.get("areas_of_improvement", []):
                        st.markdown(f"""
                        <div class="rg-improve-card">
                            <div class="rg-improve-area">◈ {area.get("area","")}</div>
                            <div class="rg-improve-issue">Issue: {area.get("issue","")}</div>
                            <div class="rg-improve-fix">Fix: {area.get("fix","")}</div>
                        </div>""", unsafe_allow_html=True)

                with e4:
                    st.markdown('<div class="rg-section-sublabel" style="margin-bottom:1rem">Add these to boost ATS visibility for this role</div>', unsafe_allow_html=True)
                    pills = "".join(f'<span class="rg-kw-pill">{kw}</span>' for kw in result.get("keywords_to_add", []))
                    st.markdown(f'<div style="margin-top:0.5rem">{pills}</div>', unsafe_allow_html=True)