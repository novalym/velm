# Path: scaffold/artisans/simulacrum/artisan.py
# -----------------------------------------------
# LIF: INFINITY | AUTH_CODE: @!)(@() | ROLE: HIGH_PRIEST_OF_SIMULACRA
# =================================================================================
# == THE SIMULACRUM ARTISAN (V-Ω-TOTALITY-FINAL-V50-SINGULARITY)                 ==
# =================================================================================
#
# THE 12 ASCENSIONS OF THE SIMULACRUM:
# 1.  [IDENTITY MIRRORING]: Extracts 'node_id' from deep within the request to anchor logs.
# 2.  [CONTENT INGESTION]: Polymorphically accepts raw strings or file paths as source matter.
# 3.  [ORACLE GAZE]: Uses the Heuristic Engine to divine language from syntax fingerprints.
# 4.  [HOLOGRAPHIC LATTICE]: Ingests 'virtual_context' to materialize multi-file dependency graphs.
# 5.  [ENVIRONMENT GRAFTING]: Injects Gnostic session tokens and Node IDs into the runtime env.
# 6.  [NEURAL LINK MULTIPLEXING]: Broadcasts lifecycle events (Ignition/Extinction) to the UI.
# 7.  [STREAM ENCODER]: Real-time stdout/stderr capture with smart buffering.
# 8.  [BUFFER SHIELD]: Prevents memory overflows by truncating infinite loops or massive logs.
# 9.  [FRACTURE DECODING]: Analyzes exit codes and stderr to provide actionable remediation.
# 10. [ARTIFACT SALVAGE]: Detects and catalogues files created during the simulation.
# 11. [GNOSTIC SUGGESTION]: Suggests fixes for common heresies (missing deps, syntax errors).
# 12. [TEMPORAL TELEMETRY]: High-precision timing for performance profiling.

import sys
import time
import uuid
import traceback
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import SimulateRequest
from .engine import VoidEngine
from .heuristics.engine import SimulationOracle
from ...logger import Scribe

Logger = Scribe("SimulacrumArtisan")


