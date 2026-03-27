"""
Report formatting — dimension interpretation and full report assembly.
"""

from typing import Any, TypedDict

from mbti_analyzer.config import (
    DIMENSIONS,
    DIMENSION_POLES,
    COGNITIVE_STACKS,
    COGNITIVE_FUNCTIONS,
    COGNITIVE_POSITION_LABELS,
    TYPE_DESCRIPTIONS,
    MODERATE_DIMENSION_THRESHOLD,
)


# ---------------------------------------------------------------------------
# Report structure types
# ---------------------------------------------------------------------------

class DimensionResult(TypedDict):
    percentage: int
    primary: str
    moderate: bool
    strength_level: str
    strength_description: str
    description: str
    balance_note: str | None
    label: str


class CognitiveFunctionEntry(TypedDict):
    code: str
    position: str
    position_cn: str
    name: str
    description: str


class GrowthArea(TypedDict):
    function: str
    name: str
    advice: str


class CognitiveAnalysis(TypedDict):
    stack: list[str]
    functions: list[CognitiveFunctionEntry]
    growth_area: GrowthArea | None


class LetterProfile(TypedDict):
    EI: str
    SN: str
    TF: str
    JP: str


class AnalysisReport(TypedDict):
    type: str
    role: str
    summary: str
    dimensions: dict[str, DimensionResult]
    letter_profile: LetterProfile
    cognitive_functions: CognitiveAnalysis
    moderate_dimensions_count: int
    has_moderate_dimensions: bool
    adaptability_note: str | None


# ---------------------------------------------------------------------------
# Strength helpers
# ---------------------------------------------------------------------------

_STRENGTH_LEVELS = [
    (0.30, "very_strong",  "非常明显的偏好"),
    (0.15, "strong",       "较强的偏好"),
    (0.05, "moderate",     "中等偏好"),
    (0.00, "slight",       "轻微偏好，具有双向适应性"),
]


def _strength_from_score(score: float) -> tuple[str, str]:
    distance = abs(score - 0.5)
    for threshold, level, desc in _STRENGTH_LEVELS:
        if distance >= threshold:
            return level, desc
    return "slight", "轻微偏好，具有双向适应性"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def interpret_score(score: float, dim_key: str) -> DimensionResult:
    """
    Build a dimension result dict from a 0–1 score.

    Args:
        score: Dimension score in [0.0, 1.0].
        dim_key: One of "EI", "SN", "TF", "JP".

    Returns:
        Populated DimensionResult TypedDict.
    """
    pct = round(score * 100)
    poles = DIMENSION_POLES[dim_key]
    high_letter, low_letter = poles[0], poles[1]

    strength_level, strength_desc = _strength_from_score(score)
    primary = high_letter if score > 0.5 else low_letter
    moderate = 0.4 <= score <= 0.6

    return DimensionResult(
        percentage=pct,
        primary=primary,
        moderate=moderate,
        strength_level=strength_level,
        strength_description=strength_desc,
        description=f"{pct}% {primary}",
        balance_note=(
            "此维度较为平衡，你可以灵活适应两种模式" if moderate else None
        ),
        label=DIMENSIONS[dim_key]["name"],
    )


def get_cognitive_function_analysis(mbti: str) -> CognitiveAnalysis:
    """
    Generate the cognitive function stack analysis for a given MBTI type.

    Args:
        mbti: A validated 4-letter MBTI type.

    Returns:
        CognitiveAnalysis TypedDict.
    """
    stack = COGNITIVE_STACKS.get(mbti, [])
    positions = ["dominant", "auxiliary", "tertiary", "inferior"]

    functions: list[CognitiveFunctionEntry] = []
    for i, code in enumerate(stack):
        info = COGNITIVE_FUNCTIONS.get(code, {})
        pos_key = positions[i]
        functions.append(
            CognitiveFunctionEntry(
                code=code,
                position=pos_key,
                position_cn=COGNITIVE_POSITION_LABELS[pos_key]["cn"],
                name=info.get("name", "Unknown"),
                description=info.get("description", ""),
            )
        )

    # Growth area based on the inferior function
    growth_area: GrowthArea | None = None
    if len(stack) >= 4:
        inferior_code = stack[3]
        inf_info = COGNITIVE_FUNCTIONS.get(inferior_code, {})
        growth_area = GrowthArea(
            function=inferior_code,
            name=inf_info.get("name", ""),
            advice=(
                f"发展你的{inf_info.get('name', '')}能力是个人成长的关键领域。"
                f"当压力过大时，这个功能可能以不成熟的方式表现出来。"
            ),
        )

    return CognitiveAnalysis(
        stack=stack,
        functions=functions,
        growth_area=growth_area,
    )


def build_report(mbti: str, scores: dict[str, float]) -> AnalysisReport:
    """
    Assemble a complete analysis report dict.

    Args:
        mbti: 4-letter MBTI type.
        scores: Dimension key → 0–1 float.

    Returns:
        Fully populated AnalysisReport TypedDict.
    """
    type_info = TYPE_DESCRIPTIONS.get(
        mbti, {"role": "Unknown", "summary": "Unknown type"}
    )

    dimensions = {
        dim_key: interpret_score(scores[dim_key], dim_key)
        for dim_key in ("EI", "SN", "TF", "JP")
    }

    moderate_count = sum(1 for d in dimensions.values() if d["moderate"])

    cognitive = get_cognitive_function_analysis(mbti)

    return AnalysisReport(
        type=mbti,
        role=type_info["role"],
        summary=type_info["summary"],
        dimensions=dimensions,
        letter_profile=LetterProfile(
            EI=mbti[0], SN=mbti[1], TF=mbti[2], JP=mbti[3]
        ),
        cognitive_functions=cognitive,
        moderate_dimensions_count=moderate_count,
        has_moderate_dimensions=moderate_count > 0,
        adaptability_note=(
            "你的多个维度呈现中等偏好，说明你具有良好的适应性，"
            "可以根据不同情境灵活切换倾向。"
            if moderate_count >= 2
            else None
        ),
    )
