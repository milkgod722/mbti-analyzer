#!/usr/bin/env python3
"""
MBTI Analysis Engine
Takes raw MBTI answers or a 4-letter type, outputs structured analysis.
"""

import json
import sys
from typing import Optional

# MBTI dimensions
DIMENSIONS = {
    "EI": {"name": "Extraversion vs Introversion", "E": "Extraversion", "I": "Introversion"},
    "SN": {"name": "Sensing vs Intuition", "S": "Sensing", "N": "Intuition"},
    "TF": {"name": "Thinking vs Feeling", "T": "Thinking", "F": "Feeling"},
    "JP": {"name": "Judging vs Perceiving", "J": "Judging", "P": "Perceiving"},
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


def score_to_type(ei_score: float, sn_score: float, tf_score: float, jp_score: float) -> str:
    """Convert dimension scores (0.0-1.0) to MBTI 4-letter type."""
    e_or_i = "E" if ei_score > 0.5 else "I"
    s_or_n = "S" if sn_score > 0.5 else "N"
    t_or_f = "T" if tf_score > 0.5 else "F"
    j_or_p = "J" if jp_score > 0.5 else "P"
    return e_or_i + s_or_n + t_or_f + j_or_p


def interpret_score(score: float, high_label: str, low_label: str) -> dict:
    """Return interpretation dict for a dimension score."""
    pct = round(score * 100)
    moderate = 0.4 <= score <= 0.6
    return {
        "percentage": pct,
        "primary": high_label if score > 0.5 else low_label,
        "moderate": moderate,
        "description": f"{pct}% {high_label}" if score > 0.5 else f"{pct}% {low_label}",
    }


def analyze_answers(answers: list[int]) -> dict:
    scores: dict = {
        "EI": sum(1 for a in answers[:10] if a > 3) / 10,
        "SN": sum(1 for a in answers[10:20] if a > 3) / 10,
        "TF": sum(1 for a in answers[20:30] if a > 3) / 10,
        "JP": sum(1 for a in answers[30:40] if a > 3) / 10,
    }
    mbti = score_to_type(scores["EI"], scores["SN"], scores["TF"], scores["JP"])
    return build_report(mbti, scores)


def analyze_type(mbti: str, scores: Optional[dict] = None) -> dict:
    """Analyze a given MBTI type string."""
    mbti = mbti.upper()
    if mbti not in TYPE_DESCRIPTIONS:
        raise ValueError(f"Invalid MBTI type: {mbti}")
    if scores is None:
        # Infer approximate scores from the type
        scores = {
            "EI": 0.9 if mbti[0] == "E" else 0.1,
            "SN": 0.9 if mbti[1] == "S" else 0.1,
            "TF": 0.9 if mbti[2] == "T" else 0.1,
            "JP": 0.9 if mbti[3] == "J" else 0.1,
        }
    return build_report(mbti, scores)


def build_report(mbti: str, scores: dict) -> dict:
    """Build a full analysis report dict."""
    type_info = TYPE_DESCRIPTIONS.get(mbti, {"role": "Unknown", "summary": "Unknown type"})
    
    def fmt(d, key):
        s = scores[d]
        labels = {"EI": ("E", "I"), "SN": ("S", "N"), "TF": ("T", "F"), "JP": ("J", "P")}
        return interpret_score(s, labels[d][0], labels[d][1])

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
    }


def main():
    inp = json.loads(sys.stdin.read())
    
    if "answers" in inp:
        result = analyze_answers(inp["answers"])
    elif "type" in inp:
        result = analyze_type(inp["type"], inp.get("scores"))
    else:
        print(json.dumps({"error": "Provide 'answers' (list of 40 scores 1-5) or 'type' (4-letter MBTI)"}))
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
