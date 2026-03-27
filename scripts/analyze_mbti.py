#!/usr/bin/env python3
"""
MBTI Analysis Engine
Takes raw MBTI answers or a 4-letter type, outputs structured analysis.

Features:
- Input validation with clear error messages
- Edge case handling for incomplete/invalid data
- Moderate dimension detection with thresholds
- Cognitive function stack analysis
"""

import json
import sys
from typing import Optional
from enum import Enum

# Constants
MIN_ANSWER_VALUE = 1
MAX_ANSWER_VALUE = 5
EXPECTED_ANSWER_COUNT = 40
QUESTIONS_PER_DIMENSION = 10

# Thresholds for dimension strength interpretation
class DimensionStrength(Enum):
    VERY_STRONG = 0.80  # 80%+ = very strong preference
    STRONG = 0.65       # 65-79% = strong preference
    MODERATE = 0.55     # 55-64% = moderate preference
    SLIGHT = 0.45       # 45-54% = slight/balanced preference
    # Below 45% = preference for the opposite pole

# MBTI dimensions
DIMENSIONS = {
    "EI": {"name": "Extraversion vs Introversion", "E": "Extraversion", "I": "Introversion"},
    "SN": {"name": "Sensing vs Intuition", "S": "Sensing", "N": "Intuition"},
    "TF": {"name": "Thinking vs Feeling", "T": "Thinking", "F": "Feeling"},
    "JP": {"name": "Judging vs Perceiving", "J": "Judging", "P": "Perceiving"},
}

# Cognitive function stacks for all 16 types (Dom, Aux, Tert, Inf)
COGNITIVE_STACKS = {
    "INTJ": ["Ni", "Te", "Fi", "Se"],  # Introverted Intuition dominant
    "INTP": ["Ti", "Ne", "Si", "Fe"],  # Introverted Thinking dominant
    "ENTJ": ["Te", "Ni", "Se", "Fi"],  # Extraverted Thinking dominant
    "ENTP": ["Ne", "Ti", "Fe", "Si"],  # Extraverted Intuition dominant
    "INFJ": ["Ni", "Fe", "Ti", "Se"],  # Introverted Intuition dominant
    "INFP": ["Fi", "Ne", "Si", "Te"],  # Introverted Feeling dominant
    "ENFJ": ["Fe", "Ni", "Se", "Ti"],  # Extraverted Feeling dominant
    "ENFP": ["Ne", "Fi", "Te", "Si"],  # Extraverted Intuition dominant
    "ISTJ": ["Si", "Te", "Fi", "Ne"],  # Introverted Sensing dominant
    "ISFJ": ["Si", "Fe", "Ti", "Ne"],  # Introverted Sensing dominant
    "ESTJ": ["Te", "Si", "Ne", "Fi"],  # Extraverted Thinking dominant
    "ESFJ": ["Fe", "Si", "Ne", "Ti"],  # Extraverted Feeling dominant
    "ISTP": ["Ti", "Se", "Ni", "Fe"],  # Introverted Thinking dominant
    "ISFP": ["Fi", "Se", "Ni", "Te"],  # Introverted Feeling dominant
    "ESTP": ["Se", "Ti", "Fe", "Ni"],  # Extraverted Sensing dominant
    "ESFP": ["Se", "Fi", "Te", "Ni"],  # Extraverted Sensing dominant
}

# Cognitive function descriptions
COGNITIVE_FUNCTIONS = {
    "Ni": {"name": "Introverted Intuition", "description": "深层洞察与模式识别，关注内在愿景和长远预见"},
    "Ne": {"name": "Extraverted Intuition", "description": "探索可能性与联系，善于发散思维和创意联想"},
    "Si": {"name": "Introverted Sensing", "description": "回顾过往经验与细节，注重传统和可靠的方法"},
    "Se": {"name": "Extraverted Sensing", "description": "活在当下，敏锐感知外部环境和即时体验"},
    "Ti": {"name": "Introverted Thinking", "description": "内部逻辑分析，追求精确理解和理论框架"},
    "Te": {"name": "Extraverted Thinking", "description": "高效组织与目标导向，注重外部系统和客观标准"},
    "Fi": {"name": "Introverted Feeling", "description": "深层价值观与真实自我，追求内心和谐与真诚"},
    "Fe": {"name": "Extraverted Feeling", "description": "关注他人情感与社会和谐，善于维护人际关系"},
}

