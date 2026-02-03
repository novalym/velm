# Path: core/artisans/analyze/artisan.py
# --------------------------------------

import time
import sys
import json
import concurrent.futures
import os
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple

# --- CORE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import AnalyzeRequest
from ...core.daemon.serializer import gnostic_serializer

# --- THE MODULAR ORGANS (SUB-SYSTEMS) ---
from .core.context import AnalysisContext
from .divination.grammar import GrammarOracle
from .orchestrator import AnalysisOrchestrator
from .redemption.healer import RedemptionHealer
from .reporting.diagnostics import DiagnosticForge
# We import the Ignore logic to respect .gitignore during batch scans
from ...utils import get_ignore_spec

# [ASCENSION 13]: CANCELLATION TOKEN SUPPORT
# We lazily import or mock the token if running standalone
try:
    from ...core.lsp.base.rpc.cancellation import CancellationToken
except ImportError:
    class CancellationToken:
        def check(self): pass
        @classmethod
        def none(cls): return cls()


class AnalyzeArtisan(BaseArtisan[AnalyzeRequest]):
    """
    =================================================================================
    == THE ANALYZE ARTISAN (V-Ω-FORENSIC-TRACER-V13-CANCELLABLE)                   ==
    =================================================================================
    LIF: 10,000,000,000,000 | ROLE: OMNISCIENT_PERCEIVER

    The Sovereign Eye of the God-Engine.
    It is no longer just a parser; it is a Massively Parallel Perception Engine.

    [ASCENSION LOG]:
    1.  **Forensic Announcer:** Screams state to stderr.
    2.  **Quantum Context Mirror:** Pre-loads content if missing.
    3.  **Path Canonizer:** Windows path normalization.
    4.  **Batch Optimizer:** Pre-flight checks.
    5.  **Thread-Pool Sizing:** Dynamic CPU scaling.
    6.  **Telemetry Injection:** Trace ID propagation.
    7.  **Binary Ward:** Null-byte detection.
    8.  **Shadow Resurrection:** IDE unsaved buffer priority.
    9.  **Error Sarcophagus:** Global try/catch safety.
    10. **Result Enrichment:** Guaranteed data shape.
    11. **Auto-Redemption Hook:** Self-healing triggers.
    12. **Void Guard:** Null-safe orchestration.
    13. **Cancellation Awareness:** Checks token inside heavy loops.
    """

    def __init__(self, engine: Any):
        super().__init__(engine)

        # [FACULTY 1]: THE NAVIGATOR (Path Resolution)
        self.context_mgr = AnalysisContext(engine)

        # [FACULTY 2]: THE CONDUCTOR (Logic Routing)
        self.orchestrator = AnalysisOrchestrator(engine)

        # [FACULTY 3]: THE MEDIC (Auto-Fix)
        self.healer = RedemptionHealer(engine)

    def execute(self, request: AnalyzeRequest, token: Any = None) -> ScaffoldResult:
        """
        [THE GRAND RITE OF INQUEST - CANCELLABLE]
        """
        start_ns = time.perf_counter_ns()

        # [ASCENSION 13]: CANCELLATION BINDING
        # If dispatched via LSP, 'token' will be a CancellationToken.
        # If via CLI, it might be None. We normalize.
        cancel_token = token if token else CancellationToken.none()

        # [CHECK]: Pre-flight check
        cancel_token.check()

        # [ASCENSION 1]: FORENSIC ENTRY LOG
        sys.stderr.write(f"\n[AnalyzeArtisan] 🔵 Rite Initiated. Input: '{request.file_path}'\n")

        # 1. DIVINE THE SANCTUM (ROOT RESOLUTION)
        target_root = self.context_mgr.resolve_target_root(request.project_root)

        # [ASCENSION 3]: PATH CANONIZER
        # Ensure root is absolute and normalized
        target_root = target_root.resolve()

        sys.stderr.write(f"[AnalyzeArtisan]    Anchor: {target_root}\n")

        # [CHECK]: Post-resolution check
        cancel_token.check()

        # [ASCENSION 9]: ERROR SARCOPHAGUS (Global Trap)
        try:
            # We warp the Engine's reality to the target.
            with self.engine.temporary_context(target_root):

                # 2. RESOLVE THE LOCUS
                target_input = request.file_path or "."
                if target_input == "memory.scaffold" and not request.content:
                    target_input = "."

                physical_path = (target_root / target_input).resolve()

                # [FORENSIC LOG]: Path Resolution
                sys.stderr.write(f"[AnalyzeArtisan]    Physical Path: {physical_path}\n")

                # 3. BRANCHING REALITY (BATCH VS SINGLE)
                if physical_path.is_dir() or request.batch:
                    sys.stderr.write(f"[AnalyzeArtisan]    Mode: PANOPTICON (Batch)\n")
                    return self._conduct_panopticon(physical_path, target_root, request, start_ns, cancel_token)
                else:
                    sys.stderr.write(f"[AnalyzeArtisan]    Mode: INQUEST (Single)\n")
                    return self._conduct_inquest(physical_path, target_root, request, start_ns, cancel_token)

        except Exception as e:
            # Check if it was a purposeful cancellation
            if "Architect's Will has shifted" in str(e):
                sys.stderr.write(f"[AnalyzeArtisan] 🛑 Rite Cancelled by Client.\n")
                # Re-raise to let Dispatcher handle the response
                raise e

            # [ASCENSION 9]: CATASTROPHIC WARD
            tb = traceback.format_exc()
            sys.stderr.write(f"[AnalyzeArtisan] 💥 Execution Fracture: {e}\n{tb}\n")
            return self.failure(f"Perception Fracture: {e}", details=str(e))

    def _conduct_inquest(
            self,
            physical_path: Path,
            root: Path,
            request: AnalyzeRequest,
            start_ns: int,
            token: Any
    ) -> ScaffoldResult:
        """
        [MODE B]: THE SINGLE FILE INQUEST
        Deep forensic analysis of a specific scripture.
        """
        # [CHECK]: Entry check
        token.check()

        # 1. Resolve Content (Shadow vs Disk)
        # [ASCENSION 8]: SHADOW RESURRECTION
        content, is_binary, err = self.context_mgr.resolve_multiversal_content(
            request.content,
            physical_path,
            getattr(request, 'session_id', 'global')
        )

        if err:
            sys.stderr.write(f"[AnalyzeArtisan] ❌ Content Resolution Error: {err}\n")
            return self.failure(f"Void Scripture: {err}", data={"path": str(physical_path)})

        # [ASCENSION 7]: BINARY WARD
        if is_binary:
            sys.stderr.write(f"[AnalyzeArtisan] ⚠️ Binary Detected. Skipping.\n")
            return self.success(
                "Binary Construct (Skipped)",
                data={"path": str(physical_path), "status": "binary"}
            )

        sys.stderr.write(f"[AnalyzeArtisan]    Content Size: {len(content)} chars\n")

        # 2. Divine Tongue
        grammar = request.grammar or GrammarOracle.divine(str(physical_path), content)
        sys.stderr.write(f"[AnalyzeArtisan]    Divined Grammar: {grammar}\n")

        # 3. Assemble Context
        # [ASCENSION 6]: TELEMETRY INJECTION
        # We inject trace_id if present
        trace_id = request.metadata.get('trace_id', 'unknown') if request.metadata else 'unknown'

        ctx = {
            "content": content,
            "file_path": physical_path,
            # [ASCENSION 3]: PATH CANONIZER (Relativity)
            # Ensure logical path is relative to root for consistent reporting
            "logical_path": physical_path.relative_to(root) if physical_path.is_relative_to(root) else physical_path,
            "project_root": root,
            "grammar": grammar,
            "cursor_offset": request.cursor_offset,
            "telemetry": {"start_time": time.monotonic(), "trace_id": trace_id},
            "engine": self.engine,
            "args": request
        }

        # 4. Execute Orchestrator
        sys.stderr.write(f"[AnalyzeArtisan]    Conducting Orchestration...\n")

        # [CHECK]: Before heavy computation
        token.check()

        # [ASCENSION 12]: VOID GUARD
        data = self.orchestrator.conduct(ctx) or {}

        # [FORENSIC LOG]: Result Check
        diag_count = len(data.get('diagnostics', []))
        sys.stderr.write(f"[AnalyzeArtisan]    Orchestrator returned {diag_count} diagnostics.\n")

        # [ASCENSION 10]: RESULT ENRICHMENT
        # Inject top-level keys for the Herald Header
        data['path'] = str(physical_path)
        data.setdefault('metrics', {})['line_count'] = len(content.splitlines())
        data['metrics']['grammar'] = grammar

        # [FIX]: Ensure 'name' exists for the Structural MRI (Tree View)
        if 'structure' in data:
            def _repair_mri_nodes(items):
                for item in items:
                    if 'path' in item and 'name' not in item:
                        item['name'] = os.path.basename(item['path'])
                    if 'children' in item:
                        _repair_mri_nodes(item['children'])

            _repair_mri_nodes(data['structure'])

        # 5. Forge Result
        result = self.success("Analysis Complete", data=data)

        # 6. [ASCENSION 11]: AUTO-REDEMPTION HOOK
        if request.auto_redeem:
            # [CHECK]: Before optional heavy fix
            token.check()
            sys.stderr.write(f"[AnalyzeArtisan]    Initiating Auto-Redemption...\n")
            self.healer.perform_auto_redemption(result, physical_path, root)

        # 7. Telemetry
        self._inject_telemetry(result, start_ns, grammar, request.is_shadow)

        return result

    def _analyze_single_safe(
            self,
            path: Path,
            root: Path,
            original_request: AnalyzeRequest,
            token: Any
    ) -> ScaffoldResult:
        """
        [HELPER]: A fail-safe wrapper for single file analysis within the swarm.
        """
        try:
            # [CHECK]: Check inside the worker thread
            token.check()

            sub_request = original_request.model_copy(update={
                "file_path": str(path),
                "content": None,
                "cursor_offset": -1
            })

            content, is_binary, err = self.context_mgr.resolve_multiversal_content(
                None, path, "global"
            )

            if is_binary or err:
                return self.failure("Binary/Void")

            grammar = GrammarOracle.divine(str(path), content)

            ctx = {
                "content": content,
                "file_path": path,
                "logical_path": path.relative_to(root),
                "project_root": root,
                "grammar": grammar,
                "cursor_offset": -1,
                "telemetry": {},
                "engine": self.engine,
                "args": sub_request
            }

            data = self.orchestrator.conduct(ctx)

            # [THE CURE]: Inject names for batch results display
            if data:
                data['name'] = path.name
                data['path'] = str(path)

            return self.success("OK", data=data)

        except Exception as e:
            # If cancelled, propagate up
            if "Architect's Will" in str(e): raise e
            return self.failure(str(e))

    def _conduct_panopticon(
            self,
            directory: Path,
            root: Path,
            request: AnalyzeRequest,
            start_ns: int,
            token: Any
    ) -> ScaffoldResult:
        """
        [MODE A]: THE PANOPTICON (BATCH SWARM)
        Spawns a thread pool to analyze the entire sanctum in parallel.
        """
        # [CHECK]: Entry
        token.check()

        # 1. Harvest Targets
        targets = self._harvest_files(directory, root)

        if not targets:
            return self.success("Sanctum Empty", data={"summary": {"total_files": 0}})

        # 2. Ignite the Swarm
        # [ASCENSION 5]: THREAD-POOL SIZING
        # Max 8 workers to prevent GIL thrashing
        max_workers = min(8, os.cpu_count() or 4)
        sys.stderr.write(f"[AnalyzeArtisan]    Igniting Swarm with {max_workers} workers for {len(targets)} targets.\n")

        results_map = {}
        errors = []

        summary = {
            "total_files": len(targets),
            "total_heresies": 0,
            "max_complexity": 0,
            "complex_files": []
        }

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Map futures to paths
            # [ASCENSION 13]: Pass token to workers
            future_to_path = {
                executor.submit(self._analyze_single_safe, p, root, request, token): p
                for p in targets
            }

            # [ASCENSION 13]: MONITORING LOOP
            # We iterate completions but check token status in main thread too
            try:
                for future in concurrent.futures.as_completed(future_to_path):
                    # [CHECK]: Main thread check during aggregation
                    token.check()

                    path = future_to_path[future]
                    rel_path = str(path.relative_to(root))

                    try:
                        # Retrieve Sub-Result
                        file_result = future.result()

                        if file_result.success and file_result.data:
                            # Aggregate Gnosis
                            metrics = file_result.data.get('metrics', {})
                            diagnostics = file_result.data.get('diagnostics', [])

                            cc = metrics.get('cyclomatic_complexity', 0)
                            heresies = len(diagnostics)

                            # Update Summary
                            summary["total_heresies"] += heresies
                            summary["max_complexity"] = max(summary["max_complexity"], cc)
                            if cc > 15:
                                summary["complex_files"].append(rel_path)

                            # Store lightweight record
                            results_map[rel_path] = {
                                "complexity": cc,
                                "heresies": heresies,
                                "loc": metrics.get('line_count', 0),
                                "status": "clean" if heresies == 0 else "tainted",
                                "diagnostics": diagnostics  # Include full detail for UI
                            }
                        else:
                            errors.append(f"{rel_path}: {file_result.message}")

                    except Exception as e:
                        if "Architect's Will" in str(e): raise e
                        errors.append(f"{rel_path}: {str(e)}")

            except Exception as e:
                # Cancel pending
                executor.shutdown(wait=False, cancel_futures=True)
                raise e

        # 3. Forge Holistic Result
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        final_data = {
            "mode": "batch",
            "path": str(directory),
            "summary": summary,
            "results": results_map,
            "errors": errors,
            "meta": {
                "duration_ms": duration_ms,
                "targets_scanned": len(targets)
            }
        }

        sys.stderr.write(f"[AnalyzeArtisan]    Panopticon Concluded. {summary['total_heresies']} total heresies.\n")

        return self.success(
            f"Panopticon Complete. Scanned {len(targets)} scriptures.",
            data=final_data
        )

    def _harvest_files(self, directory: Path, root: Path) -> List[Path]:
        """
        [THE REAPER]
        Recursively collects valid source files, respecting .gitignore.
        """
        ignore_spec = get_ignore_spec(root)
        harvest = []

        # Abyssal Filter (Hardcoded Performance Savers)
        SKIP_DIRS = {'.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build'}

        for current_root, dirs, files in os.walk(directory):
            # Prune Abyssal Directories in-place
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]

            for file in files:
                abs_path = Path(current_root) / file

                # 1. Ignore Dotfiles
                if file.startswith('.'): continue

                # 2. Check GitIgnore
                try:
                    rel_path = abs_path.relative_to(root)
                    if ignore_spec and ignore_spec.match_file(str(rel_path)):
                        continue
                except ValueError:
                    continue

                harvest.append(abs_path)

        return harvest

    def _inject_telemetry(self, result: ScaffoldResult, start_ns: int, grammar: str, is_shadow: bool):
        """Standardizes metadata injection."""
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        if result.data:
            result.data['meta'] = {
                'duration_ms': duration_ms,
                'grammar': grammar,
                'mode': 'shadow' if is_shadow else 'disk'
            }