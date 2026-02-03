# Path: scaffold/artisans/distill/core/tracer/engine.py
# -----------------------------------------------------

import json
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, NamedTuple

from .contracts import RuntimeState, TracePoint
from .snapshot import SnapshotReader
from .probes.python_probe import PythonSeance
from .symbolic import SymbolicExecutor
from .....logger import Scribe
from .....core.cortex.contracts import CortexMemory

Logger = Scribe("RuntimeWraith")


class TraceResult(NamedTuple):
    touched_files: Set[str]
    runtime_state: RuntimeState


class RuntimeWraith:
    """
    =============================================================================
    == THE RUNTIME WRAITH (V-Ω-HYBRID-TRACER-ULTIMA)                           ==
    =============================================================================
    LIF: 10,000,000,000

    The Sovereign of Analysis. It unifies Dynamic Tracing (Execution) and
    Static Tracing (Symbolic) into a single, fault-tolerant interface.

    If a runtime command is provided, it witnesses the living execution.
    If not, it performs a symbolic astral projection to infer connections.
    """

    def __init__(self, project_root: Path):
        self.root = project_root
        self.snapshot_reader = SnapshotReader(project_root)
        self.symbolic_executor: Optional[SymbolicExecutor] = None

    def trace(
            self,
            seeds: List[str],
            depth: int,
            memory: CortexMemory,
            strategy: str = 'balanced',
            trace_command: Optional[str] = None
    ) -> TraceResult:
        """
        [THE HYBRID RITE OF TRACING]
        Orchestrates the Gaze.
        1. If `trace_command` exists, perform Dynamic Tracing.
        2. If not, perform Static Symbolic Tracing from the `seeds`.
        """
        touched_files = set(seeds)
        state = RuntimeState()

        # --- PATH I: DYNAMIC TRACING (THE GOLDEN PATH) ---
        if trace_command:
            Logger.info(f"Wraith initiating Dynamic Trace: [yellow]{trace_command}[/yellow]")
            try:
                # 1. Capture State (Variables, Exceptions) via Seance
                if "python" in trace_command:
                    probe = PythonSeance(self.root)
                    state = probe.conduct(trace_command)

                # 2. Capture Coverage (Files Touched) via Golden Path
                dynamic_files = self.trace_golden_path(trace_command)
                touched_files.update(dynamic_files)

            except Exception as e:
                Logger.error(f"Dynamic Tracing faltered: {e}. Falling back to Symbolic.")

        # --- PATH II: STATIC SYMBOLIC TRACING (THE ASTRAL PROJECTION) ---
        # We always augment with symbolic tracing if the strategy permits,
        # or if dynamic tracing wasn't requested/failed.
        if strategy in ['balanced', 'surgical', 'comprehensive']:
            Logger.info("Wraith initiating Symbolic Trace...")
            self.symbolic_executor = SymbolicExecutor(memory)

            # Expand from seeds
            current_layer = set(seeds)
            for _ in range(depth):
                next_layer = set()
                for file_path in current_layer:
                    # Find what this file imports
                    deps = memory.get_dependencies_of(file_path)
                    next_layer.update(deps)

                    # Find what imports this file (if comprehensive)
                    if strategy == 'comprehensive':
                        deps_on = memory.get_dependents_of(file_path)
                        next_layer.update(deps_on)

                if not next_layer: break

                touched_files.update(next_layer)
                current_layer = next_layer

        return TraceResult(touched_files=touched_files, runtime_state=state)

    def capture_state(self,
                      trace_command: Optional[str] = None,
                      snapshot_path: Optional[str] = None) -> RuntimeState:
        """Legacy interface for pure state capture."""
        state = RuntimeState()
        if snapshot_path:
            Logger.info(f"Resurrecting state from snapshot: {snapshot_path}")
            static_state = self.snapshot_reader.load(Path(snapshot_path))
            self._merge_states(state, static_state)
        if trace_command:
            Logger.info(f"Summoning the Wraith to trace: '{trace_command}'")
            if "python" in trace_command:
                probe = PythonSeance(self.root)
                live_state = probe.conduct(trace_command)
                self._merge_states(state, live_state)
            else:
                Logger.warn("The Wraith only speaks Python in this epoch. Trace command ignored.")
        return state

    def trace_golden_path(self, command: str) -> Set[str]:
        """
        Conducts a 'dry run' of a command to discover all imported/executed files.
        Returns a set of relative file path strings that are part of the 'living soul'.
        """
        Logger.info(f"The Wraith traces the Golden Path via: [yellow]'{command}'[/yellow]")
        living_souls: Set[str] = set()
        try:
            result = subprocess.run(
                command,
                cwd=self.root,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )

            # Gaze upon both stdout and stderr for file paths
            output = result.stdout + "\n" + result.stderr

            # This regex is a Gnostic Gaze for file paths relative to the project.
            for match in re.finditer(r'([\w\-\./\\]+\.(?:py|ts|js|go|rs|rb))', output):
                path_str = match.group(1)
                try:
                    full_path = (self.root / path_str).resolve()
                    if full_path.is_file() and full_path.is_relative_to(self.root):
                        rel_path = full_path.relative_to(self.root).as_posix()
                        living_souls.add(rel_path)
                except (ValueError, OSError):
                    continue

            Logger.success(f"Golden Path traced. Perceived {len(living_souls)} living souls.")
            return living_souls

        except Exception as e:
            Logger.error(f"The Golden Path trace was shattered by a paradox: {e}")
            return set()

    def _merge_states(self, primary: RuntimeState, secondary: RuntimeState):
        """Merges two realities into one."""
        for file, lines in secondary.annotations.items():
            if file not in primary.annotations:
                primary.annotations[file] = {}
            for line, notes in lines.items():
                if line not in primary.annotations[file]:
                    primary.annotations[file][line] = []
                primary.annotations[file][line].extend(notes)