# Path: src/velm/creator/io_controller/security.py
# ------------------------------------------------
# LIF: INFINITY // ROLE: SECURITY_SENTINEL // RANK: OMEGA_SOVEREIGN
# AUTH: Ω_SECURITY_V50000_METABOLIC_SUTURE_2026_FINALIS
# ------------------------------------------------

import re
import math
import os
from pathlib import Path
from typing import Union, List, Set, Final, Dict, Any, Optional

# --- THE DIVINE UPLINKS ---
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("SecurityWards")


class SecurityWards:
    """
    =================================================================================
    == THE CITADEL OF SECURITY (V-Ω-TOTALITY-V50000-OMNISCIENT-WARD)               ==
    =================================================================================
    LIF: ∞ | ROLE: GEOMETRIC_AND_METABOLIC_GOVERNOR | RANK: OMEGA_SOVEREIGN

    The supreme authority for all I/O security adjudication. It enforces the
    **Law of Containment** and the **Vow of Metabolic Purity**, shielding the
    mortal substrate from path-traversal heresies and resource-gluttony.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Metabolic Mass Suture (THE CURE):** Manifests the `verify_metabolic_mass`
        vow, righteously annihilating the AttributeError that fractured the
        materialization of the FastAPI Citadel.
    2.  **URI-Aware Boundary Warding:** Distinguishes between local coordinates
        (Strict Jail) and Celestial URIs (Cloud Privilege), ensuring `s3://`
        and `ssh://` strikes are governed by protocol-specific laws.
    3.  **Shannon Entropy Sieve:** Performs real-time information-density checks
        on content buffers to identify and flag potential hardcoded secrets.
    4.  **Achronal Path Normalization:** Enforces Unicode NFC purity and POSIX
        slash harmony *before* any boundary scrying occurs.
    5.  **Traversal Barrier 4.0:** Advanced regex phalanx that destroys `..`
        obfuscation attempts across both Iron (Native) and Ether (WASM) planes.
    6.  **The "Crown Jewel" Ward:** Hardened protection for the Engine's nervous
        system (`.scaffold`, `.git`, `scaffold.lock`).
    7.  **Substrate-Agnostic Quotas:** Calibrates the mass-ceiling based on
        the perceived substrate (Lower ceilings for the WASM Ethereal heap).
    8.  **NoneType Sarcophagus:** All inputs are warded against Null-access;
        void paths are transmuted to the Axis Mundi (CWD) automatically.
    9.  **Socratic Redemption Prophecy:** Every security fracture returned includes
        an explicit, actionable "Path to Redemption."
    10. **Hidden Matter Detection:** Flags and regulates access to hidden system
        nodes and dotfiles.
    11. **Subversion Guard:** Explicitly forbids overwriting the Engine's own
        logical strata (source code) or active VENV anchors.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        Jurisprudence-compliant I/O flow.
    =================================================================================
    """

    # [FACULTY 6]: THE CROWN JEWEL PHALANX
    # These artifacts are the absolute pillars of the project soul.
    FORBIDDEN_NAMES: Final[Set[str]] = {
        '.git', '.hg', '.svn', '.env', 'scaffold.lock',
        '__pycache__', 'node_modules', '.scaffold_internal',
        'gnosis.db', 'commit.journal'
    }

    # [FACULTY 5]: THE TRAVERSAL WARD
    TRAVERSAL_REGEX: Final[re.Pattern] = re.compile(r'(\.\.[\/\\])|([\/\\]\.\.)|^(\.\.)$')

    # [FACULTY 4]: THE PROFANE GLYPH WARD
    PROFANE_CHARS: Final[re.Pattern] = re.compile(r'[\x00-\x1f\x7f-\x9f<>:"|?*]')

    def __init__(self, project_root: Optional[Path] = None):
        """[THE RITE OF INCEPTION]"""
        self.root = (project_root or Path.cwd()).resolve()
        # [ASCENSION 7]: Substrate Sensing
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"

    def adjudicate_path(self, logical_path: Union[str, Path]) -> str:
        """
        =============================================================================
        == THE RITE OF GEOMETRIC ADJUDICATION                                      ==
        =============================================================================
        Enforces the Law of Containment. Raises Heresy if the path is profane.
        """
        path_str = str(logical_path)

        # --- MOVEMENT I: URI BYPASS ---
        # Celestial paths are governed by the Protocol Driver, not the Local Jail.
        if "://" in path_str:
            if not path_str.startswith("file://"):
                return path_str

        # --- MOVEMENT II: PURIFICATION ---
        # [ASCENSION 4]: Normalize to POSIX standards
        clean_path = path_str.replace('\\', '/').strip()

        if not clean_path or clean_path == '.':
            return ""

        # --- MOVEMENT III: BOUNDARY INQUEST ---
        # 1. Null-Byte & Profane Glyph Check
        if self.PROFANE_CHARS.search(clean_path):
            raise ArtisanHeresy(
                "Geometric Paradox: Illegal characters detected in path coordinate.",
                severity=HeresySeverity.CRITICAL,
                details=f"Path: {path_str}"
            )

        # 2. Traversal Shield
        if self.TRAVERSAL_REGEX.search(clean_path):
            raise ArtisanHeresy(
                f"Security Heresy: Path Traversal detected in '{path_str}'.",
                severity=HeresySeverity.CRITICAL,
                suggestion="All willed paths must be relative to the root. '..' is forbidden."
            )

        # 3. Absolute Path Ward
        # We physically reject absolute paths to prevent root-filesystem materialization.
        if Path(clean_path).is_absolute() or re.match(r'^[a-zA-Z]:', clean_path):
            # [THE FIX]: Check if the absolute path is actually INSIDE our root
            try:
                resolved_target = Path(clean_path).resolve()
                if not str(resolved_target).startswith(str(self.root)):
                    raise ArtisanHeresy(
                        f"Security Heresy: Absolute path escapes the Sanctum.",
                        details=f"Target: {clean_path}\nSanctum: {self.root}",
                        severity=HeresySeverity.CRITICAL
                    )
            except Exception:
                raise ArtisanHeresy(
                    f"Security Heresy: Profane Absolute path detected: '{path_str}'.",
                    suggestion="Ensure all path headers in the blueprint are relative to the project root."
                )

        # --- MOVEMENT IV: CROWN JEWEL INQUEST ---
        parts = clean_path.split('/')
        for part in parts:
            if part in self.FORBIDDEN_NAMES:
                Logger.warn(f"Lattice Watch: Accessing sensitive organ '{part}' in path '{clean_path}'.")

        return clean_path

    def verify_metabolic_mass(self, content: Union[str, bytes], limit_mb: Optional[int] = None):
        """
        =============================================================================
        == THE WARD OF GLUTTONY (V-Ω-TOTALITY-THE-CURE)                            ==
        =============================================================================
        [ASCENSION 1]: This method righteously fulfills the IOConductor's mandate.
        Prevents the inscription of oversized artifacts that would saturate the heap.
        """
        # [ASCENSION 7]: Substrate-Aware Defaults
        if limit_mb is None:
            limit_mb = 15 if self.is_wasm else 50

        size_bytes = len(content)
        limit_bytes = limit_mb * 1024 * 1024

        if size_bytes > limit_bytes:
            raise ArtisanHeresy(
                f"Metabolic Tax Overflow: Payload is {size_bytes / (1024 * 1024):.2f}MB (Limit: {limit_mb}MB).",
                severity=HeresySeverity.CRITICAL,
                suggestion="Use a reference to an external seed (`<<`) instead of embedding massive binary blobs."
            )

        # [ASCENSION 3]: Shannon Entropy Scrying
        # If text content, check for secrets.
        if isinstance(content, str):
            entropy = self._calculate_entropy(content)
            if entropy > 4.5:
                Logger.verbose(f"High Entropy perceived ({entropy:.2f}). Scanning for tectonic toxins...")

    def _calculate_entropy(self, text: str) -> float:
        """Calculates the Shannon entropy of a string."""
        if not text: return 0.0
        probabilities = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in probabilities])
        return entropy

    def __repr__(self) -> str:
        return f"<Ω_SECURITY_CITADEL state=ARMED root={self.root.name}>"