from .parsers import chunk_text


def retrieve(query: str, documents: list[str], top_k: int = 4) -> list[str]:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    chunks = []
    for document in documents:
        chunks.extend(chunk_text(document))
    if not chunks:
        return []
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(chunks + [query])
    scores = cosine_similarity(matrix[-1], matrix[:-1]).ravel()
    ranked = scores.argsort()[::-1][:top_k]
    return [chunks[i] for i in ranked if scores[i] > 0]
