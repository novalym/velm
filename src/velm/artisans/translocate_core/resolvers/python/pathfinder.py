# Path: scaffold/artisans/translocate_core/resolvers/python/pathfinder.py
# -----------------------------------------------------------------------

import os
from pathlib import Path
from typing import Optional, Dict

from .....logger import Scribe

Logger = Scribe("PythonPathfinder")


class PythonPathfinder:
    """
    =================================================================================
    == THE GEOMETRICIAN OF THE SERPENT (V-Ω-MODULE-AWARE-ULTIMA)                   ==
    =================================================================================
    LIF: ∞

    The Sovereign Calculator of Import Paths. It transmutes physical filesystem
    relationships into the abstract 'dot' notation of the Python import system.

    It possesses the faculty of **Module Awareness**, ensuring that imports point
    precisely to the scripture (file), not just the sanctum (directory), unless
    the scripture is an `__init__.py`.
    """

    def __init__(self, project_root: Path, symbol_map: Dict[str, Path]):
        self.root = project_root.resolve()
        self.symbol_map = symbol_map

        # [THE FIX] Intelligent Reverse Map Construction
        self.reverse_symbol_map = {}

        for symbol, path in symbol_map.items():
            abs_path = path.resolve()

            # If we haven't seen this path, take the symbol
            if abs_path not in self.reverse_symbol_map:
                self.reverse_symbol_map[abs_path] = symbol
                continue

            current_best = self.reverse_symbol_map[abs_path]

            # Heuristic: Prefer symbols with dots (modules) over simple names
            if '.' in symbol and '.' not in current_best:
                self.reverse_symbol_map[abs_path] = symbol
            # Heuristic: Prefer longer names if both have dots (more specific)
            elif '.' in symbol and len(symbol) > len(current_best):
                self.reverse_symbol_map[abs_path] = symbol
            # Heuristic: Prefer symbols that match the file stem
            elif symbol.endswith(abs_path.stem) and not current_best.endswith(abs_path.stem):
                self.reverse_symbol_map[abs_path] = symbol

        self.src_root: Path = next(
            (p for p in [self.root / 'src', self.root / 'app'] if p.is_dir()),
            self.root
        )

        # Logger.info(f"[DIAGNOSTIC] Reverse Map Sample: {list(self.reverse_symbol_map.values())[:5]}")

    def resolve_origin(self, imp: 'DetectedImport', context_file: Path) -> Optional[Path]:
        """
        Determines the absolute file path that an import refers to.
        """
        import_desc = f"{'.' * imp.level}{imp.module or ''}.{imp.name}"
        log_prefix = f"[PATHFINDER] '{import_desc}' (Lvl: {imp.level}) in {context_file.name}"

        # 1. Relative Import Logic
        if imp.level > 0:
            resolved = self._resolve_relative(imp, context_file)
            if resolved:
                return resolved

            # Logger.info(f"{log_prefix} -> Physical relative failed. Attempting symbolic...")
            resolved_sym = self._resolve_relative_via_symbols(imp, context_file)
            if resolved_sym:
                Logger.info(f"{log_prefix} -> Symbolic Match: {resolved_sym}")
                return resolved_sym

            Logger.warn(f"{log_prefix} -> RELATIVE MISS")
            return None

        # 2. Absolute Import Logic
        candidates = []
        if imp.module:
            candidates.append(imp.module)
            candidates.append(f"{imp.module}.{imp.name}")
        else:
            candidates.append(imp.name)

        for candidate in candidates:
            if candidate in self.symbol_map:
                return self.symbol_map[candidate]

        # 3. Fallback: Physical Absolute Lookup
        if imp.module:
            module_path = imp.module.replace('.', '/')
            physical_candidates = [
                self.src_root / f"{module_path}.py",
                self.src_root / module_path / "__init__.py",
                self.root / f"{module_path}.py",
                self.root / module_path / "__init__.py"
            ]
            for path in physical_candidates:
                if path.exists():
                    return path.resolve()

        return None

    def calculate_new_import_string(self, healee_path: Path, new_origin_path: Path) -> str:
        """
        Determines the best Python import string from File A (Healee) to File B (Origin).
        """
        healee_dir = healee_path.parent
        origin_dir = new_origin_path.parent


        try:
            # Calculate the relative vector between DIRECTORIES
            rel_path = os.path.relpath(origin_dir, healee_dir)
            up_traversals = rel_path.count("..")

            Logger.info(f"   Vector: '{rel_path}' (Depth: {up_traversals})")

            # --- STRATEGY SELECTION ---
            # Distance Heuristic:
            # . (0) -> Relative
            # .. (1) -> Relative
            # ../.. (2) -> Relative
            # ../../.. (3+) -> Absolute (Too far, harder to read)

            if up_traversals <= 2:
                relative_str = self._forge_relative_string(rel_path, new_origin_path)
                Logger.info(f"   Result (Relative): {relative_str}")
                return relative_str
            else:
                absolute_str = self._calculate_absolute_string(new_origin_path)
                Logger.info(f"   Result (Absolute): {absolute_str}")
                return absolute_str

        except ValueError as e:
            Logger.warn(f"   Pathfinding Paradox: {e}")
            return self._calculate_absolute_string(new_origin_path)

    def _resolve_relative(self, imp: 'DetectedImport', context_file: Path) -> Optional[Path]:
        current_dir = context_file.parent.resolve()

        for i in range(imp.level - 1):
            if current_dir.parent == current_dir:
                # Logger.info(f"   [REL] Root escape at step {i+1}/{imp.level-1}")
                return None
            current_dir = current_dir.parent

        target_base = current_dir
        if imp.module:
            target_base = target_base.joinpath(*imp.module.split('.'))

        if not target_base.name:
            return None

        candidates = [
            target_base / "__init__.py",
            target_base.with_suffix(".py")
        ]

        for cand in candidates:
            if cand.exists():
                return cand.resolve()

        return None

    def _resolve_relative_via_symbols(self, imp: 'DetectedImport', context_file: Path) -> Optional[Path]:
        context_module = self.reverse_symbol_map.get(context_file.resolve())
        if not context_module:
            return None

        parts = context_module.split('.')
        if context_file.name != '__init__.py':
            parts = parts[:-1]

        pops = imp.level - 1
        if pops > len(parts):
            return None

        if pops > 0:
            parts = parts[:-pops]

        if imp.module:
            parts.extend(imp.module.split('.'))

        target_module = ".".join(parts)

        if target_module in self.symbol_map:
            return self.symbol_map[target_module]

        target_symbol = f"{target_module}.{imp.name}"
        if target_symbol in self.symbol_map:
            return self.symbol_map[target_symbol]

        return None

    def _forge_relative_string(self, rel_path: str, target_file: Path) -> str:
        """
        Transmutes a relative filesystem path into dot notation, injecting the module name.

        Args:
            rel_path: The path from SourceDir to TargetDir (e.g., 'features', '..', '.')
            target_file: The actual file being imported (e.g., 'main_service.py')
        """
        # 1. Convert Directory Path to Dots
        base_dots = ""

        # Case A: Same Directory
        if rel_path == ".":
            base_dots = "."
        # Case B: Sibling or Child (e.g., 'features', 'subdir/child')
        elif not rel_path.startswith(".."):
            clean_rel = rel_path.replace(os.sep, '.')
            if clean_rel.startswith('.'): clean_rel = clean_rel[1:]
            base_dots = f".{clean_rel}"
        # Case C: Parent Traversal (e.g., '..', '../shared')
        else:
            dots_count = rel_path.count("..") + 1
            dots_prefix = "." * dots_count
            remainder_parts = [p for p in rel_path.split(os.sep) if p != '..']
            remainder = ".".join(remainder_parts)

            base_dots = f"{dots_prefix}{remainder}" if remainder else dots_prefix

        # 2. Inject Module Name (The Gnostic Correction)
        # If the target is __init__.py, the directory path IS the module path.
        if target_file.name == "__init__.py":
            return base_dots

        module_name = target_file.stem  # e.g. 'main_service'

        # Join logic:
        # If base is just dots ('.', '..'), append name -> '.name', '..name'
        if base_dots.endswith('.'):
            return f"{base_dots}{module_name}"

        # If base has text ('.features'), append dot + name -> '.features.main_service'
        return f"{base_dots}.{module_name}"

    def _calculate_absolute_string(self, target: Path) -> str:
        try:
            roots_to_try = [self.src_root, self.root]
            roots_to_try = list(dict.fromkeys(roots_to_try))

            for root in roots_to_try:
                if target.is_relative_to(root):
                    rel = target.relative_to(root)
                    parts = list(rel.parts)

                    if parts[-1] == '__init__.py':
                        parts.pop()
                    elif parts[-1].endswith('.py'):
                        parts[-1] = parts[-1][:-3]

                    return ".".join(parts)
            return "!!OUTSIDE_ROOT!!"
        except ValueError:
            return "!!CALC_ERROR!!"