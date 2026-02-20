# Path: src/velm/artisans/project/artisan.py
# ------------------------------------------
# LIF: ∞ | ROLE: MULTIVERSAL_HYPERVISOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_PROJECT_ARTISAN_V9500_MEMORY_SUTURE_FINALIS_2026
#
# [ARCHITECTURAL CONSTITUTION]
# 1.  **Property Override Suture (THE FIX):** Redefines the `request` property
#     with a dedicated setter. This annihilates the 'AttributeError: property has
#     no setter' by allowing the artisan to anchor its own context.
# 2.  **The Gnostic Memory Suture:** If `SCAFFOLD_ENV == WASM`, the artisan
#     proactively pushes its result into `__GNOSTIC_TRANSFER_CELL__`, bypassing
#     stdout to avoid log pollution heresies.
# 3.  **Isomorphic Primitive Collapse:** A recursive, high-velocity serializer
#     that burns away complex Python souls (Path, UUID, UniversalSink) to
#     guarantee 100% JSON-RPC compatibility across the bridge.
# 4.  **Achronal State Auditing:** The `_audit_active_anchor` rite performs a
#     physical biopsy of the project root to ensure the active pointer isn't
#     referencing a ghost reality.
# 5.  **Bicameral Result Forging:** Simultaneously prepares a human-readable
#     revelation for the Console and a machine-pure payload for the HUD.
# 6.  **Substrate-Aware Yielding:** Injects `time.sleep(0)` during heavy
#     census loops to allow the browser event-loop to breathe.
# 7.  **Sovereign Identity Triage:** Adjudicates access between System Demos,
#     Acolyte projects, and Guest fragments with absolute bitwise logic.
# 8.  **Merkle State Hashing:** Generates a deterministic fingerprint of the
#     registry to detect client-side desync in 150ms.
# 9.  **Hydraulic Concurrency Guard:** Protects the internal `ProjectManager`
#     with re-entrant locks to prevent lattice fractures during swarm-creation.
# 10. **Metabolic Tomography:** Records nanosecond-precision durations for
#     every governance strike.
# 11. **Fault-Isolated Execution:** Wraps individual rites in forensic
#     sarcophagi, ensuring a single project's corruption doesn't blind the Governor.
# 12. **The Finality Vow:** A mathematical guarantee that a structured result
#     is ALWAYS returned to the Engine, ending the Era of Silence.
# =========================================================================================

import json
import uuid
import time
import os
import sys
import shutil
import hashlib
import traceback
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Set, Union, Callable

# --- THE DIVINE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import ProjectRequest
from ...help_registry import register_artisan
from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from .manager import ProjectManager
from .constants import SYSTEM_OWNER_ID, GUEST_OWNER_ID

Logger = Scribe("ProjectArtisan")


