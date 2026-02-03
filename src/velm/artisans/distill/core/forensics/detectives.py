# Path: scaffold/artisans/distill/core/oracle/forensics/detectives.py
# -------------------------------------------------------------------

import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from .contracts import Indictment
from .grimoire import STACK_PATTERNS, GENERIC_PATH_REGEX, ERROR_HEADERS
from .filters import ApophaticWards
from .....logger import Scribe

Logger = Scribe("ForensicDetectives")


class StructureDetective:
    """
    The Recursive Hunter.
    Walks through nested JSON/Dict structures to find strings that look like
    Tracebacks or Error Messages.
    """

    # Keys that smell like trouble
    TARGET_KEYS = {
        'traceback', 'stack', 'error', 'message', 'detail', 'heresy',
        'failures', 'exceptions', 'cause'
    }

    @classmethod
    def hunt(cls, data: Any) -> List[str]:
        """
        Recursively extracts potential error strings from a JSON object.
        """
        evidence = []

        if isinstance(data, dict):
            for k, v in data.items():
                # If key suggests an error, grab the value
                if k.lower() in cls.TARGET_KEYS:
                    if isinstance(v, str):
                        evidence.append(v)
                    elif isinstance(v, (list, dict)):
                        evidence.extend(cls.hunt(v))
                # Otherwise, keep digging
                else:
                    evidence.extend(cls.hunt(v))

        elif isinstance(data, list):
            for item in data:
                evidence.extend(cls.hunt(item))

        elif isinstance(data, str):
            # Heuristic: If a bare string is huge and looks like a stack trace
            if len(data) > 50 and '\n' in data and 'File "' in data:
                evidence.append(data)

        return evidence


class TextDetective:
    """
    The Pattern Walker.
    Scans raw text blocks to identify File Paths and Line Numbers.
    """

    @classmethod
    def investigate(cls, text: str, project_root: Path) -> List[Indictment]:
        indictments = []

        # 1. Identify Language Specific Patterns
        for lang, pattern in STACK_PATTERNS.items():
            matches = list(pattern.finditer(text))
            if matches:
                total_frames = len(matches)
                for i, match in enumerate(matches):
                    path_str = match.group("path")
                    line_num = int(match.group("line"))

                    # Weighting: Bottom of stack (crash site) > Top of stack
                    # Linear interpolation from 50 to 100
                    weight = 50 + int((i / total_frames) * 50)

                    if not ApophaticWards.is_noise(path_str):
                        indictments.append(Indictment(
                            path=Path(path_str),
                            score=weight,
                            reason=f"{lang.title()} Trace Frame",
                            line_number=line_num
                        ))

        # 2. Generic Path Fallback (if no structured trace found)
        if not indictments:
            candidates = GENERIC_PATH_REGEX.findall(text)
            for path_str in candidates:
                if not ApophaticWards.is_noise(path_str):
                    # We can't determine line number or depth, so we give a static score
                    indictments.append(Indictment(
                        path=Path(path_str),
                        score=40,
                        reason="Heuristic Path Match",
                        line_number=None
                    ))

        return indictments

    @classmethod
    def extract_error_header(cls, text: str) -> Optional[str]:
        """Finds the specific error message (e.g. ValueError: X)."""
        for pattern in ERROR_HEADERS:
            match = re.search(pattern, text, re.MULTILINE)
            if match:
                return match.group(1).strip()
        return None

