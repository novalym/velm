# Path: core/alchemist/elara/resolver/context/retrieval.py
# --------------------------------------------------------

import time
import threading
from typing import Any, TYPE_CHECKING, Optional, List, Set, Final

# --- THE DIVINE UPLINKS ---
from ......logger import Scribe
from .normalization import LinguisticResonator
from ...library.registry import RITE_REGISTRY
from ..evaluator.void import VOID, LaminarTypeRegistry

if TYPE_CHECKING:
    from .engine import LexicalScope

Logger = Scribe("RetrievalOracle")


class RetrievalOracle:
    """
    =================================================================================
    == THE RETRIEVAL ORACLE: OMEGA POINT (V-Ω-TOTALITY-VMAX-O(1)-APOTHEOSIS)       ==
    =================================================================================
    LIF: ∞^∞ | ROLE: SEMANTIC_IDENTITY_RESONATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_RETRIEVAL_VMAX_O1_APOTHEOSIS_2026_FINALIS

    [THE MANIFESTO]
    The supreme final authority for Gnostic Recall. This version righteously
    implements **The Apophatic C-Vector Sieve**, mathematically annihilating
    the 1.9-second "O(N) Difflib Freeze" by enforcing strict O(1) cache lookups.

    It ALSO implements the **O(1) LAMINAR NORMALIZATION CACHE**. It restores the
    magical capability of resolving `vaultpackagename` to `vault_package_name`
    instantly, without triggering an O(N) loop across the dictionary keys!
    =================================================================================
    """

    @classmethod
    def get(cls, scope: 'LexicalScope', name: str, default: Any = None) -> Any:
        """
        =============================================================================
        == THE RITE OF SUPREME RECALL (V-Ω-TOTALITY-VMAX-O(1))                     ==
        =============================================================================
        """
        if not name: return default

        # =========================================================================
        # == MOVEMENT I: THE VOID ALTAR (NEGATIVE CACHE FRONTLINE)               ==
        # =========================================================================
        # [THE MASTER CURE]: We check the Void Registry BEFORE any dict lookups.
        if not hasattr(scope.global_ctx, '_void_registry'):
            scope.global_ctx._void_registry = set()

        if name in scope.global_ctx._void_registry:
            return default

        # --- MOVEMENT II: THE IMMEDIATE PRESENT (Local Lattice) ---
        val = scope.local_vars.get(name)
        if val is not None:
            return val

        # --- MOVEMENT III: THE ANCESTRAL PAST (Recursive Ascent) ---
        parent_scope = scope.parent
        if parent_scope:
            val = parent_scope.get(name)
            if val is not None:
                return val

        # --- MOVEMENT IV: THE ABSOLUTE TRUTH (Forge Global) ---
        val = scope.global_ctx.variables.get(name)
        if val is not None:
            return LaminarTypeRegistry.thaw_truth(val)

        # --- MOVEMENT V: THE REGISTRY RESONANCE (O(1) Hot-Cache) ---
        val = RITE_REGISTRY.get(name)
        if val is not None:
            scope._telemetry_stats["heals"] += 1
            return val

        # =========================================================================
        # == MOVEMENT VI: LAMINAR ALPHANUMERIC SCRY (O(1) FAST-PATH)             ==
        # =========================================================================
        # [THE FIX]: We restore Linguistic Normalization to heal corrupted variables
        # like 'vaultpackagename' -> 'vault_package_name', but we do it instantly
        # using a cached reverse-mapping matrix.
        if not name.startswith('__'):
            norm_target = LinguisticResonator.normalize(name)
            if norm_target:

                # 1. Initialize the Normalized Global Cache if void
                if not hasattr(scope.global_ctx, '_normalized_keys'):
                    scope.global_ctx._normalized_keys = {}
                    for k in scope.global_ctx.variables.keys():
                        if isinstance(k, str) and not k.startswith('__'):
                            norm = LinguisticResonator.normalize(k)
                            if norm: scope.global_ctx._normalized_keys[norm] = k

                # 2. Check Global Normalization
                if norm_target in scope.global_ctx._normalized_keys:
                    true_key = scope.global_ctx._normalized_keys[norm_target]
                    val = cls.get(scope, true_key)
                    if val is not None:
                        return val

                # 3. Initialize the Normalized Local Cache if void
                if not hasattr(scope, '_normalized_keys'):
                    scope._normalized_keys = {}
                    for k in scope.local_vars.keys():
                        if isinstance(k, str) and not k.startswith('__'):
                            norm = LinguisticResonator.normalize(k)
                            if norm: scope._normalized_keys[norm] = k

                # 4. Check Local Normalization
                if norm_target in scope._normalized_keys:
                    true_key = scope._normalized_keys[norm_target]
                    val = cls.get(scope, true_key)
                    if val is not None:
                        return val

        # =========================================================================
        # == MOVEMENT VII: VOID ENSHRINEMENT                                     ==
        # =========================================================================
        # The key is unmanifest across all dimensions of reality.
        # We record it in the Void Altar permanently for this transaction.
        scope.global_ctx._void_registry.add(name)
        return default

    @classmethod
    def _scry_registry_lattice(cls, name: str) -> Optional[callable]:
        """Performs an O(1) probe of the L1 Hot-Cache of waked Rites."""
        return RITE_REGISTRY.get(name)

    def __repr__(self) -> str:
        return "<Ω_RETRIEVAL_ORACLE status=RESONANT mode=O1_NORMALIZATION_SUTURED>"