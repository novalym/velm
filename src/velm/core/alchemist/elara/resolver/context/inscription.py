# Path: core/alchemist/elara/resolver/context/inscription.py
# ----------------------------------------------------------

import hashlib
from typing import Any, TYPE_CHECKING
from .....runtime.vessels import SGF_RESERVOIRS
from ......logger import Scribe
from .jurisprudence import ContractWarden
from .radiation import HUDMulticaster

if TYPE_CHECKING:
    from .engine import LexicalScope

Logger = Scribe("InscriptionEngine")

class InscriptionEngine:
    """
    =============================================================================
    == THE INSCRIPTION ENGINE (V-Ω-KINETIC-PEN)                                ==
    =============================================================================
    LIF: ∞ | ROLE: STATE_MATERIALIZER
    Handles the physical assignment of Gnosis, updating Merkle chains,
    verifying locks, and routing telemetry.
    """

    @classmethod
    def set_local(cls, scope: 'LexicalScope', key: str, value: Any, lock: bool = False):
        """[THE RITE OF KINETIC INSCRIPTION]"""
        # 1. Adjudicate
        ContractWarden.adjudicate(scope, key, value)

        # 2. Sovereignty Ward
        if key.startswith('__') and not scope.global_ctx.variables.get('_is_shadow'):
            if key not in SGF_RESERVOIRS and key not in scope.IMMUNITY_WHITELIST:
                Logger.warn(f"Sovereignty Breach: Mutation of internal '{key}' warded.")
                return

        if key in scope._locks:
            raise PermissionError(f"Gnostic Schism: Key '{key}' is immutable.")

        # 3. Redirection of Will
        if key in ('__woven_matter__', '__woven_commands__'):
            scope.global_ctx.variables[key] = value
            return

        # Type Harmonization
        if isinstance(value, str):
            val_low = value.lower().strip()
            if val_low in ('true', 'yes', 'on', 'resonant'): value = True
            elif val_low in ('false', 'no', 'off', 'fractured'): value = False
            elif val_low in ('null', 'none', 'void'): value = None

        with scope._lock:
            scope.local_vars[key] = value
            scope._provenance[key] = f"scope_{scope._id}_L{scope.depth}"
            if lock: scope._locks.add(key)

            # Merkle Update
            payload = str(value).encode('utf-8', errors='ignore')
            scope._merkle_chain.append(hashlib.md5(f"{key}:".encode() + payload).hexdigest())

        HUDMulticaster.radiate(scope, key, value)

    @classmethod
    def set_global(cls, scope: 'LexicalScope', key: str, value: Any):
        """[ASCENSION 3]: Mutates the Prime Timeline directly."""
        with scope._lock:
            scope.global_ctx.variables[key] = value
            HUDMulticaster.radiate(scope, key, value)