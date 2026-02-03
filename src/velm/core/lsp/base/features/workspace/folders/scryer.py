# Path: core/lsp/features/workspace/folders/scryer.py
# ----------------------------------------------------
import os
import json
from pathlib import Path
from typing import Optional
from .models import RootAura


class RealityScryer:
    """[THE ORACLE] Peeks into folders to divine their purpose."""

    def divine_aura(self, path: Path) -> RootAura:
        """Determines the linguistic/architectural flavor of a folder."""
        if (path / ".scaffold").exists() or (path / "scaffold.scaffold").exists():
            return RootAura.SCAFFOLD

        if (path / "pyproject.toml").exists() or (path / "requirements.txt").exists():
            return RootAura.PYTHON

        if (path / "package.json").exists():
            return RootAura.NODE

        if (path / "Cargo.toml").exists() or (path / "go.mod").exists():
            return RootAura.SYSTEMS

        return RootAura.UNKNOWN

    def divine_name(self, path: Path) -> Optional[str]:
        """Attempts to find the 'True Name' from manifest files."""
        # 1. Check package.json
        p_json = path / "package.json"
        if p_json.exists():
            try:
                data = json.loads(p_json.read_text(encoding='utf-8', errors='ignore'))
                if "name" in data: return data["name"]
            except:
                pass

        # 2. Check pyproject.toml (simple parse)
        p_toml = path / "pyproject.toml"
        if p_toml.exists():
            try:
                content = p_toml.read_text(encoding='utf-8', errors='ignore')
                import re
                match = re.search(r'name\s*=\s*"(.*?)"', content)
                if match: return match.group(1)
            except:
                pass

        # Fallback to directory name
        return path.name

