# Path: src/velm/parser_core/hierophant.py
# ----------------------------------------
# LIF: ∞ | ROLE: GEOMETRIC_ORACLE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_HIEROPHANT_V500_SPATIAL_TOTALITY_FINALIS
# =========================================================================================

import os
import re
import time
import hashlib
import unicodedata
from pathlib import Path
from threading import RLock
from typing import List, Tuple, Optional, Dict, Final, Any, Set

from ..logger import Scribe
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("GnosticHierophant")


class HierophantOfUnbreakableReality:
    """
    =================================================================================
    == THE GNOSTIC HIEROPHANT (V-Ω-TOTALITY-V500.0-UNBREAKABLE)                    ==
    =================================================================================
    The Supreme Governor of Spatial Resolution. It transmutes textual intent into 
    unbreakable geometric coordinates across multiple reality strata.
    =================================================================================
    """

    # [ASCENSION 10]: THE DEPTH CEILING
    MAX_STRATA_DEPTH: Final[int] = 32

    # [ASCENSION 2 & 3]: THE PHANTOM FOREST SIEVE (THE CURE)
    # 1. Box Drawing (\u2500-\u257F)
    # 2. Block Elements (\u2580-\u259F)
    # 3. Geometric Shapes (\u25A0-\u25FF)
    # 4. Misc Symbols/Emojis (\u2600-\u27BF, \U0001F300-\U0001FAFF)
    # 5. Markdown List Markers
    JUNK_PATTERN: Final[re.Pattern] = re.compile(
        r'('
        r'[\u2500-\u257F\u2580-\u259F\u25A0-\u25FF\u2600-\u27BF]+|'  # Boxes/Blocks/Shapes
        r'[\U0001F300-\U0001FAFF]+|'  # Emojis/Pictographs
        r'^[\s\t]*[\*\-\+]\s+|'  # Markdown Bullets
        r'^[\s\t]*\d+\.\s+|'  # Markdown Numbering
        r'^[\s\t]*>\s+'  # Markdown Quotes
        r')'
    )

    # [ASCENSION 4]: THE ANTI-MATTER PHALANX
    # Code fragments that mistakenly leaked into the path stream.
    MATTER_LEAK_SIGNATURES: Final[List[re.Pattern]] = [
        re.compile(r'^\s*def\s+\w+\('),
        re.compile(r'^\s*class\s+\w+'),
        re.compile(r'^\s*import\s+[\w.]+'),
        re.compile(r'^\s*from\s+[\w.]+\s+import'),
        re.compile(r'^\s*return\s+'),
        re.compile(r'\{\{.*?\}\}'),  # Unresolved Jinja
    ]

    def __init__(self, root_path: Path):
        """
        The Rite of Inception. Anchors the Hierophant to the physical root.
        """
        self._lock = RLock()
        self.root_path = root_path.resolve()

        # [STACK]: Stores (CurrentAbsolutePath, IndentLevel)
        # We start at -1 to allow 0-indent items to attach to project root.
        self.path_stack: List[Tuple[Path, int]] = [(self.root_path, -1)]

        # [ASCENSION 21]: FORENSIC TRACE LOG
        self.trace_log: List[Dict[str, Any]] = []

    # =========================================================================
    # == RITE I: PATH WEAVING (THE MULTIVERSAL COMPASS)                      ==
    # =========================================================================

    def weave_path(self, raw_path_str: str, indent: int, origin_path: Optional[Path] = None) -> Path:
        """
        =============================================================================
        == THE RITE OF PATH WEAVING (V-Ω-TOTALITY)                                 ==
        =============================================================================
        [ASCENSION 1]: THE ORIGIN COMPASS.
        Resolves a coordinate relative to the indentation stack, while allowing 
        relative pivots (./, ../) to resolve against the originating scripture.
        """
        with self._lock:
            # --- MOVEMENT 0: THE COMPASS SUTURE ---
            # If an origin_path is willed (e.g. from an @import in a lib folder),
            # we use its location as the geometric base for relative segments.
            effective_rel_base = origin_path.parent if (origin_path and origin_path.is_file()) else self.root_path

            # --- MOVEMENT I: TEMPORAL ALIGNMENT (STACK UNWIND) ---
            # We unwind the stack to find the parent node matching the current indentation.
            while len(self.path_stack) > 1 and indent <= self.path_stack[-1][1]:
                self.path_stack.pop()

            current_logical_parent = self.path_stack[-1][0]

            # --- MOVEMENT II: THE ATOMIC SIEVE (PURIFICATION) ---
            purified_input = self._purify_path_stream(raw_path_str)

            # [ASCENSION 12]: VOID-VESSEL RECOVERY
            if not purified_input or purified_input == ".":
                return current_logical_parent

            # --- MOVEMENT III: GEOMETRIC ADJUDICATION ---
            working_path: Path

            # 1. Absolute Path Attempt (Security Guarded)
            if purified_input.startswith('/') or (len(purified_input) > 1 and purified_input[1] == ':'):
                working_path = self._restrict_to_sanctum(Path(purified_input))

            # 2. Relative Pivot (./ or ../)
            elif purified_input.startswith('.'):
                # Resolve relative to the script that spoke the intent
                working_path = self._restrict_to_sanctum((effective_rel_base / purified_input).resolve())

            # 3. Standard Indentation-Relative Path
            else:
                working_path = current_logical_parent
                # Split atoms: 'src/api' -> ['src', 'api']
                path_atoms = [a for a in purified_input.split('/') if a and a != '.']

                for i, atom in enumerate(path_atoms):
                    # [ASCENSION 11]: INDENTATION GRAVITY
                    # If this is not the last atom in a multi-segment path, 
                    # it is an implicit directory.
                    is_implicit_dir = i < (len(path_atoms) - 1)

                    working_path = working_path / atom

                    if is_implicit_dir:
                        self._push_to_stack(working_path, indent)

            # --- MOVEMENT IV: FINALITY VOW ---
            # If the original willed string ended in a slash, it's an explicit directory.
            if purified_input.endswith(('/', '\\')):
                self._push_to_stack(working_path, indent)

            # [ASCENSION 21]: RECORD THE SPATIAL DECISION
            self._log_trace(raw_path_str, indent, working_path)

            return working_path

    # =========================================================================
    # == RITE II: THE PURITY SIEVE                                           ==
    # =========================================================================

    def _purify_path_stream(self, raw: str) -> str:
        """
        [ASCENSION 2, 3, 4 & 7]: The Universal Geometric Purifier.
        """
        # 1. Forensic Matter Leak Detection
        # [THE CURE]: We block the strike if it contains code signatures.
        for pattern in self.MATTER_LEAK_SIGNATURES:
            if pattern.search(raw):
                raise ArtisanHeresy(
                    f"Geometric Paradox: Code fragment detected in path definition.",
                    details=f"The Gnostic Parser leaked matter into topography: '{raw.strip()}'",
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Verify indentation. Code must be indented under a path header."
                )

        # 2. Phantom Forest Sieve: Annihilate Tree-Art and Emojis
        clean = self.JUNK_PATTERN.sub('', raw)

        # 3. Normalize Unicode (NFKC) & Slashes
        clean = unicodedata.normalize('NFKC', clean.strip()).replace('\\', '/')

        # 4. Strip trailing colons (Common AI artifact)
        if clean.endswith(':') and not (len(clean) == 2 and clean[0].isalpha()):
            clean = clean[:-1]

        return clean.strip()

    def _restrict_to_sanctum(self, target: Path) -> Path:
        """
        [ASCENSION 6]: THE BOUNDARY WARD.
        Ensures the coordinate never escapes the ordained Axis Mundi.
        """
        try:
            abs_target = target.resolve()
            abs_root = self.root_path.resolve()

            # [STRIKE]: Adjudicate Containment
            common = os.path.commonpath([str(abs_root), str(abs_target)])
            if common != str(abs_root):
                Logger.warn(f"Spatial Breach Blocked: '{target}' attempted escape. Re-anchoring.")
                return abs_root
            return abs_target
        except (ValueError, Exception):
            return self.root_path

    def _push_to_stack(self, path: Path, indent: int):
        """Pushes a new strata onto the path stack with depth governance."""
        if len(self.path_stack) >= self.MAX_STRATA_DEPTH:
            raise ArtisanHeresy(
                f"Topological Exhaustion: Path depth exceeds limit of {self.MAX_STRATA_DEPTH}.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Flatten your blueprint structure. Deep nesting is an architectural sin."
            )

        # [ASCENSION 8]: CASE-RESONANCE CHECK
        self._scry_casing_collision(path)

        # Only push if it's a new coordinate
        if self.path_stack[-1][0] != path:
            self.path_stack.append((path, indent))

    def _scry_casing_collision(self, path: Path):
        """[ASCENSION 8]: Detects casing drift on case-insensitive substrates."""
        if not path.parent.exists(): return

        try:
            name_lower = path.name.lower()
            for existing in path.parent.iterdir():
                if existing.name.lower() == name_lower and existing.name != path.name:
                    Logger.warn(f"Casing Resonance Collision: '{path.name}' vs existing '{existing.name}'")
        except Exception:
            pass

    # =========================================================================
    # == RITE III: METABOLISM & NAVIGATION                                   ==
    # =========================================================================

    def re_anchor(self, new_root: Path):
        """
        =============================================================================
        == THE RITE OF RE-ANCHORING (V-Ω-DIMENSIONAL-SHIFT)                        ==
        =============================================================================
        """
        with self._lock:
            self.root_path = new_root.resolve()
            # Total Purgation of the stack
            self.path_stack = [(self.root_path, -1)]
            Logger.info(f"Hierophant re-anchored to: {self.root_path}")

    def get_current_dir(self) -> Path:
        """Returns the current path depth."""
        return self.path_stack[-1][0]

    def _log_trace(self, input_str: str, indent: int, resolved: Path):
        """[ASCENSION 21]: The Forensic Ledger Scribe."""
        try:
            rel_out = resolved.relative_to(self.root_path)
        except ValueError:
            rel_out = resolved

        self.trace_log.append({
            "ts": time.time_ns(),
            "in": input_str,
            "indent": indent,
            "out": str(rel_out).replace('\\', '/'),
            "merkle": hashlib.md5(str(resolved).encode()).hexdigest()[:8]
        })
        # Keep log metabolic mass capped
        if len(self.trace_log) > 500:
            self.trace_log.pop(0)

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_HIEROPHANT depth={len(self.path_stack)} root={self.root_path.name} status=RESONANT>"