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
            raw = open(args.json_file, encoding="utf-8").read()
        return json.loads(raw)

    if args.json:
        return json.loads(args.json)

    return {}


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    # Determine output mode
    pretty = not args.no_pretty and sys.stdout.isatty()
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
            inp = _load_json_input(args)
            if "answers" in inp:
                result = analyze_answers(inp["answers"])
            elif "type" in inp:
                result = analyze_type(inp["type"], inp.get("scores"))
            else:
                error_payload = {
                    "error": "Missing input",
                    "usage": "Provide --type MBTI, --answers 40 scores, "
                             "or --json '{\"type\": \"...\"}'",
                }

    except ValidationError as exc:
        error_payload = {
            "error": "Validation error",
            "message": exc.message,
        }
        if hasattr(exc, "suggestion") and exc.suggestion:  # type: ignore[attr-defined]
            error_payload["suggestion"] = exc.suggestion  # type: ignore[attr-defined]

    except Exception as exc:
        error_payload = {
            "error": "Unexpected error",
            "message": str(exc),
            "type": type(exc).__name__,
        }

    output = error_payload if error_payload else result
    if output is None:
        output = error_payload or {"error": "No input provided"}

    sys.stdout.write(json.dumps(output, ensure_ascii=False, indent=indent))
    sys.stdout.write("\n")

    return 1 if error_payload else 0


if __name__ == "__main__":
    sys.exit(main())
