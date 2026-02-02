# Path: core/lsp/features/diagnostics/formatter.py
# ------------------------------------------------

import logging
import re
from typing import List, Any, Dict, Union, Optional
from ...types import (
    Diagnostic,
    DiagnosticSeverity,
    Range,
    Position,
    CodeDescription,
    DiagnosticTag,
    DiagnosticRelatedInformation
)
from ...document import TextDocument
from ...utils.text import strip_ansi

Logger = logging.getLogger("DiagnosticFormatter")


class LspDiagnosticFormatter:
    """
    =============================================================================
    == THE TRANSMUTER (V-Ω-IMMUTABLE-RECONSTRUCTION-ENGINE)                    ==
    =============================================================================
    LIF: 10,000,000 | ROLE: DATA_NORMALIZER | RANK: SOVEREIGN

    Bridges the gap between raw Python analysis and the strict VS Code Schema.

    [THE CURE]: Respcts Pydantic V2 Immutability.
    It does NOT mutate ranges. It measures the document, calculates valid
    coordinates, and forges NEW Range objects.
    """

    def to_lsp(self, findings: List[Any], doc: TextDocument) -> List[Diagnostic]:
        """
        Converts internal findings to strict, clamped LSP Diagnostic objects.
        """
        lsp_diagnostics: List[Diagnostic] = []

        # [ASCENSION 1]: PHYSICS CONSTANTS
        # We cache these to avoid repeated lock acquisition on the document
        line_count = doc.line_count
        max_line_index = max(0, line_count - 1)

        for finding in findings:
            try:
                # 1. EXTRACT RAW GNOSIS
                # We extract values into primitives first. We do NOT touch the object yet.
                if isinstance(finding, dict):
                    raw_range = finding.get('range')
                    raw_msg = finding.get('message', 'Unknown Heresy')
                    raw_sev = finding.get('severity')
                    raw_code = finding.get('code')
                    raw_source = finding.get('source')
                    raw_data = finding.get('data') or {}
                    raw_tags = finding.get('tags')
                    raw_related = finding.get('relatedInformation')
                    raw_url = finding.get('url')
                else:
                    # Assume Object/Pydantic
                    raw_range = getattr(finding, 'range', None)
                    raw_msg = getattr(finding, 'message', 'Unknown Heresy')
                    raw_sev = getattr(finding, 'severity', None)
                    raw_code = getattr(finding, 'code', None)
                    raw_source = getattr(finding, 'source', None)
                    raw_data = getattr(finding, 'data', {})
                    raw_tags = getattr(finding, 'tags', None)
                    raw_related = getattr(finding, 'related_information', None)
                    raw_url = getattr(finding, 'url', None)

                # 2. DIVINE COORDINATES (THE CLAMP)
                # We define start/end line/char as integers first.
                if raw_range:
                    # Handle Pydantic Range object or Dict
                    if hasattr(raw_range, 'start'):
                        s_l = raw_range.start.line
                        s_c = raw_range.start.character
                        e_l = raw_range.end.line
                        e_c = raw_range.end.character
                    else:
                        s_l = raw_range.get('start', {}).get('line', 0)
                        s_c = raw_range.get('start', {}).get('character', 0)
                        e_l = raw_range.get('end', {}).get('line', 0)
                        e_c = raw_range.get('end', {}).get('character', 0)
                else:
                    # Fallback to line numbers if Range object missing
                    # Support 'line', 'lineno', 'line_num'
                    if isinstance(finding, dict):
                        l = finding.get('line') or finding.get('lineno') or finding.get('line_num') or 0
                    else:
                        l = getattr(finding, 'line', getattr(finding, 'lineno', getattr(finding, 'line_num', 0)))

                    s_l = int(l)
                    e_l = int(l)
                    s_c = 0
                    e_c = 999  # Sentinel for "Whole Line"

                # [ASCENSION 2]: GEOMETRIC CLAMPING
                # Force the coordinates into the document's physical reality.
                start_line = max(0, min(s_l, max_line_index))
                end_line = max(0, min(e_l, max_line_index))

                # Clamp characters (Optional but safe)
                # For high performance, we might skip precise column clamping if we trust the browser,
                # but clamping start < end is critical.
                start_char = max(0, int(s_c))
                end_char = max(0, int(e_c))

                # [ASCENSION 12]: VOID GUARD (Inverted Range)
                if start_line > end_line or (start_line == end_line and start_char > end_char):
                    end_line = start_line
                    end_char = start_char + 1

                # 3. FORGE IMMUTABLE GEOMETRY
                # We create NEW Position/Range objects. We do NOT mutate the input.
                final_range = Range(
                    start=Position(line=start_line, character=start_char),
                    end=Position(line=end_line, character=end_char)
                )

                # 4. TRANSMUTE ATTRIBUTES

                # ANSI Exorcism
                clean_msg = strip_ansi(str(raw_msg))

                # Severity Mapping
                severity = self._map_severity(raw_sev, clean_msg)

                # Code Description (Clickable Links)
                code_desc = None
                if raw_url:
                    code_desc = CodeDescription(href=str(raw_url))

                # Tags (Deprecated/Unused)
                tags = self._map_tags(raw_tags, clean_msg)

                # Source
                source = str(raw_source) if raw_source else "Gnostic Sentinel"

                # 5. FORGE THE VESSEL
                diagnostic = Diagnostic(
                    range=final_range,
                    severity=severity,
                    code=str(raw_code) if raw_code else "HERESY",
                    source=source,
                    message=clean_msg,
                    tags=tags,
                    codeDescription=code_desc,
                    relatedInformation=raw_related,  # Pass through if valid
                    data=raw_data  # Preserve fix commands
                )

                lsp_diagnostics.append(diagnostic)

            except Exception as e:
                # [ASCENSION 13]: FAULT ISOLATION
                # A formatting error on one finding must not blind the Architect to others.
                # Logger.warning(f"Diagnostic Formatting Fracture: {e}")
                continue

        return lsp_diagnostics

    def _map_severity(self, raw: Any, msg: str) -> DiagnosticSeverity:
        """
        [ASCENSION 5]: SEVERITY ALCHEMY
        Maps arbitrary inputs to LSP Enums and promotes based on keywords.
        """
        # 1. Keyword Promotion (Overrides)
        u_msg = msg.upper()
        if "PANIC" in u_msg or "FATAL" in u_msg or "SECURITY" in u_msg or "CRITICAL" in u_msg:
            return DiagnosticSeverity.Error

        # 2. Direct Mapping
        if isinstance(raw, (DiagnosticSeverity, int)):
            # Ensure valid range 1-4
            val = int(raw)
            if 1 <= val <= 4:
                return DiagnosticSeverity(val)

        # 3. String Fuzzy Match
        s = str(raw).upper()
        if 'ERR' in s or '1' in s or 'CRIT' in s: return DiagnosticSeverity.Error
        if 'WARN' in s or '2' in s: return DiagnosticSeverity.Warning
        if 'INFO' in s or '3' in s: return DiagnosticSeverity.Information
        if 'HINT' in s or '4' in s: return DiagnosticSeverity.Hint

        return DiagnosticSeverity.Information

    def _map_tags(self, raw: Any, msg: str) -> Optional[List[DiagnosticTag]]:
        """
        [ASCENSION 8]: TAG TRANSMUTATION
        Detects Unnecessary/Deprecated flags.
        """
        tags = []

        # Check Explicit
        if raw and isinstance(raw, list):
            for t in raw:
                if t == 1 or t == DiagnosticTag.Unnecessary: tags.append(DiagnosticTag.Unnecessary)
                if t == 2 or t == DiagnosticTag.Deprecated: tags.append(DiagnosticTag.Deprecated)

        # Check Implicit (Message Heuristics)
        u_msg = msg.upper()
        if "UNUSED" in u_msg or "UNNECESSARY" in u_msg:
            if DiagnosticTag.Unnecessary not in tags:
                tags.append(DiagnosticTag.Unnecessary)

        if "DEPRECATED" in u_msg:
            if DiagnosticTag.Deprecated not in tags:
                tags.append(DiagnosticTag.Deprecated)

        return tags if tags else None