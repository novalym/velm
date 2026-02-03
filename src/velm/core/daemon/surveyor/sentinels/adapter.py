# Path: core/daemon/surveyor/sentinels/adapter.py
# -----------------------------------------------
# LIF: INFINITY | AUTH_CODE: Ω_ADAPTER_POLYMORPHIC_V2
# SYSTEM: GNOSTIC_SURVEYOR | ROLE: DEEP_LOGIC_BRIDGE
# =================================================================================

import time
import re
import traceback
import inspect
from pathlib import Path
from typing import List, Dict, Any, Callable, Union, Optional

from .base import BaseSentinel
from ..constants import (
    SEVERITY_ERROR, SEVERITY_WARNING,
    SEVERITY_INFO, SEVERITY_HINT
)

# [ASCENSION 1]: FLOOD CONTROL
# Prevents a single broken analyzer from flooding the UI.
MAX_DIAGNOSTICS_PER_FILE = 100


class DeepSentinelAdapter(BaseSentinel):
    """
    =============================================================================
    == THE DEEP SENTINEL ADAPTER (V-Ω-UNIVERSAL-TRANSLATOR)                    ==
    =============================================================================

    A hardened wrapper that allows any Python function to act as a Sentinel.
    It bridges the gap between the high-speed Surveyor loop and heavy/legacy
    analysis tools.

    [CAPABILITIES]:
    1. POLYMORPHIC IDENTITY: Absorbs 'context', 'tool_name', or 'source' arguments.
    2. EXCEPTION SHIELDING: Swallows crashes in the wrapped tool.
    3. FORMAT NORMALIZATION: Converts arbitrary dicts into strict LSP Diagnostics.
    4. SEVERITY MAPPING: Translates string levels ('CRITICAL') to LSP ints (1).
    """

    def __init__(
            self,
            analyzer_func: Callable[..., Union[List[Dict], None]],
            tool_name: str = "Deep Analysis Engine",
            description: str = "External Logic Adapter",
            **kwargs  # [ASCENSION 2]: Absorb unknown args (e.g. 'context')
    ):
        super().__init__()
        self._analyzer_func = analyzer_func
        self._description = description

        # [ASCENSION 3]: IDENTITY RESOLUTION
        # If 'context' was passed (legacy), use it as the tool name.
        self._tool_name = kwargs.get('context') or tool_name

        # Introspect the function to optimize calls later
        try:
            self._sig = inspect.signature(analyzer_func)
        except:
            self._sig = None

    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        """
        [THE RITE OF DELEGATION]
        Executes the wrapped function and transmutes its output.
        """
        start_time = time.perf_counter()
        diagnostics = []

        try:
            # [ASCENSION 4]: SMART INVOCATION
            # Only pass arguments the function actually accepts to avoid TypeErrors
            call_kwargs = {'content': content, 'file_path': file_path}

            if self._sig:
                if 'root_path' in self._sig.parameters:
                    call_kwargs['root_path'] = root_path
                # Add other context if needed
            else:
                # Blind call - pass everything and hope for **kwargs
                call_kwargs['root_path'] = root_path

            # Execute
            raw_results = self._analyzer_func(**call_kwargs)

            # [ASCENSION 5]: THE VOID GUARD
            if not raw_results:
                return []

            if not isinstance(raw_results, list):
                # If a single dict is returned, wrap it
                raw_results = [raw_results]

            # [ASCENSION 6]: THE HERESY TRANSMUTER
            for i, item in enumerate(raw_results):
                if i >= MAX_DIAGNOSTICS_PER_FILE:
                    break

                # Filter nulls
                if not item: continue

                normalized = self._normalize_result(item, i)
                if normalized:
                    # [ASCENSION 7]: CHRONOMETRIC TAGGING
                    normalized['data']['meta'] = {
                        'tool': self._tool_name,
                        'duration_ms': (time.perf_counter() - start_time) * 1000
                    }
                    diagnostics.append(normalized)

        except Exception as e:
            # [ASCENSION 8]: EXECUTION SANDBOX
            # If the deep tool crashes, we report the crash as a diagnostic on line 0
            # rather than crashing the Surveyor thread.
            error_msg = f"{self._tool_name} Fractured: {str(e)}"
            # traceback.print_exc() # For internal debug

            diagnostics.append(self.forge_diagnostic(
                line=0,
                msg=error_msg,
                severity=SEVERITY_WARNING,  # Downgraded to warning to not block build
                source="Gnostic Adapter",
                code="ADAPTER_FAILURE",
                suggestion="Check the Daemon logs for full traceback."
            ))

        return diagnostics

    def _normalize_result(self, item: Dict[str, Any], index: int) -> Optional[Dict]:
        """
        [THE ALCHEMICAL FILTER]
        Maps arbitrary dictionary keys to the strict Gnostic Diagnostic Schema.
        """
        if not isinstance(item, dict):
            return None

        # 1. DIVINE LINE NUMBER
        # Try standardized keys first, then fallbacks
        line = item.get('line') or item.get('lineno') or item.get('row') or item.get('line_number') or 0
        try:
            line = int(line)
            # Ensure 0-indexed for LSP (LSP uses 0-based, humans use 1-based)
            # We assume inputs are 1-based if coming from external tools like linters.
            if line > 0: line -= 1
        except (ValueError, TypeError):
            line = 0

        # 2. DIVINE MESSAGE
        # [ASCENSION 9]: OUTPUT SANITIZATION
        raw_msg = item.get('message') or item.get('msg') or item.get('text') or item.get('error') or "Unknown Anomaly"
        clean_msg = self._strip_ansi(str(raw_msg))

        # 3. DIVINE SEVERITY
        raw_sev = item.get('severity') or item.get('level') or item.get('type')
        severity = self._map_severity(raw_sev)

        # 4. DIVINE CODE
        code = item.get('code') or item.get('id') or item.get('rule') or "EXTERNAL_RULE"

        # 5. DIVINE SUGGESTION / FIX
        # [ASCENSION 10]: SUGGESTION PASSTHROUGH
        suggestion = item.get('suggestion') or item.get('fix') or item.get('hint')

        # 6. FORGE DIAGNOSTIC
        return self.forge_diagnostic(
            line=line,
            msg=clean_msg,
            severity=severity,
            source=self._tool_name,
            code=str(code),
            suggestion=suggestion
        )

    def _map_severity(self, raw: Any) -> int:
        """
        [ASCENSION 11]: SEVERITY NORMALIZATION
        Fuzzy-matches strings to LSP Integers.
        """
        if isinstance(raw, int):
            if 1 <= raw <= 4: return raw
            return SEVERITY_INFO

        if not isinstance(raw, str):
            return SEVERITY_INFO

        s = raw.upper()

        if 'CRIT' in s or 'ERR' in s or 'FATAL' in s or 'FAIL' in s:
            return SEVERITY_ERROR
        if 'WARN' in s or 'POTENTIAL' in s:
            return SEVERITY_WARNING
        if 'INFO' in s or 'NOTE' in s or 'LOG' in s:
            return SEVERITY_INFO
        if 'HINT' in s or 'TODO' in s or 'SUGGEST' in s:
            return SEVERITY_HINT

        return SEVERITY_INFO

    def _strip_ansi(self, text: str) -> str:
        """
        [ASCENSION 12]: VISUAL PURITY
        Removes terminal color codes.
        """
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)