# Type descriptions (abbreviated - full descriptions in references/)
TYPE_DESCRIPTIONS = {
    "INTJ": {"role": "Architect", "summary": "Strategic thinkers with a drive for self-improvement"},
    "INTP": {"role": "Logician", "summary": "Curious explorers who love uncovering patterns"},
    "ENTJ": {"role": "Commander", "summary": "Bold, imaginative leaders who favor logic over tradition"},
    "ENTP": {"role": "Debater", "summary": "Inventive and energetic trouble-solvers"},
    "INFJ": {"role": "Advocate", "summary": "Quiet nurturers with strong principles"},
    "INFP": {"role": "Mediator", "summary": "Poetic, kind, and idealistic romantics"},
    "ENFJ": {"role": "Protagonist", "summary": "Charismatic leaders who inspire others"},
    "ENFP": {"role": "Campaigner", "summary": "Enthusiastic, creative, and socially aware"},
    "ISTJ": {"role": "Logistician", "summary": "Practical facticians who keep things organized"},
    "ISFJ": {"role": "Defender", "summary": "Reliable protectors who are devoted to caring for others"},
    "ESTJ": {"role": "Executive", "summary": "Excellent organizers who value tradition and stability"},
    "ESFJ": {"role": "Consul", "summary": "Popular and popular people-persons who prioritize harmony"},
    "ISTP": {"role": "Virtuoso", "summary": "Bold and practical experimentalists"},
    "ISFP": {"role": "Adventurer", "summary": "Flexible and artistic explorers"},
    "ESTP": {"role": "Entrepreneur", "summary": "Bold and energetic doers who thrive in fast-paced env"},
    "ESFP": {"role": "Entertainer", "summary": "Spontaneous and enthusiastic performers"},
}

# Valid MBTI types for validation
VALID_MBTI_TYPES = set(TYPE_DESCRIPTIONS.keys())


class ValidationError(Exception):
    """Custom exception for input validation errors."""
    pass


def validate_mbti_type(mbti: str) -> str:
    """
    Validate and normalize an MBTI type string.
    
    Args:
        mbti: 4-letter MBTI type string
        
    Returns:
        Normalized uppercase MBTI type
        
    Raises:
        ValidationError: If type is invalid
    """
    if not mbti or not isinstance(mbti, str):
        raise ValidationError("MBTI type must be a non-empty string")
    
    mbti = mbti.upper().strip()
    
    if len(mbti) != 4:
        raise ValidationError(f"MBTI type must be exactly 4 letters, got {len(mbti)}: '{mbti}'")
    
    # Check each position for valid letters
    valid_positions = [
        ("E", "I"),  # Position 0
        ("S", "N"),  # Position 1
        ("T", "F"),  # Position 2
        ("J", "P"),  # Position 3
    ]
    
    for i, (letter, (opt1, opt2)) in enumerate(zip(mbti, valid_positions)):
        if letter not in (opt1, opt2):
            raise ValidationError(
                f"Invalid letter '{letter}' at position {i+1}. "
                f"Expected '{opt1}' or '{opt2}'"
            )
    
    if mbti not in VALID_MBTI_TYPES:
        raise ValidationError(f"Invalid MBTI type: {mbti}")
    
    return mbti


def validate_answers(answers: list) -> list[int]:
    """
    Validate answer list with comprehensive checks.
    
    Args:
        answers: List of answer scores
        
    Returns:
        Validated list of integers
        
    Raises:
        ValidationError: If answers are invalid
    """
    if not answers or not isinstance(answers, list):
        raise ValidationError("Answers must be a non-empty list")
    
    # Check answer count
    if len(answers) < EXPECTED_ANSWER_COUNT:
        raise ValidationError(
            f"Incomplete answer set: got {len(answers)} answers, "
            f"expected {EXPECTED_ANSWER_COUNT}. "
            f"Missing {EXPECTED_ANSWER_COUNT - len(answers)} answers."
        )
    
    if len(answers) > EXPECTED_ANSWER_COUNT:
        # Warn but continue with first 40
        answers = answers[:EXPECTED_ANSWER_COUNT]
    
    validated = []
    invalid_indices = []
    
    for i, answer in enumerate(answers):
        try:
            val = int(answer)
        except (ValueError, TypeError):
            invalid_indices.append((i + 1, answer, "not a number"))
            continue
        
        if val < MIN_ANSWER_VALUE or val > MAX_ANSWER_VALUE:
            # Clamp to valid range with warning
            clamped = max(MIN_ANSWER_VALUE, min(MAX_ANSWER_VALUE, val))
            invalid_indices.append((i + 1, val, f"clamped to {clamped}"))
            validated.append(clamped)
        else:
            validated.append(val)
    
    if invalid_indices:
        warnings = [f"Q{idx}: {val} ({msg})" for idx, val, msg in invalid_indices]
        # Log warnings but don't fail
        print(f"Warning: Some answers required adjustment: {', '.join(warnings)}", 
              file=sys.stderr)
    
    return validated


