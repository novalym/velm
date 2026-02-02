import json
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Any, Optional

from ..contracts import BaseHealer, HealingDiagnosis
from ....inquisitor import get_treesitter_gnosis
from ....logger import Scribe

Logger = Scribe("TSImportHealer")


class TypeScriptImportHealer(BaseHealer):
    """
    =================================================================================
    == THE GNOSTIC INQUISITOR OF THE TYPESCRIPT COSMOS (V-\u03a9-TSCONFIG-ORACLE)       ==
    =================================================================================
    A God-Engine of healing that understands the sacred scripture of `tsconfig.json`,
    including `baseUrl` and `paths` aliases.
    =================================================================================
    """

    def __init__(self, project_root: Path, context: Dict[str, Any]):
        super().__init__(project_root, context)
        # [FACULTY 1] The tsconfig.json Oracle
        self._tsconfig_gnosis = self._load_tsconfig()
        self._tsconfig_base_url = self.project_root / self._tsconfig_gnosis.get("compilerOptions", {}).get("baseUrl",
                                                                                                           ".")
        self._tsconfig_paths = self._tsconfig_gnosis.get("compilerOptions", {}).get("paths", {})

    @property
    def name(self) -> str:
        return "TSImportAligner"

    @property
    def supported_extensions(self) -> List[str]:
        return ['.ts', '.tsx']

    def _load_tsconfig(self) -> Dict[str, Any]:
        """A Gaze for `tsconfig.json` or `jsconfig.json`."""
        for config_name in ["tsconfig.json", "jsconfig.json"]:
            config_path = self.project_root / config_name
            if config_path.is_file():
                try:
                    # Humble Gaze: Strip comments before parsing JSON
                    content = config_path.read_text(encoding='utf-8')
                    content_no_comments = re.sub(r'//.*?\n|/\*.*?\*/', '', content, flags=re.S)
                    return json.loads(content_no_comments)
                except Exception:
                    continue
        return {}

    def prophesy_healing_plan(self, file_to_heal: Path, translocation_map: Dict[Path, Path]) -> List[HealingDiagnosis]:
        """[FACULTY 5] The Prophetic Mind, now with the Oracle's wisdom."""
        healing_plan: List[HealingDiagnosis] = []
        try:
            content = file_to_heal.read_text(encoding='utf-8')
        except Exception:
            return []

        dossier = get_treesitter_gnosis(file_to_heal, content)
        if "error" in dossier or "imports" not in dossier.get("dependencies", {}):
            return []

        future_healee_path = translocation_map.get(file_to_heal.resolve(), file_to_heal.resolve())

        for imp_data in dossier["dependencies"]["imports"]:
            line_num = imp_data.get("line_num")
            original_import_str = imp_data.get("path")
            if not original_import_str or not line_num: continue
            if not (original_import_str.startswith('.') or original_import_str.startswith('/') or any(
                    alias in original_import_str for alias in self._tsconfig_paths)):
                continue  # Node modules

            original_abs_path = self._resolve_original_path(file_to_heal, original_import_str)
            if not original_abs_path: continue

            future_origin_path = translocation_map.get(original_abs_path, original_abs_path)
            new_import_path = self._calculate_new_import_path(future_healee_path, future_origin_path)

            if new_import_path != original_import_str:
                Logger.verbose(
                    f"  -> TS Healing Prophecy for '{file_to_heal.name}': L{line_num} ('{original_import_str}' -> '{new_import_path}')")
                healing_plan.append(HealingDiagnosis(
                    file_path=file_to_heal,
                    healer_name=self.name,
                    description=f"Recalculate aliased/relative import path to '{new_import_path}'",
                    metadata={"line_num": line_num, "original_import_str": original_import_str,
                              "new_import_path": new_import_path}
                ))
        return healing_plan

    def heal(self, file_path: Path, content: str, diagnoses: List[HealingDiagnosis]) -> Tuple[str, bool]:
        """[FACULTY 7] The Surgical Hand."""
        if not diagnoses: return content, False
        lines = content.splitlines()
        changes_made = False
        for diagnosis in sorted(diagnoses, key=lambda d: d.metadata.get("line_num", 0), reverse=True):
            meta = diagnosis.metadata
            line_idx, old_path, new_path = meta.get("line_num", 1) - 1, meta.get("original_import_str"), meta.get(
                "new_import_path")
            if 0 <= line_idx < len(lines):
                line = lines[line_idx]
                healed_line = line.replace(f"'{old_path}'", f"'{new_path}'").replace(f'"{old_path}"', f'"{new_path}"')
                if healed_line != line:
                    lines[line_idx], changes_made = healed_line, True
        return "\n".join(lines), changes_made

    def _resolve_original_path(self, source_file: Path, import_str: str) -> Optional[Path]:
        """[FACULTY 2] The Path Alias Alchemist."""
        # 1. Gaze for Path Aliases
        for alias, mappings in self._tsconfig_paths.items():
            alias_prefix = alias.rstrip('/*')
            if import_str.startswith(alias_prefix):
                for mapping in mappings:
                    mapping_prefix = mapping.rstrip('/*')
                    remapped_path = import_str.replace(alias_prefix, mapping_prefix, 1)
                    absolute_path = (self._tsconfig_base_url / remapped_path).resolve()
                    resolved = self._check_candidates(absolute_path)
                    if resolved: return resolved

        # 2. Gaze for Relative Paths
        if import_str.startswith('.'):
            absolute_path = (source_file.parent / import_str).resolve()
            return self._check_candidates(absolute_path)

        return None

    def _calculate_new_import_path(self, healee_path: Path, target_path: Path) -> str:
        """Prophesies the new path, preferring aliases if possible."""
        # 1. Prophesy an Alias Path
        for alias, mappings in self._tsconfig_paths.items():
            alias_prefix = alias.rstrip('/*')
            for mapping in mappings:
                mapping_prefix = mapping.rstrip('/*')
                try:
                    mapped_root = (self._tsconfig_base_url / mapping_prefix).resolve()
                    if target_path.is_relative_to(mapped_root):
                        rel_path = target_path.relative_to(mapped_root)
                        aliased_path = (Path(alias_prefix) / rel_path).as_posix()
                        base, _ = os.path.splitext(aliased_path)
                        if base.endswith('/index'): base = base[:-6] or '.'
                        return base
                except (ValueError, Exception):
                    continue

        # 2. Prophesy a Relative Path (Fallback)
        rel_path = os.path.relpath(target_path, healee_path.parent)
        rel_path_posix = Path(rel_path).as_posix()
        base, _ = os.path.splitext(rel_path_posix)
        if base.endswith('/index'): base = base[:-6] or '.'
        return base if base.startswith('.') else f"./{base}"

    def _check_candidates(self, base_path: Path) -> Optional[Path]:
        """Checks for extensionless files and index files."""
        if base_path.is_file(): return base_path.resolve()
        for ext in self.supported_extensions + ['.d.ts', '.js', '.jsx', '.json']:
            if base_path.with_suffix(ext).is_file():
                return base_path.with_suffix(ext).resolve()
        if base_path.is_dir():
            for ext in self.supported_extensions + ['.d.ts']:
                if (base_path / f"index{ext}").is_file():
                    return (base_path / f"index{ext}").resolve()
        return None