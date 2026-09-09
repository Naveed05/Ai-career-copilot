from src.career_tools import create_cover_letter, rewrite_resume


def test_resume_rewrite_fallback_is_safe():
    result = rewrite_resume("Python developer with SQL experience", "Need Python and SQL", None)
    assert result["headline"]
    assert isinstance(result["bullets"], list)


def test_cover_letter_fallback_uses_inputs():
    letter = create_cover_letter("Python developer", "Need Python", "Acme", "Data Analyst", None)
    assert "Acme" in letter
    assert "Data Analyst" in letter
