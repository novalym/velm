# Path: artisans/analyze/reporting/diagnostics.py
# -----------------------------------------------

import re
import time
from typing import List, Dict, Any, Optional, Union


class DiagnosticForge:
    """
    =============================================================================
    == THE DIAGNOSTIC FORGE (V-Ω-LSP-FACTORY-ULTIMA)                           ==
    =============================================================================
    LIF: 100,000,000,000 | ROLE: DATA_TRANSMUTER

    A static factory class dedicated to forging standardized Language Server Protocol
    (LSP) structures from raw, chaotic, or proprietary inputs.

    ### THE PANTHEON OF 6 FACULTIES:
    1.  **The Markup Purifier:** Strips `rich` console tags (`[bold]`) to ensure clean UI text.
    2.  **The Range Creator:** Forges standard LSP `Range` objects from simple line numbers.
    3.  **The Severity Mapper:** Transmutes strings ('CRITICAL') into LSP Integers (1).
    4.  **The Coordinate Mapper:** Converts byte offsets to Line/Character positions.
    5.  **The Heresy Formatter:** The main pipeline for converting a list of raw heresies.
    6.  **The Bounds Guard:** Clamps coordinates to prevent client-side crashes.
    """

    # LSP Severity Codes
    SEV_ERROR = 1
    SEV_WARNING = 2
    SEV_INFO = 3
    SEV_HINT = 4

    @staticmethod
    def make_range(line: int, start_char: int = 0, end_char: int = 999) -> Dict[str, Dict[str, int]]:
        """
        [THE MISSING LINK - RESTORED]
        Forges a standard LSP Range object for a specific line.
        Default end_char=999 ensures the full line is highlighted.

        Args:
            line: 0-indexed line number.
            start_char: 0-indexed start character.
            end_char: 0-indexed end character.
        """
        safe_line = max(0, int(line))
        return {
            "start": {"line": safe_line, "character": max(0, start_char)},
            "end": {"line": safe_line, "character": max(0, end_char)}
        }

    @staticmethod
    def purify_markup(text: Optional[str]) -> str:
        """
        [THE PURIFIER]
        Strips Rich/Console markup tags to ensure raw text visibility in the Editor.
        Example: "[bold red]Error[/]" -> "Error"
        """
        if not text:
            return ""
        # Regex matches [tag], [/tag], [tag=value]
        return re.sub(r'\[/?\w+(?:=[^\]]+)?\]', '', str(text))

    @staticmethod
    def map_severity(raw_severity: Union[str, int]) -> int:
        """
        [THE JUDGE]
        Transmutes arbitrary severity indicators into LSP Constants.
        """
        s = str(raw_severity).upper()
        if s in ('1', 'CRITICAL', 'ERROR', 'FATAL'): return DiagnosticForge.SEV_ERROR
        if s in ('2', 'WARNING', 'WARN'): return DiagnosticForge.SEV_WARNING
        if s in ('3', 'INFO', 'LOG', 'SYSTEM'): return DiagnosticForge.SEV_INFO
        if s in ('4', 'HINT', 'SUGGESTION'): return DiagnosticForge.SEV_HINT
        return DiagnosticForge.SEV_INFO  # Default

    @staticmethod
    def offset_to_position(content: str, offset: int) -> Dict[str, int]:
        """
        [THE CHRONOMANCER]
        Transmutes a linear byte offset into a 2D (Line, Character) coordinate.
        Essential for connecting Tree-sitter (Offset) to LSP (Position).
        """
        if offset < 0:
            return {"line": 0, "character": 0}

        # Clamp offset to content length
        safe_offset = min(len(content), offset)

        sub_content = content[:safe_offset]
        line_count = sub_content.count('\n')
        last_newline = sub_content.rfind('\n')

        # If no newline, we are on the first line
        character_count = safe_offset if last_newline == -1 else safe_offset - (last_newline + 1)

        return {"line": line_count, "character": character_count}

    @staticmethod
    def format_diagnostics(diagnostics: List[Dict[str, Any]], content: str) -> List[Dict[str, Any]]:
        """
        [THE GRAND TRANSMUTER]
        Processes a raw list of internal heresy dictionaries into a strict
        LSP-compliant list of Diagnostics.

        Features:
        - Content Boundary Protection (Line Clamping)
        - Markup Purification
        - Metadata Preservation (for Auto-Fixes)
        """
        final_diagnostics = []
        content_lines = content.splitlines()
        max_line_index = max(0, len(content_lines) - 1)

        for d in diagnostics:
            try:
                # 1. Divine Coordinates
                # Prefer explicit range if available, else fallback to line number
                if 'range' in d:
                    rng = d['range']
                    # Ensure range structure validity
                    if 'start' not in rng or 'end' not in rng:
                        line_num = int(d.get('internal_line', 0))
                        rng = DiagnosticForge.make_range(line_num)
                else:
                    line_num = int(d.get('internal_line', 0))
                    # [ASCENSION]: Clamp line number to physical reality
                    safe_line = min(max(0, line_num), max_line_index)
                    rng = DiagnosticForge.make_range(safe_line)

                # 2. Purify Text
                clean_message = DiagnosticForge.purify_markup(d.get('message', 'Unknown Heresy'))
                clean_details = DiagnosticForge.purify_markup(d.get('details'))
                clean_suggestion = DiagnosticForge.purify_markup(d.get('suggestion'))

                # 3. Resolve Severity
                severity = DiagnosticForge.map_severity(d.get('severity', 2))

                # 4. Resolve Code
                code = str(d.get('code', 'GNOSIS'))

                # 5. Forge Artifact
                diagnostic = {
                    "range": rng,
                    "severity": severity,
                    "code": code,
                    "source": str(d.get('source', 'Scaffold')),
                    "message": clean_message,
                    "tags": d.get('tags', []),  # Support for Unnecessary/Deprecated tags
                    "data": {
                        # [ASCENSION]: Rich Context for the Healer
                        "heresy_key": code,
                        "details": clean_details,
                        "suggestion": clean_suggestion,
                        "internal_line": rng['start']['line'],
                        # Pass through any fix commands provided by the origin
                        "fix_command": d.get('fix_command'),
                        "raw_data": d.get('data')  # Original payload if any
                    }
                }

                final_diagnostics.append(diagnostic)

            except Exception:
                # [SILENCE WARD]: A failure to format one diagnostic
                # must not prevent the others from being proclaimed.
                continue

        return final_diagnostics