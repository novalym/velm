# Path: src/velm/core/sentinel_conduit.py
# ---------------------------------------
# LIF: INFINITY // ROLE: IPC_STATIC_ANALYSIS_BRIDGE
# AUTH: Ω_SENTINEL_V3_IPC_HARDENED_FINALIS
# ---------------------------------------

import json
import shutil
import subprocess
import tempfile
import os
import time
from pathlib import Path
from typing import List, Optional, Dict, Any

from ..contracts.heresy_contracts import Heresy, HeresySeverity
from ..logger import Scribe

Logger = Scribe("SentinelConduit")

# =========================================================================
# == DIAGNOSTIC TELEMETRY GATE                                           ==
# =========================================================================
# Enables deep tracing of Inter-Process Communication (IPC) payloads.
# Kept disabled by default to maintain zero-noise console output.
_DEBUG_MODE = os.environ.get("SCAFFOLD_DEBUG") == "1"


class SentinelConduit:
    """
    Manages Inter-Process Communication (IPC) with the external 'sentinel' static analysis engine.

    This class serves as a fault-tolerant bridge between the Python runtime and an
    external polyglot linter binary. It is designed to be completely decoupled from the
    host environment's configuration state; if the binary is missing, this component
    enters a 'Passive' state, bypassing analysis without raising exceptions.

    Architectural Design:
    1.  **Ephemeral Sandboxing:** Source code is streamed to a temporary file descriptor
        rather than passed via stdin. This avoids shell buffer limits (E2BIG) and ensures
        encoding consistency across OS boundaries.
    2.  **Fault Isolation:** The execution of the external binary is wrapped in a strict
        timeout/catch block. A crash in the linter will never crash the parent Engine.
    3.  **Cross-Platform Locking:** File handles are explicitly closed before subprocess
        invocation to satisfy Windows NTFS exclusive locking requirements.
    4.  **Protocol Normalization:** Transmutes raw JSON stdout from the binary into
        strongly-typed `Heresy` objects used by the internal adjudication system.
    """

    def __init__(self):
        """
        Initializes the bridge by resolving the absolute path of the Sentinel binary.
        Performs a silent path lookup; no errors are raised if the tool is missing.
        """
        # Resolve binary location from system PATH
        self.sentinel_path: Optional[str] = shutil.which("sentinel")

        # In Debug mode, we log the resolution status for environment troubleshooting.
        # In Production, we remain silent to avoid alarming users who haven't installed the optional tooling.
        if _DEBUG_MODE:
            if self.sentinel_path:
                Logger.debug(f"Sentinel binary resolved at: {self.sentinel_path}")
            else:
                Logger.debug("Sentinel binary not found in PATH. Static analysis subsystem disabled.")

    def adjudicate(self, filename: str, content: str) -> List[Heresy]:
        """
        Executes the static analysis routine against the provided content.

        Args:
            filename (str): The logical name of the file (used for linter context, e.g., extension detection).
            content (str): The in-memory content of the file to analyze.

        Returns:
            List[Heresy]: A list of detected code issues. Returns empty if the tool is missing or the code is clean.
        """
        # 1. Availability Check: Fast exit if the tool is unmanifest.
        if not self.sentinel_path:
            return []

        start_time = time.perf_counter()
        heresies: List[Heresy] = []
        temp_file_path: Optional[Path] = None

        try:
            # 2. Ephemeral Materialization (The IPC Transfer)
            # We create a temp file with the same extension as the source to trigger correct language rules.
            # delete=False is required for Windows compatibility (allows closing handle before subprocess opens it).
            suffix = Path(filename).suffix
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=suffix, encoding='utf-8') as tf:
                tf.write(content)
                temp_file_path = Path(tf.name)

            # 3. Construct Command Vector
            # We request JSON output for machine-readable deterministic parsing.
            command = [
                self.sentinel_path,
                "lint",
                "--json",
                str(temp_file_path)
            ]

            if _DEBUG_MODE:
                Logger.debug(f"IPC Dispatch: `{' '.join(command)}`")

            # 4. Kinetic Execution
            # We enforce a hard timeout to prevent the main thread from hanging on a stalled linter.
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=30  # 30s Execution Budget
            )

            # 5. Exit Code Adjudication
            # 0 = Clean, 1 = Issues Found, >1 = System Crash
            if result.returncode > 1:
                # Log internal crash details only in debug mode to prevent console spam
                if _DEBUG_MODE:
                    Logger.error(f"Sentinel subprocess crashed (Exit {result.returncode}):\n{result.stderr}")
                return []

            # 6. Payload Ingestion & Transmutation
            if result.stdout:
                try:
                    payload = json.loads(result.stdout)

                    # The payload structure is expected to be: List[FileReport]
                    if isinstance(payload, list):
                        for file_report in payload:
                            # Extract issues associated with this file context
                            raw_issues = file_report.get("heresies", [])
                            for issue in raw_issues:
                                heresies.append(Heresy(
                                    message=issue.get("message", "Unknown Static Analysis Warning"),
                                    line_num=issue.get("line", 0),
                                    line_content=issue.get("context", ""),
                                    severity=HeresySeverity(issue.get("severity", "WARNING").upper()),
                                    suggestion=issue.get("suggestion"),
                                    code=issue.get("code", "SENTINEL_DETECT")
                                ))
                except json.JSONDecodeError as e:
                    if _DEBUG_MODE:
                        Logger.error(f"Sentinel JSON serialization failed: {e}. Output was: {result.stdout[:100]}...")

        except subprocess.TimeoutExpired:
            if _DEBUG_MODE:
                Logger.warn("Sentinel execution timed out. Aborting analysis to preserve system responsiveness.")
        except Exception as e:
            # Catch-all for IO errors, Permission denied, etc.
            if _DEBUG_MODE:
                Logger.error(f"Sentinel IPC Bridge fault: {e}")

        finally:
            # 7. Purge Ephemeral Artifacts
            # Ensure the temp file is deleted regardless of execution outcome.
            if temp_file_path and temp_file_path.exists():
                try:
                    temp_file_path.unlink()
                except OSError as e:
                    if _DEBUG_MODE:
                        Logger.warn(f"Failed to clean up temp artifact {temp_file_path}: {e}")

        # 8. Performance Telemetry (Debug Only)
        if _DEBUG_MODE:
            duration = (time.perf_counter() - start_time) * 1000
            if heresies:
                Logger.debug(f"Analysis complete. {len(heresies)} issues detected in {duration:.2f}ms.")
            else:
                Logger.debug(f"Analysis complete. Clean result in {duration:.2f}ms.")

        return heresies