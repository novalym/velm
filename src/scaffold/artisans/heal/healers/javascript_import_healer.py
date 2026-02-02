import os
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional, Set

from ..contracts import BaseHealer, HealingDiagnosis
from ....inquisitor import get_treesitter_gnosis
from ....logger import Scribe

Logger = Scribe("JSImportHealer")


class JavaScriptImportHealer(BaseHealer):
    """
    =================================================================================
    == THE GNOSTIC INQUISITOR OF THE JAVASCRIPT COSMOS (V-\u03a9-TREE-SITTER-ULTIMA)    ==
    =================================================================================
    A divine artisan that uses Tree-sitter to perceive and heal the Gnostic bonds
    (imports and requires) within JavaScript and JSX scriptures.
    =================================================================================
    """

    @property
    def name(self) -> str:
        return "JSImportAligner"

    @property
    def supported_extensions(self) -> List[str]:
        return ['.js', '.jsx']

    def prophesy_healing_plan(self, file_to_heal: Path, translocation_map: Dict[Path, Path]) -> List[HealingDiagnosis]:
        """[FACULTY 3] The Prophetic Mind. Forges the complete healing plan."""
        healing_plan: List[HealingDiagnosis] = []
        try:
            content = file_to_heal.read_text(encoding='utf-8')
        except Exception:
            return []

        # [FACULTY 1] The Tree-sitter Gaze
        dossier = get_treesitter_gnosis(file_to_heal, content)
        if "error" in dossier or "imports" not in dossier.get("dependencies", {}):
            return []

        future_healee_path = translocation_map.get(file_to_heal.resolve(), file_to_heal.resolve())

        for imp_data in dossier["dependencies"]["imports"]:
            line_num = imp_data.get("line_num")
            original_import_str = imp_data.get("path")

            if not original_import_str or not line_num:
                continue

            # [FACULTY 8] The Node Modules Oracle
            if not (original_import_str.startswith('.') or original_import_str.startswith('/')):
                continue  # It's a package import, not a local one.

            # Resolve the original absolute path of the imported file
            original_abs_path = self._resolve_original_path(file_to_heal, original_import_str)
            if not original_abs_path:
                continue

            # The future absolute path of the imported file
            future_origin_path = translocation_map.get(original_abs_path, original_abs_path)

            # [FACULTY 4] The Path Alchemist
            new_import_path = self._calculate_new_import_path(future_healee_path, future_origin_path)

            # [FACULTY 11] The Idempotency Ward
            if new_import_path != original_import_str:
                Logger.verbose(
                    f"  -> Healing Prophecy for '{file_to_heal.name}': L{line_num} ('{original_import_str}' -> '{new_import_path}')")
                healing_plan.append(HealingDiagnosis(
                    file_path=file_to_heal,
                    healer_name=self.name,
                    description=f"Recalculate import path from '{original_import_str}' to '{new_import_path}'",
                    metadata={
                        "line_num": line_num,
                        "original_import_str": original_import_str,
                        "new_import_path": new_import_path
                    }
                ))

        return healing_plan

    def heal(self, file_path: Path, content: str, diagnoses: List[HealingDiagnosis]) -> Tuple[str, bool]:
        """[FACULTY 9] The Surgical Hand."""
        if not diagnoses:
            return content, False

        self.logger.verbose(f"The JavaScript Healer's Hand awakens for '{file_path.name}'.")

        lines = content.splitlines()
        changes_made = False

        # Sort descending by line number to prevent index invalidation
        for diagnosis in sorted(diagnoses, key=lambda d: d.metadata.get("line_num", 0), reverse=True):
            meta = diagnosis.metadata
            line_idx = meta.get("line_num", 1) - 1
            original_path = meta.get("original_import_str")
            new_path = meta.get("new_import_path")

            if 0 <= line_idx < len(lines):
                line = lines[line_idx]
                # Surgically replace only the path string literal
                healed_line = line.replace(f"'{original_path}'", f"'{new_path}'").replace(f'"{original_path}"',
                                                                                          f'"{new_path}"')
                if healed_line != line:
                    lines[line_idx] = healed_line
                    changes_made = True

        return "\n".join(lines), changes_made

    def _resolve_original_path(self, source_file: Path, import_str: str) -> Optional[Path]:
        """[FACULTY 5 & 6] The Extensionless Prophet & Index Seer."""
        base_dir = source_file.parent
        target_path = (base_dir / import_str).resolve()

        # Check for exact match first
        if target_path.exists():
            return target_path

        # Check for extensionless files
        for ext in self.supported_extensions + ['.json']:
            if target_path.with_suffix(ext).is_file():
                return target_path.with_suffix(ext).resolve()

        # Check for directory index file
        if target_path.is_dir():
            for ext in self.supported_extensions:
                if (target_path / f"index{ext}").is_file():
                    return (target_path / f"index{ext}").resolve()

        return None

    def _calculate_new_import_path(self, healee_path: Path, target_path: Path) -> str:
        """Calculates the new relative path and strips its extension."""
        try:
            rel_path = os.path.relpath(target_path, healee_path.parent)
            rel_path_posix = Path(rel_path).as_posix()

            # Strip extension
            base, _ = os.path.splitext(rel_path_posix)

            # Handle index files
            if base.endswith('/index'):
                base = base[:-6] or '.'

            return base if base.startswith('.') else f"./{base}"
        except ValueError:
            # Paths are on different drives on Windows
            return target_path.as_posix()