# Path: core/runtime/engine/execution/dispatcher.py
# -------------------------------------------------

import os
import sys
import time
import traceback
import uuid
import json
from typing import Any, Optional, Dict, List
from pathlib import Path
from contextlib import contextmanager

from .....interfaces.base import ScaffoldResult, Artifact
from .....interfaces.requests import BaseRequest
from ....state.machine import GnosticRite
from .context import ContextLevitator
from ....daemon.serializer import gnostic_serializer
from .....artisans.analyze.reporting.privacy import PrivacySentinel

class QuantumDispatcher:
    """
    =============================================================================
    == THE QUANTUM DISPATCHER (V-Ω-MULTICAST-PRISM)                            ==
    =============================================================================
    LIF: INFINITY | ROLE: SIGNAL_DIFFRACTION_ENGINE

    Manages the routing of intent to action and the projection of results.

    ### THE 12 ASCENSIONS OF DISPATCH:
    1.  **The Multicast Prism:** Splits a single Artisan result into multiple
        targeted JSON-RPC streams (Diagnostics, Topology, Status).
    2.  **The Spatial Levitator:** Warps `cwd` for the duration of the rite.
    3.  **The Transactional Guard:** Wraps execution in atomic rollback scopes.
    4.  **The Forensic Anchor:** Injects Trace IDs into the stack for debugging.
    5.  **The Simulation Divert:** Automatically routes dry-runs to the Sim Engine.
    6.  **The URI Canonizer:** Normalizes file paths for UI matching (VS Code).
    7.  **The Survey Resonator:** Special handling for Grand Survey telemetry.
    8.  **The JIT Awakener:** Lazy-loads skills if they are dormant.
    9.  **The Silent Hand:** Executes background rites without blocking the shell.
    10. **The Artifact Herald:** Announces created files to the File Tree.
    11. **The Error Transmuter:** Converts crashes into structured JSON errors.
    12. **The Result Sanitizer:** Ensures all output is JSON-safe before broadcast.
    """

    def __init__(self, engine: Any):
        self.engine = engine
        self.levitator = ContextLevitator(engine)
        self._trace_enabled = os.environ.get("SCAFFOLD_TRACE") == "1"

    def _trace(self, msg: str):
        if self._trace_enabled:
            sys.stderr.write(f"[DISPATCH] {msg}\n")
            sys.stderr.flush()

    def levitate_context(self, root):
        """Public API for Artisans to request levitation."""
        return self.levitator.levitate(root)

    def dispatch(self, request: BaseRequest) -> ScaffoldResult:
        """
        The Grand Rite of Dispatch.
        """
        request_type = type(request).__name__
        self._trace(f"Dispatching {request_type} :: ID {request.request_id}")
        start_time = time.monotonic()

        # [DAEMON EXORCISM]: Force local mode if cold
        if not (getattr(self.engine.context, '_state_mask', 0) & 2):
            os.environ["SCAFFOLD_LOCAL_MODE"] = "1"

        try:
            # 1. Forensic Anchoring
            if self.engine.traceback_handler:
                self.engine.traceback_handler.inject_context(
                    request,
                    self.engine.project_root,
                    getattr(self.engine.context, 'session_id', '0xVOID')
                )

            # 2. Resolve Artisan
            handler_def = self.engine.registry.get(type(request))

            # [JIT RECOVERY]
            if not handler_def:
                self._trace("Artisan Dormant. Awakening Skills...")
                self.engine.bootstrap.awaken_skills()
                handler_def = self.engine.registry.get(type(request))

            if not handler_def:
                return self.engine.failure(f"No Artisan consecrated for: {request_type}")

            # 3. Instantiate
            artisan = handler_def(self.engine) if isinstance(handler_def, type) else handler_def

            # Inject Engine Reference
            if hasattr(artisan, 'engine') and getattr(artisan, 'engine', None) is None:
                artisan.engine = self.engine

            # Heal Request Root
            if not request.project_root:
                request.project_root = self.engine.project_root

            artisan_name = getattr(artisan, 'name', artisan.__class__.__name__)

            # 4. Simulation Intercept
            is_sim_internal = request.variables.get('SCAFFOLD_SIMULATION', False) if request.variables else False
            wants_sim = getattr(request, 'preview', False) or getattr(request, 'dry_run', False)

            if wants_sim and not is_sim_internal:
                return self._conduct_simulation(request)

            # 5. The Atomic Execution Core
            def _execute_core(req: BaseRequest) -> ScaffoldResult:
                self._trace(f">>> INVOKING {artisan_name}")
                try:
                    # [TRANSACTIONAL GUARD]
                    with self.engine.transactions.atomic_rite(f"{artisan_name}:{req.request_id}") as tx_id:

                        # Inject Context safely
                        if req.context is None: req.context = {}
                        req.context['transaction_id'] = tx_id

                        if hasattr(artisan, 'execute'):
                            res = artisan.execute(req)
                        elif callable(artisan):
                            res = artisan(req)
                        else:
                            raise Exception(f"Artisan '{artisan_name}' has no execute method.")

                        return res
                except Exception as ex:
                    self._trace(f"!!! CRASH in {artisan_name}: {ex}")
                    return self.engine.healer.handle_panic(ex, req, time.monotonic() - start_time)

            # 6. Pipeline Ignition
            with GnosticRite(rite_name=artisan_name, initial_vars=request.variables):
                # Execute through middleware
                final_result = self.engine.pipeline.execute(request, _execute_core)

                if final_result is None:
                    sys.stderr.write("\n[SCAFFOLD] ⚠️ Warning: Middleware returned VOID. Bypassing protection.\n")
                    final_result = _execute_core(request)

            # 7. Final Polish
            if final_result and hasattr(final_result, 'duration_seconds') and not final_result.duration_seconds:
                final_result.duration_seconds = time.monotonic() - start_time

            # [ASCENSION 1]: MULTICAST THE REVELATION
            # If we are in the Daemon (Akashic link exists), we broadcast the fragments.
            if getattr(self.engine, 'akashic', None):
                self._multicast_revelation(request, final_result, artisan_name)

            return final_result

        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            return self.engine.failure(f"Engine Fracture: {e}", details=traceback.format_exc())

    def _multicast_revelation(self, request: BaseRequest, result: ScaffoldResult, artisan_name: str):
        """
        =============================================================================
        == THE MULTICAST PRISM (V-Ω-TOTALITY-V9005-URI-COMPLIANT)                  ==
        =============================================================================
        LIF: ∞ | ROLE: SIGNAL_DIFFRACTION_ENGINE | RANK: OMEGA_SOVEREIGN
        AUTH_CODE: Ω_PRISM_V9_URI_PARITY

        [THE CURE]: This version replaces the inline URI logic with the official
        UriUtils from the Daemon stratum, ensuring 100% parity with the LSP Server.
        """
        import time
        import inspect
        from pathlib import Path
        from .....interfaces.requests import BaseRequest
        from .....interfaces.base import ScaffoldResult
        from .....artisans.analyze.reporting.privacy import PrivacySentinel

        # [ASCENSION 1]: IMPORT THE SOVEREIGN URI ORACLE
        # This ensures the Engine and the LSP speak the same path-language.
        try:
            from ....lsp.base.utils import UriUtils
        except ImportError:
            # Fallback for standalone kernel mode
            UriUtils = None

        # 0. VITALITY CHECK
        akashic = getattr(self.engine, 'akashic', None)
        if not akashic or not result:
            return

        if inspect.isawaitable(result):
            return

            # --- DATA HARVEST ---
        data = result.data if isinstance(result.data, dict) else {}
        trace_id = getattr(request, 'trace_id', 'tr-unbound')
        ts = time.time()

        # [THE CURE]: ISOMORPHIC URI SYNTHESIS
        def to_gnostic_uri(path_candidate: Any) -> str:
            if not path_candidate: return "file:///unknown"
            p_str = str(path_candidate)

            # If already a protocol-anchored URI, do not mutate.
            if p_str.startswith(('file:', 'scaffold-shadow:', 'inmemory:', 'vscode-vfs:')):
                return p_str

            # [ASCENSION 1]: Use the official Transformer if available
            if UriUtils:
                return UriUtils.to_uri(Path(p_str))

            # Emergency fallback logic
            clean_path = p_str.replace('\\', '/')
            return f"file:///{clean_path.lstrip('/')}"

        # =========================================================================
        # == BEAM 1: THE DIAGNOSTIC STREAM (RED SQUIGGLES)                       ==
        # =========================================================================
        diagnostics = result.diagnostics or data.get("diagnostics", [])
        if diagnostics or "Analyze" in artisan_name:
            target_path = data.get("path") or getattr(request, 'file_path', None)
            if target_path:
                uri = to_gnostic_uri(target_path)

                safe_diagnostics = []
                for d in diagnostics:
                    # Redact PII at the edge before broadcast
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

                # Haptic Kick for Errors (Severity 1)
                if any(d.get('severity') == 1 for d in safe_diagnostics):
                    akashic.broadcast({
                        "method": "gnostic/vfx",
                        "params": {"type": "shake", "intensity": 0.8, "uri": uri},
                        "trace_id": trace_id
                    })

        # =========================================================================
        # == BEAM 2: THE STRUCTURAL STREAM (GNOSTIC MIRROR)                      ==
        # =========================================================================
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
                            "latency_ms": result.duration_seconds * 1000 if hasattr(result, 'duration_seconds') else 0
                        }
                    },
                    "trace_id": trace_id,
                    "tags": ["TOPOLOGY", "MIRROR"]
                })

        # =========================================================================
        # == BEAM 3: THE VITALITY STREAM (METABOLISM)                            ==
        # =========================================================================
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

        # =========================================================================
        # == BEAM 4: THE ARTIFACT HERALD (FILESYSTEM DELTA)                      ==
        # =========================================================================
        if result.artifacts:
            created = [str(a.path).replace('\\', '/') for a in result.artifacts if a.action == 'create']
            modified = [str(a.path).replace('\\', '/') for a in result.artifacts if a.action == 'modify']
            deleted = [str(a.path).replace('\\', '/') for a in result.artifacts if a.action == 'delete']
            if created or modified or deleted:
                akashic.broadcast({
                    "method": "scaffold/artifacts",
                    "params": {
                        "created": created, "modified": modified, "deleted": deleted,
                        "project_root": str(self.engine.project_root)
                    },
                    "trace_id": trace_id,
                    "tags": ["FILESYSTEM", "MANIFEST"]
                })

        return True



    def _path_to_uri(self, path_str: str) -> str:
        """Helper to forge a valid file:// URI from any OS path."""
        try:
            # 1. Normalize Slashes
            clean = str(path_str).replace("\\", "/")

            # 2. Handle Windows Drive Letters (c:/ -> /c%3a/) or just ensure it starts with /
            # Simple approach: If not starts with /, prepend /
            if not clean.startswith('/'):
                clean = '/' + clean

            # 3. Prepend Protocol
            return f"file://{clean}"
        except Exception:
            return path_str

    def _conduct_simulation(self, request: BaseRequest) -> ScaffoldResult:
        """
        Redirects the request to the Simulation Subsystem.
        """
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
        pass