# 🚀 AI Career Copilot

AI Career Copilot is a portfolio-ready Streamlit application for turning a resume + job description into an actionable interview and job-application plan.

## What it does

- 📄 Extracts text from PDF resumes
- 🎯 Calculates a transparent baseline ATS-style similarity score
- 🔎 Finds likely skill/keyword gaps
- 💪 Surfaces strengths shared by the resume and role
- 🤖 Adds optional LLM analysis through OpenAI, Groq, or Gemini
- 🎤 Generates role-specific interview questions
- 🧠 Retrieves relevant resume/JD context for grounded Q&A
- 🔐 Keeps API keys in environment variables rather than source code
- 🧪 Includes automated tests and GitHub Actions CI

## Architecture

```text
Resume PDF ──► PDF Parser ──► Resume Text ──┐
                                             ├─► Scoring / Skill Gaps
Job Description ────────────────────────────┘
                                             │
                                             ├─► Optional LLM Analysis
                                             ├─► Interview Coach
                                             └─► TF-IDF Retrieval / Grounded Q&A
```

## Run locally

```bash
git clone https://github.com/Naveed05/Ai-career-copilot.git
cd Ai-career-copilot
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

On Windows PowerShell, create `.env` manually if `cp` is unavailable.

### Optional AI providers

Add only the provider key you intend to use:

```env
OPENAI_API_KEY=...
GROQ_API_KEY=...
GOOGLE_API_KEY=...
```

The core scoring, gap analysis, interview fallback questions, and retrieval features work without an API key.

## Security

- Never commit `.env` or provider API keys.
- `.env.example` contains placeholders only.
- Uploaded resume files are not required to be committed to Git.
- Do not treat the baseline match score as an actual hiring probability; it is a similarity signal.
- LLM output should be reviewed before using it in a real application.

## Testing

```bash
pytest -q
```

## Project structure

```text
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   ├── analyzer.py
│   ├── config.py
│   ├── llm.py
│   ├── parsers.py
│   ├── rag.py
│   └── scoring.py
└── tests/
    └── test_scoring.py
```

## Roadmap

- Persistent user profiles
- Resume version comparison
- Cover-letter generation
- Semantic embeddings/vector database
- Deployment with managed secrets
- Evaluation dataset for analysis quality
