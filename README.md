# 🚀 AI Career Copilot

AI Career Copilot is a polished Streamlit application that turns a resume + target job description into a practical job-application strategy.

## ✨ Features

- 📄 Extract text from PDF resumes
- 🎯 Transparent baseline ATS-style match scoring
- 🔎 Skill-gap and keyword detection
- 💪 Resume strengths and recommendations
- 🤖 Optional OpenAI, Groq, or Gemini analysis
- ✍️ Resume headline, summary, and bullet optimization
- 💌 Tailored cover-letter generation
- 🎤 Role-specific interview questions
- 💬 Grounded Q&A over the resume and job description
- 📥 Download a complete career report as PDF
- 🔐 Environment-based API key handling
- 🧪 Automated tests + GitHub Actions CI

## 🖥️ Product flow

```text
             ┌───────────────┐
Resume PDF ─►│  PDF Parser   │──► Resume Text ──┐
             └───────────────┘                  │
                                                ▼
Job Description ───────────────────────────► Fit Engine
                                                │
                     ┌──────────────────────────┼──────────────────────────┐
                     ▼                          ▼                          ▼
              Resume Optimizer          Interview Coach             Cover Letter
                     │                          │                          │
                     └──────────────────────────┼──────────────────────────┘
                                                ▼
                                      Grounded Q&A + PDF Report
```

## 🛠️ Tech stack

- Python
- Streamlit
- scikit-learn (TF-IDF / cosine similarity)
- pypdf
- OpenAI / Groq / Gemini (optional)
- ReportLab (PDF export)
- pytest + GitHub Actions

## ▶️ Run locally

```bash
git clone https://github.com/Naveed05/Ai-career-copilot.git
cd Ai-career-copilot
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and add only the provider key you intend to use:

```env
OPENAI_API_KEY=...
GROQ_API_KEY=...
GOOGLE_API_KEY=...
```

Then start the app:

```bash
streamlit run app.py
```

The core matching, retrieval, and fallback features work without an LLM key.


Do not put real API keys in this GitHub repository. Use Community Cloud's Secrets field for deployment secrets.

After deployment, pushes to the GitHub repository can update the deployed app automatically.

## 🔐 Security & responsible use

- Never commit `.env` or API keys.
- `.env.example` contains placeholders only.
- Uploaded resumes do not need to be stored in Git.
- The match score is a similarity signal, not a hiring probability.
- LLM suggestions must be reviewed before being used in a real application.
- The optimizer is instructed not to fabricate experience, qualifications, employers, or metrics.

## 🧪 Testing

```bash
pytest -q
```

## 📁 Project structure

```text
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── .github/workflows/ci.yml
├── src/
│   ├── analyzer.py
│   ├── career_tools.py
│   ├── config.py
│   ├── llm.py
│   ├── parsers.py
│   ├── rag.py
│   ├── report.py
│   └── scoring.py
└── tests/
    ├── test_career_tools.py
    └── test_scoring.py
```

## 🚀 Future upgrades

- User profiles and saved resume versions
- Resume version comparison
- Semantic embeddings/vector database
- Application tracker and job-history dashboard
- Deployment with managed secrets
- Evaluation dataset and LLM quality metrics
