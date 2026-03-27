#!/usr/bin/env python3
"""
Backward-compatible wrapper — calls mbti_analyzer.cli.main().

All logic lives in the mbti_analyzer package.
"""

import sys
import json

from mbti_analyzer import (
    ValidationError,
    validate_answers,
    validate_mbti_type,
    calculate_dimension_scores,
    score_to_type,
    infer_scores_from_type,
    build_report,
)


def analyze_answers(answers):
    validated = validate_answers(answers)
    scores = calculate_dimension_scores(validated)
    mbti = score_to_type(scores["EI"], scores["SN"], scores["TF"], scores["JP"])
    return build_report(mbti, scores)


def analyze_type(mbti, scores=None):
    mbti = validate_mbti_type(mbti)
    if scores is None:
        scores = infer_scores_from_type(mbti)
    return build_report(mbti, scores)


def main():
    try:
        raw_input = sys.stdin.read().strip()

        if not raw_input:
            print(
                json.dumps(
                    {
                        "error": "No input provided",
                        "usage": (
                            "Provide JSON with 'answers' (list of 40 scores 1-5) "
                            "or 'type' (4-letter MBTI)"
                        ),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            sys.exit(1)

        try:
            inp = json.loads(raw_input)
        except json.JSONDecodeError as e:
            print(
                json.dumps(
                    {
                        "error": f"Invalid JSON input: {e}",
                        "received": (
                            raw_input[:100] + "..."
                            if len(raw_input) > 100
                            else raw_input
                        ),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            sys.exit(1)

        if not isinstance(inp, dict):
            print(
                json.dumps(
                    {
                        "error": (
                            f"Input must be a JSON object, got {type(inp).__name__}"
                        )
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            sys.exit(1)

        if "answers" in inp:
            result = analyze_answers(inp["answers"])
        elif "type" in inp:
            result = analyze_type(inp["type"], inp.get("scores"))
        else:
            print(
                json.dumps(
                    {
                        "error": "Missing required field",
                        "usage": (
                            "Provide 'answers' (list of 40 scores 1-5) or "
                            "'type' (4-letter MBTI)"
                        ),
                        "received_keys": list(inp.keys()),
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
            sys.exit(1)

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except ValidationError as exc:
        print(
            json.dumps(
                {"error": "Validation error", "message": str(exc)},
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)
    except Exception as exc:
        print(
            json.dumps(
                {
                    "error": "Unexpected error",
                    "message": str(exc),
                    "type": type(exc).__name__,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
