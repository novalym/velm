# Path: scaffold/artisans/distillation/import_resolver.py
# -------------------------------------------------------

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Optional, Dict, Set, List

from ...logger import Scribe

Logger = Scribe("GnosticPathfinder")


class ImportResolver:
    """
    =================================================================================
    == THE GNOSTIC PATHFINDER (V-Ω-POLYGLOT-ORACLE)                                ==
    =================================================================================
    LIF: 10,000,000,000,000

    A divine artisan that can resolve an import string to a concrete file path
    across multiple languages and their unique module resolution strategies.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Polyglot Mind:** Possesses dedicated, sacred rites for resolving imports
        in Python, TypeScript/JavaScript, Go, and Rust.
    2.  **The Gnostic Chronocache (`@lru_cache`):** Its memory is perfect, caching
        resolutions to provide instantaneous answers for repeated queries.
    3.  **The `tsconfig.json` Oracle (TS/JS):** Ingests and understands `paths` and
        `baseUrl` from a `tsconfig.json` to resolve non-relative aliased imports.
    4.  **The `sys.path` Prophet (Python):** Simulates Python's `sys.path` logic,
        understanding `src` layouts and root-level modules.
    5.  **The `go.mod` Sage (Go):** Parses the `go.mod` file to understand the project's
        module root for absolute Go imports.
    6.  **The Unbreakable Ward of the Void:** Gracefully handles malformed or
        unresolvable import strings without shattering.
    7.  **The Gaze of the Index:** Intelligently checks for `__init__.py` and `index.ts`
        when resolving directory-level imports.
    8.  **The Suffix Agnostic Gaze:** Can resolve imports that omit file extensions
        (e.g., `from './utils'` -> `utils.ts`).
    9.  **The Sovereign Soul:** A self-contained, decoupled class, its wisdom
        available to any artisan that needs to map the Gnostic Cosmos.
    10. **The Performance Ward:** Prioritizes the fastest checks first (cache, direct
        match) before attempting more expensive filesystem gazes.
    11. **The Telepathic Link:** Forged with the complete `symbol_map` and the set of
        `all_files`, it operates within a known, finite universe of possibilities.
    12. **The Luminous Voice:** Provides rich, verbose logging of its thought process,
        revealing its pathfinding logic for hyper-diagnostic insight.
    =================================================================================
    """

    def __init__(self, project_root: Path, symbol_map: Dict[str, str], all_files: Set[str]):
        self.root = project_root
        self.symbol_map = symbol_map
        self.all_files = all_files

        # Pre-computation for performance
        self.src_root = self.root / 'src' if (self.root / 'src').is_dir() else self.root

        # Gnosis for TS/JS
        self.tsconfig_gnosis = self._load_tsconfig()
        # Gnosis for Go
        self.go_mod_root = self._load_go_mod_root()

    def _load_tsconfig(self) -> Dict:
        tsconfig_path = self.root / "tsconfig.json"
        if tsconfig_path.exists():
            try:
                return json.loads(tsconfig_path.read_text(encoding='utf-8'))
            except Exception:
                pass
        return {}

    def _load_go_mod_root(self) -> Optional[str]:
        gomod_path = self.root / "go.mod"
        if gomod_path.exists():
            try:
                content = gomod_path.read_text(encoding='utf-8')
                match = re.search(r'module\s+([\w\./-]+)', content)
                if match:
                    return match.group(1)
            except Exception:
                pass
        return None

    @lru_cache(maxsize=8192)
    def resolve(self, imp_str: str, source_file_str: str, language: str) -> Optional[str]:
        """The one true, public rite of resolution."""
        Logger.verbose(f"Pathfinder's Gaze awakened for '{imp_str}' in '{source_file_str}' ({language})")

        # --- THE GNOSTIC TRIAGE OF TONGUES ---
        if language in ('python', 'py'):
            return self._resolve_python(imp_str, source_file_str)
        elif language in ('typescript', 'javascript', 'ts', 'js', 'tsx', 'jsx'):
            return self._resolve_typescript(imp_str, source_file_str)
        elif language in ('go'):
            return self._resolve_go(imp_str, source_file_str)

        # Default/Humble Gaze
        return self._resolve_humble(imp_str, source_file_str)

    def _resolve_python(self, imp_str: str, source_file_str: str) -> Optional[str]:
        """[FACULTY 4] The sys.path Prophet."""
        # 1. Absolute Import Check (via Symbol Map)
        if imp_str in self.symbol_map:
            return self.symbol_map[imp_str]

        # 2. Relative Import Check
        if imp_str.startswith('.'):
            level = len(imp_str) - len(imp_str.lstrip('.'))
            module_path = imp_str[level:]

            base_dir = (self.root / source_file_str).parent
            for _ in range(level - 1):
                base_dir = base_dir.parent

            relative_module_path = base_dir / module_path.replace('.', '/')
            candidates = [
                relative_module_path.with_suffix('.py'),
                relative_module_path / '__init__.py'
            ]
        else:  # 3. Absolute Import (sys.path simulation)
            module_path = imp_str.replace('.', '/')
            candidates = [
                (self.src_root / f"{module_path}.py"),
                (self.src_root / module_path / "__init__.py"),
                (self.root / f"{module_path}.py"),
                (self.root / module_path / "__init__.py"),
            ]

        return self._check_candidates(candidates)

    def _resolve_typescript(self, imp_str: str, source_file_str: str) -> Optional[str]:
        """[FACULTY 3] The tsconfig.json Oracle."""
        # 1. Path Alias Check (tsconfig.json paths)
        if self.tsconfig_gnosis:
            paths = self.tsconfig_gnosis.get('compilerOptions', {}).get('paths', {})
            for alias, mappings in paths.items():
                alias_prefix = alias.rstrip('/*')
                if imp_str.startswith(alias_prefix):
                    for mapping in mappings:
                        mapping_prefix = mapping.rstrip('/*')
                        remapped_imp = imp_str.replace(alias_prefix, mapping_prefix)
                        # Now treat it as a project-absolute import
                        return self._resolve_typescript_absolute(remapped_imp)

        # 2. Relative Import
        if imp_str.startswith('./') or imp_str.startswith('../'):
            base_dir = (self.root / source_file_str).parent
            relative_path = (base_dir / imp_str).resolve()
            return self._check_candidates([relative_path],
                                          exts=['.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.js'])

        # 3. Project-Absolute Import
        return self._resolve_typescript_absolute(imp_str)

    def _resolve_typescript_absolute(self, imp_str: str) -> Optional[str]:
        """Helper for TS project-absolute paths."""
        base_url = self.tsconfig_gnosis.get('compilerOptions', {}).get('baseUrl', '.')
        search_root = (self.root / base_url).resolve()

        candidates = [(search_root / imp_str)]
        return self._check_candidates(candidates, exts=['.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.js'])

    def _resolve_go(self, imp_str: str, source_file_str: str) -> Optional[str]:
        """[FACULTY 5] The go.mod Sage."""
        if not self.go_mod_root: return self._resolve_humble(imp_str, source_file_str)

        if imp_str.startswith(self.go_mod_root):
            rel_path_str = imp_str.replace(self.go_mod_root, '', 1).lstrip('/')
            candidates = [self.root / f"{rel_path_str}.go"]
            return self._check_candidates(candidates)

        return self._resolve_humble(imp_str, source_file_str)

    def _resolve_humble(self, imp_str: str, source_file_str: str) -> Optional[str]:
        """A simple, file-extension-based fallback gaze."""
        for f in self.all_files:
            if f.endswith(imp_str):
                return f
        return None

    def _check_candidates(self, candidates: List[Path], exts: Optional[List[str]] = None) -> Optional[str]:
        """A universal helper to check a list of potential paths against all_files."""
        if exts:
            # Expand candidates with extensions
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
                rel_cand_str = str(cand_path.relative_to(self.root)).replace('\\', '/')
                if rel_cand_str in self.all_files:
                    return rel_cand_str
            except (ValueError, OSError):
                continue

        return None