# Path: src/velm/core/runtime/vfs/alchemist.py
# ------------------------------------------
"""
=================================================================================
== THE GNOSTIC MATTER ALCHEMIST (V-Ω-TOTALITY-V200)                            ==
=================================================================================
LIF: ∞ | ROLE: SCRIPTURE_RESURRECTOR | RANK: OMEGA_SUPREME

The supreme artisan of recall. Transmutes raw bytes into Gnostic souls (strings)
while guarding against binary entropy, path drift, and encoding heresies.
=================================================================================
"""

import os
import json
import hashlib
import importlib
from pathlib import Path
from typing import Dict, Any, Union, Optional, Tuple


class MatterAlchemist:
    """
    =============================================================================
    == THE MATTER ALCHEMIST (V-Ω-RECALL-ENGINE)                                ==
    =============================================================================
    Distills physical bytes into Gnostic souls (strings) or Binary Husks.
    """

    MAX_METABOLIC_MASS = 5 * 1024 * 1024  # 5MB Threshold
    VAULT_ANCHOR = "/vault"

    @classmethod
    def read_soul(cls, path_str: str) -> Dict[str, Any]:
        """
        The primary rite of resurrection.
        Gathers content and metadata from the substrate.
        """
        # [ASCENSION 1]: CACHE INVALIDATION
        importlib.invalidate_caches()

        try:
            # [ASCENSION 7]: PATH TRAVERSAL WARD
            target_path = Path(path_str).resolve()
            if not str(target_path).startswith(cls.VAULT_ANCHOR):
                return cls._proclaim_heresy("SECURITY_HERESY", f"Intent escaped sanctum: {path_str}")

            if not target_path.exists():
                return cls._proclaim_heresy("VOID_MATTER", f"Scripture unmanifest: {path_str}")

            if not target_path.is_file():
                return cls._proclaim_heresy("GEOMETRIC_PARADOX", f"Locus is a sanctum, not a scripture: {path_str}")

            stats = target_path.stat()

            # [ASCENSION 5]: METABOLIC MASS THROTTLING
            if stats.st_size > cls.MAX_METABOLIC_MASS:
                return cls._proclaim_success(
                    content="[HEAVY_MATTER_REDACTED]",
                    path=target_path,
                    stats=stats,
                    is_binary=True,
                    note="File exceeds 5MB metabolic limit."
                )

            # [ASCENSION 2]: BINARY MATTER TRIAGE
            is_bin, raw_bytes = cls._peek_matter(target_path)
            if is_bin:
                return cls._proclaim_success(
                    content="[BINARY_MATTER_REDACTED]",
                    path=target_path,
                    stats=stats,
                    is_binary=True
                )

            # [ASCENSION 4]: MULTI-PASS ENCODING RESURRECTION
            soul = cls._resurrect_string(raw_bytes)

            # [ASCENSION 8]: HEREDOC NORMALIZATION
            soul = soul.replace('\r\n', '\n')

            return cls._proclaim_success(
                content=soul,
                path=target_path,
                stats=stats,
                is_binary=False
            )

        except Exception as e:
            return cls._proclaim_heresy("CATASTROPHIC_FRACTURE", str(e))

    @staticmethod
    def _peek_matter(path: Path) -> Tuple[bool, bytes]:
        """Peeks at the soul of the file to divine its nature."""
        with open(path, 'rb') as f:
            matter = f.read()
            # [ASCENSION 2]: Null byte detection is the standard for binary scrying
            is_binary = b'\x00' in matter[:8192]
            return is_binary, matter

    @staticmethod
    def _resurrect_string(matter: bytes) -> str:
        """Attempts to breathe string-life into raw bytes via multi-pass decoding."""
        for encoding in ['utf-8', 'cp1252', 'latin-1']:
            try:
                return matter.decode(encoding)
            except UnicodeDecodeError:
                continue
        # [ASCENSION 4]: Socratic Replacement fallback
        return matter.decode('utf-8', errors='replace')

    @classmethod
    def _proclaim_success(cls, content: str, path: Path, stats: os.stat_result, is_binary: bool,
                          note: Optional[str] = None) -> Dict[str, Any]:
        """Forges the successful revelation vessel."""
        # [ASCENSION 6]: MERKLE FINGERPRINTING
        fingerprint = hashlib.sha256(content.encode('utf-8', errors='ignore')).hexdigest()

        return {
            "success": True,
            "content": content,
            "path": str(path),
            "size": stats.st_size,
            "mtime": stats.st_mtime,
            "is_binary": is_binary,
            "hash": fingerprint,
            "dialect": cls._divine_dialect(path, content),
            "note": note
        }

    @staticmethod
    def _proclaim_heresy(code: str, msg: str) -> Dict[str, Any]:
        """Forges the failed revelation vessel."""
        return {
            "success": False,
            "error": code,
            "message": msg,
            "content": f"[HERESY] {code}: {msg}"
        }

    @staticmethod
    def _divine_dialect(path: Path, content: str) -> str:
        """
        [ASCENSION 3]: LINGUISTIC DIALECT DIVINATION.
        Guess the language for the Ocular UI.
        """
        ext = path.suffix.lower().lstrip('.')
        if not ext:
            # Check for shebang
            if content.startswith('#!'):
                line = content.split('\n')[0]
                if 'python' in line: return 'python'
                if 'node' in line: return 'javascript'
                if 'bash' in line or 'sh' in line: return 'shell'
            return 'plaintext'

        mapping = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'tsx': 'typescript',
            'rs': 'rust',
            'go': 'go',
            'scaffold': 'yaml',
            'symphony': 'yaml',
            'arch': 'yaml',
            'lock': 'json',
            'md': 'markdown',
            'sql': 'sql'
        }
        return mapping.get(ext, 'plaintext')


def vfs_read_scripture(path: str) -> Dict[str, Any]:
    """Universal interface for the WASM Worker's READ rite."""
    return MatterAlchemist.read_soul(path)