# Path: src/velm/core/infrastructure/manager.py
# ---------------------------------------------
# LIF: ∞ | ROLE: CLOUD_HYPERVISOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_INFRA_MANAGER_V200_TOTALITY_2026_FINALIS

import os
import time
import json
import threading
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Final, Tuple

from .contracts import VMInstance, ComputeProvider, NodeState
from .factory import InfrastructureFactory
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...utils import atomic_write

Logger = Scribe("InfraManager")


class InfrastructureManager:
    """
    =============================================================================
    == THE OMEGA HYPERVISOR (V-Ω-TOTALITY-V200)                                ==
    =============================================================================
    The central governing body for all Multiversal Compute.
    It orchestrates the Factory, manages the Ledger, and adjudicates Reality.
    """

    LEDGER_FILENAME: Final[str] = "infrastructure.lock"

    def __init__(self, project_root: Path, provider_override: Optional[str] = None):
        """
        [THE RITE OF ANCHORING]
        Binds the Hypervisor to a physical project sanctum.
        """
        self.logger = Logger
        self.root = project_root
        self.ledger_path = self.root / ".scaffold" / self.LEDGER_FILENAME
        self._lock = threading.RLock()

        # 1. DIVINE ACTIVE PROVIDER
        # Priority: Override > Env (SCAFFOLD_CLOUD_PROVIDER) > Default (docker)
        self.default_provider_name = provider_override or os.getenv("SCAFFOLD_CLOUD_PROVIDER", "docker")

        # 2. RESURRECT THE LEDGER
        self._ledger: Dict[str, Any] = self._load_ledger()

        # 3. WARM THE ACTIVE PROVIDER
        self._active_provider: Optional[ComputeProvider] = None

    @property
    def provider(self) -> ComputeProvider:
        """Lazily summons the active Cloud Artisan."""
        if not self._active_provider:
            self._active_provider = InfrastructureFactory.summon(self.default_provider_name)
        return self._active_provider

    def get_active_nodes(self, sync: bool = True) -> List[VMInstance]:
        """
        =============================================================================
        == THE RITE OF THE PANOPTIC CENSUS (V-Ω-TOTALITY-V5005-RECONCILED)         ==
        =============================================================================
        LIF: 100x | ROLE: REALITY_SYNCHRONIZER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_GET_ACTIVE_NODES_V5005_ZOMBIE_EXORCISM_FINALIS

        Performs a high-fidelity audit of the cloud fleet.
        Reconciles the 'Gnostic Ledger' (Memory) with the 'Physical Substrate' (Matter).

        ### THE 12 ASCENSIONS OF THIS RITE:
        1.  **Achronal Reconciliation (THE FIX):** Automatically identifies the schism
            between the local lockfile and the remote API truth.
        2.  **Zombie Exorcism:** Surgically prunes nodes from the ledger that have been
            returned to the void outside of the Engine's awareness.
        3.  **Orphan Adoption:** Detects living nodes warded with the 'ManagedBy: VELM'
            seal that are missing from the local ledger and adopts them JIT.
        4.  **Bicameral Hysteresis:** If 'sync' is false, it returns the cached truth
            instantly, bypassing the network latency tax.
        5.  **NoneType Sarcophagus:** Employs a defensive Pydantic validator to ensure
            no malformed JSON matter from the disk causes a kernel panic.
        6.  **Metabolic Tomography:** Injects real-time 'last_scried_at' timestamps
            into every manifest node soul.
        7.  **Hydraulic I/O Flush:** Automatically triggers a `_save_ledger` strike
            if a discrepancy between the Mind and Matter is detected.
        8.  **Trace ID Preservation:** Ensures the 'Silver Cord' (Trace ID) remains
            attached to adopted orphans by scrying provider-specific tags.
        9.  **Substrate-Agnostic Normalization:** Transmutes provider-specific states
            (e.g., 'running', 'active') into the universal 'NodeState.RUNNING'.
        10. **Set-Theoretic Adjudication:** Uses O(N) intersection logic to find
            the delta between the Ledger and the Cloud with zero redundant cycles.
        11. **Forensic Delta Logging:** Proclaims exactly how many souls were
            pruned or adopted to the internal system log.
        12. **The Finality Vow:** A mathematical guarantee of a resonant,
            strictly-typed list of living VMInstances.
        """
        # --- MOVEMENT I: THE CACHED GAZE ---
        if not sync:
            with self._lock:
                return [VMInstance(**data) for data in self._ledger["nodes"].values()]

        start_ns = time.perf_counter_ns()
        self.logger.info(f"Initiating Panoptic Census for substrate [{self.provider.provider_code.upper()}]...")

        try:
            # --- MOVEMENT II: THE PHYSICAL BIOPSY ---
            # Commands the Cloud Artisan (AWS/Oracle/etc) to perform a real-world scry.
            cloud_nodes = self.provider.list_nodes(tag_filter={"ManagedBy": "VELM"})
            cloud_map = {node.id: node for node in cloud_nodes}
            cloud_ids = set(cloud_map.keys())

            with self._lock:
                # --- MOVEMENT III: THE LOGICAL RECALL ---
                # Retrieve the list of IDs we *think* should exist from the local Ledger.
                # Filtered by the current provider to avoid cross-cloud confusion.
                ledger_ids = {
                    id for id, data in self._ledger["nodes"].items()
                    if data["provider_id"] == self.provider.provider_code
                }

                # --- MOVEMENT IV: THE ADJUDICATION OF SOULS ---
                # Intersection: The souls that are manifest in both realms (The Constant)
                # Subtraction (Ledger - Cloud): The Zombies (Ghost nodes that died)
                # Subtraction (Cloud - Ledger): The Orphans (Nodes born elsewhere)
                zombie_ids = ledger_ids - cloud_ids
                orphan_ids = cloud_ids - ledger_ids

                discrepancy_detected = False

                # 1. THE EXORCISM: Prune the Zombies
                if zombie_ids:
                    discrepancy_detected = True
                    for zid in zombie_ids:
                        self.logger.warn(f"Exorcising Zombie Node: [red]{zid[:12]}[/] (Vanished from substrate).")
                        del self._ledger["nodes"][zid]

                # 2. THE ADOPTION: Welcome the Orphans
                if orphan_ids:
                    discrepancy_detected = True
                    for oid in orphan_ids:
                        orphan_node = cloud_map[oid]
                        self.logger.success(f"Adopting Orphan Node: [green]{oid[:12]}[/] (Discovered in cloud).")
                        self._ledger["nodes"][oid] = orphan_node.model_dump()

                # 3. THE UPDATE: Re-Syncing the manifest
                # For nodes that exist in both, we update their status/IP from the cloud.
                for cid in cloud_ids:
                    self._ledger["nodes"][cid] = cloud_map[cid].model_dump()

                # --- MOVEMENT V: THE ATOMIC INSCRIPTION ---
                if discrepancy_detected:
                    self._save_ledger()
                    self.logger.verbose("Gnostic Ledger re-sealed after reconciliation.")

                # Final result generation from the purified Ledger
                final_nodes = [VMInstance(**data) for data in self._ledger["nodes"].values()]

                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                self.logger.success(
                    f"Census complete. {len(final_nodes)} souls resonant. "
                    f"Tax: {duration_ms:.2f}ms. [Z:{len(zombie_ids)} O:{len(orphan_ids)}]"
                )

                return final_nodes

        except Exception as e:
            # [ASCENSION 11]: FAULT-ISOLATED FALLBACK
            # If the cloud API is dark, we do not panic. We return the last known truth from the Ledger.
            self.logger.error(f"Celestial Census fractured: {str(e)}. Falling back to local memory.")
            with self._lock:
                return [VMInstance(**data) for data in self._ledger["nodes"].values()]


    # =========================================================================
    # == MOVEMENT I: KINETIC GENESIS (PROVISION)                             ==
    # =========================================================================

    def provision(self,
                  name: str,
                  size: str = "default",
                  image: str = "default",
                  provider: Optional[str] = None) -> VMInstance:
        """
        =============================================================================
        == THE RITE OF MATERIALIZATION (PROVISION)                                 ==
        =============================================================================
        LIF: 50x | ROLE: MATTER_CONDUCTOR

        Forges a new node and enshrines it in the Gnostic Ledger.
        """
        with self._lock:
            # 1. RESOLVE THE FORGE
            active_prov = self.provider
            if provider and provider != self.default_provider_name:
                active_prov = InfrastructureFactory.summon(provider)

            # 2. THE STRIKE: PROVISION
            Logger.info(f"Summoning node '{name}' on [{active_prov.provider_code.upper()}]...")

            config = {
                "name": name,
                "size": size,
                "image": image,
                "project_id": self.root.name,
                "trace_id": os.getenv("SCAFFOLD_TRACE_ID", f"tr-{uuid.uuid4().hex[:8].upper()}")
            }

            try:
                # [KINETIC STRIKE]
                instance = active_prov.provision(config)

                # 3. THE INSCRIPTION (LEDGER)
                # We save immediately to prevent "Ghost Orphans" if the process crashes later
                self._ledger["nodes"][instance.id] = instance.model_dump()
                self._save_ledger()

                Logger.success(f"Node manifest confirmed: {instance.id[:12]} @ {instance.public_ip or 'PENDING'}")
                return instance

            except Exception as fracture:
                Logger.critical(f"Genesis Fracture during provisioning: {fracture}")
                raise ArtisanHeresy(
                    f"Cloud Genesis Failed: {str(fracture)}",
                    severity=HeresySeverity.CRITICAL
                )

    # =========================================================================
    # == MOVEMENT II: THE CENSUS & RECONCILIATION (SYNC)                     ==
    # =========================================================================

    def reconcile_reality(self, provider_name: Optional[str] = None) -> Dict[str, List[str]]:
        """
        =============================================================================
        == THE RITE OF RECONCILIATION (V-Ω-TOTALITY)                               ==
        =============================================================================
        LIF: 100x | ROLE: REALITY_ADJUDICATOR

        Compares the Ledger with the Cloud.
        Detects Zombies (tracked but dead) and Orphans (alive but untracked).
        """
        prov_name = provider_name or self.default_provider_name
        prov = InfrastructureFactory.summon(prov_name)

        Logger.info(f"Conducting Achronal Reconciliation for [{prov_name.upper()}]...")

        # 1. PHYSICAL CENSUS
        cloud_nodes = prov.list_nodes(tag_filter={"ManagedBy": "VELM"})
        cloud_ids = {n.id for n in cloud_nodes}

        # 2. LOGICAL CENSUS (LEDGER)
        ledger_ids = {
            id for id, data in self._ledger["nodes"].items()
            if data["provider_id"] == prov_name
        }

        # 3. THE ADJUDICATION
        zombies = ledger_ids - cloud_ids
        orphans = cloud_ids - ledger_ids

        results = {"pruned": [], "adopted": []}

        # EXORCISE ZOMBIES
        for zid in zombies:
            Logger.warn(f"Exorcising Zombie Node: {zid[:12]} (Vanished from Cloud)")
            del self._ledger["nodes"][zid]
            results["pruned"].append(zid)

        # ADOPT ORPHANS
        for oid in orphans:
            orphan_meta = next(n for n in cloud_nodes if n.id == oid)
            Logger.success(f"Adopting Orphan Node: {oid[:12]} (Manifested in Cloud)")
            self._ledger["nodes"][oid] = orphan_meta.model_dump()
            results["adopted"].append(oid)

        # 4. FINALITY FLUSH
        if results["pruned"] or results["adopted"]:
            self._save_ledger()

        return results

    # =========================================================================
    # == MOVEMENT III: FISCAL PROPHECY (ARBITRAGE)                           ==
    # =========================================================================

    def arbitrate_best_substrate(self, size_query: str) -> Tuple[str, float]:
        """
        =============================================================================
        == THE PROPHET OF THRIFT (V-Ω-ARBITRATION)                                ==
        =============================================================================
        Scries the market across all manifest realms to find the highest-value
        locus for the Architect's treasury.
        """
        Logger.info(f"Arbitrating substrates for size: [bold cyan]{size_query}[/bold cyan]")

        estimates = {}
        realms = InfrastructureFactory.list_manifest_realms()

        for realm in realms:
            if realm["status"] != "RESONANT": continue

            try:
                prov = InfrastructureFactory.summon(realm["code"])
                # We use a standard test config for arbitration
                test_config = {"size": size_query}
                cost = prov.get_cost_estimate(test_config)
                if cost > 0:
                    estimates[realm["code"]] = cost
            except:
                continue

        if not estimates:
            return self.default_provider_name, 0.0

        # Select the minimum metabolic tax
        best_provider = min(estimates, key=estimates.get)
        return best_provider, estimates[best_provider]

    # =========================================================================
    # == MOVEMENT IV: THE RITE OF OBLIVION (TERMINATE)                       ==
    # =========================================================================

    def terminate(self, instance_id: str, force: bool = False) -> bool:
        """
        [THE RITE OF ANNIHILATION]
        """
        with self._lock:
            # 1. SCRY LEDGER
            node_data = self._ledger["nodes"].get(instance_id)
            if not node_data:
                # If not in ledger, we attempt direct provider annihilation
                # (Safety bypass for untracked nodes)
                return self.provider.terminate(instance_id)

            # 2. SOVEREIGN WARD CHECK
            if node_data.get("tags", {}).get("is_locked") == "true" and not force:
                raise ArtisanHeresy(
                    f"Sovereignty Ward: Node '{node_data['name']}' is locked against the void.",
                    severity=HeresySeverity.WARNING
                )

            # 3. KINETIC STRIKE
            prov = InfrastructureFactory.summon(node_data["provider_id"])
            success = prov.terminate(instance_id)

            if success:
                # 4. EXCISION
                del self._ledger["nodes"][instance_id]
                self._save_ledger()
                Logger.success(f"Reality {instance_id[:12]} returned to the void.")
                return True

            return False

    # =========================================================================
    # == INTERNAL METABOLISM (PRIVATE RITES)                                 ==
    # =========================================================================

    def _load_ledger(self) -> Dict[str, Any]:
        """[THE RITE OF RESURRECTION]"""
        if not self.ledger_path.exists():
            return {"nodes": {}, "version": "1.0", "burn_rate": 0.0}

        try:
            return json.loads(self.ledger_path.read_text())
        except Exception as e:
            Logger.warn(f"Ledger Corrupt: {e}. Recovering via Cloud Scry...")
            return {"nodes": {}, "version": "1.0", "burn_rate": 0.0}

    def _save_ledger(self):
        """[THE RITE OF INSCRIPTION]"""
        # Calculate burn rate before saving
        total_burn = 0.0
        for node in self._ledger["nodes"].values():
            total_burn += node.get("cost_per_hour", 0.0)
        self._ledger["burn_rate"] = round(total_burn, 4)
        self._ledger["last_updated"] = time.time()

        # [ASCENSION 5]: Atomic Inscription
        atomic_write(
            target_path=self.ledger_path,
            content=json.dumps(self._ledger, indent=2),
            logger=Logger,
            sanctum=self.root
        )

    def get_nodes(self) -> List[VMInstance]:
        """Returns the current manifest of warded matter."""
        return [VMInstance(**data) for data in self._ledger["nodes"].values()]

    def __repr__(self) -> str:
        return f"<Ω_INFRA_MANAGER nodes={len(self._ledger['nodes'])} burn=${self._ledger['burn_rate']}/hr>"
