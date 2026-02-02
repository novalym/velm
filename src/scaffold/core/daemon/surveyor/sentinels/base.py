# Path: core/daemon/surveyor/sentinels/base.py
# --------------------------------------------
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional
import time
import re


class BaseSentinel(ABC):
    """
    [THE SENTINEL PROTOCOL]
    The abstract contract that all specific language analyzers must sign.
    Provides common heuristic utilities for pattern matching.
    """

    def __init__(self, context: Dict[str, Any] = None):
        self.context = context or {}

        # Universal Secret Patterns (High Entropy Strings)
        self._secret_patterns = [
            (r'(api_key|secret|token|password|auth)\s*=\s*[\'"][^\'"]{20,}[\'"]', "Hardcoded Secret (Generic)"),
            (r'-----BEGIN RSA PRIVATE KEY-----', "Embedded Private Key"),
            (r'AWS_ACCESS_KEY_ID\s*=\s*[\'"]AKIA[0-9A-Z]{16}[\'"]', "AWS Access Key"),
        ]

    @abstractmethod
    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        """
        The Rite of Analysis.
        Must return a list of Diagnostic objects.
        """
        pass

    def forge_diagnostic(self, line: int, msg: str, severity: int, source: str, code: str,
                         suggestion: Optional[str] = None) -> Dict:
        """
        [THE SEAL OF JUDGMENT]
        Creates a standardized LSP Diagnostic structure.
        """
        return {
            "range": {
                "start": {"line": line, "character": 0},
                "end": {"line": line, "character": 999}
            },
            "severity": severity,
            "code": code,
            "source": source,
            "message": msg,
            "timestamp": time.time(),
            # [ASCENSION 1]: Inject "Fixability" hint for the UI
            "data": {
                "suggestion": suggestion,
                "heresy_key": code
            }
        }

    def scan_for_secrets(self, line: str, line_num: int, source: str) -> Optional[Dict]:
        """Universal secret scanning utility."""
        for pattern, desc in self._secret_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                return self.forge_diagnostic(
                    line_num,
                    f"SECURITY ALERT: {desc} detected. Transmute to Environment Variable immediately.",
                    1,  # SEVERITY_ERROR
                    source,
                    "SECURITY_HARDCODED_SECRET"
                )
        return None

