import streamlit as st
from src.analyzer import analyze, interview_questions
from src.config import get_api_key
from src.parsers import extract_pdf_text
from src.rag import retrieve

st.set_page_config(page_title="AI Career Copilot", page_icon="🚀", layout="wide")

st.title("🚀 AI Career Copilot")
st.caption("Resume intelligence • job matching • skill gaps • interview coaching")

with st.sidebar:
    st.header("Settings")
    provider = st.selectbox("AI provider", ["None", "OpenAI", "Groq", "Gemini"])
    active_provider = None if provider == "None" else provider
    if active_provider and not get_api_key(active_provider):
        st.warning(f"{active_provider} key not found. The app will use deterministic analysis until you add it to .env.")

resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
resume_text = ""
if resume_file:
    resume_text = extract_pdf_text(resume_file.getvalue())
    st.success(f"Resume loaded — {len(resume_text.split())} words")

job_description = st.text_area("Paste the job description", height=260, placeholder="Paste the complete job description here...")

if st.button("Analyze my fit", type="primary", use_container_width=True):
    if not resume_text or not job_description.strip():
        st.error("Please upload a PDF resume and paste a job description first.")
    else:
        st.session_state.analysis = analyze(resume_text, job_description, active_provider)

analysis = st.session_state.get("analysis")
if analysis:
    st.divider()
    score = analysis["match_score"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Baseline match", f"{score}%")
    c2.metric("Strengths found", len(analysis.get("strengths", [])))
    c3.metric("Skill gaps", len(analysis.get("skill_gaps", [])))

    tab1, tab2, tab3 = st.tabs(["Analysis", "Interview Coach", "Grounded Q&A"])
    with tab1:
        st.subheader("Summary")
        st.write(analysis.get("summary", ""))
        st.subheader("Strengths")
        for item in analysis.get("strengths", []):
            st.write(f"• {item}")
        st.subheader("Potential skill gaps")
        for item in analysis.get("skill_gaps", []):
            st.write(f"• {item}")
        st.subheader("Recommendations")
        for item in analysis.get("recommendations", []):
            st.write(f"• {item}")

    with tab2:
        st.subheader("Questions tailored to this role")
        for item in interview_questions(resume_text, job_description, active_provider):
            st.markdown(f"**{item.get('category', 'Question')}** — {item.get('question', '')}")

    with tab3:
        st.subheader("Ask questions about your application")
        query = st.text_input("Example: Which parts of my resume best support this role?")
        if query:
            context = retrieve(query, [resume_text, job_description])
            if context:
                st.info("Relevant context:\n\n" + "\n\n---\n\n".join(context))
            else:
                st.info("No strong matching context was found in the uploaded documents.")
