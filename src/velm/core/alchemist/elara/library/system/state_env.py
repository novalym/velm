# Path: core/alchemist/elara/library/system_rites/state_env.py
# ------------------------------------------------------------

import os
import time
import json
import hashlib
import hmac
import secrets
from pathlib import Path
from typing import Any, Dict, Optional, Union, Final, Set, List
from ..registry import register_rite
from ......logger import Scribe

Logger = Scribe("SystemRites:State")


# =============================================================================
# == STRATUM 0: THE GLOBAL MEMORY LATTICE                                    ==
# =============================================================================

@register_rite("stash")
def akashic_stash(value: Any, key: str, **kwargs) -> Any:
    """
    =============================================================================
    == THE AKASHIC STASH (V-Ω-TOTALITY-VMAX)                                   ==
    =============================================================================
    LIF: ∞ | ROLE: STATE_PRESERVER
    Inscribes matter into the global persistent memory of the current strike.
    """
    ctx = kwargs.get('context', {})
    trace_id = ctx.get('trace_id', 'tr-void')

    if '__global_stash__' not in ctx:
        ctx['__global_stash__'] = {}

    # [ASCENSION 8]: CAUSAL STAMPING
    ctx['__global_stash__'][str(key)] = {
        "val": value,
        "ts": time.time(),
        "trace": trace_id,
        "merkle": hashlib.md5(str(value).encode()).hexdigest()[:8]
    }

    # [ASCENSION 12]: HAPTIC RADIATION
    _radiate_hud_shift(key, value, trace_id, ctx)
    return value


@register_rite("recall")
def akashic_recall(value: Any, key: str = None, default: Any = None, **kwargs) -> Any:
    """Retrieves waked matter from the global memory lattice."""
    target_key = key if key else str(value)
    ctx = kwargs.get('context', {})
    entry = ctx.get('__global_stash__', {}).get(target_key)

    # [ASCENSION 7]: NoneType Sarcophagus
    if entry is None:
        return default

    # [ASCENSION 11]: TEMPORAL DECAY CHECK
    # (Future expansion: check if entry has expired)

    return entry["val"] if isinstance(entry, dict) else entry


@register_rite("burn")
def akashic_burn(value: Any, key: str = None, **kwargs) -> bool:
    """Physically evaporates a key from the memory lattice."""
    target_key = key if key else str(value)
    ctx = kwargs.get('context', {})
    if '__global_stash__' in ctx and target_key in ctx['__global_stash__']:
        del ctx['__global_stash__'][target_key]
        return True
    return False


# =============================================================================
# == STRATUM 1: SUBSTRATE ENVIRONMENT DNA                                    ==
# =============================================================================

@register_rite("env_var")
def env_var_rite(value: Any, default: Any = "") -> Any:
    """[ASCENSION 3]: Substrate Scry. Retrieves OS-level Gnosis."""
    key = str(value).strip()
    return os.environ.get(key, default)


@register_rite("set_env")
def set_env_rite(value: Any, key: str, **kwargs) -> str:
    """[ASCENSION 66]: OS-Level Environment Suture."""
    os.environ[str(key)] = str(value)

    # [ASCENSION 12]: Radiate change to the Ocular HUD
    ctx = kwargs.get('context', {})
    _radiate_hud_shift(key, value, ctx.get('trace_id', 'tr-env'), ctx)

    return str(value)


@register_rite("require_env")
def require_env_rite(value: Any, key: str = None) -> Any:
    """Enforces the existence of an OS variable, raising a Heresy if unmanifest."""
    target_key = key if key else str(value)
    val = os.environ.get(target_key)
    if val is None:
        raise ValueError(f"ENVIRONMENTAL_VOID_HERESY: Required variable '{target_key}' is missing from the substrate.")
    return val


# =============================================================================
# == STRATUM 2: THE DOTENV ALCHEMIST                                         ==
# =============================================================================

@register_rite("read_env")
def read_env_rite(value: Any) -> Dict[str, str]:
    """[ASCENSION 69]: Inhales a .env file and transmutes it into a Gnostic Dict."""
    p = Path(str(value).strip().strip('"\''))
    env_dict = {}
    if p.exists() and p.is_file():
        # [ASCENSION 19]: FAULT-ISOLATED HEALING
        content = p.read_text(encoding='utf-8', errors='replace')
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith('#'): continue
            if '=' in line:
                k, v = line.split('=', 1)
                # Strip quotes and spacing
                env_dict[k.strip()] = v.strip().strip('\'"')
    return env_dict


