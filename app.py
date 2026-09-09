import streamlit as st

from src.analyzer import analyze, interview_questions
from src.career_tools import create_cover_letter, grounded_answer, rewrite_resume
from src.config import get_api_key
from src.parsers import extract_pdf_text
from src.rag import retrieve
from src.report import build_pdf

st.set_page_config(page_title="AI Career Copilot", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# -----------------------------
# Visual system
# -----------------------------
st.markdown(
    """
<style>
:root {
    --ink: #172033;
    --muted: #667085;
    --line: #e7eaf0;
    --soft: #f7f8fc;
    --brand: #6d5dfc;
    --brand-2: #22b8cf;
}
.block-container {max-width: 1240px; padding-top: 1.4rem; padding-bottom: 4rem;}
[data-testid="stSidebar"] {border-right: 1px solid var(--line);}
[data-testid="stSidebar"] .block-container {padding-top: 1.8rem;}
.hero {
    position: relative; overflow: hidden; padding: 2.0rem 2.2rem; border-radius: 24px;
    background: linear-gradient(135deg, #eef0ff 0%, #f4f8ff 52%, #eafcff 100%);
    border: 1px solid #dfe4ff; margin-bottom: 1.35rem;
}
.hero:after {content:""; position:absolute; width:180px; height:180px; right:-60px; top:-80px; border-radius:50%; background:rgba(109,93,252,.12);}
.hero-kicker {font-size:.78rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; color:#6254e7; margin-bottom:.45rem;}
.hero h1 {font-size:2.55rem; line-height:1.08; margin:0 0 .55rem; color:var(--ink);}
.hero p {font-size:1.05rem; color:#596579; margin:0; max-width:720px;}
.badge {display:inline-block; padding:.28rem .62rem; border-radius:999px; font-size:.78rem; font-weight:700; background:#fff; border:1px solid var(--line); margin:.18rem .18rem .18rem 0; color:#475467;}
.section-card {background:#fff; border:1px solid var(--line); border-radius:18px; padding:1.05rem 1.15rem; margin:.55rem 0;}
.mini-card {background:var(--soft); border:1px solid var(--line); border-radius:16px; padding:1rem; min-height:112px;}
.mini-label {font-size:.78rem; color:var(--muted); font-weight:700; text-transform:uppercase; letter-spacing:.06em;}
.mini-title {font-size:1.03rem; font-weight:800; color:var(--ink); margin-top:.35rem;}
.score-card {background:linear-gradient(145deg,#171c2c,#2b3150); color:white; border-radius:20px; padding:1.15rem 1.25rem;}
.score-number {font-size:3rem; font-weight:900; line-height:1;}
.score-label {opacity:.72; font-size:.82rem; margin-top:.25rem;}
.tip {padding:.85rem 1rem; border-radius:14px; background:#f6f7fb; border:1px solid var(--line); color:#566173; font-size:.9rem;}
hr {border-color: var(--line) !important;}
div[data-testid="stMetric"] {background:#fff; border:1px solid var(--line); padding:.85rem 1rem; border-radius:16px; box-shadow:0 2px 10px rgba(16,24,40,.03);}
.stTabs [data-baseweb="tab-list"] {gap:.35rem; border-bottom:1px solid var(--line);}
.stTabs [data-baseweb="tab"] {height:48px; padding:0 15px; font-weight:700;}
.stButton > button {border-radius:12px; font-weight:750;}
[data-testid="stFileUploader"] {border:1px dashed #cdd3df; border-radius:16px; padding:.25rem; background:#fafbfc;}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("### ⚙️ AI Settings")
    provider = st.selectbox("AI provider", ["None", "OpenAI", "Groq", "Gemini"], index=1)
    active_provider = None if provider == "None" else provider
    if active_provider and get_api_key(active_provider):
        st.success(f"{active_provider} connected")
    elif active_provider:
        st.warning(f"{active_provider} key not found. Safe fallback mode is active.")
    else:
        st.info("Basic analysis works without an AI provider.")
    st.divider()
    st.markdown("**What happens to my resume?**")
    st.caption("Your uploaded PDF is processed for this session. API keys are read from environment variables or Streamlit Secrets and are not stored in the repository.")
    st.divider()
    st.caption("Built with Python · Streamlit · GenAI")

# -----------------------------
# Hero
# -----------------------------
st.markdown(
    '<div class="hero"><div class="hero-kicker">AI-powered career toolkit</div><h1>🚀 AI Career Copilot</h1><p>Turn one resume and one target job into a sharper application, smarter preparation, and a clear action plan.</p><div style="margin-top:.8rem"><span class="badge">ATS-style matching</span><span class="badge">Resume optimization</span><span class="badge">Interview coaching</span><span class="badge">Cover letters</span></div></div>',
    unsafe_allow_html=True,
)

# -----------------------------
# Inputs
# -----------------------------
left, right = st.columns([1, 1.35], gap="large")
with left:
    st.markdown("#### 1 · Your resume")
    resume_file = st.file_uploader("Upload PDF resume", type=["pdf"], help="Use a text-selectable PDF for the best extraction quality.")
    resume_text = ""
    if resume_file:
        resume_text = extract_pdf_text(resume_file.getvalue())
        words = len(resume_text.split())
        st.success(f"Resume loaded · {words:,} words")
    else:
        st.markdown('<div class="tip">📄 Upload your latest resume. We will use it as the candidate profile for the analysis.</div>', unsafe_allow_html=True)

with right:
    st.markdown("#### 2 · Target role")
    job_description = st.text_area(
        "Paste the complete job description",
        height=210,
        placeholder="Paste the job posting here — responsibilities, requirements, tools, qualifications, and preferred skills…",
        label_visibility="collapsed",
    )
    if job_description.strip():
        st.caption(f"Job description · {len(job_description.split()):,} words")
    else:
        st.markdown('<div class="tip">🎯 Tip: paste the exact job description you plan to apply to. More context gives the matcher more signal.</div>', unsafe_allow_html=True)

analyze_col, reset_col = st.columns([4, 1])
with analyze_col:
    analyze_clicked = st.button("✨ Analyze my fit", type="primary", use_container_width=True)
with reset_col:
    if st.button("Reset", use_container_width=True):
        for key in ["analysis", "questions", "rewrite", "cover_letter"]:
            st.session_state.pop(key, None)
        st.rerun()

if analyze_clicked:
    if not resume_text or not job_description.strip():
        st.error("Please upload your PDF resume and paste a job description first.")
    else:
        with st.spinner("Building your career strategy…"):
            st.session_state.analysis = analyze(resume_text, job_description, active_provider)
            st.session_state.questions = interview_questions(resume_text, job_description, active_provider)
            st.session_state.rewrite = rewrite_resume(resume_text, job_description, active_provider)
            st.session_state.cover_letter = ""

analysis = st.session_state.get("analysis")
if analysis:
    score = int(analysis.get("match_score", 0))
    if score >= 80:
        score_text = "Strong match"
    elif score >= 60:
        score_text = "Promising match"
    elif score >= 40:
        score_text = "Needs tailoring"
    else:
        score_text = "Significant gaps"

    st.markdown("### Your application snapshot")
    score_col, metrics_col = st.columns([1.15, 2.85], gap="large")
    with score_col:
        st.markdown(f'<div class="score-card"><div class="score-number">{score}%</div><div class="score-label">ATS-style match · {score_text}</div></div>', unsafe_allow_html=True)
        st.progress(max(0, min(score, 100)) / 100)
    with metrics_col:
        c1, c2, c3 = st.columns(3)
        c1.metric("Strengths", len(analysis.get("strengths", [])))
        c2.metric("Skill gaps", len(analysis.get("skill_gaps", [])))
        c3.metric("Interview questions", len(st.session_state.get("questions", [])))
        st.markdown(f'<div class="tip">💡 <strong>What this means:</strong> {analysis.get("summary", "Review the gaps and tailor your application before applying.")}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:.4rem'></div>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Fit Analysis", "✍️ Resume Optimizer", "💌 Cover Letter", "🎤 Interview Coach", "💬 Grounded Q&A"])

    with tab1:
        left, right = st.columns(2, gap="large")
        with left:
            st.markdown("#### 💪 What already works")
            strengths = analysis.get("strengths", [])
            if strengths:
                for item in strengths:
                    st.markdown(f"- {item}")
            else:
                st.info("No strong matches were detected yet.")
        with right:
            st.markdown("#### 🧩 What to improve")
            gaps = analysis.get("skill_gaps", [])
            if gaps:
                for item in gaps:
                    st.markdown(f"- {item}")
            else:
                st.success("No major skill gaps detected by the baseline matcher.")
        st.markdown("#### 🚀 Recommended next moves")
        for i, item in enumerate(analysis.get("recommendations", []), 1):
            st.markdown(f"**{i}.** {item}")
        focus = analysis.get("interview_focus", [])
        if focus:
            st.markdown("#### 🎯 Interview focus")
            st.write(" · ".join(focus))

    with tab2:
        rewrite = st.session_state.get("rewrite", {})
        st.subheader("Make your resume more targeted")
        st.caption("The optimizer improves positioning while avoiding fabricated employers, qualifications, responsibilities, or metrics.")
        st.markdown("#### Suggested headline")
        st.code(rewrite.get("headline", ""), language=None)
        st.markdown("#### Suggested professional summary")
        st.text_area("Summary", rewrite.get("summary", ""), height=150, label_visibility="collapsed")
        st.markdown("#### Improved bullet directions")
        for bullet in rewrite.get("bullets", []):
            st.markdown(f"- {bullet}")
        keywords = rewrite.get("keywords_to_emphasize", [])
        if keywords:
            st.markdown("#### Keywords to emphasize")
            st.write(" · ".join(keywords))
        st.download_button("⬇️ Download optimization notes", str(rewrite), file_name="resume_optimization_notes.txt", mime="text/plain", width="stretch", on_click="ignore")

    with tab3:
        st.subheader("Generate a tailored cover letter")
        company = st.text_input("Company", placeholder="e.g. Barclays", key="company_name")
        role = st.text_input("Role", placeholder="e.g. Data Analyst", key="role_name")
        if st.button("✨ Generate cover letter", key="cover_letter_btn", type="primary"):
            if not company.strip() or not role.strip():
                st.error("Add the company and role first.")
            else:
                with st.spinner("Writing a tailored letter…"):
                    st.session_state.cover_letter = create_cover_letter(resume_text, job_description, company, role, active_provider)
        if st.session_state.get("cover_letter"):
            st.text_area("Cover letter", st.session_state.cover_letter, height=430, label_visibility="collapsed")
            st.download_button("⬇️ Download cover letter", st.session_state.cover_letter, file_name="cover_letter.txt", mime="text/plain", width="stretch", on_click="ignore")
        else:
            st.markdown('<div class="tip">💌 Add the company and exact role title. The generator will keep the letter grounded in your resume.</div>', unsafe_allow_html=True)

    with tab4:
        st.subheader("Practice questions tailored to this role")
        questions = st.session_state.get("questions", [])
        categories = {}
        for item in questions:
            categories.setdefault(item.get("category", "Question"), []).append(item.get("question", ""))
        for category, items in categories.items():
            st.markdown(f"#### {category}")
            for idx, question in enumerate(items, 1):
                with st.container(border=True):
                    st.markdown(f"**{idx}. {question}**")
        st.markdown('<div class="tip">🎤 Practice out loud. For behavioral questions, use a simple Situation → Action → Result structure.</div>', unsafe_allow_html=True)

    with tab5:
        st.subheader("Ask questions about your resume ↔ this job")
        query = st.text_input("What do you want to know?", placeholder="Which parts of my resume best support this role?", key="qa_query")
        if query:
            context = retrieve(query, [resume_text, job_description])
            if context:
                st.markdown(grounded_answer(query, context, active_provider))
                with st.expander("View retrieved evidence"):
                    st.write("\n\n---\n\n".join(context))
            else:
                st.info("No strong matching context was found in the uploaded documents.")

    st.divider()
    st.markdown("### 📦 Your application package")
    p1, p2 = st.columns([2.5, 1], gap="large")
    with p1:
        st.caption("Export the analysis, recommendations, interview questions, and any generated cover letter as one shareable PDF report.")
    with p2:
        pdf = build_pdf(analysis, st.session_state.get("questions", []), st.session_state.get("cover_letter", ""))
        st.download_button("📥 Download career report", pdf, file_name="ai_career_copilot_report.pdf", mime="application/pdf", width="stretch", on_click="ignore")
else:
    st.markdown("### A simple 3-step workflow")
    c1, c2, c3 = st.columns(3, gap="medium")
    c1.markdown('<div class="mini-card"><div class="mini-label">01 · Upload</div><div class="mini-title">Your resume</div><p>Give the Copilot your latest PDF resume.</p></div>', unsafe_allow_html=True)
    c2.markdown('<div class="mini-card"><div class="mini-label">02 · Match</div><div class="mini-title">Your target role</div><p>Paste the exact job description you want to win.</p></div>', unsafe_allow_html=True)
    c3.markdown('<div class="mini-card"><div class="mini-label">03 · Improve</div><div class="mini-title">Your application plan</div><p>Get fit analysis, resume guidance, interview prep, and a cover letter.</p></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:.8rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-card"><strong>🎯 Best results come from specificity.</strong><br><span style="color:#667085">Use the exact job posting, not a shortened summary. The Copilot compares your resume against the language and requirements in that posting.</span></div>', unsafe_allow_html=True)
