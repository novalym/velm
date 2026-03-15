# Path: core/alchemist/elara/library/system_rites/legacy_text_suture.py
# ---------------------------------------------------------------------

import re
from pathlib import Path
from ......logger import Scribe

Logger = Scribe("SystemRites:Emulation")

class SystemAlchemist:
    """A specialized organ that emulates Unix behaviors on non-Unix Iron."""
    @classmethod
    def emulate_grep(cls, pattern: str, target: str) -> str:
        try:
            p = Path(str(target).strip('"\''))
            if not p.exists(): return ""
            regex = re.compile(str(pattern).strip('"\''), re.IGNORECASE)
            content = p.read_text(encoding='utf-8', errors='ignore')
            matches =[line.strip() for line in content.splitlines() if regex.search(line)]
            return "\n".join(matches)
        except Exception as e:
            Logger.debug(f"Grep Emulation fractured: {e}")
            return ""

    @classmethod
    def emulate_ls(cls, target: str) -> str:
        try:
            p = Path(str(target).strip('"\''))
            if not p.exists(): return ""
            return "\n".join([f.name for f in p.iterdir()])
        except Exception:
            return ""

def list_capabilities() -> dict:
    from ..registry import RITE_REGISTRY
    return RITE_REGISTRY.list_capabilities()

def __repr__() -> str:
    capabilities = list_capabilities()
    return (
        f"<Ω_SYSTEM_RITES version=88.0-TOTALITY status=RESONANT "
        f"rites={len(capabilities['global'])} mode=ARCHITECTURAL_LIBERATION>"
    )