from .llm import ask_llm
from .scoring import calculate_match_score, extract_skill_gaps, top_resume_strengths


def analyze(resume: str, job_description: str, provider: str | None = None) -> dict:
    score = calculate_match_score(resume, job_description)
    gaps = extract_skill_gaps(resume, job_description)
    strengths = top_resume_strengths(resume, job_description)
    result = {
        "match_score": score,
        "strengths": strengths,
        "skill_gaps": gaps,
        "summary": f"Baseline ATS-style similarity is {score}%. Review the skill gaps before applying.",
        "recommendations": [
            "Mirror relevant job-description terminology only when it is truthful.",
            "Prioritize measurable outcomes in experience bullets.",
            "Move the most relevant skills and projects closer to the top of the resume.",
        ],
    }
    if provider:
        prompt = f'''Analyze this resume against this job description. Return JSON with keys: summary (string), strengths (array of strings), skill_gaps (array of strings), recommendations (array of strings), interview_focus (array of strings). Do not invent facts.\n\nRESUME:\n{resume[:12000]}\n\nJOB DESCRIPTION:\n{job_description[:10000]}'''
        llm_result = ask_llm(provider, prompt)
        if llm_result:
            result.update(llm_result)
            result["match_score"] = score
    return result


def interview_questions(resume: str, job_description: str, provider: str | None = None) -> list[dict]:
    fallback = [
        {"category": "Resume", "question": "Walk me through the experience on your resume that is most relevant to this role."},
        {"category": "Technical", "question": "Which technical skill in the job description are you strongest in, and how have you used it?"},
        {"category": "Gap", "question": "The role asks for skills that are not obvious on your resume. How would you demonstrate your ability to learn them?"},
        {"category": "Behavioral", "question": "Tell me about a difficult project and how you handled the challenge."},
        {"category": "Impact", "question": "What measurable result are you most proud of from your recent work or projects?"},
        {"category": "Role fit", "question": "Why are you interested in this position and how does it fit your career goals?"},
    ]
    if not provider:
        return fallback
    prompt = f'''Create 8 interview questions tailored to this resume and job description. Return JSON with a single key questions containing objects with category and question. Do not invent candidate facts.\nRESUME:\n{resume[:10000]}\nJOB DESCRIPTION:\n{job_description[:9000]}'''
    result = ask_llm(provider, prompt)
    return result.get("questions", fallback) if result else fallback
