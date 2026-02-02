# Path: core/resolvers/pathfinder.py
# ----------------------------------

"""
=================================================================================
== THE GNOSTIC PATHFINDER (V-Ω-UNIVERSAL-ORACLE-FIXED)                         ==
=================================================================================
LIF: 10,000,000,000,000

A divine artisan that can resolve an import string to a concrete file path
across multiple languages and their unique module resolution strategies.

[THE FIX]: Enforces strict POSIX normalization when checking candidate paths
against the global file set, ensuring cross-platform harmony.
"""
from pathlib import Path
from typing import Dict, Set, Optional, List
from functools import lru_cache

from ...logger import Scribe
from ...artisans.translocate_core.resolvers.python.pathfinder import PythonPathfinder
from ...artisans.translocate_core.resolvers.typescript.pathfinder import TSPathfinder
from ...artisans.translocate_core.resolvers.javascript.pathfinder import JSPathfinder
from ...artisans.translocate_core.resolvers.go.pathfinder import GoPathfinder
from ...artisans.translocate_core.resolvers.rust.pathfinder import RustPathfinder
from ...artisans.translocate_core.resolvers.ruby.pathfinder import RubyPathfinder

Logger = Scribe("GnosticPathfinder")


class GnosticPathfinder:
    """The Universal Oracle of Paths."""

    def __init__(self, project_root: Path, symbol_map: Dict[str, str], all_files: Set[str]):
        self.root = project_root.resolve()
        self.symbol_map = symbol_map
        self.all_files = all_files

        # The Pantheon of Pathfinders
        self.resolvers = {
            "python": PythonPathfinder(self.root, {k: self.root / v for k, v in symbol_map.items()}),
            "typescript": TSPathfinder(self.root),
            "javascript": JSPathfinder(self.root),
            "go": GoPathfinder(self.root),
            "rust": RustPathfinder(self.root),
            "ruby": RubyPathfinder(self.root),
        }
        Logger.verbose(f"Gnostic Pathfinder consecrated with {len(self.resolvers)} language specialists.")

    @lru_cache(maxsize=8192)
    def resolve(self, imp_str: str, source_file_str: str, language: str) -> Optional[str]:
        """
        The Grand Rite of Gnostic Triage.
        Delegates the Gaze to the correct specialist.
        """
        # Normalize language aliases
        lang_map = {
            "py": "python", "ts": "typescript", "tsx": "typescript",
            "js": "javascript", "jsx": "javascript", "rs": "rust", "rb": "ruby"
        }
        lang_key = lang_map.get(language, language)
        specialist = self.resolvers.get(lang_key)

        if not specialist:
            return None

        try:
            resolved_path: Optional[Path] = None
            source_path_abs = self.root / source_file_str

            if lang_key == "python":
                from ...artisans.translocate_core.resolvers.python.contracts import DetectedImport
                level = len(imp_str) - len(imp_str.lstrip('.'))
                module_parts = imp_str[level:].split('.')
                module = ".".join(module_parts[:-1]) if len(module_parts) > 1 else None
                name = module_parts[-1]
                imp_vessel = DetectedImport(line_num=0, module=module, name=name, alias=None, level=level,
                                            is_wildcard=False)
                resolved_path = specialist.resolve_origin(imp_vessel, source_path_abs)

            elif lang_key == "go":
                resolved_path = specialist.resolve_file_path(imp_str)

            elif lang_key == "rust":
                resolved_path = specialist.module_to_file(imp_str)

            elif lang_key == "ruby":
                kind = 'relative' if imp_str.startswith('.') else 'absolute'
                resolved_path = specialist.resolve_origin(imp_str, source_path_abs, kind)

            elif lang_key in ("javascript", "typescript"):
                resolved_path = specialist.resolve_absolute_path(source_path_abs, imp_str)

            if resolved_path:
                return self._check_candidates([resolved_path])

            return None

        except Exception as e:
            Logger.warn(f"Pathfinder's Gaze for '{imp_str}' faltered in '{source_file_str}'. Paradox: {e}")
            return None

    def _check_candidates(self, candidates: List[Path], exts: Optional[List[str]] = None) -> Optional[str]:
        """
        A universal helper to check a list of potential paths against all_files.
        [THE FIX] Ensures strict POSIX normalization relative to root.
        """
        if exts:
            expanded_candidates = []
            for cand in candidates:
                for ext in exts:
                    if ext.startswith('/'):  # index.ts
                        expanded_candidates.append(cand / ext.lstrip('/'))
                    else:
                        expanded_candidates.append(cand.with_suffix(ext))
            candidates = expanded_candidates

        for cand_path in candidates:
            try:
                # Ensure we are checking absolute paths
                abs_cand = cand_path.resolve()

                # Must be relative to project root
                if not abs_cand.is_relative_to(self.root):
                    continue

                # Normalize to POSIX string
                rel_cand_str = abs_cand.relative_to(self.root).as_posix()

                if rel_cand_str in self.all_files:
                    return rel_cand_str

            except (ValueError, OSError):
                continue

        return None