@register_rite("write_env")
def write_env_rite(value: Any, data: Dict[str, str], **kwargs) -> bool:
    """[ASCENSION 69]: Physical inscription of Gnostic DNA into the Iron."""
    try:
        p = Path(str(value).strip().strip('"\''))

        # [ASCENSION 5]: HYDRAULIC PACING
        p.parent.mkdir(parents=True, exist_ok=True)

        # [ASCENSION 18]: LINGUISTIC PURITY (SCREAMING_SNAKE)
        lines = ["# == GNOSTIC ENVIRONMENT MANIFEST =="]
        for k, v in data.items():
            lines.append(f"{str(k).upper()}={str(v)}")

        p.write_text("\n".join(lines) + "\n", encoding='utf-8')
        return True
    except Exception as e:
        Logger.error(f"Dotenv write fracture: {e}")
        return False


# =============================================================================
# == STRATUM 3: JURISPRUDENCE & SECURITY                                     ==
# =============================================================================

@register_rite("seal")
@register_rite("vow")
def immutable_vow_seal(value: Any, key: str = None, **kwargs) -> Any:
    """[ASCENSION 16]: Wards a key against any future mutation."""
    target_key = key if key else str(value)
    ctx = kwargs.get('context', {})
    if '__immutable_wards__' not in ctx:
        ctx['__immutable_wards__'] = set()
    ctx['__immutable_wards__'].add(target_key)
    return value


@register_rite("autonomic_seal")
def autonomic_cryptographic_seal(value: Any, key_name: str, **kwargs) -> str:
    """
    =============================================================================
    == THE APOPHATIC SECRET SEAL (V-Ω-TOTALITY-VMAX-AUTO-ENTROPY)              ==
    =============================================================================
    [THE MASTER CURE]: Detects hungry voids and fills them with pure entropy.
    """
    if value and str(value).strip() and str(value) != "REPLACE_ME":
        return value

    target = key_name.upper()
    # [ASCENSION 9]: Shannon Entropy Recognition
    if any(token in target for token in ("SECRET", "KEY", "TOKEN", "PASSWORD", "SALT", "SIGNATURE")):
        from secrets import token_hex, token_urlsafe
        # [STRIKE]: Materializing 64-character high-status entropy
        new_soul = token_hex(32) if "KEY" in target else token_urlsafe(48)
        Logger.success(f"🛡️ [SECURITY] Autonomic Inception: Forged entropy for '{key_name}'.")
        return new_soul

    return value


@register_rite("mask")
@register_rite("shroud")
def mask_sensitive_state(value: Any, **kwargs) -> str:
    """[ASCENSION 2]: Shrouds value in logs while preserving it in Mind."""
    s = str(value)
    if len(s) < 8: return "****"
    return f"{s[:4]}...[SHROUDED]...{s[-4:]}"


# =============================================================================
# == STRATUM 4: TEMPORAL & SPATIAL UTILITIES                                 ==
# =============================================================================

@register_rite("snapshot")
def environment_snapshot(value: Any = None, **kwargs) -> str:
    """[ASCENSION 23]: Forges a Merkle-Seal of the entire current Mind-State."""
    ctx = kwargs.get('context', {})
    # Filter for serializable, non-internal data
    mind_matter = {k: v for k, v in ctx.items() if not str(k).startswith('__')}
    canonical = json.dumps(mind_matter, sort_keys=True, default=str)

    seal = hashlib.sha256(canonical.encode()).hexdigest()
    if value:  # If a var name was provided, store the seal
        ctx[str(value)] = seal
    return seal


@register_rite("is_iron")
def check_native_substrate(value: Any = None, **kwargs) -> bool:
    """Returns True if the engine is striking the physical Iron (Native OS)."""
    return os.environ.get("SCAFFOLD_ENV") != "WASM"


@register_rite("drift_check")
def detect_environmental_drift(value: Any, expected_hash: str, **kwargs) -> bool:
    """[ASCENSION 4]: Adjudicates if the local iron has drifted from the Law."""
    current_val = os.environ.get(str(value))
    if current_val is None: return True

    current_hash = hashlib.md5(current_val.encode()).hexdigest()
    return current_hash != expected_hash


# =============================================================================
# == INTERNAL KINETICS                                                       ==
# =============================================================================

def _radiate_hud_shift(key: str, value: Any, trace: str, ctx: Dict[str, Any]):
    """[ASCENSION 12]: Radiates state evolution to the Ocular HUD."""
    engine = ctx.get('__engine__')
    if engine and hasattr(engine, 'akashic') and engine.akashic:
        try:
            # Entropy Masking for HUD safety
            is_secret = any(s in str(key).upper() for s in ("KEY", "SECRET", "PASS", "TOKEN"))
            display_val = "[REDACTED]" if is_secret else str(value)[:100]

            engine.akashic.broadcast({
                "method": "novalym/hud_pulse",
                "params": {
                    "type": "GNOSIS_SHIFT",
                    "label": f"STATE_SET: {key}",
                    "message": f"Value: {display_val}",
                    "color": "#64ffda" if not is_secret else "#a855f7",
                    "trace": trace
                }
            })
        except:
            pass


def __repr__() -> str:
    return "<Ω_STATE_ENV_STRATUM version=TOTALITY_VMAX_2026 status=RESONANT mode=PANOPTICON>"