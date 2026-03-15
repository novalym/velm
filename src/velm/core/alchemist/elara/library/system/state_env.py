# Path: core/alchemist/elara/library/system_rites/state_env.py
# ------------------------------------------------------------

import os
from typing import Any, Dict
from pathlib import Path
from ..registry import register_rite
from ......logger import Scribe

Logger = Scribe("SystemRites:State")

@register_rite("stash")
def akashic_stash(value: Any, key: str, **kwargs) -> Any:
    ctx = kwargs.get('context', {})
    if '__global_stash__' not in ctx: ctx['__global_stash__'] = {}
    ctx['__global_stash__'][str(key)] = value
    return value

@register_rite("recall")
def akashic_recall(value: Any, key: str = None, default: Any = None, **kwargs) -> Any:
    target_key = key if key else str(value)
    ctx = kwargs.get('context', {})
    return ctx.get('__global_stash__', {}).get(target_key, default)

@register_rite("env_var")
def env_var_rite(value: Any, default: Any = "") -> Any:
    """Retrieves an OS environment variable."""
    return os.environ.get(str(value), default)

@register_rite("set_env")
def set_env_rite(value: Any, key: str) -> str:
    """[ASCENSION 66]: OS-Level Environment Suture."""
    os.environ[str(key)] = str(value)
    return str(value)

@register_rite("read_env")
def read_env_rite(value: Any) -> Dict[str, str]:
    """[ASCENSION 69]: Dotenv Alchemist (Read)."""
    p = Path(str(value))
    env_dict = {}
    if p.exists() and p.is_file():
        for line in p.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                env_dict[k.strip()] = v.strip().strip('\'"')
    return env_dict

@register_rite("write_env")
def write_env_rite(value: Any, data: Dict[str, str]) -> bool:
    """[ASCENSION 69]: Dotenv Alchemist (Write)."""
    try:
        p = Path(str(value))
        p.parent.mkdir(parents=True, exist_ok=True)
        lines =[f"{k}={v}" for k, v in data.items()]
        p.write_text("\n".join(lines) + "\n", encoding='utf-8')
        return True
    except Exception as e:
        Logger.error(f"Dotenv write fracture: {e}")
        return False

@register_rite("seal")
@register_rite("vow")
def immutable_vow_seal(value: Any, key: str = None, **kwargs) -> Any:
    target_key = key if key else str(value)
    ctx = kwargs.get('context', {})
    if '__immutable_wards__' not in ctx: ctx['__immutable_wards__'] = set()
    ctx['__immutable_wards__'].add(target_key)
    return value