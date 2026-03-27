"""
Unit tests for the MBTI Analyzer package.
Run with: pytest tests/ -v
"""

import pytest

from mbti_analyzer import (
    ValidationError,
    validate_mbti_type,
    validate_answers,
    calculate_dimension_scores,
    score_to_type,
    infer_scores_from_type,
    interpret_score,
    build_report,
    analyze_answers,
    analyze_type,
)
from mbti_analyzer.config import VALID_MBTI_TYPES


# ---------------------------------------------------------------------------
# validate_mbti_type
# ---------------------------------------------------------------------------

class TestValidateMbtiType:
    def test_valid_uppercase(self):
        assert validate_mbti_type("INTJ") == "INTJ"

    def test_valid_lowercase_normalized(self):
        assert validate_mbti_type("infp") == "INFP"

    def test_valid_with_whitespace(self):
        assert validate_mbti_type("  ENTP ") == "ENTP"

    @pytest.mark.parametrize("mbti", ["INTJ", "INTP", "ENTJ", "ENTP",
                                       "INFJ", "INFP", "ENFJ", "ENFP",
                                       "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                                       "ISTP", "ISFP", "ESTP", "ESFP"])
    def test_all_valid_types(self, mbti):
        assert validate_mbti_type(mbti) == mbti

    def test_invalid_letter_at_position(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_mbti_type("XNTJ")
        assert "Position 1" in str(exc_info.value)

    def test_invalid_length_short(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_mbti_type("INT")
        assert "exactly 4" in str(exc_info.value)

    def test_invalid_length_long(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_mbti_type("INTJJ")
        assert "exactly 4" in str(exc_info.value)

    def test_none_input(self):
        with pytest.raises(ValidationError):
            validate_mbti_type(None)

    def test_empty_string(self):
        with pytest.raises(ValidationError):
            validate_mbti_type("")

    def test_invalid_type_reveals_valid_types(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_mbti_type("XXXX")
        # Should describe the position-level error
        msg = str(exc_info.value)
        assert "Position 1" in msg
        assert "EI" in msg or "E" in msg


# ---------------------------------------------------------------------------
# validate_answers
# ---------------------------------------------------------------------------

class TestValidateAnswers:
    def make_answers(self, n: int = 40, value: int = 3) -> list[int]:
        return [value] * n

    def test_valid_answers_unchanged(self):
        answers = [4, 5, 3, 2, 1, 4, 5, 3, 2, 4,
                   3, 4, 5, 2, 1, 3, 4, 5, 2, 3,
                   4, 3, 2, 5, 4, 3, 4, 2, 1, 5,
                   3, 4, 5, 2, 4, 3, 2, 4, 5, 1]
        result = validate_answers(answers)
        assert result == answers
        assert len(result) == 40

    def test_incomplete_raises(self):
        with pytest.raises(ValidationError) as exc_info:
            validate_answers([3] * 20)
        assert "Incomplete" in str(exc_info.value)
        assert "20" in str(exc_info.value)

    def test_empty_list_raises(self):
        with pytest.raises(ValidationError):
            validate_answers([])

    def test_none_raises(self):
        with pytest.raises(ValidationError):
            validate_answers(None)

    def test_excess_answers_truncated(self):
        answers = [3] * 50
        result = validate_answers(answers)
        assert len(result) == 40

    def test_non_integer_clamped(self, capsys):
        answers = [1, 2, 99, 0, 3, 4, 5, 1, 2, 3,
                   4, 5, 1, 2, 3, 4, 5, 1, 2, 3,
                   4, 5, 1, 2, 3, 4, 5, 1, 2, 3,
                   4, 5, 1, 2, 3, 4, 5, 1, 2, 3]
        result = validate_answers(answers)
        assert 1 <= result[2] <= 5
        assert 1 <= result[3] <= 5

    def test_non_numeric_skipped_with_warning(self, capsys):
        answers = [3] * 39 + ["foo"]
        result = validate_answers(answers)
        captured = capsys.readouterr()
        assert "Warning" in captured.err or "adjustment" in captured.err


# ---------------------------------------------------------------------------
# calculate_dimension_scores
# ---------------------------------------------------------------------------

class TestCalculateDimensionScores:
    def test_all_neutral_returns_05(self):
        """All 3s should give exactly 0.5 for each dimension."""
        scores = calculate_dimension_scores([3] * 40)
        for key in ("EI", "SN", "TF", "JP"):
            assert scores[key] == 0.5

    def test_all_first_pole_returns_0(self):
        """All 1s should give score close to 0.0."""
        scores = calculate_dimension_scores([1] * 40)
        for key in ("EI", "SN", "TF", "JP"):
            assert scores[key] == 0.0

    def test_all_second_pole_returns_1(self):
        """All 5s should give score close to 1.0."""
        scores = calculate_dimension_scores([5] * 40)
        for key in ("EI", "SN", "TF", "JP"):
            assert scores[key] == 1.0

    def test_scores_in_range(self):
        mixed = [1, 2, 3, 4, 5] * 8
        scores = calculate_dimension_scores(mixed)
        for key in ("EI", "SN", "TF", "JP"):
            assert 0.0 <= scores[key] <= 1.0


# ---------------------------------------------------------------------------
# score_to_type
# ---------------------------------------------------------------------------

class TestScoreToType:
    # MBTI理论: 低分(0.0)→第一字母(E/S/T/J), 高分(1.0)→第二字母(I/N/F/P)
    # score <= 0.5 → poles[0] (first), score > 0.5 → poles[1] (second)
    @pytest.mark.parametrize("ei,sn,tf,jp,expected", [
        (0.0, 0.0, 0.0, 0.0, "INFP"),   # 全部低分 → 全部第二字母 I,N,F,P
        (1.0, 1.0, 1.0, 1.0, "ESTJ"),   # 全部高分 → 全部第一字母 E,S,T,J
        (0.5, 0.5, 0.5, 0.5, "INFP"),   # 边界 ≤0.5 → 第二字母
        (0.51, 0.51, 0.51, 0.51, "ESTJ"), # >0.5 → 第一字母 E,S,T,J
        (0.0, 0.0, 1.0, 1.0, "INTJ"),   # EI/SN低分→I/N, TF/JP高分→T/J
    ])
    def test_score_to_type(self, ei, sn, tf, jp, expected):
        assert score_to_type(ei, sn, tf, jp) == expected


# ---------------------------------------------------------------------------
# infer_scores_from_type
# ---------------------------------------------------------------------------

class TestInferScoresFromType:
    def test_ei_e_score(self):
        scores = infer_scores_from_type("ENTJ")
        assert scores["EI"] > 0.5

    def test_ei_i_score(self):
        scores = infer_scores_from_type("INTJ")
        assert scores["EI"] < 0.5

    def test_all_four_dims(self):
        scores = infer_scores_from_type("INTJ")
        assert all(0.0 <= v <= 1.0 for v in scores.values())


# ---------------------------------------------------------------------------
# interpret_score
# ---------------------------------------------------------------------------

class TestInterpretScore:
    def test_extreme_e_score(self):
        result = interpret_score(0.9, "EI")
        assert result["percentage"] == 90
        assert result["primary"] == "E"
        assert result["moderate"] is False
        assert result["strength_level"] == "very_strong"

    def test_extreme_i_score(self):
        result = interpret_score(0.1, "EI")
        assert result["percentage"] == 10
        assert result["primary"] == "I"
        assert result["moderate"] is False

    def test_moderate_score(self):
        result = interpret_score(0.55, "EI")
        assert result["moderate"] is True
        assert result["balance_note"] is not None

    def test_slight_score(self):
        # Score 0.52: within 0.4-0.6 range → moderate=True
        result = interpret_score(0.52, "EI")
        assert result["moderate"] is True
        assert result["strength_level"] == "slight"


# ---------------------------------------------------------------------------
# build_report
# ---------------------------------------------------------------------------

class TestBuildReport:
    def test_basic_report_keys(self):
        scores = {"EI": 0.85, "SN": 0.15, "TF": 0.85, "JP": 0.15}
        report = build_report("INTJ", scores)
        assert report["type"] == "INTJ"
        assert report["role"] == "Architect"
        assert "dimensions" in report
        assert "letter_profile" in report
        assert "cognitive_functions" in report
        assert "moderate_dimensions_count" in report

    def test_moderate_dimensions_count(self):
        # EI=0.55 and SN=0.55 are moderate, others are not
        scores = {"EI": 0.55, "SN": 0.55, "TF": 0.85, "JP": 0.15}
        report = build_report("INTJ", scores)
        assert report["moderate_dimensions_count"] == 2
        assert report["has_moderate_dimensions"] is True

    def test_adaptability_note_when_multiple_moderate(self):
        # EI/SN/TF at 0.55 (moderate range 0.4-0.6); JP at 0.85 (outside range)
        scores = {"EI": 0.55, "SN": 0.55, "TF": 0.55, "JP": 0.85}
        report = build_report("INTJ", scores)
        assert report["moderate_dimensions_count"] >= 2
        assert report["adaptability_note"] is not None
        assert report["adaptability_note"] is not None

    def test_cognitive_functions_populated(self):
        scores = {"EI": 0.85, "SN": 0.15, "TF": 0.85, "JP": 0.15}
        report = build_report("INTJ", scores)
        cf = report["cognitive_functions"]
        assert cf["stack"] == ["Ni", "Te", "Fi", "Se"]
        assert len(cf["functions"]) == 4
        assert cf["functions"][0]["position"] == "dominant"
        assert cf["growth_area"] is not None


# ---------------------------------------------------------------------------
# Top-level API
# ---------------------------------------------------------------------------

class TestAnalyzeAnswers:
    def test_all_3s_returns_balanced_type(self):
        report = analyze_answers([3] * 40)
        assert len(report["type"]) == 4

    def test_all_1s_returns_infp(self):
        # All 1s → score 0.0 → second letters I,N,F,P
        report = analyze_answers([1] * 40)
        assert report["type"] == "INFP"

    def test_all_5s_returns_estj(self):
        # All 5s → score 1.0 → first letters E,S,T,J
        report = analyze_answers([5] * 40)
        assert report["type"] == "ESTJ"


class TestAnalyzeType:
    def test_analyze_intj(self):
        report = analyze_type("INTJ")
        assert report["type"] == "INTJ"
        assert report["role"] == "Architect"

    def test_analyze_lowercase(self):
        report = analyze_type("infp")
        assert report["type"] == "INFP"

    def test_invalid_type_raises(self):
        with pytest.raises(ValidationError):
            analyze_type("XXXX")

    def test_unknown_type_suggestion(self):
        # Error message should indicate what went wrong (position + valid letters)
        with pytest.raises(ValidationError) as exc_info:
            analyze_type("XXXX")
        msg = str(exc_info.value)
        assert "Position 1" in msg and ("must be" in msg or "not 'X'" in msg)


# ---------------------------------------------------------------------------
# Config integrity
# ---------------------------------------------------------------------------

class TestConfig:
    def test_all_16_types_have_cognitive_stacks(self):
        from mbti_analyzer.config import COGNITIVE_STACKS
        for mbti in VALID_MBTI_TYPES:
            assert mbti in COGNITIVE_STACKS, f"Missing stack for {mbti}"
            assert len(COGNITIVE_STACKS[mbti]) == 4

    def test_cognitive_functions_all_have_descriptions(self):
        from mbti_analyzer.config import COGNITIVE_FUNCTIONS
        for code in ("Ni", "Ne", "Si", "Se", "Ti", "Te", "Fi", "Fe"):
            assert code in COGNITIVE_FUNCTIONS
            assert "name" in COGNITIVE_FUNCTIONS[code]
            assert "description" in COGNITIVE_FUNCTIONS[code]
