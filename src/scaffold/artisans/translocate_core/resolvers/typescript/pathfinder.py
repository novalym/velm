# // scaffold/artisans/translocate_core/resolvers/typescript/pathfinder.py
# ------------------------------------------------------------------------

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from ..javascript.pathfinder import JSPathfinder


class TSPathfinder(JSPathfinder):
    """
    The Geometrician of TypeScript.
    Understands `tsconfig.json` Path Aliases.
    """

    def __init__(self, project_root: Path):
        super().__init__(project_root)
        self.tsconfig = self._load_tsconfig()
        self.base_url = self.root / self.tsconfig.get('compilerOptions', {}).get('baseUrl', '.')
        self.paths = self.tsconfig.get('compilerOptions', {}).get('paths', {})

    def _load_tsconfig(self) -> Dict[str, Any]:
        """Reads tsconfig.json with comment-stripping heuristic."""
        # Simple implementation, robust handling implied in a real system
        path = self.root / "tsconfig.json"
        if not path.exists(): return {}
        try:
            # Naive read; use a JSON5 parser ideally, or regex strip comments
            import re
            content = path.read_text(encoding='utf-8')
            clean = re.sub(r'//.*', '', content)
            clean = re.sub(r'/\*.*?\*/', '', clean, flags=re.DOTALL)
            return json.loads(clean)
        except:
            return {}

    def is_node_module(self, specifier: str) -> bool:
        # Check aliases first
        for alias in self.paths:
            alias_prefix = alias.rstrip('*')
            if specifier.startswith(alias_prefix):
                return False  # It's an alias to local code!
        return super().is_node_module(specifier)

    def resolve_absolute_path(self, context_file: Path, specifier: str) -> Optional[Path]:
        # 1. Check Aliases
        for alias, targets in self.paths.items():
            alias_prefix = alias.rstrip('*')
            if specifier.startswith(alias_prefix):
                # We typically take the first target
                target_map = targets[0].rstrip('*')
                remainder = specifier[len(alias_prefix):]

                # Resolve mapping relative to baseUrl
                mapped_path = (self.base_url / target_map / remainder).resolve()
                return self._probe_file(mapped_path)

        # 2. Fallback to Standard JS Relative
        return super().resolve_absolute_path(context_file, specifier)

    def calculate_new_specifier(self, healee_path: Path, new_origin: Path) -> str:
        # 1. Try to use an Alias (Reverse Lookup)
        # Does the new_origin fall under a configured path?
        for alias, targets in self.paths.items():
            target_map = targets[0].rstrip('*')
            mapped_root = (self.base_url / target_map).resolve()

            if new_origin.is_relative_to(mapped_root):
                rel = new_origin.relative_to(mapped_root)
                # Reconstruct alias
                alias_base = alias.rstrip('*')

                spec = f"{alias_base}{rel.as_posix()}"
                # Strip extension
                base, ext = os.path.splitext(spec)
                if ext in self.EXTENSIONS:
                    if base.endswith('/index'): return base[:-6]
                    return base
                return spec

        # 2. Fallback to Relative
        return super().calculate_new_specifier(healee_path, new_origin)