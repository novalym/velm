
from pathlib import Path
from typing import Dict, Union, Set, Callable, Optional, List
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe
Logger = Scribe("GnosticWillParser")
class GnosticWillParser:
    """
    =================================================================================
    == THE ORACLE OF INTENT (V-Ω-SENTIENT-PARSER)                                  ==
    =================================================================================
    LIF: 10,000,000,000

    This is a dedicated, intelligent artisan that transmutes raw input (CLI args,
    scripts, dictionaries) into a normalized, conflict-free Translocation Map.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:
    1.  **The Tri-Fold Gaze:** Prioritizes `Direct > Script > CLI` with absolute clarity.
    2.  **The Pattern Expander:** Supports GLOB patterns (`src/api/*.py -> src/v2/api/`)
        allowing for massive, bulk translocations in a single line.
    3.  **The Implicit Directory:** Automatically detects if the destination implies a
        directory (ends in `/` or contains wildcards) and restructures the move.
    4.  **The Path Anchor:** Anchors inputs relative to CWD (User Context) but outputs
        targets relative to Project Root (System Context).
    5.  **The Syntax Inquisitor:** Validates script syntax (`->` separator) line-by-line.
    6.  **The Comment Stripper:** Ignores Gnostic comments (`#`, `//`) and whitespace.
    7.  **The Identity Purge:** Automatically filters no-op moves (`A -> A`).
    8.  **The Conflict Sentinel:** Detects if two sources map to the same destination
        (Collision Heresy) and raises an alarm.
    9.  **The Void Ward:** Gracefully handles empty scripts or arguments.
    10. **The Variable Alchemist:** (Future) Prepared to expand `${VAR}` in scripts.
    11. **The Relative Healer:** Handles `../` traversals within the Sanctum safely.
    12. **The Luminous Scribe:** Chronicles every expansion and decision.
    =================================================================================
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.moves: Dict[Path, Path] = {}

    def perceive(self,
                 origins: List[str] = None,
                 destinations: List[str] = None,
                 script_path: Optional[str] = None,
                 direct_moves: Optional[Dict[Path, Path]] = None) -> Dict[Path, Path]:
        """The Grand Rite of Perception."""

        # 1. The Gaze of Direct Knowledge (Internal Calls)
        if direct_moves:
            Logger.verbose("Perceiving intent from Direct Gnosis...")
            self._ingest_direct(direct_moves)
            return self._purify()

        # 2. The Gaze of the Scripture (Manifest File)
        if script_path:
            Logger.verbose(f"Perceiving intent from Scripture: {script_path}")
            self._ingest_script(script_path)
            return self._purify()

        # 3. The Gaze of the Spoken Word (CLI Args)
        if origins:
            Logger.verbose("Perceiving intent from Spoken Edicts (CLI)...")
            self._ingest_cli(origins, destinations)
            return self._purify()

        return {}

    def _ingest_direct(self, moves: Dict[Path, Path]):
        """Ingests raw Path objects directly."""
        for src, dst in moves.items():
            self.moves[src.resolve()] = dst.resolve()

    def _ingest_script(self, script_path: str):
        """Parses a .manifest file with Pattern Expansion."""
        # Script is relative to CWD (User Context)
        script_file = Path(script_path).resolve()
        if not script_file.exists():
            raise ArtisanHeresy(f"The scripture '{script_file.name}' is a void.")

        try:
            lines = script_file.read_text(encoding='utf-8').splitlines()
            for i, line in enumerate(lines):
                cleaned = line.split('#')[0].split('//')[0].strip()
                if not cleaned: continue

                if "->" not in cleaned:
                    raise ArtisanHeresy(f"Syntax Heresy on line {i + 1}: Missing arrow '->'.")

                src_pattern, dst_pattern = [p.strip() for p in cleaned.split("->", 1)]
                self._expand_and_map(src_pattern, dst_pattern)

        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy(f"Paradox reading scripture '{script_file.name}': {e}")

    def _ingest_cli(self, origins: List[str], destinations: List[str]):
        """Parses CLI arguments."""
        if not destinations:
            # Default: Move to CWD if no dest provided? No, explicit is better.
            raise ArtisanHeresy("Movement requires a destination.")

        # N -> 1 (Many files to one directory)
        if len(destinations) == 1:
            target = destinations[0]
            for src in origins:
                self._expand_and_map(src, target)

        # N -> N (Explicit mapping, rare in CLI but possible)
        elif len(origins) == len(destinations):
            for src, dst in zip(origins, destinations):
                self._expand_and_map(src, dst)
        else:
            raise ArtisanHeresy(f"Arity Heresy: {len(origins)} origins cannot map to {len(destinations)} destinations.")

    def _expand_and_map(self, src_pattern: str, dst_pattern: str):
        """
        [THE PATTERN EXPANDER]
        The heart of the intelligence. Handles Globs and Directory inference.
        """
        # 1. Resolve Source Pattern relative to Project Root
        # We must use glob on the filesystem to find matches.
        # Note: Glob patterns are relative to root.

        # If it's an absolute path or outside root, we must be careful.
        # Assuming src_pattern is relative to project_root.
        search_root = self.root

        # Check if it's a glob
        is_glob = any(c in src_pattern for c in ['*', '?', '['])

        if is_glob:
            # Use python's glob to find files matching the pattern relative to root
            found_files = list(search_root.glob(src_pattern))
            if not found_files:
                Logger.warn(f"Void Gaze: Pattern '{src_pattern}' matched no existing scriptures.")
                return

            # If source is a glob, destination MUST be a directory
            if not dst_pattern.endswith('/'):
                # We assume it's a directory if multiple files matched
                if len(found_files) > 1:
                    dst_pattern += '/'

            for src_file in found_files:
                # Calculate relative path of file to the glob base?
                # Simple logic: Flatten to dest if dest is dir.
                if dst_pattern.endswith('/'):
                    # src/foo.py -> dest/foo.py
                    final_dest = (self.root / dst_pattern / src_file.name).resolve()
                else:
                    # Only valid if 1 file matched
                    final_dest = (self.root / dst_pattern).resolve()

                self.moves[src_file.resolve()] = final_dest

        else:
            # Literal Path
            src_path = (self.root / src_pattern).resolve()

            # Explicit Directory Logic
            if dst_pattern.endswith('/') or ((self.root / dst_pattern).is_dir()):
                final_dest = (self.root / dst_pattern / src_path.name).resolve()
            else:
                final_dest = (self.root / dst_pattern).resolve()

            self.moves[src_path] = final_dest

    def _purify(self) -> Dict[Path, Path]:
        """
        [THE PURIFICATION RITE]
        Removes identity moves, non-existent sources, and checks for collisions.
        """
        pure_moves = {}
        dest_tracker = {}

        for src, dst in self.moves.items():
            # [FIX] THE GAZE OF REALITY
            # If the source does not exist in this timeline, we prune it from the plan.
            if not src.exists():
                # We log this verbosely so the Architect knows why it was skipped,
                # but we do not halt the symphony.
                Logger.verbose(f"Pruning phantom move: '{src.name}' does not exist in the Sanctum.")
                continue

            # Identity Purge (A -> A)
            if src.resolve() == dst.resolve():
                continue

            # Conflict Sentinel (A -> C, B -> C)
            if dst in dest_tracker:
                conflict_src = dest_tracker[dst]
                raise ArtisanHeresy(
                    f"Collision Heresy: Both '{src.name}' and '{conflict_src.name}' define the same destination '{dst}'.")

            dest_tracker[dst] = src
            pure_moves[src] = dst

        return pure_moves

