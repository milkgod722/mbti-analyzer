"""
Input validation — MBTI type strings and questionnaire answer lists.
"""

import sys
from typing import Any

from mbti_analyzer.config import (
    VALID_MBTI_TYPES,
    MIN_ANSWER_VALUE,
    MAX_ANSWER_VALUE,
    EXPECTED_ANSWER_COUNT,
    NEUTRAL_ANSWER_VALUE,
    DIMENSION_POLES,
)


class ValidationError(Exception):
    """Raised when user input fails validation."""

    def __init__(self, message: str, suggestion: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.suggestion = suggestion


def validate_mbti_type(mbti: Any) -> str:
    """
    Validate and normalize an MBTI type string.

    Args:
        mbti: A value expected to be a 4-letter MBTI type string.

    Returns:
        Normalized uppercase 4-letter MBTI type.

    Raises:
        ValidationError: If the value is not a valid MBTI type.
    """
    if not mbti or not isinstance(mbti, str):
        raise ValidationError(
            "MBTI type must be a non-empty string.",
            suggestion="Provide a 4-letter type such as 'INTJ' or 'enfp'.",
        )

    mbti = mbti.upper().strip()

    if len(mbti) != 4:
        raise ValidationError(
            f"MBTI type must be exactly 4 characters (got {len(mbti)}: '{mbti}').",
            suggestion="Types are 4 letters, e.g. 'INFP', 'ESTJ'.",
        )

    for pos, (dim_key, (first, second)) in enumerate(DIMENSION_POLES.items()):
        if mbti[pos] not in (first, second):
            raise ValidationError(
                f"Position {pos + 1} of '{mbti}' ({dim_key}) must be "
                f"'{first}' or '{second}', not '{mbti[pos]}'.",
                suggestion=f"The '{dim_key}' dimension accepts only '{first}' or '{second}'.",
            )

    if mbti not in VALID_MBTI_TYPES:
        raise ValidationError(
            f"'{mbti}' is not a recognised MBTI type.",
            suggestion=f"Valid types are: {', '.join(sorted(VALID_MBTI_TYPES))}.",
        )

    return mbti


# Internal type alias for a validated answer list
ValidatedAnswers = list[int]
ValidatedScores = dict[str, float]


def validate_scores(raw_scores: Any) -> ValidatedScores:
    """
    Validate optional pre-computed dimension scores.

    Args:
        raw_scores: Mapping expected to contain EI/SN/TF/JP scores in [0.0, 1.0].

    Returns:
        A normalized dict with float values for each dimension.

    Raises:
        ValidationError: If the mapping shape or values are invalid.
    """
    if not isinstance(raw_scores, dict) or not raw_scores:
        raise ValidationError(
            "Scores must be a non-empty object with EI, SN, TF, and JP values.",
            suggestion="Provide scores like {\"EI\": 0.15, \"SN\": 0.85, \"TF\": 0.2, \"JP\": 0.9}.",
        )

    expected_keys = tuple(DIMENSION_POLES.keys())
    missing = [key for key in expected_keys if key not in raw_scores]
    unexpected = [key for key in raw_scores if key not in DIMENSION_POLES]

    if missing or unexpected:
        parts: list[str] = []
        if missing:
            parts.append(f"missing {', '.join(missing)}")
        if unexpected:
            parts.append(f"unexpected {', '.join(unexpected)}")
        raise ValidationError(
            f"Scores object must contain exactly EI, SN, TF, and JP ({'; '.join(parts)}).",
            suggestion="Use exactly these keys: EI, SN, TF, JP.",
        )

    validated: ValidatedScores = {}
    for dim_key in expected_keys:
        raw_value = raw_scores[dim_key]
        try:
            value = float(raw_value)
        except (TypeError, ValueError) as exc:
            raise ValidationError(
                f"Score '{dim_key}' must be numeric, got {raw_value!r}.",
                suggestion="Each dimension score must be a number between 0.0 and 1.0.",
            ) from exc

        if not 0.0 <= value <= 1.0:
            raise ValidationError(
                f"Score '{dim_key}' must be between 0.0 and 1.0, got {value}.",
                suggestion="Keep every dimension score within the inclusive range 0.0-1.0.",
            )

        validated[dim_key] = value

    return validated


def validate_answers(raw_answers: Any) -> ValidatedAnswers:
    """
    Validate a list of questionnaire answers.

    Accepts fewer than 40 answers (raises error), but truncates answers
    beyond 40. Non-numeric values are replaced with a neutral answer and
    out-of-range values are clamped, with a warning printed to stderr.

    Args:
        raw_answers: A list (or iterable) of answer values.

    Returns:
        A list of exactly 40 integers, each in the range 1–5.

    Raises:
        ValidationError: If the input is not a non-empty list with at
            least 40 items.
    """
    if not raw_answers or not isinstance(raw_answers, list):
        raise ValidationError(
            "Answers must be a non-empty list of integers.",
            suggestion="Provide a JSON array of 40 integers between 1 and 5, "
                      "e.g. {\"answers\": [4, 5, 3, 2, 1, ...]}.",
        )

    if len(raw_answers) < EXPECTED_ANSWER_COUNT:
        raise ValidationError(
            f"Incomplete answer set: got {len(raw_answers)} answers, "
            f"need {EXPECTED_ANSWER_COUNT} "
            f"(missing {EXPECTED_ANSWER_COUNT - len(raw_answers)}).",
            suggestion=f"Ensure all 40 questions are answered. "
                      f"Each answer should be an integer from 1 to 5.",
        )

    # Truncate to 40 if excess answers are provided
    answers = raw_answers[:EXPECTED_ANSWER_COUNT]

    validated: list[int] = []
    warnings: list[str] = []

    for i, raw in enumerate(answers):
        try:
            val = int(raw)
        except (ValueError, TypeError):
            warnings.append(
                f"Q{i + 1}: {raw!r} (not a number, replaced with {NEUTRAL_ANSWER_VALUE})"
            )
            validated.append(NEUTRAL_ANSWER_VALUE)
            continue

        if val < MIN_ANSWER_VALUE:
            warnings.append(f"Q{i + 1}: {val} (clamped to {MIN_ANSWER_VALUE})")
            validated.append(MIN_ANSWER_VALUE)
        elif val > MAX_ANSWER_VALUE:
            warnings.append(f"Q{i + 1}: {val} (clamped to {MAX_ANSWER_VALUE})")
            validated.append(MAX_ANSWER_VALUE)
        else:
            validated.append(val)

    if warnings:
        print(
            f"Warning: {len(warnings)} answer(s) required adjustment: "
            f"{', '.join(warnings)}",
            file=sys.stderr,
        )

    return validated
