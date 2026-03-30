"""
MBTI Analyzer — modular personality analysis engine.
"""

from mbti_analyzer.config import (
    DIMENSIONS,
    COGNITIVE_STACKS,
    COGNITIVE_FUNCTIONS,
    TYPE_DESCRIPTIONS,
    VALID_MBTI_TYPES,
    EXPECTED_ANSWER_COUNT,
    MIN_ANSWER_VALUE,
    MAX_ANSWER_VALUE,
    QUESTIONS_PER_DIMENSION,
)
from mbti_analyzer.validators import (
    ValidationError,
    validate_mbti_type,
    validate_answers,
    validate_scores,
)
from mbti_analyzer.calculator import (
    calculate_dimension_scores,
    score_to_type,
    infer_scores_from_type,
    analyze_answers,
    analyze_type,
)
from mbti_analyzer.formatter import interpret_score, build_report

__all__ = [
    # config
    "DIMENSIONS",
    "COGNITIVE_STACKS",
    "COGNITIVE_FUNCTIONS",
    "TYPE_DESCRIPTIONS",
    "VALID_MBTI_TYPES",
    "EXPECTED_ANSWER_COUNT",
    "MIN_ANSWER_VALUE",
    "MAX_ANSWER_VALUE",
    "QUESTIONS_PER_DIMENSION",
    # validators
    "ValidationError",
    "validate_mbti_type",
    "validate_answers",
    "validate_scores",
    # calculator
    "calculate_dimension_scores",
    "score_to_type",
    "infer_scores_from_type",
    "analyze_answers",
    "analyze_type",
    # formatter
    "interpret_score",
    "build_report",
]
