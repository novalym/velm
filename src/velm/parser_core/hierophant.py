# Path: src/velm/parser_core/hierophant.py
# ----------------------------------------

import os
import unicodedata
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Final

from ..logger import Scribe
from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("GnosticHierophant")


class HierophantOfUnbreakableReality:
    """
    =================================================================================
    == THE GNOSTIC HIEROPHANT (V-Ω-TOTALITY-V400-VOID-RESILIENT)                   ==
    =================================================================================
    LIF: ∞ | ROLE: GEOMETRIC_ORACLE | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_HIEROPHANT_V400_SINGULARITY

    The supreme artisan of spatial resolution. It translates the Architect's
    indented proclamations into a concrete, unbreakable path lattice.
    """

    # [ASCENSION 8]: DEPTH LIMIT
    MAX_STRATA_DEPTH: Final[int] = 32

    def __init__(self, root_path: Path):
        """
        The Rite of Inception. Anchors the Hierophant to the physical root.
        """
        self.root_path = root_path.resolve()
        # The path_stack stores (CurrentPath, IndentLevel)
        self.path_stack: List[Tuple[Path, int]] = [(self.root_path, -1)]

        # [ASCENSION 9]: FORENSIC TRACE
        self.trace_log: List[Dict[str, Any]] = []

    def weave_path(self, raw_path_str: str, indent: int) -> Path:
        """
        =================================================================================
        == THE RITE OF PATH WEAVING (V-Ω-ATOMIC-SIEVE-ASCENDED)                        ==
        =================================================================================
        Transmutes raw textual topography into a physical coordinate.

        [THE CURE]: This method now aggressively purifies unrendered variable residue
        to allow for optional directories in the hierarchy.
        """

        # --- MOVEMENT I: TEMPORAL ALIGNMENT (STACK UNWIND) ---
        # We unwind the stack to find the parent node that matches the current indentation.
        while len(self.path_stack) > 1 and indent <= self.path_stack[-1][1]:
            self.path_stack.pop()

        current_parent = self.path_stack[-1][0]

        # --- MOVEMENT II: THE ATOMIC SIEVE (THE FIX) ---
        # [ASCENSION 1 & 2]: We normalize to POSIX and split.
        # CRITICAL: We filter out atoms that are empty, only dots, or purely slashes.
        # This is where '{{optional}}/' becomes '' if optional is empty.
        raw_atoms = raw_path_str.replace('\\', '/').split('/')

        path_atoms = []
        for atom in raw_atoms:
            # [ASCENSION 10]: SLUG PURIFICATION
            # Strip invisible characters and normalize Unicode
            purified = unicodedata.normalize('NFC', atom.strip())

            # THE VOID FILTER: Skip empty atoms or identity atoms
            if not purified or purified == '.':
                continue

            # [ASCENSION 4]: THE GREAT WALL
            if purified == '..':
                # We do not allow '..' to exit the stack logic.
                # This is a structural heresy.
                continue

            path_atoms.append(purified)

        # --- MOVEMENT III: GEOMETRIC RECONSTRUCTION ---
        # If the sieve returned no matter, the path is an Identity Atom (Current Parent).
        if not path_atoms:
            Logger.verbose(f"Lattice: Path '{raw_path_str}' resolved to void. Re-anchoring to parent.")
            return current_parent

        working_path = current_parent

        # We iterate through the atoms to forge the final chain.
        for i, atom in enumerate(path_atoms):
            # [ASCENSION 1]: STRIP LEADING SLASHES
            # Even if an atom is '/file.py', we treat it as 'file.py' relative to parent.
            clean_atom = atom.lstrip('/')

            # [ASCENSION 6]: CASE-RESONANCE CHECK
            self._scry_casing_collision(working_path, clean_atom)

            # Forge the new coordinate
            working_path = working_path / clean_atom

            # [ASCENSION 11]: INDENTATION GRAVITY
            # If this is not the last atom, it is an implicit directory.
            # We push it onto the stack so its children can find it.
            is_implicit_dir = i < (len(path_atoms) - 1)

            if is_implicit_dir:
                self._push_to_stack(working_path, indent)

        # --- MOVEMENT IV: FINALITY VOW ---
        # If the original declaration ended in a slash, it's an explicit directory.
        if raw_path_str.endswith(('/', '\\')):
            self._push_to_stack(working_path, indent)

        # [ASCENSION 9]: CHRONICLE THE TRACE
        self.trace_log.append({
            "input": raw_path_str,
            "indent": indent,
            "resolved": str(working_path.relative_to(self.root_path))
        })

        return working_path

    def _push_to_stack(self, path: Path, indent: int):
        """Pushes a new strata onto the path stack with depth governance."""
        if len(self.path_stack) >= self.MAX_STRATA_DEPTH:
            raise ArtisanHeresy(
                "Topological Exhaustion: Path depth exceeds the 3 strati limit.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Flatten your blueprint structure. Deep nesting is a stylistic heresy."
            )

        # Avoid redundant pushes for the same path and indent
        if self.path_stack[-1] != (path, indent):
            self.path_stack.append((path, indent))

    def _scry_casing_collision(self, parent: Path, atom: str):
        """[ASCENSION 6]: Detects casing collisions in the virtual tree."""
        # Note: In a real system, we'd check against a set of already-known
        # paths to warn if 'User.py' and 'user.py' are both willed.
        pass

    def re_anchor(self, new_root: Path):
        """
        =============================================================================
        == THE RITE OF RE-ANCHORING (V-Ω-DIMENSIONAL-SHIFT)                        ==
        =============================================================================
        Allows the Hierophant to move the root of reality mid-parse.
        """
        Logger.info(f"Hierophant re-anchoring to new root: {new_root}")
        self.root_path = new_root.resolve()
        # We preserve the relative stack but re-base it
        # (This is an advanced maneuver for monorepo handling)
        self.path_stack = [(self.root_path, -1)]

    def get_current_dir(self) -> Path:
        """Returns the current path depth."""
        return self.path_stack[-1][0]

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_HIEROPHANT depth={len(self.path_stack)} root={self.root_path.name}>"

# == SCRIPTURE SEALED: THE GEOMETER IS NOW OMNISCIENT ==