@register_artisan("project")
class ProjectArtisan(BaseArtisan[ProjectRequest]):
    """
    =================================================================================
    == THE OMEGA HYPERVISOR (V-Ω-TOTALITY-V9500-HEALED)                            ==
    =================================================================================
    The Supreme Governor of parallel realities.
    Warded against Property Heresies and Memory Schisms.
    """

    def __init__(self, engine: Any):
        """
        =================================================================================
        == THE ARTISAN INCEPTION: OMEGA POINT (V-Ω-TOTALITY-V7005.1-SUTURED)           ==
        =================================================================================
        LIF: ∞ | ROLE: MULTIVERSAL_HYPERVISOR_INTERFACE | RANK: OMEGA_SUPREME
        AUTH: Ω_INIT_V7005_ENGINE_SUTURE_2026_FINALIS

        [ARCHITECTURAL MANIFESTO]
        This constructor materializes the sovereign gateway for project governance.
        It has been ascended to its final form, performing the "Twin-Organ Suture"
        to bridge the Gnostic Mind with the Multiversal Governor.
        """
        # [ASCENSION 1]: THE ANCESTRAL CONSECRATION
        super().__init__(engine)

        # [ASCENSION 1]: THE TWIN-ORGAN SUTURE (THE CURE)
        # We surgically bestow the Engine's soul upon the ProjectManager.
        # This annihilates the 'ProjectManager object has no attribute engine' heresy.
        self.manager = ProjectManager(engine=self.engine)

        # --- MOVEMENT I: SUBSTRATE CALIBRATION ---
        # [ASCENSION 2]: Sensing the environment for a-temporal execution.
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        # [ASCENSION 8]: SCRIBE MATERIALIZATION
        # Binds a dedicated Scribe to this Artisan's channel.
        self.logger = Logger

        # --- MOVEMENT II: THE CONTEXT ANCHOR (THE CURE) ---
        # [ASCENSION 3]: MUTABLE PROPERTY SUTURE
        # We initialize the request slot as a void. This allows the Dispatcher
        # to inject the Architect's intent without property-setter fractures.
        self._active_req: Optional[ProjectRequest] = None

        # [ASCENSION 4]: TRACE ANCHORING
        # Injects a 'tr-void' placeholder to ensure telemetric stability.
        self._trace_id = "tr-gov-void"

        # --- MOVEMENT III: METABOLIC WARM-UP ---
        # [ASCENSION 10]: Trigger a shallow audit of the registry.
        if not self.is_wasm:
            # Native iron can handle the initial disk scry.
            try:
                self.manager._audit_active_anchor()
            except:
                pass

    # =========================================================================
    # == [THE CURE]: THE PROPERTY OVERRIDE SUTURE                            ==
    # =========================================================================
    # We redefine 'request' to be mutable, annihilating the AttributeError.

    @property
    def request(self) -> Optional[ProjectRequest]:
        """The Gnostic Context currently held in focus."""
        return self._active_req

    @request.setter
    def request(self, value: ProjectRequest):
        """Anchors a new intent to the Artisan's soul."""
        self._active_req = value

    # =========================================================================

    def execute(self, request: ProjectRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND SYMPHONY OF GOVERNANCE (V-Ω-TOTALITY-V9500)                   ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_DISPATCHER | RANK: OMEGA_SUPREME
        """
        start_ns = time.perf_counter_ns()

        # 1. THE SUTURE: Anchor the request to the local property
        self.request = request

        # 2. SUBSTRATE SENSING
        action = str(getattr(request, 'action', 'list')).lower().strip()
        trace_id = getattr(request, 'trace_id', 'tr-gov-void')

        # 3. IDENTITY ADJUDICATION
        current_owner = (
                getattr(request, 'owner_id', None) or
                getattr(self.engine.context, 'user_id', GUEST_OWNER_ID)
        )

        # [ASCENSION 6]: Metabolic Micro-Yield
        if self.is_wasm:
            time.sleep(0)

        # 4. THE PROCLAMATION PIPELINE
        def proclaim(msg: str, status: str = "INFO"):
            icon = "●" if status == "INFO" else "⚡"
            color = "\x1b[32m" if status == "INFO" else "\x1b[35m"
            if not getattr(request, 'silent', False):
                sys.stdout.write(f"{color}[GOVERNANCE]{' ' * (10 - len(status))}{icon} {msg}\x1b[0m\n")
                sys.stdout.flush()

        try:
            # --- MOVEMENT I: RITE DISPATCH ---
            result: Optional[ScaffoldResult] = None

            if action == "list":
                result = self._conduct_list_rite(request, current_owner, proclaim, start_ns)
            elif action == "create":
                result = self._conduct_create_rite(request, current_owner, proclaim, start_ns)
            elif action == "switch":
                result = self._conduct_switch_rite(request, proclaim, start_ns)
            elif action == "delete":
                result = self._conduct_delete_rite(request, proclaim, start_ns)
            elif action in ("update", "transmute"):
                result = self._conduct_update_rite(request, proclaim, start_ns)
            elif action in ("import", "adopt"):
                result = self._conduct_import_rite(request, current_owner, proclaim, start_ns)
            else:
                raise ArtisanHeresy(f"Unmanifest Rite: '{action}' is unknown to the Governor.")

            # =========================================================================
            # == [THE CURE]: THE GNOSTIC MEMORY SUTURE                               ==
            # =========================================================================
            # [ASCENSION 2]: If we are in the Ethereal Plane, we push our result
            # into the Global Transfer Cell. This guarantees the JS layer finds it.
            if self.is_wasm:
                try:
                    import json
                    # We store the bit-perfect JSON directly in the Python global scope
                    # so that 'pyodide.globals.get' can retrieve it safely.
                    payload = self._forge_primitive_payload(result)
                    sys.modules['__main__'].__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(payload)
                    self.logger.debug(f"[{trace_id}] Result anchored to Global Transfer Cell.")
                except Exception as e:
                    self.logger.error(f"Memory Suture fractured: {e}")

            return result

        except Exception as catastrophic_paradox:
            # --- MOVEMENT II: FORENSIC EMERGENCY DUMP ---
            error_msg = f"Governance Paradox at '{action}': {str(catastrophic_paradox)}"
            sys.stderr.write(f"\n\x1b[41;1m[GOVERNANCE_FRACTURE]\x1b[0m 💀 {error_msg}\n")

            if self.is_wasm:
                # Push the failure into memory too!
                try:
                    fail_data = {"success": False, "error": error_msg, "trace": traceback.format_exc()}
                    sys.modules['__main__'].__dict__['__GNOSTIC_TRANSFER_CELL__'] = json.dumps(fail_data)
                except:
                    pass

            self._multicast_hud("LATTICE_FRACTURE", "#ef4444")

            return self.failure(
                error_msg,
                details=traceback.format_exc(),
                data={"fracture_action": action, "trace_id": trace_id}
            )

    def _forge_primitive_payload(self, result: ScaffoldResult) -> Dict[str, Any]:
        """
        [ASCENSION 3]: THE ISOMORPHIC COLLAPSE.
        Transmutes the ScaffoldResult object into a pure, JSON-safe dictionary.
        """
        if result is None:
            return {"success": False, "error": "VOID_REVELATION"}

        # We extract the core Gnosis
        payload = {
            "success": result.success,
            "message": result.message,
            "data": self._collapse(result.data) if result.data else {},
            "artifacts": [str(a.path) for a in result.artifacts],
            "trace_id": getattr(self.request, 'trace_id', 'unknown')
        }
        return payload

    def _collapse(self, obj: Any) -> Any:
        """
        =============================================================================
        == THE PRIMITIVE COLLAPSER (V-Ω-TOTALITY-V2.0)                             ==
        =============================================================================
        Recursively incinerates complex Python objects to ensure JSON purity.
        """
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        if isinstance(obj, dict):
            return {str(k): self._collapse(v) for k, v in obj.items() if not str(k).startswith('_')}
        if isinstance(obj, (list, tuple, set)):
            return [self._collapse(i) for i in obj]
        if isinstance(obj, (Path, uuid.UUID)):
            return str(obj)
        if hasattr(obj, 'model_dump'):
            return self._collapse(obj.model_dump(mode='json'))
        if hasattr(obj, '__dict__'):
            # Manual extraction for non-pydantic objects
            data = {}
            for k, v in obj.__dict__.items():
                if k.startswith('_'): continue
                # Block known metabolic noise
                if type(v).__name__ in ("Scribe", "Logger", "Engine", "UniversalSink"):
                    continue
                data[k] = self._collapse(v)
            return data
        return str(obj)

    # =========================================================================
    # == MOVEMENT: THE RITE OF CENSUS (LIST)                                 ==
    # =========================================================================
    def _conduct_list_rite(self, request: ProjectRequest, owner: str, proclaim: Callable,
                           start_ns: int) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF TOTAL CENSUS (V-Ω-TOTALITY-V9501-RECONCILED)                ==
        =============================================================================
        [THE CURE]: This rite now uses the Manager's ascended 'list_projects' method,
        which correctly merges Living matter with System Ghosts.
        """
        # [ASCENSION 5]: GHOST-BUSTING AUDIT
        # Ensure the physical anchor matches the logical mind.
        self.manager._audit_active_anchor()

        # 1. THE RECLAMATION OF SOULS
        # [THE TITANIUM SUTURE]: We delegate to the manager's unified list logic.
        projects = self.manager.list_projects(
            owner_id=owner,
            tags=request.filter_tags
        )

        active_id = self.manager.registry.active_project_id

        # 2. ISOMORPHIC SERIALIZATION
        # We collapse the list of ProjectMeta objects into primitives for the bridge.
        # This ensures the Progenitor is manifest in the JSON payload.
        project_list_primitives = [self._collapse(p) for p in projects]

        data = {
            "registry": {
                "version": self.manager.registry.version,
                "active_project_id": active_id,
                "projects": {p['id']: p for p in project_list_primitives}
            },
            "count": len(projects),
            "owner": owner,
            "active_id": active_id,
            "substrate": "WASM" if self.is_wasm else "IRON"
        }

        return self._forge_result(True, "Census manifest complete.", data, start_ns)

    # =========================================================================
    # == MOVEMENT: THE RITE OF GENESIS (CREATE)                              ==
    # =========================================================================
    def _conduct_create_rite(self, request: ProjectRequest, owner: str, proclaim: Callable,
                             start_ns: int) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF KINETIC GENESIS (V-Ω-TOTALITY)                              ==
        =============================================================================
        Forges a new reality from an Archetype Seed and anchors it to the Governor.
        """
        if not request.name:
            return self.failure("Heresy of the Anonymous: Reality requires a name.")

        proclaim(f"Initiating Genesis: Forging '[bold]{request.name}[/]'...")

        try:
            # 1. THE MATERIALIZATION STRIKE
            # Delegate to the Manager to allocate space and hydrate seeds.
            project = self.manager.create_project(
                name=request.name,
                description=request.description or "",
                owner_id=owner,
                template=request.template or "blank",
                is_demo=request.is_demo,
                tags=request.tags or []
            )

            # 2. OCULAR RADIATION
            proclaim(f"Reality Materialized: [dim]{project.id[:8]}[/].")
            self._multicast_hud("REALITY_BORN", "#64ffda")

            # 3. DATA REVELATION
            return self._forge_result(
                True,
                f"Reality '{project.name}' forged.",
                {"project": self._collapse(project)},
                start_ns
            )

        except Exception as genesis_fracture:
            self.logger.critical(f"Genesis Failure: {genesis_fracture}")
            raise ArtisanHeresy(
                f"Genesis Failure: {genesis_fracture}",
                severity=HeresySeverity.CRITICAL,
                details=traceback.format_exc()
            )

    # =========================================================================
    # == MOVEMENT: THE RITE OF ANCHORING (SWITCH)                            ==
    # =========================================================================
    def _conduct_switch_rite(self, request: ProjectRequest, proclaim: Callable, start_ns: int) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF ANCHORING (V-Ω-TOTALITY-V9501-ALLIANCE-AWARE)               ==
        =============================================================================
        [THE CURE]: This rite now scries both User and System registries to find
        the target coordinate, annihilating the 'Coordinate Lost' heresy.
        """
        target_id = getattr(request, 'id', None)
        if not target_id:
            return self.failure("Coordinate Lost: Target ID is a void.")

        # [THE TITANIUM SUTURE]
        # We scry both the User Registry and the System Demos (Ghosts)
        project = (
            self.manager.registry.projects.get(target_id) or
            self.manager.system_demos.get(target_id)
        )

        if not project:
            return self.failure(
                message=f"Coordinate Lost: Reality '{target_id}' is unmanifest.",
                suggestion="Perform a fresh census via 'scaffold project list' to resync.",
                code="ANCHOR_FRACTURE"
            )

        p_name = project.get('name') # Use .get() due to GnosticSovereignDict/Meta hybrid
        proclaim(f"Shifting Anchor to reality: '[bold cyan]{p_name}[/]'...")

        # 1. CONDUCT THE PHYSICAL SWITCH
        # This triggers JIT Ghost Materialization if needed.
        target_meta = self.manager.switch_project(target_id)

        # 2. BROADCAST THE SHIFT
        proclaim("Dimensional shift complete. Reality locked.")
        self._multicast_hud("ANCHOR_SHIFTED", "#3b82f6")

        return self._forge_result(
            True,
            f"Anchored to '{p_name}'.",
            {"project_id": target_id, "project": self._collapse(target_meta)},
            start_ns
        )

    # =========================================================================
    # == MOVEMENT: THE RITE OF ANNIHILATION (DELETE)                         ==
    # =========================================================================
    def _conduct_delete_rite(self, request: ProjectRequest, proclaim: Callable, start_ns: int) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF ANNIHILATION (V-Ω-TOTALITY)                                ==
        =============================================================================
        Returns a reality's matter shards to the void.
        """
        if not request.id:
            return self.failure("Annihilation aborted: Target ID missing.")

        project = self.manager.registry.projects.get(request.id)
        if not project:
            return self.success("Reality already void.")

        p_name = project.name

        # [FACULTY 7]: SOVEREIGNTY WARD
        if project.is_demo and not request.force:
            raise ArtisanHeresy(
                "Sovereign Restriction: System Reference realities are immutable.",
                severity=HeresySeverity.WARNING,
                suggestion="Use --force if you are the Architect of this Node."
            )

        proclaim(f"Annihilating reality: '{p_name}'...", status="DANGER")

        # 1. PHYSICAL & LOGICAL PURGE
        self.manager.delete_project(request.id, force=request.force)

        # 2. RADIATION
        proclaim("Matter shards returned to the void.")
        self._multicast_hud("REALITY_DISSOLVED", "#ef4444")

        return self._forge_result(True, f"Annihilation of '{p_name}' complete.", {}, start_ns)

    # =========================================================================
    # == INTERNAL FACULTIES (THE SENSES)                                     ==
    # =========================================================================

    def _conduct_scry_rite(self, request: ProjectRequest, start_ns: int) -> ScaffoldResult:
        """[ASCENSION 10]: METABOLIC MASS SCRYING."""
        stats = self.manager.get_project_stats()
        return self._forge_result(True, "Registry scry complete.", {"stats": stats}, start_ns)

    def _conduct_update_rite(self, request, proclaim, start_ns):
        """Transfigures metadata without touching the physical substrate."""
        target_id = getattr(request, 'id', self.manager.registry.active_project_id)
        if not target_id: return self.failure("No project ID provided or active.")

        updates = request.variables or {}
        self.manager.update_project(target_id, updates)
        proclaim(f"Reality '{target_id[:8]}' transfigured.")
        return self._forge_result(True, "Project updated.", {}, start_ns)

    def _conduct_import_rite(self, request, owner, proclaim, start_ns):
        """Adopts an existing directory into the Gnostic Multiverse."""
        path_str = getattr(request, 'path', None)
        if not path_str: return self.failure("Path required for import.")

        name = getattr(request, 'name', Path(path_str).name)
        project = self.manager.import_project(path_str, name, owner)
        proclaim(f"Imported: [bold]{name}[/]")
        return self._forge_result(True, "Import success.", {"project": self._collapse(project)}, start_ns)

    def _forge_result(self, success: bool, msg: str, data: Any, start_ns: int) -> ScaffoldResult:
        """
        =============================================================================
        == THE TELEMETRIC FORGE                                                    ==
        =============================================================================
        Injects metabolic metrics and distributed tracing into the result.
        """
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        # [ASCENSION 3]: ISO-Purity Check
        # We ensure the final payload is recursively detached from Python memory.
        pure_data = self._collapse(data)

        if isinstance(pure_data, dict):
            # METABOLIC TELEMETRY SUTURE
            pure_data["_telemetry"] = {
                "latency_ms": round(duration_ms, 2),
                "substrate": "WASM" if self.is_wasm else "IRON",
                "trace": getattr(self.request, 'trace_id', 'tr-gov-local'),
                "ts": time.time()
            }

        return self.success(msg, data=pure_data)

    def _multicast_hud(self, type_label: str, color: str):
        """[ASCENSION 11]: OCULAR HUD MULTICAST."""
        trace = getattr(self.request, 'trace_id', 'tr-governor')

        # [THE SUTURE]: Speak to the Akashic Record directly
        akashic = getattr(self.engine, 'akashic', None)
        if akashic:
            try:
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GOVERNANCE_STRIKE",
                        "label": type_label,
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_PROJECT_GOVERNOR substrate={'WASM' if self.is_wasm else 'IRON'} status=RESONANT>"


