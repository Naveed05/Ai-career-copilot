from src.scoring import calculate_match_score


def test_empty_score():
    assert calculate_match_score("", "Python developer") == 0.0


def test_relevant_resume_scores_higher():
    high = calculate_match_score("Python SQL machine learning pandas", "Python SQL machine learning")
    low = calculate_match_score("History literature art", "Python SQL machine learning")
    assert high > low
