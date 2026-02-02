# Path: scaffold/artisans/shadow_clone/config_injector.py
# =================================================================================
# == THE CONFIGURATION WEAVER (V-Ω-ENV-PATCHER)                                 ==
# =================================================================================
from pathlib import Path
from typing import Dict, Any
import re
from ...logger import Scribe

Logger = Scribe("ConfigWeaver")


class ConfigInjector:
    """
    Surgically alters the .env file of the Shadow Realm.
    Replaces existing keys if found, appends if new.
    """

    def inject(self, shadow_root: Path, overrides: Dict[str, Any]):
        env_path = shadow_root / ".env"

        # Read existing or start fresh
        lines = []
        if env_path.exists():
            lines = env_path.read_text(encoding='utf-8').splitlines()

        new_lines = []
        overridden_keys = set()

        # 1. Update existing keys
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                new_lines.append(line)
                continue

            # Simple key=value parse
            if "=" in line:
                key = line.split("=")[0].strip()
                if key in overrides:
                    if overrides[key] is not None:
                        new_lines.append(f"{key}={overrides[key]}")
                        overridden_keys.add(key)
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        # 2. Append new keys
        if len(overridden_keys) < len(overrides):
            new_lines.append("\n# --- [SCAFFOLD SHADOW INJECTIONS] ---")
            for k, v in overrides.items():
                if k not in overridden_keys and v is not None:
                    new_lines.append(f"{k}={v}")

        # 3. Inscribe
        env_path.write_text("\n".join(new_lines), encoding='utf-8')
        Logger.info(f"Injected {len(overrides)} config overrides into Shadow Realm.")