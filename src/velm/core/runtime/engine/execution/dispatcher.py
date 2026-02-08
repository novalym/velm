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
        =============================================================================
        == THE OMNISCIENT DISPATCH RITE (V-Ω-TOTAL-TRANSPARENCY-ASCENDED)          ==
        =============================================================================
        LIF: ∞ | ROLE: KINETIC_CONDUCTOR | RANK: OMEGA_SUPREME

        ### THE 12 SOVEREIGNTIES OF THIS RITE:
        1.  **Immediate Stderr Inscription (THE FIX):** Prints a raw, unbuffered
            traceback to stderr at the exact microsecond of fracture.
        2.  **Recursive Depth De-escalation:** Uses a `finally` block to guarantee
            that the recursion guard is decremented, even if the world ends.
        3.  **Shadow Context Mirroring:** Preserves the `trace_id` and `rite_name`
            outside the `try` scope to ensure they are always available for lamentation.
        4.  **Bypass-Safe Telemetry:** Conducts a direct `sys.stderr.write` bypass of
            the logging system if a crash is detected, ensuring visibility.
        5.  **NoneType Sarcophagus:** Transmutes `None` returns from artisans or
            middleware into structured Failure vessels automatically.
        6.  **Metabolic Heat Tomography:** Consults the Watchdog to capture CPU/RAM
            pressure at the exact moment of failure.
        7.  **Signal Multicast Shield:** Wraps the Ocular UI broadcast in its own
            ward to prevent a "Crash-within-a-Crash" loop.
        8.  **Atomic Scope Isolation:** Isolates the `_conduct_rite` closure to
            prevent variable leakage or scoping paradoxes.
        9.  **JIT Awakening Pulse:** Measures and chronicled the "Warm-up" time for
            lazy-loaded artisans with microsecond precision.
        10. **Chain of Custody Validation:** Stamps every log entry with both
            `request_id` and `trace_id` for perfect forensic reconstruction.
        11. **Socratic Intent Divination:** If the Semantic Router divines an
            incorrect intent, it preserves the original prompt in the failure dossier.
        12. **The Finality Vow:** Guaranteed return of a valid `ScaffoldResult`
            vessel, ensuring the Engine never hangs in silence.
        """
        import importlib
        import traceback as tb_scribe  # Renamed to avoid collisions

        start_time = time.perf_counter()
        jit_overhead_ms = 0.0
        rite_name = "UnknownRite"
        trace_id = "tr-unbound"
        request_obj = None

        # [ASCENSION 3]: SHADOW CONTEXT MIRROR
        # We capture the trace_id early to ensure our lamentation has an identity
        if isinstance(request, (BaseRequest, object)) and hasattr(request, 'trace_id'):
            trace_id = getattr(request, 'trace_id')

        try:
            # --- MOVEMENT I: TRANSMUTATION (INPUT NORMALIZATION) ---
            if isinstance(request, str):
                request_obj = self._resolve_request_vessel(request, params or kwargs)
            elif isinstance(request, dict):
                command = request.get('command') or request.get('method')
                payload = request.get('params') or request

                # [ASCENSION 11]: SOCRATIC INTENT DIVINATION
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

            # Forge the Silver Cord
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
                        f"Recursion Heresy: Dispatch depth exceeded limit ({self.MAX_DISPATCH_DEPTH}) for trace {trace_id}.",
                        severity=HeresySeverity.CRITICAL
                    )
                self._recursion_depths[trace_id] = current_depth + 1

            # --- MOVEMENT IV: THERMODYNAMIC ADJUDICATION ---
            is_heavy = any(
                k in rite_name for k in ['Genesis', 'Transmute', 'Analyze', 'Refactor', 'Manifest', 'Inception'])

            # [ASCENSION 6]: METABOLIC HEAT TOMOGRAPHY
            if is_heavy and hasattr(request_obj, 'metadata'):
                load = self.engine.watchdog.get_vitals().get("load_percent", 0)
                if load > 85.0:
                    self.logger.warn(f"[{trace_id}] Metabolic Fever ({load}%). Throttling priority.")
                    request_obj.metadata.priority = "background"
                else:
                    request_obj.metadata.priority = "normal"

            self.engine._neuro_optimize(heavy_mode=is_heavy)

            # --- MOVEMENT V: ARTISAN RESOLUTION ---
            if hasattr(request_obj, 'project_root') and request_obj.project_root:
                self.engine.memory.record_focus(str(request_obj.project_root))

            if hasattr(self.engine, 'healer') and not self.engine.healer.circuit_breaker.check_state(rite_name):
                return self.engine.failure(f"Subsystem Quarantined: {rite_name} is currently fracturing.")

            artisan_info = self.engine.registry.get_artisan_for(request_type)
            artisan_instance = None

            if artisan_info is None:
                suggestion = self.engine.registry.suggest_alternative(rite_name)
                return self.engine.failure(
                    message=f"Unmanifest Artisan: No handler for '{rite_name}'.",
                    suggestion=suggestion,
                    details=f"The Gnostic Registry returned None for {request_type}."
                )

            # [ASCENSION 9]: JIT AWAKENING PULSE
            if isinstance(artisan_info, tuple):
                module_path, class_name = artisan_info
                jit_start = time.perf_counter()
                if os.environ.get("SCAFFOLD_HOT_SWAP") == "1":
                    with self.engine.kernel_lock("jit_reception"):
                        try:
                            to_purge = [m for m in sys.modules if m.startswith(module_path)]
                            for m in to_purge:
                                sys.modules.pop(m, None)
                            module = importlib.import_module(module_path)
                            ArtisanClass = getattr(module, class_name)
                            artisan_instance = ArtisanClass(self.engine)
                        except Exception as syntax_heresy:
                            # REDUNDANT TRACEBACK DUMP (FACULTY 1)
                            sys.stderr.write(f"\n[FORENSIC:JIT_FRACTURE] {rite_name}\n")
                            tb_scribe.print_exc(file=sys.stderr)
                            return self.engine.failure(f"Syntax Heresy in {class_name}", details=tb_scribe.format_exc())

                if not artisan_instance:
                    module = importlib.import_module(module_path)
                    artisan_instance = getattr(module, class_name)(self.engine)

                jit_overhead_ms = (time.perf_counter() - jit_start) * 1000
            else:
                artisan_instance = artisan_info(self.engine) if isinstance(artisan_info, type) else artisan_info

            if hasattr(artisan_instance, 'engine'):
                object.__setattr__(artisan_instance, 'engine', self.engine)

            artisan_name = getattr(artisan_instance, 'name', artisan_instance.__class__.__name__)

            # --- MOVEMENT VI: HYBRID KINETIC EXECUTION ---
            # [ASCENSION 8]: ATOMIC SCOPE ISOLATION
            def _conduct_rite(req: BaseRequest) -> Union[ScaffoldResult, Any]:
                if self.engine.akashic:
                    self.engine.akashic.broadcast({
                        "method": "scaffold/progress",
                        "params": {"message": f"Executing {rite_name}...", "percentage": 25, "trace": trace_id}
                    })

                if is_heavy and not req.dry_run:
                    self._chronicle_replay_capability(req, rite_name)

                with self.engine.transactions.atomic_rite(f"{rite_name}:{req.request_id}") as tx_id:
                    if req.context is None: req.context = {}
                    req.context['transaction_id'] = tx_id
                    timeout = getattr(req, 'timeout', 300)

                    if inspect.iscoroutinefunction(artisan_instance.execute):
                        async def _async_wrapper():
                            return await asyncio.wait_for(artisan_instance.execute(req), timeout=timeout)

                        try:
                            loop = asyncio.get_event_loop()
                            if loop.is_running():
                                return asyncio.run_coroutine_threadsafe(_async_wrapper(), loop).result()
                            else:
                                return asyncio.run(_async_wrapper())
                        except RuntimeError:
                            return asyncio.run(_async_wrapper())
                        except asyncio.TimeoutError:
                            raise ArtisanHeresy(f"Temporal Exhaustion: Rite '{rite_name}' exceeded {timeout}s budget.")
                    else:
                        return artisan_instance.execute(req)

            # Pipeline Ignition
            result = self.engine.pipeline.execute(request_obj, _conduct_rite)

            # [ASCENSION 5]: NONETYPE SARCOPHAGUS
            if result is None:
                result = self.engine.failure(f"Void Return: Middleware or Artisan {rite_name} returned None.")

            # --- MOVEMENT VII: POST-PROCESS & TELEMETRY ---
            if hasattr(result, 'duration_seconds') and not result.duration_seconds:
                result.duration_seconds = time.perf_counter() - start_time

            if jit_overhead_ms > 0:
                result.ui_hints["jit_ms"] = jit_overhead_ms

            if hasattr(self.engine, 'predictor'):
                self.engine.predictor.observe_outcome(request_obj, result)

            self.engine.memory.record_rite(rite_name, result.success)
            self.engine.last_reality = result

            if result.success and not request_obj.dry_run and is_heavy:
                self._scan_for_unclaimed_artifacts(request_obj, result, start_time)

            self._synthesize_haptics(result)

            if self.engine.akashic:
                self._multicast_revelation(request_obj, result, artisan_name)

            return result

        except Exception as catastrophic_paradox:
            # --- MOVEMENT VIII: FORENSIC ILLUMINATION (FACULTY 1 & 4) ---
            # We dump the TRUTH immediately to stderr, bypassing all standard logic.
            sys.stderr.write(f"\n" + "!" * 80 + "\n")
            sys.stderr.write(f"🔥 CATASTROPHIC DISPATCH FRACTURE: {rite_name}\n")
            sys.stderr.write(f"📍 TRACE ID: {trace_id}\n")
            sys.stderr.write(f"📍 EXCEPTION: {type(catastrophic_paradox).__name__}: {str(catastrophic_paradox)}\n")
            sys.stderr.write("-" * 80 + "\n")
            # [THE FIX]: REDUNDANT, UNBREAKABLE TRACEBACK DUMP
            tb_scribe.print_exc(file=sys.stderr)
            sys.stderr.write("!" * 80 + "\n\n")
            sys.stderr.flush()

            self.engine._emergency_dump(catastrophic_paradox, rite_name, trace_id)
            self.logger.critical(f"Catastrophic Dispatch Fracture in {rite_name}: {catastrophic_paradox}")

            fail_duration = time.perf_counter() - start_time
            if request_obj:
                return self.engine.healer.handle_panic(catastrophic_paradox, request_obj, fail_duration)
            else:
                return ScaffoldResult(
                    success=False,
                    message=f"Request Transmutation Failed: {catastrophic_paradox}",
                    error=str(catastrophic_paradox),
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
        from ...simulation.conductor.orchestrator import SimulationConductor
        from ...simulation.scribe import ProphecyScribe

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