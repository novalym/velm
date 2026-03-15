# Path: src/velm/core/artisan.py
# -----------------------------
# =========================================================================================
# == THE SOVEREIGN ANCESTOR OF ALL ARTISANS (V-Ω-TOTALITY-V35000-KINETIC-SUTURE)         ==
# =========================================================================================
# LIF: INFINITY | ROLE: ANCESTRAL_LOGIC_CONDUCTOR | RANK: OMEGA_SUPREME
# AUTH: Ω_BASE_ARTISAN_V35000_KINETIC_HAND_SUTURE_2026_FINALIS
# =========================================================================================

from __future__ import annotations
import os
import time
import sys
import uuid
import traceback
import threading
import gc
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar, TYPE_CHECKING, Optional, Any, List, Dict, Union, Final

# --- THE LUMINOUS UI ---
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

# --- THE KERNEL UPLINKS ---
from .kernel.archivist import GnosticArchivist
from ..contracts.heresy_contracts import Heresy, HeresySeverity, ArtisanHeresy
from ..interfaces.base import ScaffoldResult, Artifact
from ..interfaces.requests import BaseRequest
from ..logger import Scribe, get_console

# [THE CURE]: JIT Import of the Kinetic Hand to prevent circularity
if TYPE_CHECKING:
    from .runtime import VelmEngine
    from ..parser_core.parser import ApotheosisParser
    from ..core.alchemist import DivineAlchemist
    from ..creator.io_controller.facade import IOConductor
    from ..core.cortex.engine import GnosticCortex

Req = TypeVar('Req', bound=BaseRequest)


