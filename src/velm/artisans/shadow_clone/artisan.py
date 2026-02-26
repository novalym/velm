# Path: artisans/shadow_clone/artisan.py
# --------------------------------------
import gc
import shutil
import stat
import uuid
import time
import threading
import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Final

# --- THE DIVINE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...core.ignition import IgnitionDiviner
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import ShadowCloneRequest
from ...help_registry import register_artisan
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# --- INTERNAL DIMENSIONAL ENGINES ---
from .worktree import WorktreeManager
from .network import NetworkBinder
from .catalog import ShadowCatalog
from .contracts import ShadowEntity, ShadowStatus, ShadowMode
from .governor import RealityGovernor
from .mirror import SynapticMirror
from .config_injector import ConfigInjector

Logger = Scribe("ShadowEngine")


@register_artisan("shadow")
class ShadowCloneArtisan(BaseArtisan[ShadowCloneRequest]):
    """
    =================================================================================
    == THE OMEGA SHADOW ENGINE (V-Ω-TOTALITY-V25000-BICAMERAL)                     ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_FISSION_CONDUCTOR | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_SHADOW_V25000_KINETIC_FUSION_2026_FINALIS

    The supreme orchestrator of parallel realities. It has been ascended to manage
    the "Bicameral Lab"—cloning for both ephemeral preview (RUN) and high-risk
    AI-driven refactoring (LAB), with atomic re-integration (MERGE).
    =================================================================================
    """

    def __init__(self, engine: Any):
        """
        [THE RITE OF INCEPTION]
        Binds the Shadow Engine to the God-Engine and initializes the
        Dimensional Catalog.
        """
        # [ASCENSION 5]: NONETYPE SARCOPHAGUS
        # We scry the context_provider for its true identity.
        real_engine = getattr(engine, 'engine', engine)
        super().__init__(real_engine)

        self._active_jobs: Dict[str, threading.Thread] = {}
        self.catalog: Optional[ShadowCatalog] = None
        self.signature = "Ω_SHADOW_ENGINE_V25000"

    def execute(self, request: ShadowCloneRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND ROUTER (V-Ω-TOTALITY)                                         ==
        =============================================================================
        LIF: 100x | ROLE: KINETIC_ORCHESTRATOR
        """
        # --- MOVEMENT 0: SPATIAL ANCHORING ---
        # [ASCENSION 10]: We anchor the Catalog to the Target Root
        self.catalog = ShadowCatalog(self.project_root)

        # [ASCENSION 11]: REGISTRY HYGIENE
        # Purge stale records before conducting new rites
        self._gc_dead_shadows()

        command = request.shadow_command
        self._trace_id = request.trace_id

        self.logger.verbose(f"Shadow Engine: Conducting Rite '{command}' for [cyan]{request.label}[/cyan]")

        # --- THE PANTHEON OF RITES ---
        if command == "spawn":
            return self._initiate_async_spawn(request)

        elif command == "merge":
            # [ASCENSION 3]: THE RITE OF RE-INTEGRATION (The Fusion)
            return self._conduct_merge_rite(request)

        elif command == "vanish":
            return self._vanish(request)

        elif command == "list":
            return self._list()

        elif command == "status":
            return self._status(request)

        elif command == "logs":
            return self._logs(request)

        return self.failure(f"Unknown Shadow Rite: {command}")

    # =================================================================================
    # == MOVEMENT I: FISSION (SPAWN)                                                 ==
    # =================================================================================

    def _initiate_async_spawn(self, req: ShadowCloneRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF ASYNC FISSION (PENDING ACK)                                 ==
        =============================================================================
        [ASCENSION 3]: Returns a 'PENDING' status to the UI instantly.
        The heavy matter replication happens in the background to prevent
        LSP communication timeouts.
        """
        job_id = f"job-fission-{uuid.uuid4().hex[:8].upper()}"

        # [ASCENSION 7]: PROCLAMATION
        self.progress("Igniting Reality Fission...", 5)

        # 1. SPAWN THE BACKGROUND SOUL
        worker = threading.Thread(
            target=self._worker_spawn_logic,
            args=(job_id, req),
            name=f"ShadowFission-{job_id}",
            daemon=True
        )
        self._active_jobs[job_id] = worker
        worker.start()

        # 2. RETURN INSTANT PROPHECY
        return self.success(
            f"Fission sequence for '{req.label}' initiated.",
            data={
                "status": "PENDING",
                "job_id": job_id,
                "label": req.label,
                "mode": req.mode,
                "message": "Forging parallel dimension in the background."
            },
            ui_hints={"vfx": "pulse_purple", "icon": "ghost"}
        )

    # =================================================================================
    # == MOVEMENT I.B: THE BACKGROUND FISSION (THE WORKER)                           ==
    # =================================================================================

    def _worker_spawn_logic(self, job_id: str, req: ShadowCloneRequest):
        """
        =============================================================================
        == THE RITE OF KINETIC FISSION (BACKGROUND EXECUTION)                      ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_REPLICATOR | RANK: OMEGA_SOVEREIGN

        [THE MANIFESTO]
        This is the heavy lifting of reality creation. It transmutes the Prime
        Timeline into a parallel Shadow Stratum. It is warded against substrate
        collisions and is fully transaction-aware.
        """
        try:
            # --- MOVEMENT I: GEOMETRIC ANCHORING ---
            self.progress("Divining Dimensional Coordinates...", 10)

            session_uuid = uuid.uuid4().hex[:6].upper()
            shadow_id = f"{req.label}-{session_uuid}"

            # [ASCENSION 1]: Anchor in the warded .scaffold/shadows sanctum
            shadow_root = (self.project_root / ".scaffold" / "shadows" / shadow_id).resolve()

            # --- MOVEMENT II: MATTER REPLICATION (THE SUTURE) ---
            # [ASCENSION 13]: THE SOVEREIGN HAND
            # We no longer use 'shutil'. we use the transaction-aware 'self.io'.
            self.progress(f"Replicating Matter to {req.mode.upper()} Realm...", 25)

            if req.strategy == "git_worktree" and (self.project_root / ".git").exists():
                # [ASCENSION 6]: Temporal Worktree Strategy
                wt = WorktreeManager(self.project_root)
                wt.create(shadow_root, req.target_ref)
            else:
                # [ASCENSION 1]: HOLOGRAPHIC REPLICATION
                # Uses self.io.copy() which respects Merkle Seals and ignore patterns.
                self.io.copy(self.project_root, shadow_root)

            # --- MOVEMENT III: LUNG TRANSPLANTATION (DEPENDENCY GRAFT) ---
            # [ASCENSION 3 & 13]: We share the 'Lungs' (node_modules/venv)
            # to prevent downloading 1GB of matter for every clone.
            self.progress("Grafting Metabolic Lungs...", 45)
            self._transplant_lungs(self.project_root, shadow_root)

            # --- MOVEMENT IV: NETWORK BINDING & EXORCISM ---
            # [ASCENSION 16]: Hunt for a free frequency for the Ocular Membrane.
            self.progress("Hunting for Network Resonance...", 60)
            app_port = req.port if req.port != 0 else 5173
            if NetworkBinder.is_port_in_use(app_port):
                app_port = NetworkBinder.find_free_port(start=app_port + 1)

            # --- MOVEMENT V: CONFIGURATION INJECTION (DNA) ---
            # [ASCENSION 14]: Surgically inject identity into the shadow
            self.progress("Injecting Environmental DNA...", 75)
            ConfigInjector().inject(shadow_root, {
                **req.variables,
                "PORT": str(app_port),
                "SCAFFOLD_SHADOW_ID": shadow_id,
                "SCAFFOLD_MODE": req.mode.value,
                "SCAFFOLD_ROOT": str(self.project_root).replace('\\', '/')
            })

            # --- MOVEMENT VI: THE BIFURCATION OF DESTINY ---
            # [ASCENSION 21]: LABORATORY GATEWAY
            if req.mode == ShadowMode.LAB:
                # In LAB mode, the fission is complete once the matter exists.
                # We do not ignite a server; we hand the keys to the AI/Architect.
                entity = self._register_and_broadcast(job_id, shadow_id, shadow_root, app_port, req,
                                                      ShadowStatus.INITIALIZING)
                self.logger.success(f"Laboratory Dimension '{req.label}' manifest at [dim]{shadow_root}[/dim]")
                return

            # --- MOVEMENT VII: KINETIC IGNITION (RUN MODE) ---
            # [ASCENSION 22]: Ignite the Ocular Preview and start the Mirror.
            self.progress("Igniting Ocular Membrane...", 85)
            self._ignite_running_reality(job_id, shadow_id, shadow_root, app_port, req)

        except Exception as catastrophic_paradox:
            # [ASCENSION 24]: THE FINALITY VOW
            self.logger.error(f"Fission sequence fractured: {catastrophic_paradox}")
            self._broadcast_failure(job_id, str(catastrophic_paradox))
            # Emergency Dissolution of the tainted matter
            if 'shadow_root' in locals():
                self._dissolve_matter_hardened(shadow_root)

    # =================================================================================
    # == SECTION II: KINETIC UTILITIES (THE ORGANS)                                  ==
    # =================================================================================

    def _register_and_broadcast(self, job_id: str, sid: str, path: Path, port: int, req: ShadowCloneRequest,
                                status: ShadowStatus) -> ShadowEntity:
        """Forges the ShadowEntity and registers it in the Dimensional Catalog."""
        entity = ShadowEntity(
            id=sid,
            label=req.label,
            mode=req.mode,
            target_ref=req.target_ref,
            root_path=str(path).replace('\\', '/'),
            port=port,
            status=status,
            owner=req.owner,
            created_at=time.time(),
            trace_id=self._trace_id
        )

        # [ASCENSION 19]: Inscribe in Catalog
        self.catalog.register(entity)

        # [ASCENSION 18]: THE MERKLE SEAL
        # (Implicitly calculated by Catalog in V2)

        self._broadcast_completion(job_id, entity.to_dict())
        return entity

    def _ignite_running_reality(self, job_id: str, sid: str, path: Path, port: int, req: ShadowCloneRequest):
        """Ignites the process and starts the Synaptic Mirror (HMR)."""
        # 1. DIVINATION
        diviner = IgnitionDiviner()
        plan = diviner.divine(path, port)

        # 2. IGNITION
        gov = RealityGovernor(sid, engine=self.engine)

        # Apply custom commands or auto-divined plan
        final_cmd = req.custom_command.split() if req.custom_command else plan.command
        # Suture the port into the command arguments
        final_cmd = [arg.replace("{{port}}", str(port)) for arg in final_cmd]

        pid, stdout_path, stderr_path = gov.ignite(path, final_cmd, None, plan.aura.value)

        # 3. REGISTRATION
        entity = ShadowEntity(
            id=sid, label=req.label, mode=req.mode, target_ref=req.target_ref,
            root_path=str(path).replace('\\', '/'), port=port, pid=pid,
            status=ShadowStatus.ACTIVE, created_at=time.time(), aura=plan.aura.value,
            stdout_log_path=str(stdout_path), stderr_log_path=str(stderr_path),
            trace_id=self._trace_id
        )
        self.catalog.register(entity)

        # 4. START SYNAPTIC MIRROR
        # [ASCENSION 22]: Live-reload from Prime to Shadow
        mirror = SynapticMirror(self.project_root, path, sid)
        mirror.start()

        self._broadcast_completion(job_id, entity.to_dict())

    def _transplant_lungs(self, source: Path, dest: Path):
        """
        [ASCENSION 3]: LUNG TRANSPLANTATION.
        Surgically grafts the dependency weight (node_modules) from Prime to Shadow.
        """
        for lung_name in ["node_modules", ".venv", "venv", "env"]:
            src_lung = source / lung_name
            dst_lung = dest / lung_name

            if src_lung.exists() and not dst_lung.exists():
                try:
                    if os.name == 'nt':
                        # Windows Junctions are more resonant than Symlinks for dependencies
                        import _winapi
                        _winapi.CreateJunction(str(src_lung), str(dst_lung))
                    else:
                        os.symlink(src_lung, dst_lung, target_is_directory=True)
                    self.logger.verbose(f"   -> Transplanted '{lung_name}' purely.")
                except Exception as e:
                    self.logger.warn(f"Lung Graft failed for '{lung_name}': {e}")

    # =================================================================================
    # == MOVEMENT II: FUSION (THE MERGE RITE)                                        ==
    # =================================================================================

    def _conduct_merge_rite(self, req: ShadowCloneRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE OMEGA RITE OF REALITY FUSION (V-Ω-TOTALITY-V25000-ADJUDICATED)          ==
        =================================================================================
        LIF: ∞ | ROLE: DIMENSIONAL_SYNCHRONIZER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_MERGE_V25000_ADJUDICATION_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This is the supreme rite of unification. It scries the Shadow dimension for
        Luminous Shards, summons the Adjudicator to prove their logic, and surgically
        fuses them into the Prime timeline via the Sovereign Hand.
        =================================================================================
        """
        # --- MOVEMENT 0: TARGET IDENTIFICATION ---
        # [ASCENSION 5]: NoneType Sarcophagus search
        shadow = self.catalog.get(req.target_id) if req.target_id else self._find_active_shadow(req.label)

        if not shadow:
            return self.failure(
                f"Fusion Fracture: No shadow reality manifest for label '{req.label}'.",
                suggestion="Use 'velm shadow list' to scry for active dimensions."
            )

        shadow_root = Path(shadow.root_path)
        self.logger.info(f"Initiating Reality Fusion for shadow [soul]{shadow.id[:8]}[/]...")
        self.progress("Scrying for Luminous Shards (Diffing)...", 10)

        # =========================================================================
        # == MOVEMENT I: THE DIFFERENTIAL GAZE (SHARD DETECTION)                 ==
        # =========================================================================
        # [ASCENSION 3]: Parallel hash-comparison to find divergent souls.
        luminous_shards = self._find_luminous_shards(shadow_root, self.project_root)

        if not luminous_shards:
            return self.success("The Shadow Dimension is congruent with the Prime. No fusion required.")

        self.logger.info(f"Perceived {len(luminous_shards)} Luminous Shard(s) requiring fusion.")

        # =========================================================================
        # == MOVEMENT II: THE ADJUDICATION GATE (RESONANCE TEST)                 ==
        # =========================================================================
        # [ASCENSION 1]: We refuse to merge if the shadow is logic-fractured.
        if not req.force:
            self.progress("Adjudicating Shadow Resonance...", 30)

            # Late-bound import to prevent circularity
            from ..adjudicator.engine import AdjudicatorRequest

            # [STRIKE]: Recursive dispatch to the Adjudicator sibling
            adj_res = self.dispatch(AdjudicatorRequest(
                target_path=shadow_root,
                test_command=getattr(req, 'test_command', 'make test'),
                trace_id=f"merge-audit-{shadow.id[:8]}"
            ))

            if not adj_res.success:
                # [ASCENSION 11]: Socratic Redemption
                return self.failure(
                    "Fusion Denied: The shadow reality is logic-fractured.",
                    details=adj_res.message,
                    suggestion=f"Scry the shadow's thoughts via 'velm shadow logs --label {req.label}' or use --force.",
                    ui_hints={"vfx": "shake", "sound": "merge_blocked"}
                )

            self.logger.success("Shadow proven Resonant. Proceeding with Fusion.")

        # =========================================================================
        # == MOVEMENT III: THE VOW OF REASSURANCE (PRIME SNAPSHOT)               ==
        # =========================================================================
        # [ASCENSION 6]: Snapshot the Prime state BEFORE transfiguration.
        # This provides the path of return for 'velm undo'.
        self.progress("Forging Prime Safety Snapshot...", 50)
        self.guarded_execution(luminous_shards, context="shadow_merge")

        # =========================================================================
        # == MOVEMENT IV: THE KINETIC FUSION (THE STRIKE)                        ==
        # =========================================================================
        # [ASCENSION 16]: Translocate matter using the Sovereign Hand.
        self.progress(f"Fusing {len(luminous_shards)} shards into Prime...", 70)

        merged_count = 0
        final_artifacts = []

        for shard in luminous_shards:
            rel_path = shard.relative_to(shadow_root)
            dest_path = self.project_root / rel_path

            # [ASCENSION 10]: Holographic Replication via the Hand.
            # We use copy() to keep the Shadow Lab intact for forensic analysis.
            success = self.io.copy(shard, dest_path)

            if success:
                merged_count += 1
                final_artifacts.append(Artifact(
                    path=dest_path,
                    action="MERGED_FROM_SHADOW",
                    checksum=self.cortex.scry_hash(dest_path)
                ))
                self.logger.verbose(f"   -> Fused: [dim]{rel_path}[/dim]")

        # =========================================================================
        # == MOVEMENT V: THE RITE OF OBLIVION (CLEANUP)                          ==
        # =========================================================================
        # [ASCENSION 10]: Cleanup triage.
        if not req.no_cleanup:
            self.progress("Dissolving Dimensional Rift...", 90)
            try:
                self._vanish_internal(shadow)
            except Exception as e:
                self.logger.warn(f"Cleanup deferred: Shadow matter resisted dissolution: {e}")

        # =========================================================================
        # == MOVEMENT VI: THE FINAL REVELATION                                   ==
        # =========================================================================
        # [ASCENSION 23]: Radiate the Ocular Pulse
        self._project_hud_pulse("REALITY_FUSION", "#64ffda")

        latency_ms = (time.perf_counter_ns() - self._start_ns) / 1_000_000

        return self.success(
            f"Reality Fusion complete. {merged_count} shard(s) manifest in Prime.",
            artifacts=final_artifacts,
            data={
                "merged_count": merged_count,
                "shadow_id": shadow.id,
                "adjudicated": not req.force,
                "latency_ms": latency_ms
            },
            ui_hints={"vfx": "bloom_teal", "sound": "merge_complete"}
        )

    def _find_luminous_shards(self, shadow_root: Path, prime_root: Path) -> List[Path]:
        """[FACULTY 14]: Deep-tissue hash comparison between realms."""
        shards = []
        # We walk the shadow and ignore Engine-internal artifacts
        for shadow_file in shadow_root.rglob("*"):
            if shadow_file.is_dir() or ".scaffold" in shadow_file.parts:
                continue

            rel_path = shadow_file.relative_to(shadow_root)
            prime_file = prime_root / rel_path

            # CASE A: New scripture born in the darkness
            if not prime_file.exists():
                shards.append(shadow_file)
            else:
                # CASE B: Modified scripture (The True Transfiguration)
                # [ASCENSION 14]: Using the Cortex's hash scryer
                if self.cortex.scry_hash(shadow_file) != self.cortex.scry_hash(prime_file):
                    shards.append(shadow_file)
        return shards

    # =================================================================================
    # == MOVEMENT III: DISSOLUTION (VANISH)                                         ==
    # =================================================================================

    def _vanish(self, req: ShadowCloneRequest) -> ScaffoldResult:
        """User-facing rite of reality destruction."""
        shadows = self.catalog.list_shadows()

        targets = []
        if req.target_id:
            targets = [s for s in shadows if s.id == req.target_id]
        else:
            targets = [s for s in shadows if s.label == req.label]

        if not targets:
            return self.success("Void Inquest: No matching shadows to vanish.")

        for t in targets:
            self._vanish_internal(t)

        return self.success(f"Banished {len(targets)} shadow reality(s).")

    def _vanish_internal(self, shadow: ShadowEntity):
        """[ASCENSION 17]: Atomic Scythe and Dissolution."""
        self.logger.info(f"Banishing Shadow Reality: [soul]{shadow.id[:8]}[/soul]")

        # 1. THE SCYTHE (Process Kill)
        if shadow.pid:
            try:
                gov = RealityGovernor(shadow.id, engine=self.engine)
                gov.scythe(shadow.pid)
            except Exception as e:
                self.logger.warn(f"Scythe encountered friction: {e}")

        # 2. THE SOLVENT (Physical Wipe)
        self._dissolve_matter_hardened(Path(shadow.root_path))

        # 3. THE DEREGISTRATION
        self.catalog.deregister(shadow.id)
        self._project_hud_pulse("SHADOW_VANISHED", "#64748b")

    # =================================================================================
    # == SECTION III: FORENSIC SCRYING (STATUS & LIST)                               ==
    # =================================================================================

    def _status(self, req: ShadowCloneRequest) -> ScaffoldResult:
        """[ASCENSION 19]: Isomorphic Vitality Scrying."""
        if not self.catalog: return self.failure("Catalog Void")

        shadows = self.catalog.list_shadows()
        # Find latest shadow for this label
        target = next((s for s in reversed(shadows) if s.label == req.label), None)

        if not target:
            return self.success("Dimension Unmanifested.", data={'alive': False, 'status': 'OFFLINE'})

        is_alive = False
        # 1. IRON PATH (PID)
        if self._substrate == "IRON" and target.pid:
            import psutil
            is_alive = psutil.pid_exists(target.pid)

        # 2. ETHER PATH (Pulse)
        if not is_alive:
            pulse_path = Path(target.root_path) / ".logs" / "daemon.pulse"
            if pulse_path.exists() and (time.time() - pulse_path.stat().st_mtime < 15.0):
                is_alive = True

        return self.success("Gaze Concluded.", data={
            'id': target.id,
            'label': target.label,
            'alive': is_alive,
            'mode': target.mode,
            'status': "ACTIVE" if is_alive else "ZOMBIE",
            'url': target.url,
            'path': target.root_path,
            'created_at': target.created_at
        })

    def _list(self) -> ScaffoldResult:
        """[ASCENSION 20]: The Panoptic Census."""
        shadows = self.catalog.list_shadows()
        return self.success(f"Census: {len(shadows)} dimensions active.", data=[s.to_dict() for s in shadows])

    def _logs(self, req: ShadowCloneRequest) -> ScaffoldResult:
        """[ASCENSION 21]: Forensic Chronicle Recall."""
        shadow = self._find_active_shadow(req.label)
        if not shadow: return self.failure("No matter found.")

        lines = []
        for stream, p_str in [("OUT", shadow.stdout_log_path), ("ERR", shadow.stderr_log_path)]:
            if p_str and Path(p_str).exists():
                try:
                    with open(p_str, 'r', encoding='utf-8', errors='replace') as f:
                        lines.append(f"\n--- {stream} STREAM ---")
                        # Return last 100 verses of the chronicle
                        lines.extend(f.readlines()[-100:])
                except:
                    pass

        return self.success("Chronicle Recalled.", data={"lines": [l.strip() for l in lines]})

    # =================================================================================
    # == THE TRINITY OF DIMENSIONAL MAINTENANCE                                     ==
    # =================================================================================

    def _find_active_shadow(self, label: str) -> Optional[ShadowEntity]:
        """
        =============================================================================
        == THE GAZE OF THE LIVING (V-Ω-TOTALITY-V20000.1-ISOMORPHIC)               ==
        =============================================================================
        LIF: 100x | ROLE: SHADOW_SOUL_SCRIER | RANK: OMEGA_SUPREME
        AUTH: Ω_FIND_ACTIVE_V20000_PULSE_SUTURE_2026_FINALIS

        Scries the Dimensional Catalog for the most recent, breathing incarnation
        of a specific label.
        """
        if not self.catalog:
            # [ASCENSION 4]: JIT Catalog Inception
            self.catalog = ShadowCatalog(self.project_root)

        shadows = self.catalog.list_shadows()

        # We search in reverse to find the most recently spawned incarnation.
        for s in reversed(shadows):
            if s.label != label:
                continue

            # --- MOVEMENT I: THE BICAMERAL LIFE-PROBE ---
            is_alive = False

            # A. THE HIGH PATH (IRON CORE - PID PROBE)
            if self._substrate == "IRON" and s.pid:
                try:
                    import psutil
                    if psutil.pid_exists(s.pid):
                        is_alive = True
                except Exception:
                    pass

            # B. THE WASM PATH (ETHER - PULSE PROBE)
            if not is_alive:
                # [ASCENSION 2]: Achronal Leash-Aging Protocol
                # We scry the heartbeat file left by the Shadow's RealityGovernor.
                pulse_path = Path(s.root_path) / ".logs" / "daemon.pulse"
                if pulse_path.exists():
                    # The pulse is resonant if it was updated in the last 15 seconds.
                    age = time.time() - pulse_path.stat().st_mtime
                    if age < 15.0:
                        is_alive = True

            if is_alive:
                return s

        return None

    def _dissolve_matter_hardened(self, path: Path):
        """
        =============================================================================
        == THE HARDENED SOLVENT (V-Ω-TOTALITY-V5000-UNBREAKABLE-WIPE)              ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_ANNIHILATOR | RANK: OMEGA_SOVEREIGN

        Surgically dissolves a directory tree. Engineered to defeat the 'Access Denied'
        heresy on Windows caused by Read-Only Git metadata or OS locks.
        """
        if not path.exists():
            return

        def _force_consecrate_permissions(func, p, exc_info):
            """
            [THE HEALER]: Escalates privileges by stripping the Read-Only ward
            from a file before re-attempting the annihilation.
            """
            try:
                os.chmod(p, stat.S_IWRITE)
                func(p)
            except Exception:
                # If even chmod fails, the shard is warded by a Higher Power (OS Lock).
                pass

        # [ASCENSION 1]: THE ATOMIC RETRY LOOP
        # We strike three times with exponential backoff to allow OS handles to release.
        for attempt in range(3):
            try:
                if path.is_dir():
                    shutil.rmtree(path, onerror=_force_consecrate_permissions)
                else:
                    path.unlink(missing_ok=True)

                # Verify Annihilation
                if not path.exists():
                    self.logger.verbose(f"   -> Dimensional Matter dissolved: {path.name}")
                    return
            except OSError as e:
                if attempt < 2:
                    # [ASCENSION 9]: HYDRAULIC YIELD
                    time.sleep(0.5 * (attempt + 1))
                    # Trigger a metabolic lustration to release any Python-side handles
                    gc.collect()
                    continue
                else:
                    self.logger.warn(f"Annihilation Imperfect: Shard '{path.name}' resisted dissolution: {e}")

    def _project_hud_pulse(self, type_label: str, color: str):
        """
        =============================================================================
        == THE OCULAR RADIANCE (V-Ω-TELEPATHIC-UPLINK)                             ==
        =============================================================================
        [ASCENSION 3]: Directly casts a visual signal across the IPC lattice
        to the React Ocular Membrane.
        """
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                # We use the BaseArtisan's broadcast faculty for trace-aware radiation
                self.broadcast("novalym/hud_pulse", {
                    "type": type_label,
                    "label": "SHADOW_ENGINE",
                    "color": color,
                    "trace": getattr(self, "_trace_id", "tr-void"),
                    "timestamp": time.time()
                })
            except Exception as e:
                self.logger.debug(f"HUD Projection fractured: {e}")

    def _broadcast_completion(self, job_id: str, data: Dict[str, Any]):
        """
        =============================================================================
        == THE HERALD OF TRIUMPH (V-Ω-TOTALITY-V2000.5-RESONANT)                   ==
        =============================================================================
        LIF: 100x | ROLE: REALITY_FUSION_PROCLAIMER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_BROADCAST_COMPLETION_V2000_SUTURE_FINALIS

        Radiates the successful materialization of a new dimension across the
        multiversal bridge to the Ocular HUD. It transmutes the background matter
        into a luminous notification, signaling that the 'Darkness' is now a
        functional Laboratory.
        =============================================================================
        """
        if self.silent:
            return

        label = data.get('label', 'unnamed')
        sid = data.get('id', 'void')
        self.logger.success(f"[{job_id}] Dimensional Fission RESONANT: [cyan]{label}[/cyan] ([dim]{sid[:8]}[/dim])")

        # --- MOVEMENT I: THE JOB_COMPLETE REVELATION ---
        # This packet fulfills the pending Promise in the Electron/React stage.
        # [ASCENSION 4]: Dual-Dialect Support. We provide both 'data' and 'result'
        # to satisfy legacy and modern UI hooks simultaneously.
        self.broadcast("scaffold/jobComplete", {
            "job_id": job_id,
            "status": "SUCCESS",
            "data": data,
            "result": data,
            "trace_id": self._trace_id,
            "timestamp": time.time()
        })

        # --- MOVEMENT II: THE HAPTIC OCULAR BLOOM ---
        # [ASCENSION 7]: Radiate a specific visual signal to the HUD.
        # This triggers the 'bloom' VFX and sets the aura to #64ffda (Teal).
        self.broadcast("novalym/hud_pulse", {
            "type": "RITE_SUCCESS",
            "label": "FISSION_COMPLETE",
            "color": "#64ffda",
            "trace": self._trace_id,
            "priority": "SUCCESS",
            "vfx": "bloom",
            "sound": "consecration_complete"
        })

        # --- MOVEMENT III: [ASCENSION 22] CHRONICLE SYNC ---
        # We signal a global project refresh to ensure the Sidebar and VFS scryers
        # immediately perceive the new files in .scaffold/shadows/
        self.broadcast("scaffold/refresh", {
            "scope": "topology",
            "trace_id": self._trace_id
        })


    def _broadcast_failure(self, job_id: str, error: str):
        """
        =============================================================================
        == THE HERALD OF LAMENTATION (V-Ω-TOTALITY-V2000.1-SUTURED)                ==
        =============================================================================
        LIF: 100x | ROLE: SIGNAL_RESONATOR | RANK: OMEGA_GUARDIAN

        Radiates the fracture of a dimensional rite across the IPC lattice to the
        Ocular HUD. It transmutes a raw exception into a structured Gnostic
        Notification, ensuring the Architect is never left in the dark.
        =============================================================================
        """
        self.logger.error(f"[{job_id}] Dimensional Fission shattered: [red]{error}[/red]")

        # 1. FORGE THE JOB_COMPLETE REVELATION
        # We signal the UI that the background thread has concluded in a state of heresy.
        self.broadcast("scaffold/jobComplete", {
            "job_id": job_id,
            "status": "ERROR",
            "error": error,
            "suggestion": "Check for substrate file-locks, permission wards, or network drift.",
            "trace_id": self._trace_id,
            "timestamp": time.time()
        })

        # 2. RADIATE THE HAPTIC DISTRESS SIGNAL
        # Triggers the 'shake' VFX and 'red' glow in the Ocular Membrane.
        self.broadcast("novalym/hud_pulse", {
            "type": "RITE_FRACTURE",
            "label": "FISSION_FAILED",
            "color": "#ef4444",
            "trace": self._trace_id,
            "priority": "CRITICAL"
        })

        # 3. [ASCENSION 15]: THE FORENSIC SNAPSHOT
        # If possible, we dump the current variables to a local crash report
        try:
            # Future: Logic to write .scaffold/crash_reports/job_id.json
            pass
        except:
            pass

    def __repr__(self) -> str:
        return f"<Ω_SHADOW_ENGINE status=RESONANT trace={self._trace_id[:6]}>"