def score_to_type(ei_score: float, sn_score: float, tf_score: float, jp_score: float) -> str:
    """Convert dimension scores (0.0-1.0) to MBTI 4-letter type."""
    e_or_i = "E" if ei_score > 0.5 else "I"
    s_or_n = "S" if sn_score > 0.5 else "N"
    t_or_f = "T" if tf_score > 0.5 else "F"
    j_or_p = "J" if jp_score > 0.5 else "P"
    return e_or_i + s_or_n + t_or_f + j_or_p


def get_dimension_strength(score: float) -> tuple[str, str]:
    """
    Determine the strength category and description for a dimension score.
    
    Returns:
        Tuple of (strength_level, description)
    """
    # Calculate distance from center (0.5)
    distance = abs(score - 0.5)
    
    if distance >= 0.30:  # 80%+ or 20%-
        return ("very_strong", "非常明显的偏好")
    elif distance >= 0.15:  # 65-79% or 21-35%
        return ("strong", "较强的偏好")
    elif distance >= 0.05:  # 55-64% or 36-45%
        return ("moderate", "中等偏好")
    else:  # 45-54%
        return ("slight", "轻微偏好，具有双向适应性")


def interpret_score(score: float, high_label: str, low_label: str) -> dict:
    """Return interpretation dict for a dimension score with strength analysis."""
    pct = round(score * 100)
    strength_level, strength_desc = get_dimension_strength(score)
    primary = high_label if score > 0.5 else low_label
    
    # Determine if this is a "moderate" dimension (close to center)
    moderate = abs(score - 0.5) < 0.15
    
    return {
        "percentage": pct,
        "primary": primary,
        "moderate": moderate,
        "strength_level": strength_level,
        "strength_description": strength_desc,
        "description": f"{pct}% {primary}",
        "balance_note": "此维度较为平衡，你可以灵活适应两种模式" if moderate else None,
    }


def calculate_dimension_scores(answers: list[int]) -> dict:
    """
    Calculate dimension scores from validated answers.
    Uses weighted scoring based on answer values (1-5 scale).
    """
    def score_dimension(dim_answers: list[int]) -> float:
        # Convert 1-5 scale to 0-1 scale
        # 1,2 = preference for first letter, 4,5 = preference for second letter
        # 3 = neutral
        total = sum((a - 1) / 4 for a in dim_answers)  # Normalize to 0-1
        return total / len(dim_answers)
    
    return {
        "EI": score_dimension(answers[:10]),
        "SN": score_dimension(answers[10:20]),
        "TF": score_dimension(answers[20:30]),
        "JP": score_dimension(answers[30:40]),
    }


