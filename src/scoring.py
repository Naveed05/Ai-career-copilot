import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = {"the", "and", "for", "with", "that", "this", "from", "are", "you", "your", "will", "have", "has", "our", "not", "but", "into", "their", "they", "about", "using", "use", "years", "year"}


def _terms(text: str) -> list[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", text.lower())
    return [w for w in words if w not in STOPWORDS]


def calculate_match_score(resume: str, job_description: str) -> float:
    if not resume.strip() or not job_description.strip():
        return 0.0
    matrix = TfidfVectorizer(ngram_range=(1, 2), stop_words="english").fit_transform([resume, job_description])
    return round(float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0]) * 100, 1)


def extract_skill_gaps(resume: str, job_description: str, limit: int = 15) -> list[str]:
    resume_terms = set(_terms(resume))
    jd_terms = _terms(job_description)
    ranked = []
    seen = set()
    for term in jd_terms:
        if term not in resume_terms and term not in seen and len(term) >= 3:
            seen.add(term)
            ranked.append(term)
    return ranked[:limit]


def top_resume_strengths(resume: str, job_description: str, limit: int = 8) -> list[str]:
    resume_terms = set(_terms(resume))
    jd_terms = set(_terms(job_description))
    return sorted(resume_terms & jd_terms, key=len, reverse=True)[:limit]
