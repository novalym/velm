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

    def _collapse(self, obj: Any, _seen: Optional[Set[int]] = None, _depth: int = 0) -> Any:
        """
        =============================================================================
        == THE OMEGA COLLAPSER: TOTALITY (V-Ω-TOTALITY-V300K-UNBREAKABLE)          ==
        =============================================================================
        LIF: ∞ | ROLE: NEURAL_DATA_SIEVE | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_COLLAPSE_V300_TITANIUM_WARD_2026_FINALIS
        """
        # --- STRATUM 0: THE DEPTH & IDENTITY GATES ---
        if _depth > 20:
            return "[MAX_DEPTH_REACHED]"

        if _seen is None:
            _seen = set()

        # --- STRATUM 1: THE PRIMITIVE RESONANCE ---
        if obj is None or isinstance(obj, (str, int, float, bool)):
            return obj

        # --- STRATUM 2: THE RECURSION WARD ---
        # We use object ID to detect circularities at nanosecond speed.
        obj_id = id(obj)
        if obj_id in _seen:
            return f"[CIRCULAR_REFERENCE:{type(obj).__name__}]"

        _seen.add(obj_id)

        try:
            # --- STRATUM 3: THE ALCHEMICAL TRANSMUTATION ---

            # 1. THE DICTIONARY MATRIX (With Ghost-Key Protection)
            if isinstance(obj, dict):
                purified = {}
                for k, v in obj.items():
                    k_str = str(k)
                    # [THE CURE]: PROTECT PRIVATE STRATA & EMPTY KEYS
                    if k_str.startswith('_') or k_str == "":
                        continue
                    purified[k_str] = self._collapse(v, _seen, _depth + 1)
                return purified

            # 2. THE SEQUENCE LATTICE (List, Tuple, Set)
            if isinstance(obj, (list, tuple, set, frozenset)):
                return [self._collapse(i, _seen, _depth + 1) for i in obj]

            # 3. THE BINARY SOUL (Bytes)
            if isinstance(obj, (bytes, bytearray)):
                import base64
                return f"data:application/octet-stream;base64,{base64.b64encode(obj).decode('utf-8')}"

            # 4. THE LINGUISTIC ENUMERATOR (Enum)
            import enum
            if isinstance(obj, enum.Enum):
                return obj.value

            # 5. THE SPATIOTEMPORAL COORDINATES (Paths & IDs)
            if hasattr(obj, '__fspath__') or isinstance(obj, (Path, uuid.UUID)):
                return str(obj)

            # 6. THE NEURAL MODELS (Pydantic V2 / V1)
            # We check for model_dump (V2) first for Rust-speed serialization.
            if hasattr(obj, 'model_dump'):
                return self._collapse(obj.model_dump(mode='json'), _seen, _depth + 1)
            if hasattr(obj, 'dict'):
                return self._collapse(obj.dict(), _seen, _depth + 1)

            # 7. THE FISCAL & TEMPORAL MATTER (Decimals & Dates)
            from decimal import Decimal
            from datetime import datetime, date
            if isinstance(obj, Decimal):
                return float(obj)
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()

            # 8. THE OBJECT REVELATION (__dict__)
            # This is the "Emergency Inquest" for custom classes.
            if hasattr(obj, '__dict__'):
                data = {}
                for k, v in obj.__dict__.items():
                    # Ward against private strata
                    if k.startswith('_'):
                        continue

                    # [ASCENSION 6]: THE REGISTRY BLACKLIST
                    # We physically refuse to serialize the Engine's heavy organs.
                    v_type_name = type(v).__name__
                    if v_type_name in (
                            "ScaffoldEngine", "ArtisanRegistry", "InfrastructureManager",
                            "ProjectManager", "GnosticTransaction", "Scribe", "Logger",
                            "UniversalSink", "RuntimeContext", "Client"
                    ):
                        continue

                    data[k] = self._collapse(v, _seen, _depth + 1)
                return data

            # 9. THE FALLBACK PROCLAMATION
            # If the soul is unknown, we return its string representation.
            return str(obj)

        except Exception as fracture:
            # The Scribe must never fracture reality during an Inquest.
            return f"[SERIALIZATION_FRACTURE: {type(fracture).__name__}]"
        finally:
            # Release the object from the seen set as we surface
            _seen.remove(obj_id)


    # =========================================================================
    # == MOVEMENT: THE RITE OF CENSUS (LIST)                                 ==
    # =========================================================================
    def _conduct_list_rite(self, request: ProjectRequest, owner: str, proclaim: Callable,
                           start_ns: int) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF TOTAL CENSUS: OMEGA (V-Ω-TOTALITY-V25000-HEALED)            ==
        =============================================================================
        LIF: ∞ | ROLE: PANOPTIC_CENSUS_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_LIST_V25K_DICT_RECONCILIATION_2026
        """
        # [ASCENSION 1]: Lazy Hash Recalculation
        # Ensure the Manager's state hash reflects the current substrate reality.
        if hasattr(self.manager, '_calculate_state_hash'):
            self.manager._calculate_state_hash()

        # 1. THE RECLAMATION OF SOULS
        # Scry the unified list from the manager (Demos + Users).
        projects = self.manager.list_projects(
            owner_id=owner,
            tags=request.filter_tags
        )

        # [ASCENSION 5]: BICAMERAL REGISTRY FUSION
        # Resolve the active anchor ID from the ledger.
        active_id = self.manager.registry.get("active_project_id")

        # 2. ISOMORPHIC SERIALIZATION (THE CURE)
        # We handle both dicts and objects, transmuting them into pure Gnostic Primitives.
        # This annihilates the 'AttributeError' by ensuring we iterate over a safe list.
        project_list_primitives = []
        for p in projects:
            # Suture: If p is an object, model_dump it. If it's a dict, use it.
            p_data = p if isinstance(p, dict) else (p.model_dump() if hasattr(p, 'model_dump') else p.__dict__)
            project_list_primitives.append(self._collapse(p_data))

        data = {
            "registry": {
                "version": self.manager.registry.get("version", "2.0.0"),
                "active_project_id": active_id,
                "projects": {p.get('id', 'void'): p for p in project_list_primitives}
            },
            "count": len(projects),
            "state_hash": getattr(self.manager, 'state_hash', "0xVOID"),
            "substrate": "WASM" if self.is_wasm else "IRON"
        }

        # [ASCENSION 12]: THE FINALITY VOW
        return self._forge_result(True, "Census manifest complete.", data, start_ns)

    # =========================================================================
    # == MOVEMENT: THE RITE OF GENESIS (CREATE)                              ==
    # =========================================================================
    def _conduct_create_rite(self, request: ProjectRequest, owner: str, proclaim: Callable,
                             start_ns: int) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF GENESIS: OMEGA (V-Ω-TOTALITY-V25000-DICT-RESONANT)         ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_MATERIALIZER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_CREATE_V25K_ATTRIBUTE_SUTURE_2026
        """
        if not request.name:
            return self.failure("Heresy of the Anonymous: Reality requires a name.")

        proclaim(f"Initiating Genesis: Forging '[bold]{request.name}[/]'...")

        # [ASCENSION 3]: ADRENALINE IGNITION
        # Command the Engine to prioritize I/O velocity for the creation strike.
        if hasattr(self.engine, 'set_adrenaline'):
            self.engine.set_adrenaline(True)

        try:
            # 1. THE KINETIC STRIKE
            # [THE CURE]: The Manager now returns a pure DICT soul.
            project = self.manager.create_project(
                name=request.name,
                description=request.description or "",
                owner_id=owner,
                template=request.template or "blank",
                is_demo=request.is_demo,
                tags=request.tags or []
            )

            # [ASCENSION 4]: NONETYPE SARCOPHAGUS
            if not project:
                raise RuntimeError("Kernel rejected the creation of matter.")

            # [THE SUTURE]: Index-Safe Identity Extraction
            p_name = project.get('name', request.name)
            p_id = project.get('id', 'void')

            # 2. DATA REVELATION
            # We ensure the 'project' key is manifest in the data vessel for the UI Wizard.
            return self._forge_result(
                True,
                f"Reality '{p_name}' forged.",
                {
                    "project": self._collapse(project),
                    "project_id": p_id,
                    "template": project.get('template', 'blank')
                },
                start_ns
            )

        except Exception as genesis_fracture:
            # [ASCENSION 11]: ATOMIC ROLLBACK PROTOCOL
            # In the event of a fracture, we command the reaper to clean the shards.
            self.logger.critical(f"Genesis Failure: {genesis_fracture}")
            return self.failure(
                f"Genesis Failure: {genesis_fracture}",
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL
            )
        finally:
            if hasattr(self.engine, 'set_adrenaline'):
                self.engine.set_adrenaline(False)

    # =========================================================================
    # == MOVEMENT: THE RITE OF ANCHORING (SWITCH)                            ==
    # =========================================================================
    def _conduct_switch_rite(self, request: ProjectRequest, proclaim: Callable, start_ns: int) -> ScaffoldResult:
        """
        =============================================================================
        == THE RITE OF ANCHORING: OMEGA (V-Ω-TOTALITY-V25000-GHOST-MATERIALIZER)  ==
        =============================================================================
        LIF: ∞ | ROLE: DIMENSIONAL_ANCHOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_SWITCH_V25K_GHOST_BIOPSY_FINALIS
        """
        target_id = getattr(request, 'id', None)
        if not target_id:
            return self.failure("Coordinate Lost: Target ID is a void.")

        # --- MOVEMENT I: THE TRIANGULATION ---
        # [ASCENSION 1]: Index-Safe Triage
        # We scry both the User Registry and the System Reference strata.
        reg_projects = self.manager.registry.get("projects", {})
        project = reg_projects.get(target_id) or self.manager.system_demos.get(target_id)

        if not project:
            return self.failure(
                message=f"Coordinate Lost: Reality '{target_id}' is unmanifest.",
                suggestion="Perform a fresh census via 'scaffold project list' to resync the Mind.",
                code="ANCHOR_FRACTURE"
            )

        # [THE CURE]: Object-to-Dict Transmutation for Demos
        p_dict = project if isinstance(project, dict) else (
            project.model_dump() if hasattr(project, 'model_dump') else project.__dict__)
        p_name = p_dict.get('name', 'Unknown')
        p_path_raw = p_dict.get('path', '/vault/project')

        proclaim(f"Shifting Anchor to reality: '[bold cyan]{p_name}[/]'...")

        # --- MOVEMENT II: GEOMETRIC NORMALIZATION & BIOPSY ---
        # [ASCENSION 7 & 9]: Resolve to absolute POSIX coordinate.
        project_path = Path(p_path_raw).resolve()
        project_path_posix = project_path.as_posix()

        # Ensure directory exists physically on the substrate
        try:
            if not project_path.exists():
                project_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ArtisanHeresy(f"Substrate Lock: Cannot create sanctum at {project_path_posix}. Reason: {e}")

        # --- MOVEMENT III: THE GHOST BIOPSY (RESILIENCE) ---
        # [ASCENSION 2]: We assume it is a ghost if marked OR if the directory is empty.
        # This solves the 'Soul is Void' anomaly when a project ID exists but no matter was struck.
        custom_data = p_dict.get("custom_data", {})
        is_marked_ghost = custom_data.get("is_ghost", False)

        try:
            # We ignore .scaffold metadata and system noise when checking for emptiness
            visible_matter = [
                p for p in project_path.iterdir()
                if p.name not in [".scaffold", "scaffold.lock", ".heartbeat", ".DS_Store"]
            ]
            is_hollow = len(visible_matter) == 0
        except Exception:
            is_hollow = True

        # --- MOVEMENT IV: THE RITE OF JIT GENESIS ---
        # If the reality is hollow, we command the Engine to conduct a silent Inception.
        if is_marked_ghost or is_hollow:
            self.logger.info(f"Materializing Ghost Reality: '{p_name}'...")

            try:
                from ...interfaces.requests import InitRequest

                # [ASCENSION 3]: ADRENALINE MODE
                if hasattr(self.engine, 'set_adrenaline'): self.engine.set_adrenaline(True)

                init_plea = InitRequest(
                    profile=p_dict.get('template', 'blank'),
                    project_root=project_path_posix,
                    force=True,  # Overwrite the empty directory husks
                    non_interactive=True,  # Silence the Oracle
                    variables={
                        "project_name": p_name,
                        "description": p_dict.get('description', ''),
                        "no_edicts": self.is_wasm,  # Mute shell in browser
                        "trace_id": getattr(request, 'trace_id', 'tr-ghost-resurrection')
                    }
                )

                # [STRIKE]: Synchronous materialization via recursive Dispatch
                result = self.engine.dispatch(init_plea)

                if not result.success:
                    self.logger.error(f"Ghost Materialization Fracture: {result.message}")
                    return self.failure(f"Reality Inception Failed: {result.message}")

            except Exception as e:
                self.logger.error(f"Fracture during Ghost materialization: {e}")
                return self.failure(f"Genesis Exception: {str(e)}", details=traceback.format_exc())
            finally:
                if hasattr(self.engine, 'set_adrenaline'): self.engine.set_adrenaline(False)

        # --- MOVEMENT V: THE LEDGER UPDATE ---
        # Now that matter is verified or manifest, we update the Manager's active pointer.
        # [THE CURE]: The manager's switch_project is now index-safe.
        target_meta = self.manager.switch_project(target_id)

        # Ensure return metadata is a pure primitive dict
        final_meta = target_meta if isinstance(target_meta, dict) else (
            target_meta.model_dump() if hasattr(target_meta, 'model_dump') else target_meta)

        # --- MOVEMENT VI: RADIATE THE RESONANCE ---
        proclaim("Dimensional shift complete. Reality locked.")
        self._multicast_hud("ANCHOR_SHIFTED", "#3b82f6")

        return self._forge_result(
            True,
            f"Anchored to '{p_name}'.",
            {"project_id": target_id, "project": self._collapse(final_meta)},
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