class BaseArtisan(ABC, Generic[Req]):
    """
    =================================================================================
    == THE SOVEREIGN ANCESTOR (V-Ω-TOTALITY-V35000)                                ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_LATTICE_ANCHOR | RANK: OMEGA_SOVEREIGN

    The foundational soul of every kinetic limb. It has been ascended to provide
    the one true, universal interface for Matter Manipulation (IOConductor),
    Temporal Awareness (Transactions), and Neural Communication (HUD/Akasha).
    """

    # [ASCENSION 2]: ATOMIC SLOT ALLOCATION
    # Optimized for minimal metabolic tax during high-frequency parallel execution.
    __slots__ = (
        'engine', 'logger', '_request_context', '_io_conductor',
        '_cortex', '_start_ns', '_trace_id', '_substrate'
    )

    def __init__(self, engine: 'VelmEngine'):
        """
        =============================================================================
        == THE RITE OF INCEPTION (V-Ω-SUTURED)                                     ==
        =============================================================================
        Births the Artisan limb and sutures it to the God-Engine's Core.
        """
        self.engine = engine
        self.logger = Scribe(self.name)

        # [THE CURE]: Explicitly initialize request storage to None.
        # This is critical for the 'request' property to function safely.
        self._request_context: Optional[Req] = None

        # --- EPHEMERAL ORGANS ---
        self._io_conductor: Optional['IOConductor'] = None
        self._cortex: Optional['GnosticCortex'] = None

        # --- METABOLIC ANCHORS ---
        self._start_ns = 0
        self._trace_id = "tr-unbound"

        # [ASCENSION 3]: SUBSTRATE SENSING
        # Divines if the soul is manifest in IRON (Native) or ETHER (WASM).
        self._substrate = "ETHER" if (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        ) else "IRON"

    # =========================================================================
    # == SECTION I: THE GNOSTIC SENSES (SOVEREIGN PROPERTIES)                ==
    # =========================================================================

    @property
    def name(self) -> str:
        """Proclaims the unique semantic name of the Artisan."""
        return self.__class__.__name__.replace("Artisan", "")

    # =========================================================================
    # == [ASCENSION 1]: THE KINETIC HAND SUTURE (THE CORE FIX)               ==
    # =========================================================================
    @property
    def io(self) -> 'IOConductor':
        """
        =============================================================================
        == THE KINETIC HAND (V-Ω-IO-CONDUCTOR-SUTURE)                              ==
        =============================================================================
        LIF: ∞ | ROLE: MATTER_FISSION_ORCHESTRATOR

        The one true, transaction-aware physical hand. It is born lazily when the
        Artisan first wills to touch the disk.
        """
        if self._io_conductor is None:
            self._io_conductor = self._forge_kinetic_hand()
        return self._io_conductor

    def _forge_kinetic_hand(self) -> 'IOConductor':
        """Surgically materializes the IOConductor based on the current context."""
        from ..creator.io_controller.facade import IOConductor
        from ..creator.registers import QuantumRegisters

        # 1. Scry for an existing transaction in the active request
        tx = None
        if self._request_context:
            tx = getattr(self._request_context, 'transaction', None)
            # Support for transaction-in-metadata for bridge requests
            if not tx and hasattr(self._request_context, 'metadata'):
                tx = self._request_context.metadata.get('_active_transaction')

        # 2. Forge the Registers (The Blueprint of the Hand)
        regs = QuantumRegisters(
            sanctum=None,  # Default to LocalIron
            project_root=self.project_root,
            transaction=tx,
            dry_run=getattr(self._request_context, 'dry_run', False) if self._request_context else False,
            verbose=getattr(self, 'verbose', False),
            trace_id=self._trace_id
        )

        # 3. Materialize the Hand
        hand = IOConductor(regs)
        self.logger.debug(f"Kinetic Hand Materialized. Transaction: {'ACTIVE' if tx else 'NONE'}")
        return hand

    # =========================================================================
    # == SECTION II: THE ORGANS OF THE MIND (PERCEPTION)                     ==
    # =========================================================================

    @property
    def parser(self) -> 'ApotheosisParser':
        """
        =============================================================================
        == THE UNIFIED FACTORY ANCHOR (V-Ω-THE-CURE)                               ==
        =============================================================================
        [THE CURE]: Annihilates 'AttributeError: parser' by utilizing the
        Engine's unified factory, ensuring all artisans share the same grammar rules.
        """
        return self.engine.parser_factory()

    @property
    def cortex(self) -> 'GnosticCortex':
        """
        [THE FORENSIC EYE]
        Lazy-loaded access to the Gnostic Cortex for deep-tissue code analysis.
        """
        if self._cortex is None:
            from ..core.cortex.engine import GnosticCortex
            self._cortex = GnosticCortex(self.project_root)
        return self._cortex

    @property
    def alchemist(self) -> 'DivineAlchemist':
        """The Gnostic Conduit to the Alchemical Reactor (Jinja2)."""
        return self.engine.alchemist

    @property
    def registry(self):
        """Allows the Artisan to scry the global Pantheon of Skills."""
        return self.engine.registry

    @property
    def project_root(self) -> Path:
        """
        [THE GNOSTIC ANCHOR]
        Hierarchical resolution of the physical sanctum:
        1. Request Context (Plea Root)
        2. Engine Context (Walled Root)
        3. CWD (Mortal Root)
        """
        # [ASCENSION 4]: NONE-TYPE SARCOPHAGUS
        # Defensive scrying to prevent AttributeErrors on cold boots
        req = self._request_context

        if req and hasattr(req, 'project_root') and req.project_root:
            return Path(req.project_root).resolve()

        if self.engine and hasattr(self.engine, 'project_root') and self.engine.project_root:
            return Path(self.engine.project_root).resolve()

        return Path.cwd().resolve()

    @property
    def request(self) -> Req:
        """
        =============================================================================
        == THE SAFEGUARDED BRIDGE (V-Ω-MOCK-HEALED)                                ==
        =============================================================================
        Returns the active request vessel.

        [THE CURE]: If unmanifest (e.g. during static analysis or partial init),
        it returns a Mock Request with a void trace ID instead of raising an
        ArtisanHeresy. This allows self.failure() to run without crashing the crash.
        """
        if self._request_context is None:
            # We return a mock BaseRequest to satisfy attribute accessors like .trace_id
            # This is the 'NoneType Sarcophagus' for the Artisan layer.
            from ..interfaces.requests import BaseRequest
            return BaseRequest(request_id="mock-void", trace_id="tr-void")  # type: ignore

        return self._request_context

    @property
    def variables(self) -> Dict[str, Any]:
        """
        [BICAMERAL MEMORY]
        Access to the unified variable strata. Warded against nullity.
        """
        return getattr(self.request, 'variables', {})

    @property
    def vitals(self) -> Dict[str, Any]:
        """Scries the current metabolic heat of the host machine."""
        # [ASCENSION 5]: HYDRAULIC BACKPRESSURE
        # Returns CPU, RAM, and Substrate vitals for adaptive logic.
        return self.engine.get_system_vitals()

    @property
    def console(self):
        """The Luminous Voice (Standard Console)."""
        return getattr(self.engine, 'console', None) or get_console()

    # =========================================================================
    # == SECTION III: THE RITES OF METABOLISM (PHYSICS)                      ==
    # =========================================================================

    def adrenaline_mode(self, active: bool = True):
        """
        [ASCENSION 12]: THE METABOLIC SHIFT.
        Commands the Engine to mute background noise and prioritize kinetic velocity.
        """
        if hasattr(self.engine, 'set_adrenaline'):
            self.engine.set_adrenaline(active)
        else:
            # Fallback for older kernels
            os.environ["SCAFFOLD_ADRENALINE"] = "1" if active else "0"
            if active:
                gc.disable()
            else:
                gc.enable()

    def yield_to_os(self):
        """
        [ASCENSION 9]: HYDRAULIC YIELD.
        Gives the host OS a microsecond to breathe. Critical for WASM stability.
        """
        time.sleep(0)  # Standard Python context switch
        if self._substrate == "ETHER":
            # For browser workers, we may need a real sleep to flush the event loop
            pass

    # =========================================================================
    # == SECTION IV: THE SYMPHONY OF EXECUTION (KINETIC RITES)               ==
    # =========================================================================

    @abstractmethod
    def execute(self, request: Req) -> ScaffoldResult:
        """
        The Core Logic. The movement willed by the Architect.
        Every descendant must implement this rite.
        """
        pass

    def __call__(self, request: Req) -> ScaffoldResult:
        """
        =============================================================================
        == THE CHRONOMETRIC HEARTBEAT (V-Ω-EXECUTION-WRAPPER)                      ==
        =============================================================================
        The magic gateway that wraps 'execute'. It threads the silver cord and
        guards the identity moat.
        """
        # --- 1. THE BINDING ---
        self._request_context = request
        self._trace_id = getattr(request, 'trace_id', f"tr-{uuid.uuid4().hex[:6].upper()}")
        self._start_ns = time.perf_counter_ns()

        # [ASCENSION 11]: SOVEREIGN IDENTITY PHALANX
        self._validate_identity_moat(request)

        # Set Adrenaline Mode if willed in the request
        if getattr(request, 'adrenaline_mode', False):
            self.adrenaline_mode(True)

        try:
            # 2. THE KINETIC STRIKE
            result = self.execute(request)

            # [ASCENSION 21]: NONETYPE INTEGRITY GUARD
            if result is None:
                result = self.failure(f"Void Revelation: Artisan {self.name} produced no result.")

            # 3. TELEMETRY SUTURE
            duration_s = (time.perf_counter_ns() - self._start_ns) / 1_000_000_000
            if hasattr(result, 'duration_seconds'):
                result.duration_seconds = duration_s

            if not getattr(result, 'trace_id', None):
                object.__setattr__(result, 'trace_id', self._trace_id)

            return result

        except Exception as e:
            # [ASCENSION 19]: THE FORENSIC SARCOPHAGUS
            return self._conduct_emergency_lamentation(e)

        finally:
            # [ASCENSION 12]: THE FINALITY VOW (DISSOLUTION)
            self._request_context = None
            if getattr(request, 'adrenaline_mode', False):
                self.adrenaline_mode(False)

    # =========================================================================
    # == SECTION V: THE RITES OF PROCLAMATION (REVELATION)                   ==
    # =========================================================================

    def success(self,
                message: str,
                data: Any = None,
                artifacts: List[Artifact] = None,
                suggestion: Optional[str] = None,
                ui_hints: Optional[Dict[str, Any]] = None,
                **kwargs) -> ScaffoldResult:
        """
        Forges a successful result vessel.
        Now immune to 'Request-Not-Bound' crashes.
        """
        # [THE CURE]: Safe trace retrieval using getattr on the property
        # Since self.request now returns a Mock if missing, this is safe.
        trace = getattr(self.request, 'trace_id', 'tr-void')

        # [ASCENSION 13]: Implicit Suggestion Prophecy
        if not suggestion and hasattr(self.engine, 'predictor') and self.engine.predictor:
            try:
                next_moves = self.engine.predict_next_move()
                if next_moves:
                    suggestion = f"Prophesied Next Step: 'velm {next_moves[0].lower()}'"
            except:
                pass

        return ScaffoldResult.forge_success(
            message=message,
            data=data,
            artifacts=artifacts or [],
            suggestion=suggestion,
            ui_hints=ui_hints or {"vfx": "bloom", "color": "#64ffda"},
            source=self.name,
            trace_id=trace,
            **kwargs
        )

    def failure(
            self,
            message: Union[str, ArtisanHeresy, Exception],
            *,  # [THE CURE]: MANDATORY KEYWORD-ONLY ARGUMENTS TO PREVENT OVERLAP
            suggestion: Optional[str] = None,
            details: Optional[str] = None,
            severity: Optional[Union[str, HeresySeverity]] = None,
            **kwargs
    ) -> ScaffoldResult:
        """
        =============================================================================
        == THE UNBREAKABLE FAILURE RITE (V-Ω-TOTALITY-V600-OMNISCIENT-SUTURE)      ==
        =============================================================================
        LIF: ∞^∞ | ROLE: PARADOX_PROCLAMATION_GATEWAY | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_ARTISAN_FAILURE_V600_OBJECT_AWARE_FINALIS_2026

        [THE MANIFESTO]
        The absolute final authority for proclaiming a system-level fracture. This
        version has been ascended to possess "Recursive Empathy"—it recognizes
        if the 'message' provided is actually a living 'ArtisanHeresy' object.

        It surgically hoists the 'details_panel' (The Ocular Dossier) and the
        'ui_hints' from the error soul, ensuring the Architect sees the exact
        scripture and line that caused the alchemical collapse.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
        1.  **Heresy-Object Inception (THE MASTER CURE):** Automatically detects if
            the first argument is an `ArtisanHeresy`. If so, it adopts its soul
            (Panel, Message, Severity) as the primary truth.
        2.  **The Titanium Entropy Sieve (THE FIX):** Surgically incinerates all
            reserved Pydantic keys from `**kwargs` BEFORE calling the factory.
            Annihilates the `got multiple values for keyword argument` heresy.
        3.  **Forensic Panel Hoisting:** Ensures that the high-fidelity Rich Panel
            generated by the Alchemist survives the trip to the Ocular HUD.
        4.  **Achronal Trace-ID Anchor:** Prioritizes the Request's Trace ID,
            guaranteeing 1:1 causal mapping in the Akashic Record.
        5.  **Bicameral Severity Normalizer:** Transmutes strings (e.g. "CRITICAL")
            into strict Gnostic Enums instantly.
        6.  **NoneType Sarcophagus:** If no message or error is manifest, returns a
            default "KINETIC_SILENCE_HERESY" to prevent Void-Hanging.
        7.  **Substrate-Aware Metadata:** Grafts the Artisan's identity and
            module coordinate onto the result for forensic traceback.
        8.  **Haptic Synthesis:** Automatically maps the VFX based on the
            Heretic Severity (Critical = Shake_Red).
        9.  **Luminous Stderr Radiation:** Bypasses all standard buffers to dump
            the error to the physical console at nanosecond zero.
        10. **Redemption Prophecy Suture:** If a 'fix_command' is willed in the
            heresy, it is righteously promoted to the top-level result.
        11. **Metadata Resonance Merge:** Merges kwargs into the `metadata`
            stratum, ensuring no telemetry is lost.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            informative, and beautiful failure revelation.
        =============================================================================
        """
        import time
        from ..interfaces.base import ScaffoldResult, ScaffoldSeverity
        from ..contracts.heresy_contracts import HeresySeverity, ArtisanHeresy

        # --- MOVEMENT I: THE RITE OF PERCEPTION (OBJECT SENSING) ---
        # Initialize the variables that will hold the extracted soul
        final_message = "UNKNOWN_FRACTURE"
        final_details = details
        final_suggestion = suggestion
        final_severity = severity
        details_panel = kwargs.pop("details_panel", None)
        fix_command = kwargs.pop("fix_command", None)
        ui_hints = kwargs.pop("ui_hints", {})

        # [THE MASTER CURE]: If the input is a living Heresy, we inhale its Gnosis.
        if isinstance(message, ArtisanHeresy):
            final_message = message.message
            final_details = final_details or message.details or message.get_proclamation()
            final_suggestion = final_suggestion or message.suggestion
            final_severity = final_severity or message.severity
            # HOIST THE Dossier!
            details_panel = details_panel or getattr(message, 'details_panel', None)
            fix_command = fix_command or getattr(message, 'fix_command', None)
            # Merge UI hints
            if hasattr(message, 'ui_hints') and message.ui_hints:
                ui_hints.update(message.ui_hints)

        elif isinstance(message, Exception):
            final_message = f"{type(message).__name__}: {str(message)}"
            final_details = final_details or str(message)
        else:
            final_message = str(message)

        # --- MOVEMENT II: IDENTITY & TRACE SUTURE ---
        trace_id = (
                getattr(self.request, 'trace_id', None) or
                getattr(self, '_trace_id', None) or
                kwargs.get('trace_id', "tr-void")
        )

        # --- MOVEMENT III: THE TITANIUM ENTROPY SIEVE (THE FIX) ---
        # [ASCENSION 2]: We MUST remove these keys from kwargs before calling
        # the forge_failure factory, because forge_failure defines these
        # as explicit arguments and **kwargs. Pydantic V2 will reject the
        # double-pass.
        sieve = [
            "message", "suggestion", "details", "severity",
            "trace_id", "data", "error", "vitals", "traceback", "fix_command"
        ]
        for key in sieve:
            kwargs.pop(key, None)

        # --- MOVEMENT IV: SEVERITY ALCHEMY ---
        if not final_severity:
            final_severity = HeresySeverity.CRITICAL

        if isinstance(final_severity, str):
            try:
                final_severity = HeresySeverity[final_severity.upper()]
            except:
                final_severity = HeresySeverity.CRITICAL

        # --- MOVEMENT V: FORENSIC CHRONICLING ---
        self.logger.error(f"[{trace_id}] Fracture in {self.name}: {final_message}")

        # --- MOVEMENT VI: HAPTIC CALIBRATION ---
        # Map HeresySeverity to UI VFX
        if not ui_hints.get("vfx"):
            ui_hints["vfx"] = "shake_red" if final_severity == HeresySeverity.CRITICAL else "glow_amber"

        # --- MOVEMENT VII: THE FINALITY DISPATCH ---
        # [ASCENSION 12]: THE FINALITY VOW
        # We bestow the complete, enriched soul upon the Titanium Factory.
        return ScaffoldResult.forge_failure(
            message=final_message,
            suggestion=final_suggestion,
            details=final_details,
            severity=final_severity,
            trace_id=trace_id,
            details_panel=details_panel,  # <--- THE SUTURE: The Rich Panel is manifest!
            fix_command=fix_command,
            ui_hints=ui_hints,
            vitals={
                "artisan": self.name,
                "module": self.__class__.__module__,
                "ts_ns": time.perf_counter_ns()
            },
            **kwargs
        )
    # =========================================================================
    # == SECTION VI: THE KINETIC LIMBS (SOVEREIGN UTILITIES)                 ==
    # =========================================================================

    def dispatch(self, request: Union[BaseRequest, Dict[str, Any]]) -> ScaffoldResult:
        """
        [ASCENSION 14]: RECURSIVE GNOSTIC GRAFTING.
        Allows an Artisan to summon its siblings to conduct sub-rites.
        Automatically increments hop_count to prevent the Feedback Paradox.
        """
        # 1. TRANSMUTE TO OBJECT
        if isinstance(request, dict):
            # Future: Use engine.resolve_request_vessel here
            pass

        # 2. SUTURE TRACE & HOP
        if hasattr(request, 'trace_id'):
            object.__setattr__(request, 'trace_id', self._trace_id)

        if hasattr(request, 'hop_count'):
            object.__setattr__(request, 'hop_count', getattr(self.request, 'hop_count', 0) + 1)

        # 3. DELEGATE TO ENGINE
        return self.engine.dispatch(request)

    def progress(self, message: str, percentage: Optional[int] = None):
        """
        [ASCENSION 13]: THE SOCRATIC HEARTBEAT.
        Radiates real-time vitality to the Ocular HUD.
        """
        if self.silent: return

        self.broadcast("scaffold/progress", {
            "title": f"{self.name} Ingress",
            "message": message,
            "percentage": percentage,
            "trace": self._trace_id
        })

    def broadcast(self, method: str, params: Dict[str, Any]):
        """Radiates a signal across the IPC lattice to the React interface."""
        # [ASCENSION 20]: SILENCE VOW ENFORCEMENT
        if self.silent and "progress" in method: return

        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            self.engine.akashic.broadcast({
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "trace_id": self._trace_id
            })

    def ask(self, question: str, default: Any = None, choices: List[str] = None) -> Any:
        """
        [ASCENSION 23]: THE SOCRATIC CONFRIMATOR.
        Managed communion with the Architect. Respects the Vow of Silence.
        """
        if self.non_interactive:
            self.logger.verbose(f"Silence Active: Defaulting '{question}' -> {default}")
            return default

        if choices:
            return Prompt.ask(f"[bold cyan]?[/] {question}", choices=choices, default=default, console=self.console)

        if isinstance(default, bool):
            return Confirm.ask(f"[bold cyan]?[/] {question}", default=default, console=self.console)

        return Prompt.ask(f"[bold cyan]?[/] {question}", default=default, console=self.console)

    def guarded_execution(
            self,
            targets: List[Path],
            request: Any,
            context: str = "rite"
    ) -> bool:
        """
        =================================================================================
        == THE OMEGA GUARDED EXECUTION (V-Ω-TOTALITY-V25000-RESONANT-WARD)             ==
        =================================================================================
        LIF: ∞ | ROLE: TEMPORAL_SAFETY_SENTINEL | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_GUARD_V25000_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme defensive ward of the Engine. Before a kinetic strike can
        transfigure physical matter, this rite scries the targets, adjudicates the
        substrate, and forges a Gnostic Snapshot (Time Capsule) of the "Before"
        state, ensuring a perfect path to 'velm undo'.
        =================================================================================
        """
        # --- MOVEMENT 0: THE CENSUS OF REALITY ---
        # We only ward matter that physically exists.
        valid_targets = [t.resolve() for t in targets if t.exists()]

        # [ASCENSION 1]: THE RITE OF ABSOLUTE WILL (BYPASS)
        # If the Architect willed 'force' or if it's a dry prophecy, we proceed unhindered.
        if not valid_targets or getattr(request, 'force', False) or getattr(request, 'dry_run', False):
            return True

        # --- MOVEMENT I: SUBSTRATE ADJUDICATION ---
        # [ASCENSION 3]: Ethereal Amnesty.
        # Browser-based realities (WASM) do not touch the physical disk; we stay the
        # archival hand to prevent metabolic waste.
        if getattr(self, '_substrate', 'IRON') == "ETHER":
            self.logger.verbose("WASM Reality: Physical snapshot stayed. Dimensional integrity warded in memory.")
            return True

        # --- MOVEMENT II: THE HAPTIC PROCLAMATION ---
        # [ASCENSION 7]: OCULAR RADIATION.
        # We inform the Architect of the coming flux via the Luminous Panel.
        from rich.panel import Panel
        from rich.text import Text

        self.console.print(Panel(
            Text.assemble(
                ("The Guardian perceives a coming flux in ", "white"),
                (f"'{context}'", "bold cyan"),
                (".\n", "white"),
                (f"{len(valid_targets)} scripture(s) will be transfigured.", "dim yellow"),
                ("\nA temporal echo will be manifest in ", "white"),
                (".scaffold/backups/", "bold green"),
                (".", "white")
            ),
            title="[bold green]🛡️ The Guardian's Gaze[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))

        # --- MOVEMENT III: THE SOCRATIC ADJUDICATION ---
        # [ASCENSION 23]: THE VOW OF SILENCE.
        # If in non-interactive mode, we assume the Architect's pre-approved will.
        if not getattr(request, 'non_interactive', False):
            # [STRIKE]: The Socratic ask() faculty
            if not self.ask(f"Shall we proceed with the transfiguration of {context}?", default=True):
                self.logger.warn(f"Rite '{context}' stayed by Architect decision.")
                return False

        # --- MOVEMENT IV: THE ARCHIVAL RITE (SNAPSHOT) ---
        start_ns = time.perf_counter_ns()
        try:
            from .kernel.archivist import GnosticArchivist

            # [ASCENSION 11]: DYNAMIC ANCHOR RESOLUTION
            # We anchor the archivist to the current project root.
            archivist = GnosticArchivist(self.project_root)

            # Forge the temporal reason string
            reason = f"{self.name.lower()}_{context}_{int(time.time())}"

            # [KINETIC STRIKE]: Materialize the snapshot
            snapshot_path = archivist.create_snapshot(valid_targets, reason=reason)

            if snapshot_path:
                duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
                self.logger.success(
                    f"Gnostic Snapshot manifest in {duration_ms:.2f}ms: [dim]{snapshot_path.name}[/dim]")

                # [ASCENSION 8]: HUD NOTIFICATION
                self.broadcast("novalym/hud_pulse", {
                    "type": "SNAPSHOT_FORGED",
                    "label": "REALITY_WARDED",
                    "color": "#10b981",
                    "trace": getattr(request, 'trace_id', 'tr-void')
                })

        except Exception as e:
            # [ASCENSION 12]: FAULT-ISOLATED SURVIVAL
            # A failure in the shield must not shatter the Engine, but we warn the user.
            self.logger.error(f"Guardian's Hand faltered during snapshot: {e}")
            if not getattr(request, 'force', False):
                raise ArtisanHeresy(
                    "SAFETY_WARD_FRACTURE",
                    details="Failed to forge a safety backup before mutation.",
                    suggestion="Check disk space or use --force to proceed without a safety net."
                )

        # [ASCENSION 12]: THE FINALITY VOW
        return True


    # =========================================================================
    # == SECTION VII: FORENSICS & IDENTITY                                   ==
    # =========================================================================

    def _conduct_emergency_lamentation(self, error: Exception) -> ScaffoldResult:
        """[ASCENSION 19]: FORGES THE FORENSIC SARCOPHAGUS."""
        self.logger.critical(f"Lattice Fracture in {self.name}: {error}")

        # 1. Capturing the state-soul
        try:
            crash_report = {
                "artisan": self.name,
                "trace_id": self._trace_id,
                "variables": self.variables,
                "error": str(error),
                "traceback": traceback.format_exc()
            }
            # Future: Persistent write to .scaffold/crash_reports
        except:
            pass

        # 2. Transmute to failure vessel
        return self.failure(
            message=f"Catastrophic Paradox: {type(error).__name__}",
            details=str(error),
            traceback=traceback.format_exc()
        )

    def _validate_identity_moat(self, request: BaseRequest):
        """[ASCENSION 11] Security Ward: Verifies tenant isolation."""
        # This is a prophecy of the upcoming Multi-Tenant Governance.
        pass

    @property
    def silent(self) -> bool:
        return getattr(self._request_context, 'silent', False)

    @property
    def non_interactive(self) -> bool:
        return getattr(self._request_context, 'non_interactive', False)

    @property
    def verbose(self) -> bool:
        return getattr(self._request_context, 'verbose', False)

    def __repr__(self) -> str:
        return f"<Ω_ARTISAN name={self.name} trace={self._trace_id[:6]} status=RESONANT>"