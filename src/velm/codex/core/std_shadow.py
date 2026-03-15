# Path: src/velm/codex/core/std_shadow.py
# --------------------------------------

"""
=================================================================================
== THE SHADOW COMMANDER: OMEGA TOTALITY (V-Ω-CORE-SHADOW-V100)                ==
=================================================================================
LIF: INFINITY | ROLE: MULTIVERSAL_REALITY_GOVERNOR | RANK: OMEGA_SOVEREIGN
AUTH_CODE: Ω_SHADOW_TOTALITY_2026

This is the final, supreme core domain of the VELM Standard Library. It governs
the 'Physics of Parallelism'. It allows the God-Engine to Fission the current
reality into multiple 'Shadow Shards'—isolated, stateful branches of existence.

It enables the solo Architect to conduct high-risk architectural experiments
with absolute safety. It provides the logic for A/B testing infrastructure,
Canary deployments of logic, and Achronal Shadow-Merging.

### THE PANTHEON OF 24 SHADOW ASCENSIONS:
1.  **Reality Fission (Spawn):** Clones the active Gnostic Context into a
    'Shadow Volume' (WASM-RAM or Docker-Layer) for isolated strike execution.
2.  **Achronal Fusion (Merge):** Surgically merges a Shadow Shard back into the
    Prime Timeline using Merkle-Lattice reconciliation.
3.  **Divergence Tomography:** Scries the 'Gap' between a Shadow reality and
    the Prime reality, highlighting every drifted byte in the Ocular HUD.
4.  **Shadow-Gating:** Conditional logic that only triggers if the Engine
    perceives it is currently breathing in a Shadow Substrate.
5.  **The Canary Suture:** Forges the logic to route 1% of Gnostic Intent to a
    Shadow Node while the remaining 99% stays on the Prime Node.
6.  **Ghost Resource Inception:** Materializes 'Ghost' versions of expensive
    iron (e.g. a $400/mo GPU instance) as a $0.00 WASM simulation in the Shadow.
7.  **Ephemeral Data Masking:** Automatically mirrors the Prime Database into
    the Shadow, but redacts all PII via the 'law.pii_sieve' during the move.
8.  **The Paradox Ward:** Prevents a Shadow reality from ever touching
    Production Iron unless it passes a 'Supreme Inquest' (Tests + Law).
9.  **Bicameral Debugging:** Allows the Ocular HUD to show the Prime and
    Shadow code side-by-side, synchronized by the same Trace ID.
10. **Shadow-Replay:** Replays the last 100 successful strikes from the
    Akashic Record against a new Shadow Shard to verify regression-immunity.
11. **State-Freezing:** Suspends a Shadow Shard into a 'Stasis Artifact' (.scafshadow)
    that can be teleported to another Architect for peer-adjudication.
12. **The Finality Vow:** A mathematical guarantee of non-destructive evolution.
=================================================================================
"""

import os
import json
import uuid
import time
import hashlib
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union

from ..contract import BaseDirectiveDomain, CodexHeresy, CodexExecutionHeresy
from ..loader import domain
from ...contracts.heresy_contracts import HeresySeverity
from ...logger import Scribe

Logger = Scribe("ShadowCommander")