def analyze_answers(answers: list) -> dict:
    """
    Analyze raw MBTI questionnaire answers.
    
    Args:
        answers: List of 40 integer scores (1-5)
        
    Returns:
        Complete analysis report dict
        
    Raises:
        ValidationError: If answers are invalid or incomplete
    """
    validated_answers = validate_answers(answers)
    scores = calculate_dimension_scores(validated_answers)
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
        
    Raises:
        ValidationError: If type is invalid
    """
    mbti = validate_mbti_type(mbti)
    
    if scores is None:
        # Infer approximate scores from the type
        scores = {
            "EI": 0.85 if mbti[0] == "E" else 0.15,
            "SN": 0.85 if mbti[1] == "S" else 0.15,
            "TF": 0.85 if mbti[2] == "T" else 0.15,
            "JP": 0.85 if mbti[3] == "J" else 0.15,
        }
    return build_report(mbti, scores)


def get_cognitive_function_analysis(mbti: str) -> dict:
    """
    Generate detailed cognitive function stack analysis for a type.
    
    Args:
        mbti: Valid MBTI type string
        
    Returns:
        Dict with cognitive function analysis
    """
    stack = COGNITIVE_STACKS.get(mbti, [])
    
    if not stack:
        return {"error": f"No cognitive stack defined for type {mbti}"}
    
    positions = ["dominant", "auxiliary", "tertiary", "inferior"]
    position_descriptions = {
        "dominant": "主导功能 - 你最自然、最强的心理过程",
        "auxiliary": "辅助功能 - 支持主导功能，提供平衡",
        "tertiary": "第三功能 - 较弱但在压力下可能显现",
        "inferior": "劣势功能 - 最不成熟的区域，是成长空间",
    }
    
    functions = []
    for i, func in enumerate(stack):
        func_info = COGNITIVE_FUNCTIONS.get(func, {})
        functions.append({
            "code": func,
            "position": positions[i],
            "position_cn": position_descriptions[positions[i]],
            "name": func_info.get("name", "Unknown"),
            "description": func_info.get("description", ""),
        })
    
    # Generate development advice based on inferior function
    inferior = stack[3] if len(stack) >= 4 else None
    growth_area = None
    if inferior:
        inferior_info = COGNITIVE_FUNCTIONS.get(inferior, {})
        growth_area = {
            "function": inferior,
            "name": inferior_info.get("name", ""),
            "advice": f"发展你的{inferior_info.get('name', '')}能力是个人成长的关键领域。"
                      f"当压力过大时，这个功能可能以不成熟的方式表现出来。"
        }
    
    return {
        "stack": stack,
        "functions": functions,
        "growth_area": growth_area,
    }


def build_report(mbti: str, scores: dict) -> dict:
    """Build a full analysis report dict."""
    type_info = TYPE_DESCRIPTIONS.get(mbti, {"role": "Unknown", "summary": "Unknown type"})
    
    def fmt(d, key):
        s = scores[d]
        labels = {"EI": ("E", "I"), "SN": ("S", "N"), "TF": ("T", "F"), "JP": ("J", "P")}
        return interpret_score(s, labels[d][0], labels[d][1])

    # Count moderate dimensions
    moderate_count = sum(
        1 for d in ["EI", "SN", "TF", "JP"]
        if abs(scores[d] - 0.5) < 0.15
    )
    
    # Get cognitive function analysis
    cognitive_analysis = get_cognitive_function_analysis(mbti)

    return {
        "type": mbti,
        "role": type_info["role"],
        "summary": type_info["summary"],
        "dimensions": {
            "EI": {**fmt("EI", "E/I"), "label": DIMENSIONS["EI"]["name"]},
            "SN": {**fmt("SN", "S/N"), "label": DIMENSIONS["SN"]["name"]},
            "TF": {**fmt("TF", "T/F"), "label": DIMENSIONS["TF"]["name"]},
            "JP": {**fmt("JP", "J/P"), "label": DIMENSIONS["JP"]["name"]},
        },
        "letter_profile": {
            "E/I": mbti[0],
            "S/N": mbti[1],
            "T/F": mbti[2],
            "J/P": mbti[3],
        },
        "cognitive_functions": cognitive_analysis,
        "moderate_dimensions_count": moderate_count,
        "has_moderate_dimensions": moderate_count > 0,
        "adaptability_note": (
            "你的多个维度呈现中等偏好，说明你具有良好的适应性，可以根据不同情境灵活切换倾向。"
            if moderate_count >= 2 else None
        ),
    }


def main():
    """Main entry point with comprehensive error handling."""
    try:
        raw_input = sys.stdin.read().strip()
        
        if not raw_input:
            print(json.dumps({
                "error": "No input provided",
                "usage": "Provide JSON with 'answers' (list of 40 scores 1-5) or 'type' (4-letter MBTI)"
            }))
            sys.exit(1)
        
        try:
            inp = json.loads(raw_input)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "error": f"Invalid JSON input: {str(e)}",
                "received": raw_input[:100] + "..." if len(raw_input) > 100 else raw_input
            }))
            sys.exit(1)
        
        if not isinstance(inp, dict):
            print(json.dumps({
                "error": f"Input must be a JSON object, got {type(inp).__name__}"
            }))
            sys.exit(1)
        
        if "answers" in inp:
            result = analyze_answers(inp["answers"])
        elif "type" in inp:
            result = analyze_type(inp["type"], inp.get("scores"))
        else:
            print(json.dumps({
                "error": "Missing required field",
                "usage": "Provide 'answers' (list of 40 scores 1-5) or 'type' (4-letter MBTI)",
                "received_keys": list(inp.keys())
            }))
            sys.exit(1)
        
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except ValidationError as e:
        print(json.dumps({
            "error": "Validation error",
            "message": str(e)
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "error": "Unexpected error",
            "message": str(e),
            "type": type(e).__name__
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
