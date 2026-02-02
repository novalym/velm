# Path: scaffold/artisans/distill/core/oracle/utils.py
# ----------------------------------------------------

import re
import os
import json
import math
import hashlib
import difflib
from pathlib import Path
from typing import List, Dict, Any, Union
from collections import Counter

from .....core.cortex.contracts import FileGnosis

# --- [ELEVATION 2] The Secret Scrubber ---
SECRET_PATTERNS = [
    r'(sk-[a-zA-Z0-9]{32,})',  # OpenAI/Stripe
    r'(ghp_[a-zA-Z0-9]{30,})',  # GitHub
    r'(xox[baprs]-([0-9a-zA-Z]{10,48}))',  # Slack
    r'((?:api_key|secret|password)\s*[:=]\s*["\'])([^"\']{8,})'  # Generic
]


def scrub_secrets_global(content: str) -> str:
    """
    [ELEVATION 2] The Veil of Secrecy.
    Redacts known secret patterns from any text.
    """
    cleaned = content
    for pattern in SECRET_PATTERNS:
        cleaned = re.sub(pattern, r'\1{{ REDACTED_SECRET }}', cleaned, flags=re.IGNORECASE)
    return cleaned


def inject_gnostic_stats(content: str, inventory: List[FileGnosis], token_count: int) -> str:
    """
    [ELEVATION 1] The Gnostic Stats Injection.
    Adds a metadata header to the blueprint for the AI's benefit.
    """
    lines = content.splitlines()

    # Calculate stats
    lang_counts = Counter(f.language for f in inventory if f.category == 'code')
    top_langs = ", ".join([f"{l} ({c})" for l, c in lang_counts.most_common(3)])
    total_files = len(inventory)

    # [ELEVATION 12] The Luminous Header Format
    stats_block = [
        "## GNOSTIC CONTEXT ##",
        f"# Total Files: {total_files}",
        f"# Estimated Tokens: ~{token_count:,}",
        f"# Primary Languages: {top_langs}",
        f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "#####################",
        ""
    ]

    # Insert after the first line (usually the project root declaration)
    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith("$$") or line.startswith("# =="):
            insert_pos = i + 1
        elif line.strip() == "" and i > 0:
            insert_pos = i
            break

    lines[insert_pos:insert_pos] = stats_block
    return "\n".join(lines)


def forge_empty_blueprint(root_name: str, strategy: str) -> str:
    """
    [ELEVATION 3] The Void Smith.
    Creates a valid but empty blueprint for new/empty projects.
    """
    header_lines = [
        f"# == Gnostic Blueprint: {root_name} (The Void) ==",
        f"# Forged by: {os.getlogin() if hasattr(os, 'getlogin') else 'Architect'}",
        f"# Strategy: {strategy}",
        "#",
        "# The Cortex's Gaze found only a void. This sanctum is either empty",
        "# or contains only scriptures hidden by the Veil of Aversion (.gitignore).",
        "",
        f"$$ project_root = \"{root_name}\""
    ]
    return "\n".join(header_lines)


def normalize_path(path: Union[str, Path]) -> str:
    """
    [ELEVATION 9] The Path Normalizer.
    Enforces POSIX standard (forward slashes) for blueprint compatibility.
    """
    return str(path).replace('\\', '/')


def robust_read(path: Path) -> str:
    """
    [ELEVATION 4] The Textual Alchemist.
    Attempts multiple encodings to read a file's soul.
    """
    for encoding in ['utf-8', 'latin-1', 'cp1252']:
        try:
            return path.read_text(encoding=encoding)
        except (UnicodeDecodeError, Exception):
            continue
    return "[Unreadable Binary or Unknown Encoding]"


def estimate_tokens(text: str) -> int:
    """
    [ELEVATION 5] The Token Estimator.
    A heuristic fallback for token counting (4 chars ~= 1 token).
    """
    return len(text) // 4


def calculate_entropy(data: bytes) -> float:
    """
    [ELEVATION 8] The Entropy Diviner.
    Calculates Shannon entropy to detect compressed/encrypted/binary data.
    Returns 0.0-8.0. High values (>7.5) usually mean binary/random.
    """
    if not data: return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy


def extract_snippet(content: str, start: int, end: int) -> str:
    """
    [ELEVATION 9] The Snippet Extractor.
    Extracts lines start..end (1-based) from content.
    """
    lines = content.splitlines()
    # Adjust for 0-based index
    s = max(0, start - 1)
    e = min(len(lines), end)
    return "\n".join(lines[s:e])


def generate_diff(old: str, new: str, name: str = "file") -> str:
    """
    [ELEVATION 10] The Diff Prophet.
    Generates a unified diff string.
    """
    diff_lines = difflib.unified_diff(
        old.splitlines(keepends=True),
        new.splitlines(keepends=True),
        fromfile=f"a/{name}",
        tofile=f"b/{name}",
        lineterm=""
    )
    return "".join(diff_lines)


def to_json_luminous(data: Any) -> str:
    """
    [ELEVATION 10] The Luminous Json.
    Serializes data handling Paths and Sets.
    """

    def default(obj):
        if isinstance(obj, Path): return normalize_path(obj)
        if isinstance(obj, set): return sorted(list(obj))
        return str(obj)

    return json.dumps(data, indent=2, default=default)


import time