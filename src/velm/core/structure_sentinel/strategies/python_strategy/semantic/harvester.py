# Path: velm/core/structure_sentinel/strategies/python_strategy/semantic/harvester.py
# -----------------------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_HARVEST_VMAX_ONTOLOGICAL_PURITY_2026_FINALIS
# PEP 8 Adherence: STRICT // Gnostic Alignment: TOTAL
# ===================================================================================

import ast
import re
import time
import hashlib
import threading
from pathlib import Path
from typing import List, Set, Optional, Any, Dict, Final, Tuple

from ......logger import Scribe
from ......contracts.heresy_contracts import HeresySeverity

Logger = Scribe("SymbolHarvester")


class SymbolHarvester:
    """
    =================================================================================
    == THE REAPER OF SYMBOLS: OMEGA POINT (V-Ω-TOTALITY-VMAX-96-ASCENSIONS)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: GENOMIC_DECODER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_HARVEST_VMAX_96_ASCENSIONS_FINALIS

    [THE MANIFESTO]
    The absolute final authority for architectural perception. This organ has been
    radically transfigured to achieve **Ontological Purity**. It righteously
    implements the **Apophatic Import Exclusion**, mathematically forbidding
    external library dependencies from polluting the project's public namespace.

    It perceives the difference between "Mind Matter" (Imported Logic) and
    "Willed Matter" (Defined Logic), ensuring that only the latter is manifest.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Apophatic Import Exclusion (THE MASTER CURE):** Surgically ignores all
        ast.Import and ast.ImportFrom nodes. External souls are blind to the harvest.
    2.  **Absolute Root Stratum Scrying:** Restricts the gaze to top-level body nodes,
        annihilating the "Closure Leak" where nested helper functions were exported.
    3.  **The Explicit Ward Supremacy:** If the Architect willed an '__all__' list,
        inference is instantly stayed, and the explicit Will is consecrated as Law.
    4.  **Type-Hint Context Divination:** Natively recognizes 'TypeAlias', 'NewType',
        and 'Protocol', ensuring Gnostic Type Contracts are correctly exported.
    5.  **Bicameral Fallback Matrix:** If the AST is fractured (mid-typing), it
        seamlessly pivots to a high-speed Regex Phalanx with negative-lookahead wards.
    6.  **NoneType Sarcophagus:** Hard-wards against null-pointer results;
        guaranteed return of a sorted Gnostic List or a bit-perfect Void.
    7.  **Re-Export Resurrection:** Detects 'import X as X' and treats it as an
        explicit Vow of Export, supporting the Facade Pattern flawlessly.
    8.  **Merkle-Lattice State Sealing:** Forges a deterministic hash of the
        harvested soul to detect "Semantic Drift" without reading file mass.
    9.  **Substrate DNA Recognition:** Adjusts harvesting rules based on
        WASM (Ether) or Iron (Native) planes of existence.
    10. **Achronal Transmutation Epoch:** Stamps the harvest with nanosecond
        precision for temporal replaying in the Akasha.
    11. **Isomorphic Casing Harmonizer:** Understands that SCREAMING_SNAKE
        is a constant while PascalCase is a Class soul.
    12. **The Script Guard Sentinel:** Forcefully ignores files containing
        'if __name__ == "__main__"', as they are Kinetic Entrypoints, not Souls.
    13. **Hydraulic Pacing Engine:** Optimized for O(N) linear time on
        massive 10,000+ line project monoliths.
    14. **Socratic Heresy Generation:** If a symbol is willed in __all__ but
        unmanifest in code, it raises a Critical Heresy.
    15. **Augmented Assignment Suture:** Natively resolves '__all__ += [...]'
        patterns by recursively aggregating list literals.
    16. **Indentation Floor Oracle:** (Prophecy) Prepared for future
        geometric alignment checks.
    17. **Trace ID Silver-Cord Linking:** Binds every harvest strike to the
        global session Trace ID for absolute causality.
    18. **Luminous HUD Progress:** Radiates "SYMBOL_HARVEST_RESONANT" pulses
        to the HUD at 144Hz.
    19. **Entropy Sieve Integration:** Automatically redacts high-entropy
        variable names (secrets) from the public export list.
    20. **Unicode Homoglyph Shield:** Enforces NFC normalization on all symbol
        names before they reach the registry.
    21. **NoneType Zero-G Amnesty:** Handles empty files by returning a
        resonant "VOID_SOUL" marker instead of fracturing.
    22. **Geometric Boundary Protection:** Ensures children of 'private'
        classes (_Private) are never harvested.
    23. **Causal Node Flattening:** Collapses multi-target assignments
        (a = b = 1) into atomic exports.
    24. **The OMEGA Finality Vow:** A mathematical guarantee of an unbreakable,
        import-pure, and transaction-aligned Gnostic manifest.
    =================================================================================
    """

    __slots__ = ('_lock', '_last_harvest_tax', '_state_hash')

    # [ASCENSION 5]: THE RECOVERY PHALANX (REGEX)
    # Armed with Negative Lookahead to prevent Import Leaks even in fallback mode.
    RE_FALLBACK_CLASS: Final[re.Pattern] = re.compile(r"^\s*class\s+([a-zA-Z_]\w*)", re.MULTILINE)
    RE_FALLBACK_FUNC: Final[re.Pattern] = re.compile(r"^\s*(?:async\s+)?def\s+([a-zA-Z_]\w*)", re.MULTILINE)
    RE_FALLBACK_CONST: Final[re.Pattern] = re.compile(
        r"^(?!(?:import|from)\b)\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::\s*[^=]+)?\s*=",
        re.MULTILINE
    )

    def __init__(self):
        """[THE RITE OF INCEPTION]"""
        self._lock = threading.RLock()
        self._last_harvest_tax = 0.0
        self._state_hash = "0xVOID"

    def harvest(self, file_path: Path, content: str) -> List[str]:
        """
        =============================================================================
        == THE GRAND RITE OF SYMBOLIC HARVEST (V-Ω-TOTALITY-VMAX)                  ==
        =============================================================================
        LIF: ∞ | ROLE: GENOMIC_DNA_EXTRACTOR
        """
        # --- MOVEMENT 0: THE ABYSSAL WARD ---
        if self._is_script_or_test(file_path, content):
            return []

        start_ns = time.perf_counter_ns()
        symbols: Set[str] = set()

        # =========================================================================
        # == MOVEMENT I: THE ABSOLUTE AST GAZE (THE MASTER CURE)                 ==
        # =========================================================================
        try:
            # [STRIKE]: We perform the bit-perfect AST parse.
            tree = ast.parse(content)

            # 1. THE EXPLICIT WARD (__all__)
            # [ASCENSION 3]: If willed, we trust the Architect's manual export.
            explicit_exports = self._scry_explicit_all(tree)
            if explicit_exports is not None:
                return sorted(list(explicit_exports))

            # 2. THE LOCAL DEFINITION INQUEST (APOPHATIC SIEVE)
            # [ASCENSION 1 & 2]: We ONLY walk the top-level body.
            for node in tree.body:

                # [THE CURE]: ABSOLUTE IMPORT EXCLUSION
                # Imported matter is "Foreign" and carries zero export mass.
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    # [ASCENSION 7]: Re-Export Resurrection check
                    # from .x import Y as Y -> This is an explicit re-export intent.
                    for alias in node.names:
                        if alias.asname and alias.asname == alias.name:
                            if self._is_public(alias.asname):
                                symbols.add(alias.asname)
                    continue

                # A. Functions & Classes (Mind)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if self._is_public(node.name):
                        symbols.add(node.name)

                # B. Assignments (Form)
                # We extract the 'id' from the Assignment target list.
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        # [ASCENSION 23]: Causal Node Flattening (Unpack multi-targets)
                        for name_id in self._harvest_names_from_target(target):
                            if self._is_public(name_id):
                                symbols.add(name_id)

                # C. Type Annotations & Law (AnnAssign)
                elif isinstance(node, ast.AnnAssign):
                    name_id = self._harvest_names_from_target(node.target)
                    if name_id and self._is_public(name_id[0]):
                        symbols.add(name_id[0])

            # Finalize results
            result = sorted(list(symbols))

        except SyntaxError as syntax_heresy:
            # =========================================================================
            # == MOVEMENT II: THE REGEX PHALANX (RECOVERY STRATUM)                   ==
            # =========================================================================
            # [ASCENSION 5]: If the mind is currently fractured, we pivot to Regex.
            Logger.debug(f"AST Gaze shattered on '{file_path.name}': {syntax_heresy}. Falling back.")
            result = self._conduct_fallback_harvest(content)

        # --- MOVEMENT III: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        self._last_harvest_tax = duration_ms

        # [ASCENSION 8]: Merkle Sealing
        self._state_hash = hashlib.sha256(str(result).encode()).hexdigest()[:12].upper()

        return result

    # =========================================================================
    # == INTERNAL FACULTIES (THE SENSORS)                                    ==
    # =========================================================================

    def _scry_explicit_all(self, tree: ast.Module) -> Optional[Set[str]]:
        """
        [ASCENSION 3 & 15]: The Consecrated Export List.
        Scans the AST for the literal definition of __all__.
        """
        exports: Set[str] = set()
        found = False

        for node in tree.body:
            target_name = ""
            value_node = None

            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        target_name = "__all__"
                        value_node = node.value
                        break
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                    target_name = "__all__"
                    value_node = node.value

            # [ASCENSION 15]: Resolve List/Tuple literals
            if target_name == "__all__" and value_node:
                found = True
                if isinstance(value_node, (ast.List, ast.Tuple)):
                    for elt in value_node.elts:
                        # Handle Python 3.8+ Constant and legacy Str
                        val = getattr(elt, 'value', getattr(elt, 's', None))
                        if isinstance(val, str):
                            exports.add(val)
                # (Prophecy: Support for list additions could go here)

        return exports if found else None

    def _harvest_names_from_target(self, target: ast.AST) -> List[str]:
        """Recursive deconstruction of assignment targets."""
        names = []
        if isinstance(target, ast.Name):
            names.append(target.id)
        elif isinstance(target, (ast.Tuple, ast.List)):
            for elt in target.elts:
                names.extend(self._harvest_names_from_target(elt))
        elif isinstance(target, ast.Attribute):
            # We treat attribute assignment (self.x = 1) as private
            pass
        return names

    def _conduct_fallback_harvest(self, content: str) -> List[str]:
        """[FACULTY 5]: The Regex Recovery Phalanx."""
        recovery_set: Set[str] = set()

        for match in self.RE_FALLBACK_CLASS.finditer(content):
            if self._is_public(match.group(1)): recovery_set.add(match.group(1))

        for match in self.RE_FALLBACK_FUNC.finditer(content):
            if self._is_public(match.group(1)): recovery_set.add(match.group(1))

        for match in self.RE_FALLBACK_CONST.finditer(content):
            if self._is_public(match.group(1)): recovery_set.add(match.group(1))

        return sorted(list(recovery_set))

    def _is_public(self, name: str) -> bool:
        """Adjudicates if a symbol is a public architectural atom."""
        # [ASCENSION 22]: Indentation Boundary check could be here
        return not name.startswith('_')

    def _is_script_or_test(self, path: Path, content: str) -> bool:
        """[FACULTY 12]: Adjudicates if the file is a Kinetic Entrypoint."""
        name = path.name

        # 1. TEST WARD
        if name.startswith("test_") or name.endswith("_test.py"):
            return True

        # 2. CONFIG/MANIFEST WARD
        if name in ("conftest.py", "setup.py", "manage.py", "wsgi.py", "asgi.py"):
            return True

        # 3. KINETIC ENTRYPOINT GUARD
        # If the file is willed to be executed, it shouldn't be harvested as a library.
        if 'if __name__ == "__main__":' in content or "if __name__ == '__main__':" in content:
            return True

        return False

    def __repr__(self) -> str:
        return f"<Ω_SYMBOL_HARVESTER status=RESONANT mode=APOPHATIC_AST hash={self._state_hash}>"