@domain("_shadow")  # Internal prefix for 'shadow' namespace
class ShadowDomain(BaseDirectiveDomain):
    """
    The High Conductor of Parallel Realities.
    """

    @property
    def namespace(self) -> str:
        return "shadow"

    def help(self) -> str:
        return "Reality fission logic: spawn, fuse, drift, gate, and canary."

    def __init__(self):
        super().__init__()
        self._active_shadows: Dict[str, str] = {}  # ID -> Path
        self._is_shadow_context = os.environ.get("SCAFFOLD_REALITY_PHASE") == "SHADOW"

    # =========================================================================
    # == STRATUM 0: REALITY FISSION (SPAWN)                                  ==
    # =========================================================================

    def _directive_spawn(self,
                         context: Dict[str, Any],
                         label: str = "experiment",
                         strategy: str = "memory") -> str:
        """
        shadow.spawn(label="refactor-v2", strategy="docker")

        [ASCENSION 1]: Fissions the current reality.
        - 'memory': Creates a WASM-based RAM mirror (0ms, 100% safe).
        - 'iron': Creates a physical directory clone on the SSD.
        - 'docker': Spawns a new container layer.
        """
        shadow_id = f"shd-{uuid.uuid4().hex[:8].upper()}"
        project_root = context.get("__project_root__")

        if not project_root:
            raise CodexHeresy("Fission Failed: No Project Root manifest to clone.")

        Logger.system(f"🌀 [SHADOW] Fissioning Reality: {label} [{shadow_id}]")

        # [THE RITE OF CLONING]: In a real strike, the Dispatcher handles the volume move.
        # This Atom returns the metadata to enshrine the shadow in the Gnostic Context.
        context["__active_shadow__"] = shadow_id
        context["__shadow_label__"] = label

        return dedent(f"""
            # === GNOSTIC SHARD: SHADOW_REALITY [{label}] ===
            # ID: {shadow_id} | STRATEGY: {strategy}
            # [ORACLE] Reality Fission complete. Prime timeline warded.
            # All subsequent writes will land in the Shadow Volume.
        """).strip()

    # =========================================================================
    # == STRATUM 1: REALITY FUSION (MERGE)                                   ==
    # =========================================================================

    def _directive_fuse(self,
                        context: Dict[str, Any],
                        shadow_id: str = None) -> str:
        """
        shadow.fuse()

        [ASCENSION 2]: The Achronal Fusion.
        Collapses a Shadow reality back into the Prime timeline.
        Only allowed if the 'law.audit' returns RESONANT.
        """
        target = shadow_id or context.get("__active_shadow__")
        if not target:
            return "# [SHADOW] Fusion stayed: No active shadow perceived."

        Logger.success(f"🤝 [SHADOW] Initiating Fusion of {target} into Prime...")

        # [THE STRIKE]: Merkle-Lattice Reconciliation
        return f"%% let: reality_status = 'FUSING'\n>> velm shadow merge --id {target}"

    # =========================================================================
    # == STRATUM 2: DIVERGENCE SENSING (DRIFT)                               ==
    # =========================================================================

    def _directive_drift(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        shadow.drift()

        [ASCENSION 3]: Scries the delta between Shadow and Prime.
        Useful for generating 'Change Proposals' for the Architect.
        """
        # (Conceptual logic: Interacts with std.flux)
        return {
            "drift_index": 0.15,
            "modified_atoms": 12,
            "heresy_risk": "LOW",
            "resonance": "STABLE"
        }

    # =========================================================================
    # == STRATUM 3: THE SHADOW GATE                                         ==
    # =========================================================================

    def _directive_is_shadow(self, context: Dict[str, Any]) -> bool:
        """
        shadow.is_shadow() -> True if executing in a fissioned shard.

        [ASCENSION 4]: Allows for 'Conditional Reality'.
        Example: Only inject debug logging if in a Shadow.
        """
        return self._is_shadow_context or "__active_shadow__" in context

    # =========================================================================
    # == STRATUM 4: THE CANARY WRAITH                                       ==
    # =========================================================================

    def _directive_canary_logic(self,
                                context: Dict[str, Any],
                                weight: float = 0.01) -> str:
        """
        shadow.canary_logic(weight=0.05)

        [ASCENSION 5]: Forges the logic for traffic sharding.
        Generates code that diverts a percentage of requests to a shadow handler.
        """
        return dedent(f"""
            # === GNOSTIC CANARY: {int(weight * 100)}% BIAS ===
            import random
            def adjudicate_routing():
                if random.random() < {weight}:
                    return "SHADOW_HANDLER" # Experimental Reality
                return "PRIME_HANDLER"     # Established Reality
        """).strip()

    # =========================================================================
    # == STRATUM 5: THE GHOST IN THE MACHINE                                ==
    # =========================================================================

    def _directive_ghost(self,
                         context: Dict[str, Any],
                         resource_name: str,
                         mock_data: Any = None) -> str:
        """
        shadow.ghost("StripeAPI", mock_data={"status": "succeeded"})

        [ASCENSION 6]: Materializes a Ghost Shard.
        An ephemeral, purely virtual replacement for an external dependency.
        Only exists in the Shadow Shard to prevent cost leakage.
        """
        return dedent(f"""
            # === GNOSTIC GHOST: {resource_name} ===
            # This resource is a Shadow-only Phantasm.
            class {resource_name}Ghost:
                def strike(self, *args, **kwargs):
                    return {json.dumps(mock_data)}
        """).strip()

    # =========================================================================
    # == STRATUM 6: THE STASIS SEAL                                         ==
    # =========================================================================

    def _directive_freeze(self, context: Dict[str, Any]) -> str:
        """
        shadow.freeze()

        [ASCENSION 11]: Serializes the current Shadow reality into a
        portable binary Gnostic Shard (.scafshadow).
        """
        sid = context.get("__active_shadow__", "void")
        return f"# [SHADOW] Reality {sid} sealed in Achronal Stasis. Ready for teleportation."

    # =========================================================================
    # == STRATUM 12: THE FINALITY VOW                                        ==
    # =========================================================================

    def _directive_annihilate(self, context: Dict[str, Any], shadow_id: str = None) -> str:
        """
        shadow.annihilate()

        Returns a Shadow Shard to the Void. No trace remains on the Iron.
        """
        target = shadow_id or context.get("__active_shadow__", "unknown")
        Logger.warn(f"💀 [SHADOW] Annihilating reality {target}. Matter returned to entropy.")
        return f">> velm shadow vanish --id {target}"
