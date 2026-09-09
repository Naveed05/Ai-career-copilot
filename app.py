import streamlit as st

from src.analyzer import analyze, interview_questions
from src.career_tools import create_cover_letter, grounded_answer, rewrite_resume
from src.config import get_api_key
from src.parsers import extract_pdf_text
from src.rag import retrieve
from src.report import build_pdf

st.set_page_config(page_title="AI Career Copilot", page_icon="🚀", layout="wide")

st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 2rem; padding-bottom: 3rem;}
.hero {padding: 1.5rem 1.7rem; border-radius: 20px; background: linear-gradient(135deg, rgba(99,102,241,.16), rgba(14,165,233,.10)); border: 1px solid rgba(99,102,241,.20); margin-bottom: 1.2rem;}
.hero h1 {margin-bottom: .25rem; font-size: 2.35rem;}
.hero p {margin: 0; color: #64748b; font-size: 1.02rem;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🚀 AI Career Copilot</h1><p>Turn your resume + a target job description into a practical application strategy.</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ AI Settings")
    provider = st.selectbox("AI provider", ["None", "OpenAI", "Groq", "Gemini"])
    active_provider = None if provider == "None" else provider
    if active_provider and not get_api_key(active_provider):
        st.warning(f"{active_provider} key not found. Smart features will use safe fallback responses.")
    st.divider()
    st.caption("🔐 API keys stay in environment variables and are never committed to the repository.")

resume_file = st.file_uploader("📄 Upload your resume", type=["pdf"], help="PDF only. Keep your resume text selectable for best extraction quality.")
resume_text = ""
if resume_file:
    resume_text = extract_pdf_text(resume_file.getvalue())
    st.success(f"Resume loaded · {len(resume_text.split()):,} words")

job_description = st.text_area("🎯 Paste the target job description", height=230, placeholder="Paste the complete job description here…")

if st.button("✨ Analyze my fit", type="primary", use_container_width=True):
    if not resume_text or not job_description.strip():
        st.error("Please upload a PDF resume and paste a job description first.")
    else:
        with st.spinner("Analyzing your application…"):
            st.session_state.analysis = analyze(resume_text, job_description, active_provider)
            st.session_state.questions = interview_questions(resume_text, job_description, active_provider)
            st.session_state.rewrite = rewrite_resume(resume_text, job_description, active_provider)
            st.session_state.cover_letter = ""

analysis = st.session_state.get("analysis")
if analysis:
    score = analysis["match_score"]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Match score", f"{score}%")
    c2.metric("Strengths", len(analysis.get("strengths", [])))
    c3.metric("Skill gaps", len(analysis.get("skill_gaps", [])))
    c4.metric("Interview questions", len(st.session_state.get("questions", [])))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Fit Analysis", "✍️ Resume Optimizer", "💌 Cover Letter", "🎤 Interview Coach", "💬 Grounded Q&A"])

    with tab1:
        st.subheader("Your application snapshot")
        st.info(analysis.get("summary", ""))
        left, right = st.columns(2)
        with left:
            st.markdown("#### 💪 Strengths")
            for item in analysis.get("strengths", []):
                st.markdown(f"- {item}")
        with right:
            st.markdown("#### 🧩 Skill gaps")
            for item in analysis.get("skill_gaps", []):
                st.markdown(f"- {item}")
        st.markdown("#### 🚀 Recommendations")
        for item in analysis.get("recommendations", []):
            st.markdown(f"- {item}")

    with tab2:
        rewrite = st.session_state.get("rewrite", {})
        st.subheader("Make your resume more targeted")
        st.caption("The optimizer improves positioning without fabricating experience, qualifications, or metrics.")
        st.markdown("#### Suggested headline")
        st.write(rewrite.get("headline", ""))
        st.markdown("#### Suggested summary")
        st.write(rewrite.get("summary", ""))
        st.markdown("#### Improved bullet directions")
        for bullet in rewrite.get("bullets", []):
            st.markdown(f"- {bullet}")
        keywords = rewrite.get("keywords_to_emphasize", [])
        if keywords:
            st.markdown("#### Keywords to emphasize")
            st.write(" · ".join(keywords))

    with tab3:
        st.subheader("Generate a tailored cover letter")
        company = st.text_input("Company", placeholder="e.g. Atlassian")
        role = st.text_input("Role", placeholder="e.g. Data Analyst")
        if st.button("Generate cover letter", key="cover_letter_btn"):
            with st.spinner("Writing your cover letter…"):
                st.session_state.cover_letter = create_cover_letter(resume_text, job_description, company, role, active_provider)
        if st.session_state.get("cover_letter"):
            st.text_area("Cover letter", st.session_state.cover_letter, height=420)
            st.download_button("⬇️ Download cover letter", st.session_state.cover_letter, file_name="cover_letter.txt", mime="text/plain")

    with tab4:
        st.subheader("Questions tailored to this role")
        for item in st.session_state.get("questions", []):
            st.markdown(f"**{item.get('category', 'Question')}** — {item.get('question', '')}")

    with tab5:
        st.subheader("Ask about your resume ↔ job fit")
        query = st.text_input("Example: Which parts of my resume best support this role?", key="qa_query")
        if query:
            context = retrieve(query, [resume_text, job_description])
            if context:
                st.markdown(grounded_answer(query, context, active_provider))
                with st.expander("View retrieved evidence"):
                    st.write("\n\n---\n\n".join(context))
            else:
                st.info("No strong matching context was found in the uploaded documents.")

    st.divider()
    pdf = build_pdf(analysis, st.session_state.get("questions", []), st.session_state.get("cover_letter", ""))
    st.download_button("📥 Download complete career report (PDF)", pdf, file_name="ai_career_copilot_report.pdf", mime="application/pdf", use_container_width=True)
else:
    st.markdown("### How it works")
    cols = st.columns(3)
    cols[0].markdown("**1 · Upload**  \nAdd your latest PDF resume.")
    cols[1].markdown("**2 · Match**  \nPaste a job description and analyze fit.")
    cols[2].markdown("**3 · Improve**  \nOptimize, prepare, and export your application package.")
    st.caption("Tip: Start with the exact job description you plan to apply to.")
