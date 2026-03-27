---
name: mbti-analyzer
description: MBTI personality test analysis and report generation. Use when: (1) user provides MBTI test answers (40 questions, scores 1-5), (2) user provides a 4-letter MBTI type (e.g. INFP, ENTJ) for analysis, (3) generating personality reports, (4) career advice based on MBTI, (5) relationship/interpersonal analysis using MBTI types. Handles input from JSON, text answers, or direct type specification.
---

# MBTI Analyzer Skill

Analyze MBTI personality types and generate detailed, readable reports.

## Quick Start

Two input modes supported:

**Mode 1 — Raw answers (40 questions, 1-5 scale):**
```json
{
  "answers": [4, 5, 3, 2, 1, 4, 5, 3, 2, 4, 3, 4, 5, 2, 1, 3, 4, 5, 2, 3, 4, 3, 2, 5, 4, 3, 4, 2, 1, 5, 3, 4, 5, 2, 4, 3, 2, 4, 5, 1]
}
```

**Mode 2 — Known type:**
```json
{"type": "INTJ"}
```

Run the analyzer:
```bash
python3 skills/mbti-analyzer/scripts/analyze_mbti.py <<< '<json-input>'
```

## Output Format

The engine returns a structured dict with:
- `type` — 4-letter MBTI (e.g. "INTJ")
- `role` — Type role name (e.g. "Architect")
- `summary` — One-line description
- `dimensions` — Each dimension with percentage, primary preference, and description
- `letter_profile` — The four letters broken out

## Generating Reports

After running the analyzer, use the report template at `assets/report_template.md`.

Fill the template with values from the analysis dict. If the channel/platform doesn't support Handlebars templating, manually substitute:

| Placeholder | Source |
|-------------|--------|
| `{{type}}` | `result["type"]` |
| `{{role}}` | `result["role"]` |
| `{{summary}}` | `result["summary"]` |
| `{{EI.percentage}}` | `result["dimensions"]["EI"]["percentage"]` |
| `{{EI.primary}}` | `result["dimensions"]["EI"]["primary"]` |
| `{{EI.label}}` | `result["dimensions"]["EI"]["label"]` |
| `{{EI.description}}` | `result["dimensions"]["EI"]["description"]` |
| (same for SN, TF, JP) | |
| `{{letter_profile.EI}}` | `result["letter_profile"]["E/I"]` |

### Moderate Dimension Detection

Check if any dimension has `moderate: true` (score between 40-60%). Include the adaptive note in the report when found:

```
💡 你的多个维度呈现中等偏好，说明你具有良好的适应性，
可以根据不同情境灵活切换倾向。
```

## Reference Data

Full type descriptions, career tendencies, and dimension theory: `references/mbti_types.md`

## Input Normalization

- Accept MBTI type in uppercase ("infp" → "INFP")
- Accept scores as integers 1-5
- If fewer than 40 answers given, note the limitation in the report
- Answers outside 1-5 range: clamp to nearest valid value

## Report Language

Detect language from user input:
- Chinese input → report in Simplified Chinese
- English input → report in English

Use the Chinese template (`assets/report_template.md`) for Chinese reports.

## Handling Ambiguous Cases

- **Multiple moderate dimensions**: Mention each in the 💡 note
- **Score very close to 0.5**: Note that the preference is "slight" and describe both sides
- **Unknown/Invalid MBTI type**: Raise error with list of valid types (the 16 listed in references)
