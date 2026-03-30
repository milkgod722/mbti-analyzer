"""
Configuration — constants, thresholds, and static reference data.
"""

# ---------------------------------------------------------------------------
# Answer validation
# ---------------------------------------------------------------------------
MIN_ANSWER_VALUE: int = 1
MAX_ANSWER_VALUE: int = 5
EXPECTED_ANSWER_COUNT: int = 40
QUESTIONS_PER_DIMENSION: int = 10
NEUTRAL_ANSWER_VALUE: int = 3

# ---------------------------------------------------------------------------
# Dimension strength thresholds (distance from 0.5 midpoint)
# ---------------------------------------------------------------------------

# Threshold for "moderate dimension" flag in reports
MODERATE_DIMENSION_THRESHOLD: float = 0.15

# Default score assigned to each letter when inferring from MBTI type
DEFAULT_LETTER_SCORE: float = 0.85
DEFAULT_OPPOSITE_SCORE: float = 0.15

# ---------------------------------------------------------------------------
# MBTI dimensions
# ---------------------------------------------------------------------------
DIMENSIONS: dict[str, dict[str, str]] = {
    "EI": {"name": "Extraversion vs Introversion", "E": "Extraversion", "I": "Introversion"},
    "SN": {"name": "Sensing vs Intuition",         "S": "Sensing",       "N": "Intuition"},
    "TF": {"name": "Thinking vs Feeling",          "T": "Thinking",     "F": "Feeling"},
    "JP": {"name": "Judging vs Perceiving",        "J": "Judging",      "P": "Perceiving"},
}

# Valid pole pairs per position (index → (first_letter, second_letter))
DIMENSION_POLES: dict[str, tuple[str, str]] = {
    "EI": ("E", "I"),
    "SN": ("S", "N"),
    "TF": ("T", "F"),
    "JP": ("J", "P"),
}

# ---------------------------------------------------------------------------
# Cognitive function stacks — order: Dom, Aux, Tert, Inf
# ---------------------------------------------------------------------------
COGNITIVE_STACKS: dict[str, list[str]] = {
    "INTJ": ["Ni", "Te", "Fi", "Se"],
    "INTP": ["Ti", "Ne", "Si", "Fe"],
    "ENTJ": ["Te", "Ni", "Se", "Fi"],
    "ENTP": ["Ne", "Ti", "Fe", "Si"],
    "INFJ": ["Ni", "Fe", "Ti", "Se"],
    "INFP": ["Fi", "Ne", "Si", "Te"],
    "ENFJ": ["Fe", "Ni", "Se", "Ti"],
    "ENFP": ["Ne", "Fi", "Te", "Si"],
    "ISTJ": ["Si", "Te", "Fi", "Ne"],
    "ISFJ": ["Si", "Fe", "Ti", "Ne"],
    "ESTJ": ["Te", "Si", "Ne", "Fi"],
    "ESFJ": ["Fe", "Si", "Ne", "Ti"],
    "ISTP": ["Ti", "Se", "Ni", "Fe"],
    "ISFP": ["Fi", "Se", "Ni", "Te"],
    "ESTP": ["Se", "Ti", "Fe", "Ni"],
    "ESFP": ["Se", "Fi", "Te", "Ni"],
}

# ---------------------------------------------------------------------------
# Cognitive function descriptions
# ---------------------------------------------------------------------------
COGNITIVE_FUNCTIONS: dict[str, dict[str, str]] = {
    "Ni": {"name": "Introverted Intuition",  "description": "深层洞察与模式识别，关注内在愿景和长远预见"},
    "Ne": {"name": "Extraverted Intuition", "description": "探索可能性与联系，善于发散思维和创意联想"},
    "Si": {"name": "Introverted Sensing",    "description": "回顾过往经验与细节，注重传统和可靠的方法"},
    "Se": {"name": "Extraverted Sensing",    "description": "活在当下，敏锐感知外部环境和即时体验"},
    "Ti": {"name": "Introverted Thinking",   "description": "内部逻辑分析，追求精确理解和理论框架"},
    "Te": {"name": "Extraverted Thinking",   "description": "高效组织与目标导向，注重外部系统和客观标准"},
    "Fi": {"name": "Introverted Feeling",    "description": "深层价值观与真实自我，追求内心和谐与真诚"},
    "Fe": {"name": "Extraverted Feeling",    "description": "关注他人情感与社会和谐，善于维护人际关系"},
}

COGNITIVE_POSITION_LABELS: dict[str, dict[str, str]] = {
    "dominant":  {"en": "Dominant",  "cn": "主导功能 - 你最自然、最强的心理过程"},
    "auxiliary": {"en": "Auxiliary", "cn": "辅助功能 - 支持主导功能，提供平衡"},
    "tertiary":  {"en": "Tertiary",  "cn": "第三功能 - 较弱但在压力下可能显现"},
    "inferior":  {"en": "Inferior",  "cn": "劣势功能 - 最不成熟的区域，是成长空间"},
}

# ---------------------------------------------------------------------------
# MBTI type descriptions
# ---------------------------------------------------------------------------
TYPE_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "INTJ": {"role": "Architect",   "summary": "Strategic thinkers with a drive for self-improvement"},
    "INTP": {"role": "Logician",    "summary": "Curious explorers who love uncovering patterns"},
    "ENTJ": {"role": "Commander",   "summary": "Bold, imaginative leaders who favor logic over tradition"},
    "ENTP": {"role": "Debater",     "summary": "Inventive and energetic trouble-solvers"},
    "INFJ": {"role": "Advocate",    "summary": "Quiet nurturers with strong principles"},
    "INFP": {"role": "Mediator",    "summary": "Poetic, kind, and idealistic romantics"},
    "ENFJ": {"role": "Protagonist", "summary": "Charismatic leaders who inspire others"},
    "ENFP": {"role": "Campaigner",  "summary": "Enthusiastic, creative, and socially aware"},
    "ISTJ": {"role": "Logistician", "summary": "Practical facticians who keep things organized"},
    "ISFJ": {"role": "Defender",    "summary": "Reliable protectors who are devoted to caring for others"},
    "ESTJ": {"role": "Executive",   "summary": "Excellent organizers who value tradition and stability"},
    "ESFJ": {"role": "Consul",      "summary": "Popular people-persons who prioritize harmony"},
    "ISTP": {"role": "Virtuoso",    "summary": "Bold and practical experimentalists"},
    "ISFP": {"role": "Adventurer",  "summary": "Flexible and artistic explorers"},
    "ESTP": {"role": "Entrepreneur","summary": "Bold and energetic doers who thrive in fast-paced env"},
    "ESFP": {"role": "Entertainer", "summary": "Spontaneous and enthusiastic performers"},
}

VALID_MBTI_TYPES: set[str] = set(TYPE_DESCRIPTIONS.keys())
