# Path: scaffold/utils/dossier_scribe/constellation/xray.py
# ---------------------------------------------------------

from pathlib import Path
from typing import Optional
from ....inquisitor import get_treesitter_gnosis


class GnosticXRay:
    """
    =================================================================================
    == THE SEMANTIC X-RAY (V-Ω-DEEP-PERCEPTION)                                    ==
    =================================================================================
    Uses the Tree-sitter Inquisitor to gaze into the soul of a file and extract a
    compact semantic summary (e.g., "[Class: User, Func: login]").
    """

    @staticmethod
    def scan(path: Path) -> Optional[str]:
        """
        Performs a micro-gaze into the file content.
        Returns a formatted string of the file's primary definitions.
        """
        if not path.exists() or not path.is_file():
            return None

        # We only X-Ray source code
        if path.suffix not in {'.py', '.ts', '.js', '.go', '.rs', '.java', '.rb'}:
            return None

        # Guard against large files for performance
        if path.stat().st_size > 50 * 1024:
            return None

        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            gnosis = get_treesitter_gnosis(path, content)

            if not gnosis or "error" in gnosis:
                return None

            summary_parts = []

            # Extract Classes (Top 2)
            classes = gnosis.get("classes", [])
            if classes:
                names = [c['name'] for c in classes[:2]]
                count = len(classes)
                suffix = f"+{count - 2}" if count > 2 else ""
                summary_parts.append(f"Class: {','.join(names)}{suffix}")

            # Extract Functions (Top 3)
            # We filter out dunder methods to reduce noise
            funcs = [f for f in gnosis.get("functions", []) if not f['name'].startswith('__')]
            if funcs:
                names = [f['name'] for f in funcs[:3]]
                count = len(funcs)
                suffix = f"+{count - 3}" if count > 3 else ""
                summary_parts.append(f"Func: {','.join(names)}{suffix}")

            if not summary_parts:
                return None

            return f"[{' | '.join(summary_parts)}]"

        except Exception:
            # The X-Ray must never crash the visualization
            return None