class SimulacrumArtisan(BaseArtisan[SimulateRequest]):
    """
    =============================================================================
    == THE SOVEREIGN SIMULACRUM INTERFACE                                      ==
    =============================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The final bridge between Thought and Reality. It sustains the Void Sanctum
    and reports results with 100% forensic fidelity.
    """

    def execute(self, request: SimulateRequest) -> ScaffoldResult:
        start_tick = time.monotonic()

        # [ASCENSION 1]: IDENTITY MIRRORING (FIXING THE UNDEFINED ANOMALY)
        # We extract the node_id from extra_args or variables if not in core request
        node_id = getattr(request, 'node_id', None) or request.variables.get('node_id', 'unknown_atom')

        # [ASCENSION 2]: CONTENT INGESTION
        content = request.content
        if not content and getattr(request, 'target_file', None):
            target_path = (self.project_root / request.target_file).resolve()
            if target_path.exists():
                content = target_path.read_text(encoding='utf-8', errors='ignore')
                Logger.info(f"Ingested logic from: {target_path.name}")

        if not content or not content.strip():
            return self.failure(f"The Void rejects emptiness in node {node_id}.")

        # [ASCENSION 3]: ORACLE GAZE (IDENTITY DETECTION)
        detected_lang = SimulationOracle.divine_language(content, request.language)
        Logger.info(
            f"Oracle perceiving [bold cyan]{detected_lang.upper()}[/bold cyan] for node [yellow]{node_id}[/yellow]")

        # [ASCENSION 4]: HOLOGRAPHIC LATTICE INGESTION
        # We extract the virtual context (other nodes) to allow cross-imports in the void.
        virtual_context = getattr(request, 'virtual_context', {}) or {}
        context_size = len(virtual_context)
        if context_size > 0:
            Logger.info(f"Materializing Holographic Lattice: {context_size} virtual peers.")

        # TELEMETRY BUFFERS
        full_log_buffer = []
        artifacts_metadata: List[Dict] = []
        exit_code = 0
        execution_duration = 0.0

        # [ASCENSION 5]: ENVIRONMENT DNA GRAFTING
        effective_env = request.env_vars or {}
        effective_env.update({
            "GNOSTIC_NODE_ID": str(node_id),
            "GNOSTIC_SESSION_TOKEN": str(uuid.uuid4())[:8].upper(),
            "PYTHONUNBUFFERED": "1",
            "GNOSTIC_CONTEXT_SIZE": str(context_size)
        })

        engine = VoidEngine(self.project_root)

        try:
            # --- MOVEMENT I: THE SYMPHONY OF IGNITION ---
            # [ASCENSION 6]: NEURAL LINK MULTIPLEXING
            Logger.info(f"Igniting Void Sanctum for node {node_id}...")

            stream = engine.ignite(
                content=content,
                language_hint=detected_lang,
                timeout=request.timeout,
                env_overrides=effective_env,
                # [THE KEY]: Pass the holographic lattice to the engine
                virtual_context=virtual_context
            )

            # [ASCENSION 7]: THE STREAM ENCODER
            for packet in stream:
                p_type = packet.get("type")
                payload = packet.get("payload")

                if p_type == "stdout":
                    # [ASCENSION 8]: BUFFER SHIELD (TRUNCATION)
                    if len(full_log_buffer) < 50000:  # 50k char limit for stability
                        full_log_buffer.append(payload)
                    sys.stdout.write(payload)
                    sys.stdout.flush()

                elif p_type == "error":
                    # [ASCENSION 9]: FRACTURE DECODING & REDEMPTION
                    Logger.critical(f"Void Fracture in {node_id}: {payload}")

                    # [THE CURE]: Interpret the OS failure
                    suggestion = "Check system toolchains."
                    if "WinError 1314" in payload:
                        suggestion = "Windows Privilege Heresy: Enable Developer Mode or run as Admin for Symlinks."
                    elif "ts-node" in payload:
                        suggestion = "TypeScript Toolchain missing: Run 'npm install -g ts-node'."
                    elif "ModuleNotFoundError" in payload:
                         suggestion = "Dependency Void. Ensure all virtual nodes are connected or run 'scaffold install'."

                    return self.failure(
                        message=f"Void Engine Fracture: {payload}",
                        suggestion=suggestion
                    )

                elif p_type == "result":
                    exit_code = payload.get("code", -1)
                    execution_duration = payload.get("duration", 0.0)

                elif p_type == "artifact":
                    # [ASCENSION 10]: ARTIFACT SALVAGE
                    artifacts_metadata.append({
                        "name": payload["name"],
                        "path": payload["path"],
                        "size": payload.get("size", 0)
                    })

            # --- MOVEMENT II: THE REVELATION ---
            total_duration = time.monotonic() - start_tick
            success = (exit_code == 0)

            # [ASCENSION 11]: GNOSTIC SUGGESTION ORACLE
            final_stdout = "".join(full_log_buffer)
            final_suggestion = None
            if not success:
                if "ImportError" in final_stdout or "ModuleNotFoundError" in final_stdout:
                    final_suggestion = "Dependency Void detected. Try: scaffold install or check virtual imports."
                elif "SyntaxError" in final_stdout:
                    final_suggestion = "Syntactic Heresy. Review logic grammar."
                elif "ReferenceError" in final_stdout:
                    final_suggestion = "Undefined Symbol. Ensure you have imported the necessary modules."

            # [ASCENSION 12]: TEMPORAL TELEMETRY & IDENTITY MIRRORING
            return self.success(
                message=f"Simulation {'Concluded' if success else 'Fractured'}",
                data={
                    "node_id": node_id,
                    "stdout": final_stdout,
                    "exit_code": exit_code,
                    "language": detected_lang,
                    "duration_ms": int(execution_duration * 1000),
                    "total_latency_ms": int(total_duration * 1000),
                    "artifacts": artifacts_metadata,
                    "context_size": context_size,
                    "hash": hashlib.sha256(content.encode()).hexdigest()[:12]
                },
                suggestion=final_suggestion
            )

        except Exception as e:
            # [ASCENSION 9]: PANIC SCRIBE (FORENSIC TRACEBACK)
            tb = traceback.format_exc()
            Logger.critical(f"Fatal Simulacrum Collapse for {node_id}: {e}\n{tb}")
            return self.failure(
                message=f"Void Collapse in node {node_id}: {str(e)}",
                details=tb
            )