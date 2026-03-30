#!/usr/bin/env python3
"""Backward-compatible stdin JSON wrapper around the package CLI helpers."""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from mbti_analyzer.cli import analyze_payload, build_error_payload


def main():
    raw_input = sys.stdin.read().strip()

    if not raw_input:
        payload = {
            "error": "No input provided",
            "usage": (
                "Provide JSON with 'answers' (list of 40 scores 1-5) "
                "or 'type' (4-letter MBTI)"
            ),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        payload = analyze_payload(json.loads(raw_input))
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps(build_error_payload(exc), ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
