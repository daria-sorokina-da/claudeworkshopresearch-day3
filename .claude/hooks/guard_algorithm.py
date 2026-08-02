#!/usr/bin/env python3
"""PreToolUse hook — the red line, enforced.

Two jobs:
  1. Block any write to src/algorithm/ (the off-limits algorithm module).
  2. Block writes that appear to contain live credentials.

Exit 2 blocks the action AND returns stderr to Claude, so it can self-correct.

Note this duplicates the `deny` rules in settings.json on purpose. Defence in depth:
the deny list is declarative and easy to read; the hook can explain *why*, which is
what makes the lesson stick.
"""

import json
import re
import sys

BLOCKED_PATHS = [
    (re.compile(r"(^|/)src/algorithm/"),
     "src/algorithm/ is the off-limits algorithm module. It encodes a scientific "
     "rationale that must not be modified by a model. See EXERCISE.md, red line 1."),
    (re.compile(r"\.env$"), "this is a secrets file."),
    (re.compile(r"\.pem$"), "this is a key file."),
]

SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "an AWS access key"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "an API key"),
    (re.compile(r"-----BEGIN (RSA |EC )?PRIVATE KEY"), "a private key"),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # fail open — a guardrail that breaks the tool gets switched off

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path", "") or ""
    content = tool_input.get("content", "") or ""

    for pattern, reason in BLOCKED_PATHS:
        if pattern.search(file_path):
            print(f"BLOCKED: {file_path} — {reason}", file=sys.stderr)
            return 2

    for pattern, description in SECRET_PATTERNS:
        if pattern.search(content):
            print(
                f"BLOCKED: this write appears to contain {description}. "
                "Use an environment variable.",
                file=sys.stderr,
            )
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
