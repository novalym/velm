# Path: core/runtime/engine/execution/context.py
# ----------------------------------------------

import os
import threading
from pathlib import Path
from typing import Optional, Union, Any, Dict
from contextlib import contextmanager

# Thread-local storage to track the active reality per-thread
_thread_local = threading.local()


class ContextLevitator:
    """
    =============================================================================
    == THE CONTEXT LEVITATOR (V-Ω-SPATIAL-REALITY-BENDER)                      ==
    =============================================================================
    LIF: 100,000,000,000 | ROLE: PARADOX_ANNIHILATOR

    A specialized mechanism to temporarily shift the Engine's perception of
    reality (Project Root) without destabilizing the global process state.

    It handles:
    1. RuntimeContext mutation.
    2. OS Environment Injection (SCAFFOLD_PROJECT_ROOT).
    3. Thread-local tracking of the active sanctum.
    """

    def __init__(self, engine: Any):
        self.engine = engine

    @contextmanager
    def levitate(self, temporary_root: Optional[Union[str, Path]]):
        """
        [THE RITE OF LEVITATION]
        Temporarily re-anchors the Engine to a new Project Root for the duration
        of a single block. This allows the Daemon (anchored in A) to process
        requests for Project B without a full restart.
        """
        # 1. Capture Original State (The Anchor)
        original_context_root = self.engine.context.project_root
        original_env_root = os.environ.get("SCAFFOLD_PROJECT_ROOT")

        did_shift = False
        target_root: Optional[Path] = None

        if temporary_root:
            # 2. Transmute & Resolve
            if isinstance(temporary_root, str):
                temporary_root = Path(temporary_root)

            target_root = temporary_root.resolve()

            # 3. Perform the Shift (Only if different)
            if target_root != original_context_root:
                did_shift = True

                # A. Shift the Mind (RuntimeContext)
                self.engine.context.project_root = target_root

                # B. Shift the Body (OS Environment for Subprocesses)
                os.environ["SCAFFOLD_PROJECT_ROOT"] = str(target_root)

                # C. Shift the Thread (For deep access)
                _thread_local.active_root = target_root

                # self.engine.logger.verbose(f"Context Levitated: {original_context_root} -> {target_root}")

        try:
            yield target_root
        finally:
            # 4. Restore Reality (The Grounding)
            if did_shift:
                # Restore Mind
                self.engine.context.project_root = original_context_root

                # Restore Body
                if original_env_root:
                    os.environ["SCAFFOLD_PROJECT_ROOT"] = original_env_root
                else:
                    os.environ.pop("SCAFFOLD_PROJECT_ROOT", None)

                # Restore Thread
                if hasattr(_thread_local, 'active_root'):
                    del _thread_local.active_root

                # self.engine.logger.verbose(f"Context Grounded to {original_context_root}")

    @staticmethod
    def get_current_root() -> Optional[Path]:
        """Returns the thread-local root if levitating, else None."""
        return getattr(_thread_local, 'active_root', None)