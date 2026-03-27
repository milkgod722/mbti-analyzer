"""
Score calculation — answer scoring and MBTI type derivation.
"""

from typing import TypedDict

from mbti_analyzer.config import (
    DIMENSION_POLES,
    MODERATE_DIMENSION_THRESHOLD,
    DEFAULT_LETTER_SCORE,
    DEFAULT_OPPOSITE_SCORE,
)


class DimensionScores(TypedDict):
    """Maps dimension key → score in range [0.0, 1.0]."""
    EI: float
    SN: float
    TF: float
    JP: float


def calculate_dimension_scores(answers: list[int]) -> DimensionScores:
    """
    Compute the 0–1 score for each MBTI dimension from a validated
    40-answer list (10 questions per dimension).

    Scoring convention (1–5 scale → 0–1):
        1 → 0.0  (full preference for the first pole)
        2 → 0.33
        3 → 0.5  (neutral)
        4 → 0.67
        5 → 1.0  (full preference for the second pole)

    Args:
        answers: Exactly 40 validated integers in [1, 5].

    Returns:
        Dict mapping "EI", "SN", "TF", "JP" to floats in [0.0, 1.0].
    """
    def _score_dim(segment: list[int]) -> float:
        # (a - 1) / 4 maps {1,2,3,4,5} → {0, 0.33, 0.5, 0.67, 1.0}
        total = sum((a - 1) / 4 for a in segment)
        return total / len(segment)

    return {
        "EI": _score_dim(answers[0:10]),
        "SN": _score_dim(answers[10:20]),
        "TF": _score_dim(answers[20:30]),
        "JP": _score_dim(answers[30:40]),
    }


def score_to_type(ei: float, sn: float, tf: float, jp: float) -> str:
    """
    Convert four dimension scores (each in [0.0, 1.0]) to a 4-letter
    MBTI type string.

    Convention:
        score > 0.5 → first pole letter (e.g. "E", "S", "T", "J")
        score ≤ 0.5 → second pole letter (e.g. "I", "N", "F", "P")

    Args:
        ei, sn, tf, jp: Dimension scores in [0.0, 1.0].

    Returns:
        Uppercase 4-letter MBTI type, e.g. "INTJ".
    """
    def _letter(score: float, poles: tuple[str, str]) -> str:
        # score > 0.5 → first pole (E/S/T/J), score <= 0.5 → second pole (I/N/F/P)
        return poles[0] if score > 0.5 else poles[1]

    return (
        _letter(ei, DIMENSION_POLES["EI"])
        + _letter(sn, DIMENSION_POLES["SN"])
        + _letter(tf, DIMENSION_POLES["TF"])
        + _letter(jp, DIMENSION_POLES["JP"])
    )


def infer_scores_from_type(mbti: str) -> DimensionScores:
    """
    Derive approximate dimension scores from a 4-letter MBTI type.

    Each letter receives DEFAULT_LETTER_SCORE (0.85) if it is the
    preferred pole and DEFAULT_OPPOSITE_SCORE (0.15) otherwise.

    Args:
        mbti: A validated 4-letter MBTI type.

    Returns:
        Approximate dimension scores.
    """
    scores: DimensionScores = {"EI": 0.5, "SN": 0.5, "TF": 0.5, "JP": 0.5}

    for i, dim_key in enumerate(("EI", "SN", "TF", "JP")):
        pole_letter = mbti[i]
        first_pole = DIMENSION_POLES[dim_key][0]
        scores[dim_key] = (
            DEFAULT_LETTER_SCORE if pole_letter == first_pole
            else DEFAULT_OPPOSITE_SCORE
        )

    return scores


# ---------------------------------------------------------------------------
# High-level analysis API
# ---------------------------------------------------------------------------

from typing import Optional

from mbti_analyzer.validators import validate_mbti_type, validate_answers
from mbti_analyzer.formatter import build_report


def analyze_answers(answers: list[int]) -> dict:
    """
    Analyze raw MBTI questionnaire answers.

    Args:
        answers: List of 40 integer scores (1-5)

    Returns:
        Complete analysis report dict
    """
    validated = validate_answers(answers)
    scores = calculate_dimension_scores(validated)
    mbti = score_to_type(scores["EI"], scores["SN"], scores["TF"], scores["JP"])
    return build_report(mbti, scores)


def analyze_type(mbti: str, scores: Optional[dict] = None) -> dict:
    """
    Analyze a given MBTI type string.

    Args:
        mbti: 4-letter MBTI type string
        scores: Optional pre-calculated dimension scores

    Returns:
        Complete analysis report dict
    """
    mbti = validate_mbti_type(mbti)

    if scores is None:
        scores = infer_scores_from_type(mbti)

    return build_report(mbti, scores)



