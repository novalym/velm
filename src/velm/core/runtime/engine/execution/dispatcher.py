# Path: src/velm/core/runtime/engine/execution/dispatcher.py
# ----------------------------------------------------------


import os
import sys
import time
import traceback
import uuid
import json
import inspect
import asyncio
import threading
import concurrent.futures
import base64
import re
from typing import Any, Optional, Dict, List, Union, Set, Final, Type
from pathlib import Path
from contextlib import contextmanager
from decimal import Decimal

# --- GNOSTIC UPLINKS ---
from .....interfaces.base import ScaffoldResult, Artifact
from .....interfaces.requests import BaseRequest, AnalyzeRequest, RefactorRequest
from ....state.machine import GnosticRite
from .context import ContextLevitator
from ....daemon.serializer import gnostic_serializer
from .....logger import Scribe
from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

# [ASCENSION 23]: IMPORT THE SOVEREIGN URI ORACLE
try:
    from ....lsp.base.utils import UriUtils
except ImportError:
    UriUtils = None


class QuantumDispatcher:
    """
    =================================================================================
    == THE QUANTUM DISPATCHER (V-Ω-MULTICAST-PRISM-ILLUMINATED-ASCENDED)           ==
    =================================================================================
    LIF: ∞ | ROLE: SOVEREIGN_ROUTER | RANK: OMEGA_SOVEREIGN

    The central routing authority of the God-Engine. It stands between the
    Architect's Intent and the Artisan's Hand.

    It is the Unbreakable Hub where all requests—from CLI, LSP, or AI—converge,
    are purified, executed, and chronicled.
    """

    # [ASCENSION 3]: RECURSION LIMIT
    MAX_DISPATCH_DEPTH: Final[int] = 10

    # [ASCENSION 4]: REPLAY LOG PATH
    REPLAY_LOG_PATH: Final[str] = ".scaffold/replay.jsonl"

    def __init__(self, engine: Any):
        self.engine = engine
        self.levitator = ContextLevitator(engine)
        self.logger = Scribe("QuantumDispatcher")
        self._trace_enabled = os.environ.get("SCAFFOLD_TRACE") == "1"

        # [ASCENSION 2]: Depth Tracking (TraceID -> Depth)
        self._recursion_depths: Dict[str, int] = {}
        self._recursion_lock = threading.Lock()

    def _trace(self, msg: str):
        if self._trace_enabled:
            sys.stderr.write(f"[DISPATCH] {msg}\n")
            sys.stderr.flush()

    def levitate_context(self, root: Union[str, Path, None]):
        """Public API for Artisans to request levitation."""
        return self.levitator.levitate(root)

    # =========================================================================
    # == RITE I: THE TYPE MIRROR & POLYGLOT ADAPTER                          ==
    # =========================================================================

    def _mirror_type_safety(self, data: Any, depth: int = 0) -> Any:
        """
        [ASCENSION 2 & 6]: THE UNIVERSAL GNOSTIC TYPE-MIRROR & POLYGLOT ADAPTER.
        Recursively transmutes Python types into JSON-safe primitives.
        Handles Bytes -> Base64, Path -> Str, Decimal -> Str.
        """
        if depth > 50: return "[RECURSION_LIMIT]"

        # 1. Dictionary Recursion
        if isinstance(data, dict):
            return {str(k): self._mirror_type_safety(v, depth + 1) for k, v in data.items()}

        # 2. List Recursion
        elif isinstance(data, (list, tuple, set)):
            return [self._mirror_type_safety(i, depth + 1) for i in data]

        # 3. [ASCENSION 6]: Polyglot Binary Adapter
        elif isinstance(data, bytes):
            try:
                return base64.b64encode(data).decode('utf-8')
            except Exception:
                return "[BINARY_DATA]"

        # 4. Big Integer Protection
        elif isinstance(data, int):
            if abs(data) > 9007199254740991:
                return str(data)
            return data

        # 5. Decimal Precision
        elif isinstance(data, Decimal):
            return str(data)

        # 6. Path Object Handling
        elif isinstance(data, Path):
            return str(data).replace('\\', '/')

        # 7. Pydantic Model Handling
        elif hasattr(data, 'model_dump'):
            return self._mirror_type_safety(data.model_dump(mode='json'), depth + 1)

        # 8. UUID Handling
        elif isinstance(data, uuid.UUID):
            return str(data)

        # 9. Exception Handling
        elif isinstance(data, Exception):
            return f"{type(data).__name__}: {str(data)}"

        return data

    # =========================================================================
    # == RITE II: THE GRAND DISPATCH                                         ==
    # =========================================================================
    def dispatch(self,
                 request: Union[BaseRequest, Dict[str, Any], str],
                 params: Optional[Dict[str, Any]] = None,
                 **kwargs) -> ScaffoldResult:
        """
        =================================================================================
        == THE OMNISCIENT DISPATCH RITE: TOTALITY (V-Ω-V3000-LOCK-GATED-FINALIS)       ==
        =================================================================================
        LIF: ∞ | ROLE: SOVEREIGN_TRAFFIC_CONDUCTOR | RANK: OMEGA_SUPREME
        AUTH: Ω_DISPATCH_V3000_TITANIUM_STABILITY_2026_FINALIS

        [THE MANIFESTO]
        The absolute entry point of the God-Engine. It implements the Achronal Lock
        Grid (LIF-100) to annihilate the Windows Read-Write Schism. It performs
        multi-modal intent recovery, metabolic backpressure throttling, and
        forensic dump protection with automated entropy redaction.
        =================================================================================
        """
        import time
        import hashlib
        import importlib
        import inspect
        import asyncio
        import threading
        import re
        import uuid
        import traceback as tb_scribe
        from .locking import ResourceLockManager
        from .....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
        from .....interfaces.base import ScaffoldResult, Artifact
        from .....core.runtime.vessels import GnosticSovereignDict

        # --- MOVEMENT 0: NANOSECOND CHRONOMETRY & IDENTITY ---
        start_time = time.perf_counter()
        jit_overhead_ms = 0.0
        rite_name = "UnknownRite"
        trace_id = "tr-unbound"
        request_obj = None

        # [ASCENSION 3]: SHADOW CONTEXT MIRROR
        # Pre-emptive trace identification to ensure failures are always named.
        if isinstance(request, (BaseRequest, object)) and hasattr(request, 'trace_id'):
            trace_id = getattr(request, 'trace_id') or trace_id

        try:
            # --- MOVEMENT I: TRANSMUTATION (INPUT NORMALIZATION) ---
            # [ASCENSION 4 & 11]: SOCRATIC INTENT RECOVERY & DIVINATION
            if isinstance(request, str):
                request_obj = self._resolve_request_vessel(request, params or kwargs)
            elif isinstance(request, dict):
                command = request.get('command') or request.get('method')
                payload = request.get('params') or request

                if not command and 'prompt' in payload:
                    command = self._divine_intent_from_prompt(payload['prompt'])
                    self.logger.info(f"[{trace_id}] Semantic Router divined intent: {command}")

                if not command:
                    return self.engine.failure("Void Intent: Request missing 'command' anchor.")
                request_obj = self._resolve_request_vessel(command, payload)
            else:
                request_obj = request

            request_type = type(request_obj)
            rite_name = request_type.__name__
            request_id = getattr(request_obj, 'request_id', 'unknown')
            project_root = getattr(request_obj, 'project_root', self.engine.project_root)

            # --- MOVEMENT II: CAUSAL IDENTITY (TRACE ANCHORING) ---
            meta = getattr(request_obj, 'metadata', {})
            meta_dict = meta.model_dump(mode='json') if hasattr(meta, 'model_dump') else (
                meta if isinstance(meta, dict) else {})

            trace_id = (
                    meta_dict.get('trace_id') or
                    meta_dict.get('x_nov_trace') or
                    getattr(request_obj, 'trace_id', None) or
                    f"tr-{uuid.uuid4().hex[:8].upper()}"
            )

            # [ASCENSION 9]: BICAMERAL CONTEXT MIRRORING
            # Mirror the trace ID into the Engine's primary thread cell for non-passed logging.
            self.engine.active_trace_id = trace_id

            # Suture the silver cord to the object for distributed traceability.
            if not hasattr(request_obj, 'trace_id') or getattr(request_obj, 'trace_id') in [None, "None", "tr-void"]:
                try:
                    object.__setattr__(request_obj, 'trace_id', trace_id)
                except (AttributeError, TypeError):
                    pass

            self._trace(f"Dispatching {rite_name} :: ID {request_id} :: Trace {trace_id}")

            # --- MOVEMENT III: RECURSIVE AMPLIFICATION GUARD ---
            with self._recursion_lock:
                current_depth = self._recursion_depths.get(trace_id, 0)
                if current_depth > self.MAX_DISPATCH_DEPTH:
                    raise ArtisanHeresy(
                        f"Recursion Heresy: Dispatch depth limit ({self.MAX_DISPATCH_DEPTH}) breached for {trace_id}.",
                        severity=HeresySeverity.CRITICAL
                    )
                self._recursion_depths[trace_id] = current_depth + 1

            # --- MOVEMENT IV: THERMODYNAMIC ADJUDICATION & LOCK GATING ---
            # [ASCENSION 1]: THE ACHRONAL LOCK GRID (LIF-100)
            is_writing_rite = any(
                k in rite_name for k in ['Genesis', 'Transmute', 'Create', 'Patch', 'Undo', 'Refactor'])
            is_heavy = is_writing_rite or any(k in rite_name for k in ['Analyze', 'Manifest', 'Inception', 'Index'])

            # Anchor the lock to the project root coordinate.
            resource_key = f"project:{hashlib.md5(str(project_root).encode()).hexdigest()}"

            # [ASCENSION 5 & 6]: METABOLIC BACKPRESSURE THROTTLING
            load = self.engine.watchdog.get_vitals().get("load_percent", 0)
            if load > 85.0:
                self.logger.warn(f"[{trace_id}] Metabolic Fever ({load}%). Priority set to background.")
                if hasattr(request_obj, 'metadata'):
                    request_obj.metadata.priority = "background"
                if load > 92.0:
                    time.sleep(0.1)  # Hydraulic Yield

            # =========================================================================
            # == THE QUANTUM BARRIER (ACHRONAL LOCK GRID)                           ==
            # =========================================================================
            # Substrate-aware gating: Shared lock for reading (Cortex), Exclusive for writing (Committer).
            with ResourceLockManager.acquire(resource_key, exclusive=is_writing_rite):

                self.engine._neuro_optimize(heavy_mode=is_heavy)

                # --- MOVEMENT V: ARTISAN RESOLUTION ---
                if hasattr(request_obj, 'project_root') and request_obj.project_root:
                    self.engine.memory.record_focus(str(request_obj.project_root))

                # Check Circuit Breaker health
                if hasattr(self.engine, 'healer') and not self.engine.healer.circuit_breaker.check_state(rite_name):
                    return self.engine.failure(f"Subsystem Quarantined: {rite_name} is fracturing.")

                artisan_info = self.engine.registry.get_artisan_for(request_type)
                artisan_instance = None

                if artisan_info is None:
                    suggestion = self.engine.registry.suggest_alternative(rite_name)
                    return self.engine.failure(
                        message=f"Unmanifest Artisan: No handler for '{rite_name}'.",
                        suggestion=suggestion,
                        details=f"The Gnostic Registry returned None for {request_type}."
                    )

                # [ASCENSION 9]: JIT AWAKENING PULSE (HOT-SWAP AWARE)
                if isinstance(artisan_info, tuple):
                    module_path, class_name = artisan_info
                    jit_start = time.perf_counter()
                    if os.environ.get("SCAFFOLD_HOT_SWAP") == "1":
                        with self.engine.kernel_lock("jit_reception"):
                            try:
                                for m in [m for m in sys.modules if m.startswith(module_path)]:
                                    sys.modules.pop(m, None)
                                module = importlib.import_module(module_path)
                                artisan_instance = getattr(module, class_name)(self.engine)
                            except Exception as syntax_heresy:
                                self._conduct_forensic_dump(syntax_heresy, f"JIT_FRACTURE:{class_name}", trace_id)
                                return self.engine.failure(f"Syntax Heresy in {class_name}",
                                                           details=tb_scribe.format_exc())

                    if not artisan_instance:
                        module = importlib.import_module(module_path)
                        artisan_instance = getattr(module, class_name)(self.engine)

                    jit_overhead_ms = (time.perf_counter() - jit_start) * 1000
                else:
                    artisan_instance = artisan_info(self.engine) if isinstance(artisan_info, type) else artisan_info

                if hasattr(artisan_instance, 'engine'):
                    object.__setattr__(artisan_instance, 'engine', self.engine)

                # --- MOVEMENT VI: HYBRID KINETIC EXECUTION ---
                def _conduct_rite(req: BaseRequest) -> ScaffoldResult:
                    self._broadcast_progress(f"Executing {rite_name}...", 25, trace_id)

                    if is_heavy and not req.dry_run:
                        self._chronicle_replay_capability(req, rite_name)

                    with self.engine.transactions.atomic_rite(f"{rite_name}:{req.request_id}") as tx_id:
                        if req.context is None: req.context = {}
                        req.context['transaction_id'] = tx_id

                        # Async/Sync Bifurcation
                        if inspect.iscoroutinefunction(artisan_instance.execute):
                            return asyncio.run(artisan_instance.execute(req))
                        return artisan_instance.execute(req)

                # [PIPELINE IGNITION]
                result = self.engine.pipeline.execute(request_obj, _conduct_rite)

                # [ASCENSION 5 & 6]: NONETYPE SARCOPHAGUS V2
                if result is None:
                    result = self.engine.failure(f"Void Return: Subsystem {rite_name} returned None.")

                if not result.data:
                    try:
                        object.__setattr__(result, 'data', GnosticSovereignDict())
                    except:
                        pass

                # --- MOVEMENT VII: KINETIC AFTERSHOCK (THE FIX) ---
                # [ASCENSION 3]: Immediately invalidate stale Cortex memories if reality was transfigured.
                if is_writing_rite and result.success and result.artifacts:
                    self.engine.cortex.forget_affected_areas(result.artifacts)

                # --- MOVEMENT VIII: POST-PROCESS & TELEMETRY ---
                result.duration_seconds = time.perf_counter() - start_time
                if jit_overhead_ms > 0:
                    result.ui_hints["jit_ms"] = jit_overhead_ms

                if hasattr(self.engine, 'predictor'):
                    self.engine.predictor.observe_outcome(request_obj, result)

                self.engine.memory.record_rite(rite_name, result.success)

                # [ASCENSION 23]: REVELATION (HUD MULTICAST)
                if self.engine.akashic:
                    self._multicast_revelation(request_obj, result, rite_name)

                return result

        except Exception as catastrophic_paradox:
            # --- MOVEMENT IX: FORENSIC ILLUMINATION ---
            # [ASCENSION 1 & 8]: Redundant stderr dump with Entropy Redaction.
            self._conduct_forensic_dump(catastrophic_paradox, rite_name, trace_id)

            fail_duration = time.perf_counter() - start_time
            if request_obj:
                return self.engine.healer.handle_panic(catastrophic_paradox, request_obj, fail_duration)
            else:
                return ScaffoldResult.forge_failure(
                    message=f"Dispatch Collapse: {catastrophic_paradox}",
                    traceback=tb_scribe.format_exc()
                )

        finally:
            # [ASCENSION 2 & 10]: RECURSIVE DEPTH DE-ESCALATION
            with self._recursion_lock:
                if trace_id in self._recursion_depths:
                    self._recursion_depths[trace_id] -= 1
                    if self._recursion_depths[trace_id] <= 0:
                        del self._recursion_depths[trace_id]

            if 'is_heavy' in locals() and is_heavy:
                self.engine._neuro_optimize(heavy_mode=False)

    def _conduct_forensic_dump(self, error: Exception, rite: str, trace: str):
        """
        =============================================================================
        == THE FORENSIC SCRIBE (V-Ω-ENTROPY-SAFE-REDACTION)                        ==
        =============================================================================
        [ASCENSION 8]: Performs a high-impact stderr dump while surgically scrubbing
        high-entropy variables (API keys/secrets) from the traceback string.
        """
        import re
        import sys
        import traceback as tb_scribe

        raw_tb = tb_scribe.format_exc()

        # [ENTROPY SIEVE]: Redact potential secrets before proclamation.
        # Targets standard patterns like 'sk_live', 'ghp_', 'password=', etc.
        patterns = [
            (r'(api_key|token|password|secret)\s*[:=]\s*["\']?[^\s"\'}]+["\']?', r'\1=REDACTED'),
            (r'(sk_live_[a-zA-Z0-9]{24})', '[STRIPE_KEY_REDACTED]'),
            (r'(ghp_[a-zA-Z0-9]{36})', '[GITHUB_KEY_REDACTED]')
        ]

        clean_tb = raw_tb
        for pat, repl in patterns:
            clean_tb = re.sub(pat, repl, clean_tb, flags=re.IGNORECASE)

        sys.stderr.write(f"\n" + "!" * 80 + "\n")
        sys.stderr.write(f"🔥 CATASTROPHIC DISPATCH FRACTURE: {rite}\n")
        sys.stderr.write(f"📍 TRACE ID: {trace}\n")
        sys.stderr.write(f"📍 ERROR: {type(error).__name__}: {str(error)}\n")
        sys.stderr.write("-" * 80 + "\n")
        sys.stderr.write(clean_tb)
        sys.stderr.write("!" * 80 + "\n\n")
        sys.stderr.flush()

    def _resolve_request_vessel(self, command: str, params: Dict[str, Any]) -> BaseRequest:
        """
        [THE VESSEL FORGE]
        Transmutes a raw command string into a strict Pydantic Request object.
        """
        clean_key = command.split('.')[-1].split('/')[-1]

        request_class = None
        if hasattr(self.engine, 'registry') and hasattr(self.engine.registry, 'get_request_class'):
            request_class = self.engine.registry.get_request_class(clean_key)

        if not request_class and hasattr(self.engine, 'nexus') and self.engine.nexus:
            request_class = self.engine.nexus.REQUEST_MAP.get(clean_key)

        if not request_class:
            raise ValueError(f"Unknown Rite: '{clean_key}'. The Grimoire does not contain this spell.")

        try:
            return request_class.model_validate(params)
        except Exception as e:
            try:
                return request_class(**params)
            except:
                raise ValueError(f"Schema Mismatch for '{clean_key}': {e}")

    def _divine_intent_from_prompt(self, prompt: str) -> str:
        """[ASCENSION 5]: THE SEMANTIC ROUTER"""
        p = prompt.lower()
        if any(w in p for w in ["analyze", "check", "audit", "scan"]):
            return "AnalyzeRequest"
        if any(w in p for w in ["fix", "refactor", "change", "update"]):
            return "RefactorRequest"
        if any(w in p for w in ["create", "generate", "make", "forge"]):
            return "GenesisRequest"
        return "ArchitectRequest"  # Default to chat

    def _chronicle_replay_capability(self, request: BaseRequest, rite_name: str):
        """[ASCENSION 4]: THE ECHO CHAMBER"""
        try:
            log_dir = Path(self.REPLAY_LOG_PATH).parent
            log_dir.mkdir(parents=True, exist_ok=True)

            entry = {
                "timestamp": time.time(),
                "rite": rite_name,
                "params": request.model_dump(mode='json'),
                "trace_id": getattr(request, 'trace_id', None)
            }

            with open(self.REPLAY_LOG_PATH, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + "\n")
        except:
            pass

    def _scan_for_unclaimed_artifacts(self, request: BaseRequest, result: ScaffoldResult, start_time: float):
        """[ASCENSION 3]: THE ARTIFACT BLOOM"""
        if not hasattr(request, 'project_root') or not request.project_root:
            return

        root = Path(request.project_root)
        known_paths = {a.path for a in result.artifacts}

        # Fast scan for files modified after start_time
        # Depth limit 3 to avoid scanning node_modules
        for dirpath, _, filenames in os.walk(root):
            if '.git' in dirpath or 'node_modules' in dirpath: continue

            for f in filenames:
                p = Path(dirpath) / f
                if p in known_paths: continue

                try:
                    if p.stat().st_mtime > start_time:
                        result.artifacts.append(Artifact(
                            path=p,
                            type="file",
                            action="modified (bloomed)",
                            metadata={"source": "bloom"}
                        ))
                except:
                    pass

    def _synthesize_haptics(self, result: ScaffoldResult):
        """[ASCENSION 7]: THE HAPTIC SYNTHESIZER"""
        if not result.ui_hints:
            result.ui_hints = {}

        msg = result.message.lower()
        if result.success:
            if any(w in msg for w in ["success", "complete", "done", "fixed", "forged"]):
                result.ui_hints.setdefault("vfx", "bloom")
                result.ui_hints.setdefault("sound", "success_chime")
            else:
                result.ui_hints.setdefault("vfx", "pulse_green")
        else:
            if "critical" in msg or "fracture" in msg:
                result.ui_hints.setdefault("vfx", "shake")
                result.ui_hints.setdefault("sound", "error_heavy")
            else:
                result.ui_hints.setdefault("vfx", "flash_red")

    # =========================================================================
    # == RITE III: THE MULTICAST PRISM (BROADCAST)                           ==
    # =========================================================================

    def _multicast_revelation(self, request: BaseRequest, result: ScaffoldResult, artisan_name: str):
        """
        =============================================================================
        == THE MULTICAST PRISM (V-Ω-TOTALITY-V9005-URI-COMPLIANT)                  ==
        =============================================================================
        LIF: ∞ | ROLE: SIGNAL_DIFFRACTION_ENGINE | RANK: OMEGA_SOVEREIGN

        Splits the unitary result into specialized beams of light for the Ocular UI.
        """
        from .....artisans.analyze.reporting.privacy import PrivacySentinel

        # Recursion Guard
        # We use a thread-local guard if possible, or simple name check
        # This prevents infinite loops if broadcasting triggers a log that triggers a broadcast
        if hasattr(self, '_broadcasting') and self._broadcasting:
            return
        self._broadcasting = True

        try:
            akashic = getattr(self.engine, 'akashic', None)
            if not akashic or not result:
                return

            if inspect.isawaitable(result):
                return

            data = result.data if isinstance(result.data, dict) else {}
            trace_id = getattr(request, 'trace_id', 'tr-unbound')
            ts = time.time()

            # [ASCENSION 23]: ISOMORPHIC URI SYNTHESIS
            def to_gnostic_uri(path_candidate: Any) -> str:
                if not path_candidate: return "file:///unknown"
                p_str = str(path_candidate)
                if p_str.startswith(('file:', 'scaffold-shadow:', 'inmemory:', 'vscode-vfs:')):
                    return p_str
                if UriUtils:
                    try:
                        return UriUtils.to_uri(Path(p_str))
                    except:
                        pass
                clean_path = p_str.replace('\\', '/')
                return f"file:///{clean_path.lstrip('/')}"

            # --- BEAM 1: DIAGNOSTICS ---
            diagnostics = result.diagnostics or data.get("diagnostics", [])
            if diagnostics or "Analyze" in artisan_name:
                target_path = data.get("path") or getattr(request, 'file_path', None)
                if target_path:
                    uri = to_gnostic_uri(target_path)
                    safe_diagnostics = []
                    for d in diagnostics:
                        d['message'] = PrivacySentinel.redact(d.get('message', ''))
                        safe_diagnostics.append(d)

                    akashic.broadcast({
                        "method": "textDocument/publishDiagnostics",
                        "params": {
                            "uri": uri,
                            "diagnostics": safe_diagnostics,
                            "_source": artisan_name,
                            "_ts": ts
                        },
                        "trace_id": trace_id,
                        "tags": ["HERESY", "SYNC"]
                    })

                    if any(d.get('severity') == 1 for d in safe_diagnostics):
                        akashic.broadcast({
                            "method": "gnostic/vfx",
                            "params": {"type": "shake", "intensity": 0.8, "uri": uri},
                            "trace_id": trace_id
                        })

            # --- BEAM 2: STRUCTURE ---
            if "structure" in data:
                target_path = data.get("path") or getattr(request, 'file_path', None)
                if target_path:
                    uri = to_gnostic_uri(target_path)
                    structure = data["structure"]
                    if isinstance(structure, list):
                        def _sanitize_tree(nodes):
                            for node in nodes:
                                if 'path' in node and 'name' not in node:
                                    node['name'] = node['path'].split('/')[-1]
                                if 'children' in node and node['children']:
                                    _sanitize_tree(node['children'])

                        _sanitize_tree(structure)

                    akashic.broadcast({
                        "method": "scaffold/previewStructure",
                        "params": {
                            "uri": uri,
                            "structure": structure,
                            "ascii_tree": data.get("ascii_tree", ""),
                            "meta": {
                                "timestamp": ts,
                                "latency_ms": result.duration_seconds * 1000 if hasattr(result,
                                                                                        'duration_seconds') else 0
                            }
                        },
                        "trace_id": trace_id,
                        "tags": ["TOPOLOGY", "MIRROR"]
                    })

            # --- BEAM 3: VITALITY ---
            if "stats" in data or hasattr(result, 'vitals'):
                akashic.broadcast({
                    "method": "scaffold/telemetryPulse",
                    "params": {
                        "stats": data.get("stats", {}),
                        "vitals": getattr(result, 'vitals', {}),
                        "duration_ms": result.duration_seconds * 1000 if hasattr(result, 'duration_seconds') else 0,
                        "timestamp": ts,
                        "artisan": artisan_name
                    },
                    "trace_id": trace_id,
                    "tags": ["DASHBOARD", "TELEMETRY"]
                })

            # --- BEAM 4: ARTIFACTS ---
            if result.artifacts:
                created = [str(a.path).replace('\\', '/') for a in result.artifacts if a.action == 'create']
                modified = [str(a.path).replace('\\', '/') for a in result.artifacts if a.action == 'modify']
                deleted = [str(a.path).replace('\\', '/') for a in result.artifacts if a.action == 'delete']

                if created or modified or deleted:
                    akashic.broadcast({
                        "method": "scaffold/artifacts",
                        "params": {
                            "created": created,
                            "modified": modified,
                            "deleted": deleted,
                            "project_root": str(self.engine.project_root)
                        },
                        "trace_id": trace_id,
                        "tags": ["FILESYSTEM", "MANIFEST"]
                    })

            # --- BEAM 5: HAPTIC ---
            if result.success and result.ui_hints:
                akashic.broadcast({
                    "method": "gnostic/vfx",
                    "params": result.ui_hints,
                    "trace_id": trace_id
                })

        finally:
            self._broadcasting = False

    def _conduct_simulation(self, request: BaseRequest) -> ScaffoldResult:
        """[ASCENSION 6]: Redirects the request to the Simulation Subsystem."""
        from ....simulation.conductor.orchestrator import SimulationConductor
        from ....simulation.scribe import ProphecyScribe

        conductor = SimulationConductor(self.engine)
        prophecy = conductor.conduct(request)

        if not getattr(request, 'silent', False):
            scribe = ProphecyScribe(prophecy)
            scribe.proclaim()

        artifacts = [Artifact(path=Path(diff.path), type='file', action=diff.status) for diff in prophecy.diffs]

        return ScaffoldResult(
            success=prophecy.is_pure,
            message=prophecy.summary,
            data=prophecy.model_dump(),
            heresies=prophecy.heresies,
            artifacts=artifacts
        )

    def shutdown(self):
        """Cleanup resources."""
        pass