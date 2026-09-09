from .llm import ask_llm


def rewrite_resume(resume: str, job_description: str, provider: str | None = None) -> dict:
    fallback = {
        "headline": "Results-focused professional aligned to the target role",
        "summary": "Tailor this section around the strongest evidence already present in the resume. Keep every claim factual and measurable where possible.",
        "bullets": [
            "Rewrite each experience bullet as action + task + outcome, using terminology from the job description only when accurate.",
            "Add measurable impact where the original resume already contains numbers, scale, time, quality, cost, or performance evidence.",
            "Move the most relevant technical skills and projects closer to the top of the resume.",
        ],
        "keywords_to_emphasize": [],
    }
    if not provider:
        return fallback
    prompt = f'''Improve this resume for the target job without inventing any facts. Return JSON with keys: headline (string), summary (string), bullets (array of improved bullet strings), keywords_to_emphasize (array of strings). Preserve the candidate's real experience. Never fabricate employers, tools, metrics, certifications, degrees, or responsibilities. Keep bullets concise and ATS-friendly.\n\nRESUME:\n{resume[:14000]}\n\nJOB DESCRIPTION:\n{job_description[:10000]}'''
    result = ask_llm(provider, prompt)
    return result or fallback


def create_cover_letter(resume: str, job_description: str, company: str, role: str, provider: str | None = None) -> str:
    if not provider:
        company_text = company.strip() or "the company"
        role_text = role.strip() or "this position"
        return (
            f"Dear Hiring Manager,\n\nI am excited to apply for {role_text} at {company_text}. "
            "My background includes experience and projects that align with the requirements of this role. "
            "I would welcome the opportunity to discuss how my existing skills and willingness to learn can contribute to your team.\n\n"
            "Thank you for your time and consideration.\n\nSincerely,\nCandidate"
        )
    prompt = f'''Write a professional one-page cover letter for the candidate and target role. Use only facts supported by the resume. Do not invent metrics, employers, technologies, qualifications, or achievements. Return JSON with one key: cover_letter (string). Company: {company or 'the company'}. Role: {role or 'the position'}.\n\nRESUME:\n{resume[:12000]}\n\nJOB DESCRIPTION:\n{job_description[:9000]}'''
    result = ask_llm(provider, prompt)
    return (result or {}).get("cover_letter", "") or create_cover_letter(resume, job_description, company, role, None)


def grounded_answer(query: str, context: list[str], provider: str | None = None) -> str:
    joined = "\n\n---\n\n".join(context)
    if not provider:
        return "Here is the most relevant evidence from your documents:\n\n" + joined[:5000]
    prompt = f'''Answer the user's career question using only the supplied resume/job-description context. If the context does not support an answer, say so clearly. Do not invent candidate facts. Return JSON with one key: answer (string).\n\nQUESTION:\n{query}\n\nCONTEXT:\n{joined[:12000]}'''
    result = ask_llm(provider, prompt)
    return (result or {}).get("answer", "") or "I could not generate a grounded answer from the available context."
