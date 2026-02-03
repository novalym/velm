# Path: scaffold/symphony/conductor/orchestrator.py
# -------------------------------------------------

import queue
import signal
import sys
import threading
import time
import traceback
import os
from pathlib import Path
from typing import Optional, Any, Dict, List, TYPE_CHECKING, Union
from types import SimpleNamespace

from ...contracts.heresy_contracts import ArtisanHeresy, Heresy, HeresySeverity
from ...contracts.symphony_contracts import SymphonyResult, ConductorEvent, EventType
from ...interfaces.requests import SymphonyRequest
from ...logger import Scribe, get_console

# --- THE DIVINE SUMMONS OF THE CORE ---
from ..conductor_core import (
    SymphonySetup,
    SymphonyEngine,
    SymphonyLifecycleManager,
    SymphonyResilienceManager,
    GnosticContextManager,
    SymphonyHandlers
)
from ..execution import KineticTitan, PropheticOracle
from ..renderers import (
    Renderer, BasicRenderer, RichRenderer, GitHubActionsRenderer, StreamRenderer, CinematicRenderer, RawRenderer
)

Logger = Scribe('SymphonyConductor')


class SymphonyConductor:
    """
    =================================================================================
    == THE OMNISCIENT CONDUCTOR (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA-FINALIS++)          ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)

    The God-Engine of Orchestration. It is the central nervous system that binds
    Validation, Execution, Resilience, and Visualization into a single, atomic
    movement of Will.

    ### HEALING (V-Ω):
    - **The Gnostic Bridge (`regs`):** Now exposes a `regs` property that adapts the
      internal state into a `QuantumRegisters`-compatible interface, satisfying
      the contract required by `StateHandler` and `ProclamationHandler`.
    """

    def __init__(
            self,
            symphony_path: Path,
            request_vessel: 'SymphonyRequest',
            execution_root: Optional[Path] = None
    ):
        """
        The Rite of Gnostic Inception.
        """
        # --- I. THE FORGING OF THE CORE IDENTITY & INSTRUMENTS ---
        self.symphony_path = symphony_path
        self.request = request_vessel
        self.execution_root = execution_root or symphony_path.parent
        self.logger = Logger
        self.is_aborted = False
        self._renderer_suspended = False

        # --- II. THE DIVINE BESTOWAL OF THE BODY ---
        self.console = get_console()
        self.transaction: Optional['GnosticTransaction'] = getattr(self.request, 'transaction', None)

        # --- III. THE FORGING OF THE PANTHEON OF ARTISANS ---

        # 1. Context Manager (The Memory)
        self.context_manager = GnosticContextManager(self, self.request, self.execution_root)

        # 2. Event Bus (The Nervous System)
        self.event_bus: queue.Queue = queue.Queue()

        # 3. Setup Artisan (The Architect)
        self.setup = SymphonySetup(
            context_manager=self.context_manager,
            symphony_path=self.symphony_path,
            request=self.request,
            execution_root=self.execution_root,
            is_simulation=self.is_simulation
        )

        # 4. Resilience Manager (The Guardian)
        self.resilience_manager = SymphonyResilienceManager(self)

        # 5. Lifecycle Manager (The Governor)
        self.lifecycle_manager = SymphonyLifecycleManager(self)

        # 6. Kinetic Performer (The Hand)
        self.performer = self._forge_performer()

        # 7. Handlers (The Specialists)
        self.handlers = SymphonyHandlers(
            conductor=self,
            engine=None,  # Circular dependency; injected later
            performer=self.performer,
            resilience_manager=self.resilience_manager,
            context_manager=self.context_manager
        )

        # 8. The Engine (The Heart)
        self.engine = SymphonyEngine(
            conductor=self,
            performer=self.performer,
            resilience_manager=self.resilience_manager,
            handlers=self.handlers,
            event_bus=self.event_bus,
            context_manager=self.context_manager
        )

        # 9. The Gnostic Link (Closing the Loop)
        self.handlers.engine = self.engine

        # 10. The Renderer (The Voice)
        self.renderer = self._forge_renderer()

        # 11. Signal Interception
        self._setup_signal_handlers()

    @property
    def context(self):
        """Returns the Gnostic Context Manager."""
        return self.context_manager

    @property
    def is_simulation(self) -> bool:
        return self.request.dry_run or self.request.rehearse or self.request.preview

    @property
    def non_interactive(self) -> bool:
        return self.request.non_interactive

    @property
    def regs(self) -> Any:
        """
        [THE GNOSTIC BRIDGE]
        Forges a compatibility layer that mimics `QuantumRegisters`.
        This allows artisans like `dispatch_proclamation` and `StateHandler` to
        function without modification by accessing `conductor.regs`.
        """
        # We create a lightweight vessel that carries the essential Gnosis
        return SimpleNamespace(
            sanctum=self.context_manager.cwd, # Property access -> GnosticPath
            project_root=self.execution_root,
            transaction=self.transaction,
            dry_run=self.is_simulation,
            force=self.request.force,
            verbose=self.request.verbosity > 0,
            silent=self.request.silent,
            non_interactive=self.non_interactive,
            no_edicts=False, # Symphony handles edicts internally
            gnosis=self.context_manager.variables # Property access -> Dict copy
        )

    def _forge_renderer(self) -> Renderer:
        """
        [THE ORACLE OF VISUALIZATION]
        Decides which Scribe shall proclaim the Symphony's progress.
        """
        # 1. The Explicit Will
        style = self.request.renderer.lower()

        # 2. The Auto-Gnosis (Default)
        if style == 'auto':
            # Check if running in a GitHub Actions environment
            if os.getenv("GITHUB_ACTIONS") == "true":
                style = 'github'
            # Check for Daemon mode (for IDEs)
            elif os.getenv("SCAFFOLD_DAEMON_MODE") == "1":
                style = 'stream'
            # Check for interactive terminal
            elif sys.stdout.isatty() and not self.request.non_interactive:
                style = 'rich'
            else:
                style = 'basic'

        self.logger.verbose(f"Renderer Strategy Selected: [cyan]{style}[/cyan]")

        # 3. The Summoning
        if style == 'basic':
            return BasicRenderer(self)
        elif style == 'stream':
            return StreamRenderer(self)
        elif style == 'raw':
            return RawRenderer(self)
        elif style == 'rich':
            return RichRenderer(self)
        elif style == 'cinematic':
            return CinematicRenderer(self)
        elif style == 'github':
            return GitHubActionsRenderer(self)

        # Fallback
        return BasicRenderer(self)

    def _forge_performer(self):
        """[FACULTY 4] The Performer's Forge."""
        if self.request.rehearse or self.request.dry_run:
            oracle = PropheticOracle()
            oracle.set_rehearsal_root(self.execution_root)
            return oracle
        return KineticTitan()

    def _setup_signal_handlers(self):
        """[FACULTY 8] The Signal Interceptor."""
        if threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGINT, self._handle_abort)
            signal.signal(signal.SIGTERM, self._handle_abort)

    def _handle_abort(self, signum, frame):
        if self.is_aborted: return  # Already aborting
        self.is_aborted = True
        self.logger.warn("Received Termination Signal. Initiating Phoenix Protocol...")
        # We assume the engine loop will break on is_aborted flag

    def suspend_renderer(self):
        self._renderer_suspended = True
        self.renderer.suspend()

    def resume_renderer(self):
        self._renderer_suspended = False
        self.renderer.resume()

    def conduct(self):
        """
        [THE GRAND SYMPHONY]
        The lifecycle of the entire rite.
        """
        start_time = time.time()
        was_pure = False

        try:
            # 1. Prologue
            # Get the setup data (Trinity Return)
            sanctum, edicts, vows = self.setup.initialize_symphony()

            # The Renderer's Prologue
            self.renderer.prologue(self.symphony_path, sanctum)

            # 2. Execution (The Engine's Loop)
            self.engine.execute_symphony(edicts, vows)

            was_pure = True

        except ArtisanHeresy as h:
            # Render Known Heresy
            self.renderer.render_paradox(h, None)
        except Exception as e:
            # Render Catastrophe
            self.renderer.render_paradox(e, traceback.format_exc())

        finally:
            # 3. Epilogue & Cleanup
            duration = time.time() - start_time

            try:
                # Shutdown Services / Tunnels
                self.lifecycle_manager.cleanup(
                    was_pure,
                    duration,
                    # If we rehearsed, we might have an ephemeral sanctum to clean
                    self.setup.ephemeral_sanctum_path if hasattr(self.setup, 'ephemeral_sanctum_path') else None
                )
            except Exception as e:
                self.logger.error(f"Cleanup Paradox: {e}")

            # Renderer Epilogue
            self.renderer.epilogue(was_pure, duration)

            # Final Result Forging
            result = self.engine.forge_result(was_pure, duration)
            self.renderer.render_summary_dossier(result)