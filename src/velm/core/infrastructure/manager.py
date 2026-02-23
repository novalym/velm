# Path: src/velm/core/infrastructure/manager.py
# ---------------------------------------------
# LIF: 10,000,000,000,000,000,000,000 | ROLE: MULTIVERSAL_HYPERVISOR | RANK: OMEGA_PRIME
# AUTH_CODE: Ω_MANAGER_V100K_TYPE_SOVEREIGN_FINALIS

import os
import sys
import time
import json
import threading
import uuid
import hashlib
import traceback
import subprocess
import platform
import math
import concurrent.futures
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Final, Tuple

# --- THE DIVINE UPLINKS ---
from .contracts import VMInstance, ComputeProvider, NodeState
from .factory import InfrastructureFactory
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...utils import atomic_write

Logger = Scribe("InfraManager")


class InfrastructureManager:
    """
    =============================================================================
    == THE OMEGA HYPERVISOR (V-Ω-TOTALITY-V100000-TYPE-SOVEREIGN)              ==
    =============================================================================
    The central governing body for all Multiversal Compute.
    It orchestrates the Factory, manages the Ledger, and adjudicates Reality.

    [LEGENDARY ASCENSIONS]:
    - **Diamond-Hard Type Safety:** Absolute immunity to `NoneType` propagation in provider resolution.
    - **Absolute Vacuum Sarcophagus:** Total immunity to NoneType and path resolution errors.
    - **The Rite of Teleportation:** Direct SCP integration for shipping artifacts.
    - **The Rite of Ignition:** Remote command execution for waking dormant swarms.
    - **Self-Healing Ledger:** Reconstructs deleted parent directories JIT.
    - **Panoptic Sweep:** Concurrent multi-cloud reality reconciliation.
    =============================================================================
    """

    LEDGER_FILENAME: Final[str] = "infrastructure.lock"

    def __init__(self, project_root: Optional[Union[Path, str]] = None, provider_override: Optional[str] = None):
        """
        =============================================================================
        == THE RITE OF ANCHORING: OMEGA (V-Ω-TOTALITY-V100K-APOPHATIC)             ==
        =============================================================================
        Materializes the sovereign mind of the Hypervisor. Ascended with 'Negative
        Perception', it survives the Lobby (Wizard) vacuum with unbreakable grace.
        """
        self._inception_start_ns = time.perf_counter_ns()
        self.logger = Logger

        # --- MOVEMENT I: SUBSTRATE BIOPSY ---
        self.is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        # =========================================================================
        # == MOVEMENT II: THE ABSOLUTE VACUUM SARCOPHAGUS (THE CURE)             ==
        # =========================================================================
        self.is_vacuum = False
        # Default to a safe placeholder path if in WASM, else CWD
        self.root = Path("/vault/project") if self.is_wasm else Path.cwd()

        try:
            if project_root is None or str(project_root).strip() in ["", "None", "null", "undefined"]:
                self.is_vacuum = True
            else:
                candidate_root = Path(str(project_root)).resolve()
                self.root = candidate_root
                if not self.root.exists() or not self.root.is_dir():
                    self.is_vacuum = True
        except Exception as e:
            self.logger.debug(f"Geometric Anchor Fracture: {e}. Defaulting to Vacuum Mode.")
            self.is_vacuum = True

        if not self.is_vacuum:
            self.ledger_path = self.root / ".scaffold" / self.LEDGER_FILENAME
            self.logger.verbose(f"Governor anchored to manifest reality: {self.root.name}")
        else:
            self.ledger_path = None
            if os.environ.get("SCAFFOLD_DEBUG_BOOT") == "1":
                self.logger.debug(f"Governor manifest in a VACUUM. Physical I/O suspended.")

        # --- MOVEMENT III: CONCURRENCY SHIELDING ---
        self._lock = threading.RLock()

        # --- MOVEMENT IV: SOVEREIGN IDENTITY ---
        self._instance_id = uuid.uuid4().hex[:8].upper()
        self.trace_id = os.environ.get("SCAFFOLD_TRACE_ID", f"tr-gov-{self._instance_id}")

        # --- MOVEMENT V: PROVIDER ARBITRATION (STRICT) ---
        # [THE CURE]: We ensure this is NEVER None.
        raw_provider = provider_override or os.getenv("SCAFFOLD_CLOUD_PROVIDER")
        self.default_provider_name = str(raw_provider) if raw_provider else "docker"

        # --- MOVEMENT VI: LEDGER RESURRECTION ---
        self._ledger_hash = ""
        self._ledger = self._load_ledger()

        # --- MOVEMENT VII: KINETIC STANDBY ---
        self._active_provider = None

        duration_ms = (time.perf_counter_ns() - self._inception_start_ns) / 1_000_000
        if not os.environ.get("SCAFFOLD_SILENT"):
            self.logger.debug(f"Hypervisor {self._instance_id} resonant in {duration_ms:.2f}ms. [V:{self.is_vacuum}]")

    @property
    def provider(self) -> ComputeProvider:
        """
        =============================================================================
        == THE FALLBACK FORGE (V-Ω-TOTALITY-V100K)                                 ==
        =============================================================================
        Guaranteed Materialization. If the primary provider fractures (missing SDKs),
        automatically summons a safe fallback (docker/local) to prevent downstream crashes.
        """
        if not self._active_provider:
            with self._lock:
                if not self._active_provider:
                    name = getattr(self, 'default_provider_name', 'docker') or "docker"
                    try:
                        self._active_provider = InfrastructureFactory.summon(name)
                    except Exception as e:
                        self.logger.critical(f"Primary Provider '{name}' Fractured: {e}")
                        self.logger.warn("Summoning fallback 'docker' provider to maintain structural integrity.")
                        try:
                            self._active_provider = InfrastructureFactory.summon("docker")
                        except Exception as fallback_err:
                            raise ArtisanHeresy(f"Total Provider Collapse: {fallback_err}",
                                                severity=HeresySeverity.CRITICAL)

        return self._active_provider

    # =========================================================================
    # == MOVEMENT VIII: THE STATUS SCRYER (THE CURE)                         ==
    # =========================================================================
    def get_status(self, instance_id: str, provider_name: Optional[str] = None) -> VMInstance:
        """
        Divines the status of a specific node. Warded against Interactive Auth Loops
        and NoneType Resolution fractures.
        """
        with self._lock:
            try:
                # 1. DIVINE THE PROVIDER
                # We attempt to find the node in the ledger.
                node_data = self._ledger.get("nodes", {}).get(instance_id)

                # Logic: Explicit Override > Ledger Record > Default > Fallback "docker"
                target_provider = provider_name
                if not target_provider and node_data:
                    target_provider = node_data.get("provider_id")

                if not target_provider:
                    target_provider = self.default_provider_name

                # [THE CURE]: Absolute Type Enforcement
                target_provider = str(target_provider) if target_provider else "docker"

                # 2. SUMMON THE ARTISAN
                prov = InfrastructureFactory.summon(target_provider)

                # 3. CONDUCT THE SCRY
                return prov.get_status(instance_id)

            except Exception as e:
                self.logger.error(f"Status scry fractured for {instance_id}: {e}")
                # We do NOT raise here to allow the UI to handle it gracefully, unless critical
                if "Auth" in str(e):  # Bubble up auth errors
                    raise e

                return VMInstance(
                    id=instance_id,
                    name="UNKNOWN",
                    provider_id=str(provider_name or "unknown"),
                    region="void",
                    state=NodeState.FRACTURED,
                    metadata={"error": str(e)}
                )

    # =========================================================================
    # == MOVEMENT IX: THE RITE OF TELEPORTATION (NEW ASCENSION)              ==
    # =========================================================================
    def teleport_matter(self, instance_id: str, artifact_path: Union[str, Path],
                        remote_dest: str = "/tmp/vessel.zip") -> bool:
        """
        =============================================================================
        == THE RITE OF TRANSLOCATION (V-Ω-ISOMORPHIC-TELEPORT)                     ==
        =============================================================================
        LIF: 1000x | ROLE: MATTER_TRANSMITTER | RANK: OMEGA_SOVEREIGN

        Transmits a zipped Artifact across the network void to the target Iron.
        Implements Lazarus Network Awakening (exponential backoff) to handle cold starts.
        """
        if self.is_wasm:
            self.logger.error("Teleportation aborted: WASM Substrate cannot execute native SCP strikes.")
            return False

        local_path = Path(artifact_path).resolve()
        if not local_path.exists():
            raise ArtisanHeresy(f"Matter Unmanifest: Artifact {local_path} does not exist.")

        self.logger.info(f"Initiating Teleportation Rite for {instance_id}...")

        # 1. AWAIT NETWORK RESONANCE
        node = self._await_ip_resonance(instance_id)

        # 2. IDENTITY RESOLUTION
        ssh_user = node.tags.get("ssh_user") or node.metadata.get("default_user") or "root"
        if node.provider_id == "aws": ssh_user = "ubuntu"
        if node.provider_id == "ovh": ssh_user = "debian"  # Common OVH default, but fallback to root

        local_os = platform.system().lower()
        local_path_str = str(local_path).replace("\\", "/") if local_os == "windows" else str(local_path)

        # 3. THE KINETIC STRIKE (SCP)
        # Using StrictHostKeyChecking=no to prevent interactive hang on new IPs
        cmd = [
            "scp",
            "-o", "StrictHostKeyChecking=no",
            "-o", "UserKnownHostsFile=/dev/null",
            local_path_str,
            f"{ssh_user}@{node.public_ip}:{remote_dest}"
        ]

        self.logger.verbose(f"Executing: {' '.join(cmd)}")
        self._project_hud("TELEPORT", "Transmitting Artifact to Iron...", 50, "#a855f7")

        try:
            # We allow 120 seconds for massive payloads over slow links
            subprocess.run(cmd, check=True, capture_output=True, timeout=120)
            self.logger.success(f"Artifact successfully teleported to {node.public_ip}:{remote_dest}")
            self._project_hud("TELEPORT", "Artifact Translocation Complete", 100, "#10b981")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Translocation Fracture: {e.stderr.decode()}")
            raise ArtisanHeresy(f"Matter Transmission Failed: {e.stderr.decode()}", severity=HeresySeverity.CRITICAL)
        except subprocess.TimeoutExpired:
            raise ArtisanHeresy("Translocation Timeout: The aether is too slow.", severity=HeresySeverity.CRITICAL)

    # =========================================================================
    # == MOVEMENT X: THE RITE OF IGNITION (NEW ASCENSION)                    ==
    # =========================================================================
    def ignite_reality(self, instance_id: str, command: str) -> str:
        """
        =============================================================================
        == THE RITE OF IGNITION (V-Ω-REMOTE-EXECUTION)                             ==
        =============================================================================
        Executes a shell command (like docker-compose up) on the remote node.
        """
        self.logger.info(f"Igniting Reality on {instance_id}...")
        self._project_hud("IGNITION", f"Executing Remote Will: {command[:20]}...", 50, "#fbbf24")

        with self._lock:
            # [THE CURE]: Safe Retrieval
            node_data = self._ledger.get("nodes", {}).get(instance_id)
            target_provider = node_data.get("provider_id") if node_data else self.default_provider_name
            target_provider = str(target_provider or "docker")

            prov = InfrastructureFactory.summon(target_provider)

        try:
            # The Provider conducts the rite (handles SSH mapping natively)
            output = prov.conduct_rite(instance_id, command)
            self.logger.success(f"Ignition Successful on {instance_id}.")
            self._project_hud("IGNITION", "Remote Reality Awakened", 100, "#10b981")
            return output
        except Exception as e:
            self.logger.error(f"Ignition Fracture: {e}")
            self._project_hud("IGNITION", "Ignition Fractured", 100, "#ef4444")
            raise ArtisanHeresy(f"Failed to Ignite Reality: {e}", severity=HeresySeverity.CRITICAL)

    def _await_ip_resonance(self, instance_id: str) -> VMInstance:
        """[LAZARUS NETWORK AWAKENING]: Polls until the node yields a Public IP."""
        attempts = 0
        while attempts < 15:
            node = self.get_status(instance_id)
            if node.public_ip and node.state == NodeState.RUNNING:
                return node

            self.logger.verbose(f"Node {instance_id} is waking. Awaiting IP resonance (Attempt {attempts + 1}/15)...")
            self._project_hud("TELEPORT", "Awaiting Network Resonance...", 10 + (attempts * 2), "#3b82f6")
            time.sleep(1.5 * (1.2 ** attempts))  # Exponential backoff with jitter
            attempts += 1

        raise ArtisanHeresy(f"Network Resonance Timeout: Node {instance_id} failed to yield a public coordinate.")

    def _project_hud(self, type_label: str, message: str, percentage: int, color: str):
        """Radiates a Gnostic Pulse to the Ocular UI."""
        if hasattr(self, 'engine') and self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "scaffold/progress",
                    "params": {
                        "id": "manager_pulse",
                        "title": type_label,
                        "message": message,
                        "percentage": percentage,
                        "done": percentage >= 100,
                        "ui_hints": {"color": color, "vfx": "pulse" if percentage < 100 else "bloom"},
                        "trace_id": self.trace_id
                    }
                })
            except:
                pass

    # =========================================================================
    # == CORE CRUD RITES: PROVISION, CENSUS, RECONCILE, TERMINATE            ==
    # =========================================================================

    def get_active_nodes(self, sync: bool = True) -> List[VMInstance]:
        """[THE CENSUS] Lists active nodes, reconciling with the cloud."""
        if not sync or self.is_vacuum:
            with self._lock:
                return [VMInstance(**data) for data in self._ledger.get("nodes", {}).values()]

        start_ns = time.perf_counter_ns()
        self.logger.info(f"Initiating Panoptic Census for substrate [{self.provider.provider_code.upper()}]...")

        try:
            cloud_nodes = self.provider.list_nodes(tag_filter={"ManagedBy": "VELM"})
            cloud_map = {node.id: node for node in cloud_nodes}
            cloud_ids = set(cloud_map.keys())

            with self._lock:
                self._ledger = self._load_ledger()
                ledger_ids = {nid for nid, d in self._ledger.get("nodes", {}).items() if
                              d.get("provider_id") == self.provider.provider_code}

                zombie_ids = ledger_ids - cloud_ids
                orphan_ids = cloud_ids - ledger_ids

                discrepancy_detected = False

                for zid in zombie_ids:
                    del self._ledger["nodes"][zid]
                    discrepancy_detected = True

                for oid in orphan_ids:
                    self._ledger.setdefault("nodes", {})[oid] = cloud_map[oid].model_dump()
                    discrepancy_detected = True

                for cid in cloud_ids:
                    self._ledger.setdefault("nodes", {})[cid] = cloud_map[cid].model_dump()

                if discrepancy_detected:
                    self._save_ledger()

                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                self.logger.success(f"Census complete. {len(cloud_nodes)} souls resonant. Tax: {duration_ms:.2f}ms.")
                return [VMInstance(**data) for data in self._ledger.get("nodes", {}).values()]

        except Exception as e:
            self.logger.error(f"Celestial Census fractured: {str(e)}. Using local memory.")
            with self._lock:
                return [VMInstance(**data) for data in self._ledger.get("nodes", {}).values()]

    def provision(self, name: str, size: str = "default", image: str = "default",
                  provider: Optional[str] = None) -> VMInstance:
        """[THE RITE OF MATERIALIZATION] Forges a new node."""
        with self._lock:
            active_prov = self.provider
            if provider and provider != self.default_provider_name:
                try:
                    active_prov = InfrastructureFactory.summon(provider)
                except Exception as e:
                    self.logger.warn(f"Requested provider '{provider}' failed. Falling back. Error: {e}")

            # [FISCAL SENTINEL]
            try:
                est_cost = active_prov.get_cost_estimate({"size": size})
                if est_cost > 0: self.logger.verbose(f"Fiscal Prophecy: Estimated tax for '{size}' is ${est_cost}/hr.")
            except:
                pass

            self.logger.info(f"Summoning node '{name}' on [{active_prov.provider_code.upper()}]...")

            config = {
                "name": name,
                "size": size,
                "image": image,
                "project_id": self.root.name if not self.is_vacuum else "Vacuum_Inception",
                "trace_id": os.getenv("SCAFFOLD_TRACE_ID", f"tr-{uuid.uuid4().hex[:8].upper()}")
            }

            try:
                instance = active_prov.provision(config)
                if not self.is_vacuum:
                    self._ledger = self._load_ledger()
                    self._ledger.setdefault("nodes", {})[instance.id] = instance.model_dump()
                    self._save_ledger()

                self.logger.success(f"Node manifest confirmed: {instance.id[:12]} @ {instance.public_ip or 'PENDING'}")
                return instance

            except Exception as fracture:
                self.logger.critical(f"Genesis Fracture during provisioning: {fracture}")
                # [ASCENSION 8]: Return a Fractured Dummy Node instead of exploding
                return VMInstance(
                    id=f"fail-{uuid.uuid4().hex[:8]}",
                    name=name,
                    provider_id=active_prov.provider_code,
                    region="void",
                    state=NodeState.FRACTURED,
                    metadata={"error": str(fracture)}
                )

    def terminate(self, instance_id: str, force: bool = False) -> bool:
        """[THE RITE OF OBLIVION] Annihilates a node."""
        with self._lock:
            node_data = self._ledger.get("nodes", {}).get(instance_id)

            if not node_data:
                return self.provider.terminate(instance_id)

            is_locked = node_data.get("tags", {}).get("is_locked") == "true"
            if is_locked and not force:
                raise ArtisanHeresy(
                    f"Sovereignty Violation: Node '{node_data.get('name', instance_id)}' is warded.",
                    severity=HeresySeverity.WARNING
                )

            try:
                # [THE CURE]: Strict String Casting
                prov_id = str(node_data["provider_id"] or "docker")
                prov = InfrastructureFactory.summon(prov_id)
                success = prov.terminate(instance_id)

                if success and not self.is_vacuum:
                    self._ledger = self._load_ledger()
                    if instance_id in self._ledger.get("nodes", {}):
                        del self._ledger["nodes"][instance_id]
                        self._save_ledger()
                    self.logger.success(f"Reality {instance_id[:12]} successfully returned to the void.")
                    return True
            except Exception as e:
                self.logger.error(f"Failed to return {instance_id} to the void: {e}")

            return False

    def reconcile_reality(self, provider_name: Optional[str] = None) -> Dict[str, List[str]]:
        """[THE PANOPTIC SWEEP] Concurrent multi-cloud reconciliation."""
        if self.is_vacuum:
            return {"pruned": [], "adopted": []}

        target_providers = [provider_name] if provider_name else []
        if not target_providers:
            with self._lock:
                target_providers = list(set(
                    str(data.get("provider_id")) for data in self._ledger.get("nodes", {}).values() if
                    data.get("provider_id")))
            if not target_providers:
                target_providers = [self.default_provider_name]

        all_results = {"pruned": [], "adopted": []}

        def _reconcile_single(p_name: str):
            try:
                prov = InfrastructureFactory.summon(p_name)
                cloud_nodes = prov.list_nodes(tag_filter={"ManagedBy": "VELM"})
                return p_name, cloud_nodes
            except Exception:
                return p_name, None

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(target_providers)) as executor:
            futures = [executor.submit(_reconcile_single, p) for p in target_providers]

            with self._lock:
                self._ledger = self._load_ledger()
                discrepancy_detected = False

                for future in concurrent.futures.as_completed(futures):
                    p_name, cloud_nodes = future.result()
                    if cloud_nodes is None: continue

                    cloud_ids = {n.id for n in cloud_nodes}
                    ledger_ids = {nid for nid, data in self._ledger.get("nodes", {}).items() if
                                  data.get("provider_id") == p_name}

                    zombies = ledger_ids - cloud_ids
                    orphans = cloud_ids - ledger_ids

                    for zid in zombies:
                        del self._ledger["nodes"][zid]
                        all_results["pruned"].append(zid)
                        discrepancy_detected = True

                    for oid in orphans:
                        orphan_meta = next(n for n in cloud_nodes if n.id == oid)
                        self._ledger.setdefault("nodes", {})[oid] = orphan_meta.model_dump()
                        all_results["adopted"].append(oid)
                        discrepancy_detected = True

                if discrepancy_detected:
                    self._save_ledger()

        return all_results

    def arbitrate_best_substrate(self, size_query: str) -> Tuple[str, float]:
        """[THE FISCAL PROPHET] Arbitrates costs across providers."""
        estimates = {}
        realms = InfrastructureFactory.list_manifest_realms()
        for realm in realms:
            if realm.get("status") != "RESONANT": continue
            try:
                prov = InfrastructureFactory.summon(realm["code"])
                cost = prov.get_cost_estimate({"size": size_query})
                if cost > 0: estimates[realm["code"]] = cost
            except Exception:
                continue
        if not estimates: return self.default_provider_name, 0.0
        best_provider = min(estimates, key=estimates.get)
        return best_provider, estimates[best_provider]

    # =========================================================================
    # == INTERNAL METABOLISM (PRIVATE RITES)                                 ==
    # =========================================================================

    def _load_ledger(self) -> Dict[str, Any]:
        """[THE RITE OF RESURRECTION] Safely inflates the Ledger from disk."""
        if self.is_vacuum or not self.ledger_path:
            return {"nodes": {}, "version": "8.0-VACUUM", "burn_rate": 0.0}
        try:
            if not self.ledger_path.exists():
                return {"nodes": {}, "version": "8.0-NEW", "burn_rate": 0.0}
            content = self.ledger_path.read_text(encoding='utf-8')
            self._ledger_hash = hashlib.md5(content.encode()).hexdigest()
            return json.loads(content)
        except Exception as e:
            self.logger.warn(f"Ledger Resurrection Failed: {e}. Forging clean slate.")
            return {"nodes": {}, "version": "8.0-RECOVERED", "burn_rate": 0.0}

    def _save_ledger(self):
        """[THE RITE OF ATOMIC INSCRIPTION] Saves the Ledger with Merkle checks."""
        if self.is_vacuum or not self.ledger_path: return

        total_burn = sum(node.get("cost_per_hour", 0.0) for node in self._ledger.get("nodes", {}).values())
        self._ledger["burn_rate"] = round(total_burn, 4)
        self._ledger["last_updated"] = time.time()
        self._ledger["node_count"] = len(self._ledger.get("nodes", {}))

        new_content = json.dumps(self._ledger, indent=2)
        new_hash = hashlib.md5(new_content.encode()).hexdigest()

        if new_hash != self._ledger_hash:
            try:
                self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
                atomic_write(target_path=self.ledger_path, content=new_content, logger=self.logger, sanctum=self.root)
                self._ledger_hash = new_hash
            except Exception as write_err:
                self.logger.error(f"Failed to inscribe Ledger: {write_err}")

    def get_nodes(self) -> List[VMInstance]:
        return [VMInstance(**data) for data in self._ledger.get("nodes", {}).values()]

    def __repr__(self) -> str:
        count = len(self._ledger.get("nodes", {}))
        return f"<Ω_INFRA_MANAGER nodes={count} burn_rate=${self._ledger.get('burn_rate', 0.0)}/hr vacuum={self.is_vacuum}>"