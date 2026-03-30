#!/usr/bin/env python3
"""
MBTI Analyzer CLI

Usage examples:
    python -m mbti_analyzer.cli --type INTJ
    python -m mbti_analyzer.cli --answers 4 5 3 2 1 4 5 3 2 4 ...
    python -m mbti_analyzer.cli --json '{"type": "INFP"}'
    cat answers.json | python -m mbti_analyzer.cli --json-file -
"""

import argparse
import json
import sys
from typing import Any

from mbti_analyzer import ValidationError, analyze_answers, analyze_type


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="mbti-analyzer",
        description="MBTI personality analysis engine.",
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--type", metavar="MBTI",
        help="4-letter MBTI type, e.g. INTJ, ENFP",
    )
    mode.add_argument(
        "--answers", metavar="N", type=int, nargs="+",
        help="40 integer scores (1–5), one per question",
    )
    mode.add_argument(
        "--json", metavar="TEXT",
        help="JSON input: {\"type\": \"INTJ\"} or {\"answers\": [...]}",
    )
    mode.add_argument(
        "--json-file", metavar="PATH",
        help="Read JSON input from a file (use - for stdin)",
    )

    parser.add_argument(
        "--json-output", action="store_true",
        help="Output raw JSON (default when piping)",
    )
    parser.add_argument(
        "--no-pretty", action="store_true",
        help="Disable pretty-printing (compact JSON output)",
    )

    return parser


def _load_json_input(args: argparse.Namespace) -> dict[str, Any]:
    """Extract the JSON dict from --json or --json-file."""
    if args.json_file:
        if args.json_file == "-":
            raw = sys.stdin.read()
        else:
            with open(args.json_file, encoding="utf-8") as f:
                raw = f.read()
        return json.loads(raw)

    if args.json:
        return json.loads(args.json)

    return {}


def analyze_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Analyze a JSON payload used by the CLI wrapper interfaces."""
    if not isinstance(payload, dict):
        raise ValidationError(
            f"JSON input must be an object, got {type(payload).__name__}.",
            suggestion="Provide an object like {\"type\": \"INTJ\"} or {\"answers\": [...]}",
        )

    if "answers" in payload:
        return analyze_answers(payload["answers"])
    if "type" in payload:
        return analyze_type(payload["type"], payload.get("scores"))

    raise ValidationError(
        "Missing input.",
        suggestion="Provide 'type' or 'answers' in the JSON payload.",
    )


def build_error_payload(exc: Exception) -> dict[str, Any]:
    """Convert known exceptions into stable JSON error payloads."""
    if isinstance(exc, ValidationError):
        error_payload: dict[str, Any] = {
            "error": "Validation error",
            "message": exc.message,
        }
        if exc.suggestion:
            error_payload["suggestion"] = exc.suggestion
        return error_payload

    if isinstance(exc, json.JSONDecodeError):
        return {
            "error": "Invalid JSON input",
            "message": str(exc),
        }

    return {
        "error": "Unexpected error",
        "message": str(exc),
        "type": type(exc).__name__,
    }


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    # Determine output mode
    pretty = not args.no_pretty and not args.json_output and sys.stdout.isatty()
    indent = 2 if pretty else None

    # Build the result
    result: dict[str, Any] | None = None
    error_payload: dict[str, Any] = {}

    try:
        if args.type:
            result = analyze_type(args.type)
        elif args.answers:
            result = analyze_answers(args.answers)
        else:
            result = analyze_payload(_load_json_input(args))
    except Exception as exc:
        error_payload = build_error_payload(exc)

    output = error_payload if error_payload else result
    if output is None:
        output = error_payload or {"error": "No input provided"}

    sys.stdout.write(json.dumps(output, ensure_ascii=False, indent=indent))
    sys.stdout.write("\n")

    return 1 if error_payload else 0


if __name__ == "__main__":
    sys.exit(main())
