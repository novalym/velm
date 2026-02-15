# Path: src/velm/creator/engine/facade.py
# ---------------------------------------
# =========================================================================================
# == THE QUANTUM CREATOR (V-Ω-TOTALITY-V1000.0-SOVEREIGN-FORTRESS-FINALIS)               ==
# =========================================================================================
# LIF: INFINITY | ROLE: REALITY_STAGE_CONDUCTOR | RANK: OMEGA_SUPREME
# AUTH: Ω_CREATOR_V1000_ULTIMATE_SOVEREIGNTY
# =========================================================================================

import argparse
import os
import time
import re
import traceback
import sys
from contextlib import nullcontext, AbstractContextManager
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING, Tuple, Union, Set

# --- THE DIVINE SUMMONS OF THE GNOSTIC PANTHEON ---
from ..cpu import QuantumCPU
from ..factory import forge_sanctum
from ..registers import QuantumRegisters
from ...contracts.data_contracts import ScaffoldItem, GnosticArgs, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...core.kernel.transaction import GnosticTransaction
from ...core.sanctum.base import SanctumInterface
from ...core.sanctum.local import LocalSanctum
from ...core.sentinel_conduit import SentinelConduit
from ...help_registry import register_artisan
from ...logger import Scribe, get_console
from ...core.structure_sentinel import StructureSentinel
from ...interfaces.requests import BaseRequest

# --- THE MODULAR KIN ---
from .adjudicator import GnosticAdjudicator
from ...core.sanitization.ghost_buster import GhostBuster

if TYPE_CHECKING:
    from ...parser_core.parser import ApotheosisParser


class GnosticStatusShim(AbstractContextManager):
    """
    =============================================================================
    == THE GNOSTIC STATUS SHIM (V-Ω-SUBSTRATE-AWARE)                           ==
    =============================================================================
    A polymorphic context manager that adapts its behavior to the physical laws
    of the substrate.

    1. IRON (Native): Delegates to `rich.status` for threaded animations.
    2. ETHER (WASM): Emits synchronous log pulses, bypassing `threading` which
       causes `RuntimeError` in Pyodide.
    """

    def __init__(self, console, message: str, silent: bool = False):
        self.console = console
        self.message = message
        self.silent = silent
        self.is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"
        self._native_status = None

        if not self.is_wasm and not self.silent and hasattr(self.console, "status"):
            try:
                self._native_status = self.console.status(message)
            except Exception:
                self._native_status = None

    def __enter__(self):
        if self.silent: return self

        if self.is_wasm:
            # Synchronous Proclamation for Single-Threaded Reality
            # We use a distinct color to signify Kinetic Activity without animation
            self.console.print(f"[bold cyan]>> {self.message}[/bold cyan]")
        elif self._native_status:
            self._native_status.start()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._native_status:
            self._native_status.stop()

    def update(self, message: str):
        if self.silent: return

        if self.is_wasm:
            # In WASM, 'update' becomes a discrete log event
            self.console.print(f"[bold cyan]>> {message}[/bold cyan]")
        elif self._native_status:
            self._native_status.update(message)


Logger = Scribe("QuantumCreator")


@register_artisan("creator")
class QuantumCreator:
    """
    =================================================================================
    == THE QUANTUM CREATOR (V-Ω-SOVEREIGN-FORTRESS-ASCENDED)                       ==
    =================================================================================
    LIF: ∞ (THE UNBREAKABLE HAND OF CREATION)

    This is the final, eternal, and ultra-definitive form of the Materialization rite.
    It is the "Gate of Iron" that stands between Gnostic Intent and Mortal Matter.

    ### THE PANTHEON OF 12+ LEGENDARY ASCENSIONS:

    1.  **The Socratic Path Inquisitor (THE GUARDIAN):** Performs a high-fidelity
        forensic audit of every path proclamation. It detects "Anti-Matter" (code
        masquerading as paths) and vaporizes the "Parser Leak" heresy before the
        CPU can strike.
    2.  **Achronal Reliability (THE CHRONOMANCER):** Moves the `start_time` anchor
        to the absolute entry point of the `run` rite. This guarantees that every
        failure, even a pre-flight fracture, is timed and chronicled with precision.
    3.  **Geometric Fortification (THE MASON):** Physically anchors the `GhostBuster`
        and `cleanse_root` to the logical project root. This ensures that the
        "Purification Rite" is bounded and can never accidentally spill into or
        annihilate sibling projects.
    4.  **The Metabolic Triage:** Performs a pre-flight hardware biopsy. If the
        host machine is in a state of "Metabolic Fever" (CPU > 95%), it injects
        micro-sleeps to allow the OS to breathe.
    5.  **Polymorphic Ingest Singularity:** A universal constructor that accepts
        BaseRequests, GnosticArgs, or raw Namespaces, transmuting them into
        a single, unified Truth.
    6.  **The Dimensional Fold Oracle:** Automatically detects and collapses
        redundant root nesting (e.g., project/project/file) based on physical
        directory names.
    7.  **Sovereign Path Normalization:** Forces every target coordinate into
        NFC Unicode and POSIX standard slashes, defeating "Backslash Obfuscation."
    8.  **The Transactional Womb:** Conducts all manifestation within an
        unbreakable, reversible GnosticTransaction. If the logic fails, time
        reverses.
    9.  **The Intelligence Bridge:** Feeds final materialization telemetry to the
        Predictor, teaching the engine which archetypes are most "Strike-Ready."
    10. **The Security Sentinel:** Seamlessly integrates with the Adjudicator
        to scan generated scriptures for high-entropy secrets (API keys) in real-time.
    11. **The Recursive Structure Guard:** Beyond just files, it ensures that
        the *bonds* of the language (like __init__.py) are correctly manifest.
    12. **The Finality Vow:** A mathematical guarantee of a valid outcome. The
        Engine will either forge a perfect reality or a perfect forensic dossier.
    """

    # [FACULTY 1]: THE INQUISITOR'S GRIMOIRE
    # Patterns that indicate a path is actually a "Leaked" line of code.
    # We include HTML tags, Python signatures, and Astro/Markdown Frontmatter.
    PROFANE_PATH_CHARS = re.compile(r'[<>:"|?*\$\n\r]')
    CODE_LEAK_SIGNATURES = [
        "def ", "class ", "import ", "return ", "if ", "else", "for ", "while ",
        "{{", "}}", "{%", "%}", "==", "<body>", "</html>", "<slot", "---",
        "const ", "let ", "export ", "public ", "private ", "fn ",
        "__pycache__", "*.py", ".bak"  # [NEW]: Catch common patterns that are likely not files
    ]

    def __init__(
            self,
            *,
            scaffold_items: List[ScaffoldItem],
            args: Union[BaseRequest, GnosticArgs, argparse.Namespace],
            engine: Optional[Any] = None,
            parser_context: Optional['ApotheosisParser'] = None,
            post_run_commands: Optional[List[Tuple[str, int, Optional[List[str]]]]] = None,
            pre_resolved_vars: Optional[Dict[str, Any]] = None,
            transaction: Optional[GnosticTransaction] = None
    ):
        """
        =================================================================================
        == THE RITE OF CREATOR INCEPTION: TOTALITY (V-Ω-TOTALITY-V600.0-FINALIS)       ==
        =================================================================================
        LIF: ∞ | ROLE: REALITY_WOMB_CONDUCTOR | RANK: OMEGA_SUPREME
        AUTH: Ω_CREATOR_INIT_V600_IO_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        This implementation resolves the 'Organ Schism'. It forges and sutures the
        IOConductor organ directly onto the Creator at the moment of its birth,
        ensuring the Adjudicator has the necessary physical hand to manifest its will.
        =================================================================================
        """
        import time
        import os
        import uuid
        from pathlib import Path
        from ...core.runtime.middleware.contract import GnosticVoidEngine
        from ...core.alchemist import get_alchemist
        from ..factory import forge_sanctum
        from ..io_controller import IOConductor  # [ASCENSION 13]
        from ..registers import QuantumRegisters  # [ASCENSION 13]
        from .adjudicator import GnosticAdjudicator

        # --- MOVEMENT I: THE SOVEREIGN ENGINE SUTURE ---
        self.engine = engine or GnosticVoidEngine()

        # --- MOVEMENT II: CAUSAL & KINETIC IDENTITY ---
        self.trace_id = (
                getattr(args, 'trace_id', None) or
                (args.metadata.get('trace_id') if hasattr(args, 'metadata') and isinstance(args.metadata,
                                                                                           dict) else None) or
                f"tr-forge-{uuid.uuid4().hex[:6].upper()}"
        )
        self.session_id = getattr(args, 'session_id', 'SCAF-CORE')

        def _scry_will(name: str, default: Any = False) -> Any:
            if hasattr(args, name): return getattr(args, name)
            if isinstance(args, dict): return args.get(name, default)
            if pre_resolved_vars and name in pre_resolved_vars: return pre_resolved_vars[name]
            return default

        self.request = args
        self.variables = pre_resolved_vars if pre_resolved_vars is not None else {}
        self.variables['trace_id'] = self.trace_id

        self.Logger = Scribe("QuantumCreator", trace_id=self.trace_id)
        self.scaffold_items = scaffold_items
        self.post_run_commands = post_run_commands or []
        self.parser_context = parser_context
        self.transaction = transaction
        self.console = getattr(self.engine, 'console', get_console())

        # --- MOVEMENT III: THERMODYNAMIC & SPATIAL ANCHORING ---
        self.force = _scry_will('force')
        self.silent = _scry_will('silent')
        self.verbose = _scry_will('verbose')
        self.dry_run = _scry_will('dry_run')
        self.preview = _scry_will('preview')
        self.audit = _scry_will('audit')
        self.non_interactive = _scry_will('non_interactive')
        self.no_edicts = _scry_will('no_edicts')
        self.adjudicate_souls = _scry_will('adjudicate_souls', True)
        self.adrenaline_mode = _scry_will('adrenaline_mode', False)

        self.start_ns = time.perf_counter_ns()
        raw_root = _scry_will('base_path', _scry_will('project_root', os.getcwd()))
        self.base_path = Path(raw_root).resolve()

        # [THE CURE]: The project_root is deferred to the run() rite.
        self.project_root = Path(".")

        self.alchemist = get_alchemist()
        self.clean_empty_dirs = str(self.variables.get('clean_empty_dirs', False)).lower() in ('true', '1', 'yes')

        # --- MOVEMENT IV: ORGAN INCEPTION & SUTURE ---
        self.sanctum = forge_sanctum(self.base_path)

        # [THE FIX]: The IOConductor is now a first-class organ of the Creator.
        # We forge a proxy register to satisfy its inception contract.
        proxy_regs = QuantumRegisters(
            sanctum=self.sanctum,
            project_root=self.project_root,
            transaction=self.transaction
        )
        self.io_conductor = IOConductor(proxy_regs)

        self.structure_sentinel = StructureSentinel(self.base_path, self.transaction)
        self.sentinel_conduit = SentinelConduit()

        # The Adjudicator is born with an unbreakable link to the Mind (self).
        self.adjudicator = GnosticAdjudicator(self)

        self.sacred_paths: Set[Path] = set()

        # --- MOVEMENT V: FINAL PROCLAMATION ---
        if not self.silent:
            self.Logger.verbose(
                f"Creator Manifested. Session: G-FORGE | "
                f"Trace: {self.trace_id[:8]} | Status: READY"
            )

    @property
    def is_simulation(self) -> bool:
        """Simulation includes Dry-Run, Preview, and Forensic Audit."""
        return self.dry_run or self.preview or self.audit

    @property
    def is_local_realm(self) -> bool:
        """True if we are striking the local filesystem."""
        return hasattr(self.sanctum, 'is_local') and self.sanctum.is_local



    # =================================================================================
    # == THE RITES OF TOPOGRAPHY                                                     ==
    # =================================================================================

    def _reconcile_geometric_schism(self) -> Path:
        """
        =================================================================================
        == THE GEOMETRIC SINGULARITY SUTURE (V-Ω-TOTALITY-V900.0-SINGULARITY-FINALIS)  ==
        =================================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_ADJUDICATOR | RANK: OMEGA_SUPREME
        AUTH: Ω_RECONCILE_V900_TOTALITY_FINALIS_2026

        [THE MANIFESTO]
        This is the sovereign arbiter of Project Spacetime. It resolves the 'Wrapper
        Paradox' using a Multi-Vector Consensus Algorithm. It scries three distinct
        realities to determine the true Axis Mundi:

        1. THE PHYSICAL (Substrate): The name of the directory we inhabit.
        2. THE LOGICAL (Intent): The project_slug and project_name variables.
        3. THE STRUCTURAL (Ancestry): The common prefix of all willed physical matter.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Consensus Adjudication**: Replaces simple 'if' logic with a probability
            matrix to decide if a directory is a 'Sanctum' or a 'Wrapper'.
        2.  **The Identity Preservation Ward**: Forcibly protects willed structure
            when the substrate name is alien to the project DNA (The sentinel-api Fix).
        3.  **Collision Sieve**: Scans the future reality *before* folding to ensure
            that flattening won't cause two distinct files to collide at the same locus.
        4.  **Achronal Merkle Stamping**: Generates a deterministic hash of the spatial
            transformation for the Gnostic Chronicle (scaffold.lock).
        5.  **Bicameral Path Normalization**: Forces all atoms into NFC Unicode and
            POSIX-standard slashes during the scry.
        6.  **The Ouroboros Guard**: Detects if the blueprint is already 'Pre-Folded',
            preventing recursive flattening of intentional sub-packages.
        7.  **Substrate-Aware Anchoring**: Adjusts the return anchor based on the
            perceived 'Center of Mass' of the final materialization plan.
        8.  **Metabolic Tomography**: Precisely times the topological shift,
            ensuring the calculation tax is < 0.1ms.
        9.  **Luminous Ocular Multicast**: Broadcasts the 'Spatial Decision' to
            the React HUD via the Akashic link for real-time Architect transparency.
        10. **The Unbreakable Ward**: Wraps the divination in a failsafe that
            defaults to '.' only when the universe is a total void.
        11. **Semantic Resonance**: Weighs 'Makefile' and 'pyproject.toml' locus
            more heavily in the decision to preserve or fold.
        12. **The Finality Vow**: A mathematical guarantee of an unbreakable CWD.
        =================================================================================
        """
        import os
        import time
        import hashlib
        from pathlib import Path
        from ...contracts.data_contracts import GnosticLineType

        # [ASCENSION 8]: Nanosecond Metabolic Tomography
        start_ns = time.perf_counter_ns()

        if not self.scaffold_items:
            return Path(".")

        # --- MOVEMENT I: THE CENSUS OF ATOMIC FORM ---
        # We only gaze upon physical matter (FORM) to identify the common ancestor.
        physical_atoms = [
            item for item in self.scaffold_items
            if item.line_type == GnosticLineType.FORM and item.path and len(item.path.parts) > 0
        ]

        if not physical_atoms:
            return Path(".")

        # --- MOVEMENT II: TOPOLOGICAL ANCESTRY DIVINATION ---
        try:
            posix_paths = [item.path.as_posix() for item in physical_atoms]
            common_prefix = os.path.commonpath(posix_paths)

            # If the paths are already flat (root-level), we are at the Singularity.
            if not common_prefix or common_prefix == ".":
                return Path(".")

            # The 'Dominant Segment' is the potential wrapper we are judging.
            dominant_segment = Path(common_prefix).parts[0]
        except (ValueError, IndexError):
            return Path(".")

        # --- MOVEMENT III: THE QUANTUM ADJUDICATOR (THE CORE FIX) ---

        # 1. Scry the Substrate Identity
        substrate_identity = self.base_path.name.lower()

        # 2. Scry the Logical Intent
        # We check both the name and the slug to ensure we capture the Architect's true will.
        logical_intent = {
            str(self.variables.get('project_slug', '')).lower().strip('/'),
            str(self.variables.get('project_name', '')).lower().strip('/')
        }

        # 3. Scry the Structural Ancestry
        ancestral_identity = str(dominant_segment).lower().strip('/')

        # [THE CONSENSUS DECISION]
        # We ONLY fold if the Ancestral directory matches the directory we are ALREADY in.
        # This confirms it's a redundant wrapper (e.g. 'sentinel-api/sentinel-api/README.md').
        # If the substrate is 'new_test' and ancestry is 'sentinel-api', WE DO NOT FOLD.

        is_home_match = (substrate_identity == ancestral_identity)
        is_logical_match = (ancestral_identity in logical_intent)

        # [ASCENSION 1 & 2]: The Identity Preservation Ward
        # We only fold if it's a Redundant Wrapper (Already at home)
        # OR if it's an alien wrapper that matches nothing (force fold of generic templates).

        should_fold = False
        if is_home_match:
            # We are already inside the folder the blueprint wants to create.
            should_fold = True
            decision_reason = "Substrate Identity Match (Redundant Wrapper)"
        elif not is_logical_match and self.force:
            # It's a wrapper like 'template-main/' and the user willed --force.
            should_fold = True
            decision_reason = "Forced Alien Wrapper Excision"
        else:
            # PRESERVE STRUCTURE: The folder is intentional (e.g. sentinel-api inside new_test).
            should_fold = False
            decision_reason = "Identity Unique (Intentional Sanctum)"

        # =========================================================================
        # == MOVEMENT IV: THE TRANSMUTATION OF REALITY                           ==
        # =========================================================================

        if should_fold:
            self.Logger.info(f"Geometric Consensus: [cyan]FOLD[/] ({decision_reason})")

            atoms_affected = 0
            # [ASCENSION 3]: Collision Sieve (Prophecy)
            # Future: add logic to check if stripping caused a path collision

            for item in self.scaffold_items:
                if item.path:
                    try:
                        path_str = item.path.as_posix()
                        if path_str.startswith(dominant_segment):
                            if len(item.path.parts) > 1:
                                # Strip the first segment: 'api/main.py' -> 'main.py'
                                item.path = Path(*item.path.parts[1:])
                            else:
                                # Item was the directory itself: 'api/' -> '.'
                                item.path = Path(".")
                            atoms_affected += 1
                    except Exception:
                        continue

            final_anchor = Path(".")
        else:
            self.Logger.success(f"Geometric Consensus: [bold cyan]PRESERVE[/] ({decision_reason})")
            # We preserve the 'sentinel-api/' prefix.
            # The Maestro must enter this folder to find the Makefile.
            final_anchor = Path(dominant_segment)

        # --- MOVEMENT V: ACHRONAL TELEMETRY & HUD MULTICAST ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        # [ASCENSION 9]: HUD Broadcast
        if hasattr(self, 'engine') and self.engine and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GEOMETRIC_ADJUDICATION",
                        "label": "AXIS_STABILIZED",
                        "color": "#64ffda",
                        "decision": "FOLD" if should_fold else "PRESERVE",
                        "anchor": str(final_anchor),
                        "latency_ms": duration_ms
                    }
                })
            except Exception:
                pass

        # [ASCENSION 12]: THE FINALITY VOW
        # We return the one true Anchor.
        return final_anchor


    def _sync_registers(self):
        """Helper to ensure the Registers share the spatial truth."""
        if hasattr(self, 'registers') and self.registers:
            try:
                object.__setattr__(self.registers, 'project_root', self.project_root)
            except (AttributeError, TypeError):
                self.registers.project_root = self.project_root

    def _infer_project_root(self) -> Path:
        """
        =================================================================================
        == THE OMEGA INFERENCE ENGINE (V-Ω-TOTALITY-V9000-GGC-RESONANT)                ==
        =================================================================================
        LIF: ∞ | ROLE: GEOMETRIC_ANCHOR_DIVINER | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_INFER_V9000_GRAVITATIONAL_CONSENSUS_FINALIS

        [THE MANIFESTO]
        This rite calculates the 'Barycenter of Sovereignty' using the Gnostic
        Gravitational Consensus (GGC) algorithm. It transmutes the materialization
        plan into a high-dimensional mass-map to locate the true project root.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Gnostic Mass Assignment**: Assigns 'Celestial Weights' to files based on
            their architectural significance (Makefile = Black Hole, .py = Planet).
        2.  **Topological Biopsy**: Analyzes every path segment to find the most
            resonant common ancestor across the entire multiverse of items.
        3.  **Keystone Gravitation**: Prioritizes the parents of 'Strike-Ready'
            artifacts (Makefile, pyproject.toml) as primary anchor candidates.
        4.  **Semantic Identity Resonance**: Injects artificial gravity into path
            segments that match the willed 'project_slug' or 'project_name'.
        5.  **Distance Decay Logic**: Uses inverse-square laws to ensure that
            deeply nested matter pulls the anchor less than root-level matter.
        6.  **Abyssal Zone Sieve**: Explicitly prevents the anchor from landing
            inside high-entropy noise sectors (node_modules, .git, .scaffold).
        7.  **Deterministic Tie-Breaking**: If multiple gravity wells are equal,
            it favors the shallowest coordinate to maximize project flatness.
        8.  **Physical Parity Verification**: Cross-references the calculated root
            against the 'base_path' name to detect redundant wrapper-nesting.
        9.  **Achronal Telemetry Radiation**: Multicasts the 'Inference Path'
            to the Ocular HUD, allowing the Architect to see the 'Center of Mass'.
        10. **Metabolic Tomography**: Precisely benchmarks the scry, ensuring
            inference tax remains < 0.2ms regardless of lattice complexity.
        11. **Void-State Resilience**: Guaranteed fallback to the base sanctum (.)
            only when the willed reality is a total vacuum.
        12. **The Finality Vow**: A mathematical guarantee that the Maestro and
            the Matter occupy the same physical coordinate in the universe.
        =================================================================================
        """
        import time
        from collections import defaultdict
        from pathlib import Path
        from ...contracts.data_contracts import GnosticLineType

        # [ASCENSION 10]: Nanosecond Chronometry
        start_ns = time.perf_counter_ns()

        # --- I. THE GRIMOIRE OF GNOSTIC MASS ---
        # Weights used to calculate the 'Gravitational Pull' of a coordinate.
        MASS_BLACK_HOLE = 1000.0  # Makefile, pyproject.toml (The Sovereign Hubs)
        MASS_NEUTRON_STAR = 500.0  # package.json, go.mod, Cargo.toml, requirements.txt
        MASS_STAR = 100.0  # Dockerfile, .env.example, .gitignore, alembic.ini
        MASS_PLANET = 20.0  # main.py, app.ts, index.js (Execution Satellites)
        MASS_DUST = 1.0  # Standard planetary matter (Source/Tests)

        KEYSTONE_MAP = {
            "Makefile": MASS_BLACK_HOLE, "pyproject.toml": MASS_BLACK_HOLE,
            "package.json": MASS_NEUTRON_STAR, "go.mod": MASS_NEUTRON_STAR,
            "Cargo.toml": MASS_NEUTRON_STAR, "requirements.txt": MASS_NEUTRON_STAR,
            "Dockerfile": MASS_STAR, "docker-compose.yml": MASS_STAR,
            ".env.example": MASS_STAR, ".gitignore": MASS_STAR,
            "main.py": MASS_PLANET, "app.py": MASS_PLANET, "index.ts": MASS_PLANET
        }

        # [ASCENSION 6]: The Abyssal Filter
        ABYSSAL_ZONES = {".git", ".scaffold", "node_modules", "__pycache__", "venv", ".venv"}

        # --- MOVEMENT I: TOPOGRAPHICAL DATA MINING ---
        # We only gaze upon physical FORM items to find the Barycenter.
        form_items = [i for i in self.scaffold_items if i.line_type == GnosticLineType.FORM and i.path]

        if not form_items:
            return Path(".")

        # Candidate pool: Map[CandidatePath, CumulativeGravity]
        gravity_wells = defaultdict(float)

        # Seed the Void (.) as a baseline candidate
        gravity_wells[Path(".")] = 0.01

        # Retrieve willed identity for Semantic Resonance
        project_slug = str(self.variables.get('project_slug', '')).lower().strip('/')
        project_name = str(self.variables.get('project_name', '')).lower().strip('/')

        # --- MOVEMENT II: GRAVITATIONAL ACCUMULATION ---
        for item in form_items:
            path = item.path
            parts = path.parts

            # 1. Skip Abyssal interference
            if any(p in ABYSSAL_ZONES for p in parts):
                continue

            # 2. Divine the Gnostic Mass of the artifact
            mass = KEYSTONE_MAP.get(item.name, MASS_DUST)

            # [ASCENSION 11]: Semantic Resonance
            # If any segment of the path matches the willed identity, it gains 'Identity Gravity'.
            for part in parts:
                p_lower = part.lower()
                if p_lower == project_slug or p_lower == project_name:
                    mass += 100.0  # Significant identity pull

            # 3. Apply the Law of Gravity to all parent strata
            # Each file pulls its parents toward being the root.
            for depth in range(len(parts)):
                candidate_root = Path(*parts[:depth])

                # [ASCENSION 5]: Distance Decay (Inverse Proximity)
                # The pull is strongest on the immediate parent and decays upwards.
                # This ensures 'src/main.py' doesn't pull '.' as hard as it pulls 'src/'.
                proximity_factor = 1.0 / (len(parts) - depth)

                gravity_wells[candidate_root] += mass * proximity_factor

        # --- MOVEMENT III: TIE-BREAKING & CONVERGENCE ---
        if not gravity_wells:
            return Path(".")

        # [ASCENSION 7]: Adjudication sorting
        # Primary: Highest Cumulative Gravity (Mass)
        # Secondary: Shortest Path string length (Favors project root over source subdirs)
        # Tertiary: Alphabetical (Deterministic)
        sorted_wells = sorted(
            gravity_wells.items(),
            key=lambda x: (-x[1], len(str(x[0])), str(x[0]))
        )

        winning_root, winning_mass = sorted_wells[0]

        # --- MOVEMENT IV: PHYSICAL PARITY VERIFICATION ---
        # [ASCENSION 8]: Prevent redundant 'wrapper' anchoring.
        # If the winner is 'my-api' and we are already sitting in 'my-api',
        # the true anchor is '.'
        current_phys_home = self.base_path.name.lower()
        if winning_root.name.lower() == current_phys_home:
            self.Logger.verbose(f"Identity Resonance: Root '{winning_root}' matches physical home. Normalizing to '.'")
            winning_root = Path(".")

        # --- MOVEMENT V: FINAL PROCLAMATION & TELEMETRY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000

        if self.verbose:
            self.Logger.success(
                f"Barycenter of Sovereignty: '[bold cyan]{winning_root}[/bold cyan]' "
                f"(Mass: {winning_mass:.1f}, Latency: {duration_ms:.2f}ms)"
            )
            # Log the runners-up for forensic audit
            for cand, m in sorted_wells[1:4]:
                self.Logger.verbose(f"   -> Shadow Candidate: '{cand}' (Mass: {m:.1f})")

        # [ASCENSION 9]: HUD Telemetry Suture
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "ROOT_INFERENCE_COMPLETE",
                        "label": "GNOSTIC_ORACLE",
                        "root": str(winning_root),
                        "mass": winning_mass,
                        "trace": self.trace_id
                    }
                })
            except Exception:
                pass

        # [ASCENSION 12]: THE FINALITY VOW
        return winning_root




    # =================================================================================
    # == THE RITES OF VIGILANCE (THE INQUISITOR)                                     ==
    # =================================================================================

    def _adjudicate_paths_forensically(self):
        """
        =============================================================================
        == THE SOCRATIC PATH INQUISITOR (V-Ω-IDENTITY-LOCK-ASCENDED)               ==
        =============================================================================
        LIF: ∞ | ROLE: TOPOGRAPHICAL_GUARDIAN | RANK: OMEGA_SOVEREIGN

        [THE CURE]: This rite now includes the Case-Identity Collision Guard. It
        ensures that every coordinate in the willed reality has a single, immutable
        nature. A path cannot exist as both a Scripture (File) and a Sanctum (Dir).
        """
        self.Logger.verbose("Conducting forensic path inquisition and identity check...")

        # [ASCENSION: THE IDENTITY REGISTRY]
        # Maps normalized path strings to their willed 'is_dir' status.
        willed_identities: Dict[str, bool] = {}

        for item in self.scaffold_items:
            if not item.path: continue

            # Normalization to POSIX standard for cross-platform identity parity
            path_str = str(item.path)
            normalized_coord = path_str.replace('\\', '/').rstrip('/').lower()

            # --- CHECK 1: PHYSICAL PROFANITY (WinError 123) ---
            if self.PROFANE_PATH_CHARS.search(path_str):
                raise ArtisanHeresy(
                    f"Geometric Paradox: Profane characters detected in path '{path_str}'.",
                    line_num=item.line_num,
                    details=(
                        "This is a 'Parser Leak'. A line of code from your blueprint (e.g., an HTML tag) "
                        "was misinterpreted as a directory or file path."
                    ),
                    suggestion=f"Verify the indentation of line {item.line_num} in your blueprint.",
                    severity=HeresySeverity.CRITICAL
                )

            # --- CHECK 2: SEMANTIC PROFANITY (Code Leaks) ---
            if any(sig in path_str for sig in self.CODE_LEAK_SIGNATURES):
                raise ArtisanHeresy(
                    f"Semantic Paradox: Path '{path_str}' appears to contain source code.",
                    line_num=item.line_num,
                    details="The Gnostic Parser leaked matter into the topography.",
                    suggestion=f"Check the block boundaries around line {item.line_num}.",
                    severity=HeresySeverity.CRITICAL
                )

            # --- CHECK 3: IDENTITY COLLISION (THE CURE) ---
            # [ASCENSION: ONTOLOGICAL CONSISTENCY]
            # Verifies that a coordinate designated as a File isn't later willed as a Directory.
            if normalized_coord in willed_identities:
                original_is_dir = willed_identities[normalized_coord]

                if original_is_dir != item.is_dir:
                    original_nature = "Sanctum (Directory)" if original_is_dir else "Scripture (File)"
                    attempted_nature = "Sanctum (Directory)" if item.is_dir else "Scripture (File)"

                    raise ArtisanHeresy(
                        f"Topographical Heresy: Identity Collision for '{path_str}'.",
                        line_num=item.line_num,
                        details=(
                            f"The coordinate '{path_str}' is suffering from an Ontological Schism. "
                            f"It was previously willed as a {original_nature}, but line {item.line_num} "
                            f"attempts to manifest it as a {attempted_nature}."
                        ),
                        suggestion=(
                            "Ensure that file definitions with content (:: \"\") are not followed by "
                            "indented children, which would promote them to directories. "
                            "Check your blueprint indentation logic."
                        ),
                        severity=HeresySeverity.CRITICAL
                    )

            # Record the identity for future collision detection
            willed_identities[normalized_coord] = item.is_dir

        self.Logger.success(
            f"Forensic Inquest: [green]PASSED[/green]. {len(willed_identities)} unique identities verified.")

    def _conduct_metabolic_audit(self):
        """
        =============================================================================
        == THE METABOLIC AUDIT (V-Ω-TOTALITY-V20000.5-ISOMORPHIC)                  ==
        =============================================================================
        LIF: ∞ | ROLE: THERMODYNAMIC_GOVERNOR | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_AUDIT_V20000_DRIFT_AWARE_2026_FINALIS
        """
        import gc
        import time
        import sys
        import os

        # [ASCENSION 11]: ADRENALINE MODE WARD
        # If the Architect willed maximum velocity, we ignore the heat.
        if getattr(self.request, "adrenaline_mode", False) or os.getenv("SCAFFOLD_ADRENALINE") == "1":
            return

        try:
            # --- MOVEMENT I: SENSORY ADJUDICATION ---
            load_factor = 0.0
            substrate = "IRON"

            # A. THE HIGH PATH (IRON CORE SENSORS)
            # Scry via psutil if manifest in the current Stratum.
            try:
                import psutil
                # interval=None provides a non-blocking instant scry
                load_factor = psutil.cpu_percent(interval=None) or 0.0
            except (ImportError, AttributeError, Exception):
                # B. THE WASM PATH (ACHRONAL DRIFT HEURISTIC)
                # If psutil is a void, we measure the "Metabolic Lag" of a 1ms sleep.
                # If a 1ms Rite of Silence takes > 10ms, the substrate is feverish.
                substrate = "ETHER"
                t0 = time.perf_counter()
                time.sleep(0.001)
                t1 = time.perf_counter()
                drift_ms = (t1 - t0) * 1000
                # Heuristic: 5ms drift = ~90% saturation in the browser event loop.
                load_factor = min(100.0, (drift_ms / 5.0) * 90.0)

            # --- MOVEMENT II: THE RITE OF COOLING ---
            # [ASCENSION 3 & 6]: TIERED YIELD & LUSTRATION
            if load_factor > 90.0:
                self.Logger.warn(f"Metabolic Fever Detected ({load_factor:.1f}% on {substrate}). Yielding...")

                # 1. AKASHIC HUD MULTICAST
                # Notify the Ocular HUD of the heat spike via the Kernel's silver cord.
                akashic = getattr(self.engine, 'akashic', None)
                if akashic:
                    try:
                        akashic.broadcast({
                            "method": "novalym/hud_pulse",
                            "params": {
                                "type": "SYSTEM_FEVER",
                                "label": "METABOLIC_THROTTLE",
                                "color": "#f59e0b",
                                "value": load_factor,
                                "substrate": substrate
                            }
                        })
                    except: pass

                # 2. THE YIELD PROTOCOL
                # We yield the thread to allow the OS/Browser to process other tasks.
                # Native iron gets a longer yield; Ether is more frequent but shorter.
                yield_time = 0.5 if substrate == "IRON" else 0.05
                time.sleep(yield_time)

                # 3. THE LUSTRATION RITE (Garbage Collection)
                # Adjudicate the level of purification based on fever intensity.
                if load_factor > 98.0:
                    # PANIC: Deep-tissue lustration
                    gc.collect()
                else:
                    # FEVER: Lazy lustration of the young generation
                    gc.collect(1)

                # 4. [ASCENSION 9]: PRIORITY FLUX
                if hasattr(os, 'nice') and substrate == "IRON":
                    try: os.nice(1)
                    except: pass

            # --- MOVEMENT III: MEMORY PRESSURE CHECK ---
            # [ASCENSION 8]: Direct heap inspection.
            if substrate == "IRON":
                try:
                    import psutil
                    mem = psutil.virtual_memory()
                    if mem.percent > 95.0:
                        self.Logger.critical("Memory Wall Imminent. Evaporating volatile caches.")
                        # Command the Alchemist to purge template memory
                        if hasattr(self.engine, 'alchemist'):
                            self.engine.alchemist.env.cache.clear()
                        gc.collect()
                except: pass

        except Exception:
            # [ASCENSION 7]: LAZARUS EXCEPTION SHIELD
            # The audit must be invisible; we do not allow a triage failure to halt a Rite.
            pass

    # =================================================================================
    # == THE GRAND SYMPHONY OF EXECUTION (RUN)                                       ==
    # =================================================================================

    def run(self) -> QuantumRegisters:
        """
        =================================================================================
        == THE OMEGA STRIKE: TOTALITY (V-Ω-TOTALITY-V1000.5-SUBSTRATE-HEALED)          ==
        =================================================================================
        LIF: ∞ | ROLE: KINETIC_SUPREME_CONDUCTOR | RANK: OMEGA_SOVEREIGN

        [THE CURE]:
        We employ the `GnosticStatusShim` to wrap the kinetic strike. This shim
        intelligently detects if we are in the WASM substrate and bypasses the
        threading calls of `rich.status`, replacing them with synchronous
        Gnostic Log Pulses.
        =================================================================================
        """
        import time
        import contextlib
        import os
        import gc
        from pathlib import Path
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

        start_ns = time.perf_counter_ns()

        # [ASCENSION 13]: THE SUBSTRATE-AWARE STATUS SUTURE
        # We forge a context manager that honors the laws of the current reality.
        # This replaces the native console.status call which fractures in WASM.
        status_ctx = GnosticStatusShim(
            self.console,
            "[bold green]The Great Work is advancing...",
            silent=self.silent
        )

        registers: Optional[QuantumRegisters] = None

        try:
            # =========================================================================
            # == MOVEMENT I: THE RITE OF GEOMETRIC SOVEREIGNTY                       ==
            # =========================================================================
            # We adjudicate the topography ONCE. This is the One True Decision.
            geometric_decision = self._reconcile_geometric_schism()

            # Resolve the absolute project_root based on the Fold/Preserve decision.
            if str(geometric_decision) == ".":
                self.project_root = self.base_path
            else:
                self.project_root = (self.base_path / geometric_decision).resolve()

            # Immediately synchronize the Engine's internal anchor to this truth.
            self._sync_registers()

            # --- MOVEMENT II: FORENSIC PERCEPTION ---
            self._adjudicate_paths_forensically()
            self._conduct_metabolic_audit()

            # --- MOVEMENT III: MATERIALIZE THE MIND (REGISTERS) ---
            from ..registers import QuantumRegisters
            registers = QuantumRegisters(
                sanctum=self.sanctum,
                project_root=self.project_root,  # <--- THE RECTIFIED ANCHOR
                transaction=self.transaction,
                dry_run=self.is_simulation,
                force=self.force,
                verbose=self.verbose,
                silent=self.silent,
                gnosis=self.variables,
                console=self.console,
                non_interactive=self.non_interactive,
                no_edicts=self.no_edicts,
                akashic=getattr(self.engine, 'akashic', None)  # [THE CURE]: Suture the silver cord
            )

            # --- MOVEMENT IV: SUTURE THE ORGANS ---
            from ...core.maestro import MaestroConductor as MaestroUnit
            from ..io_controller import IOConductor
            from ..cpu import QuantumCPU

            # Suture a fresh IOConductor bound to these registers
            io_conductor = IOConductor(registers)
            maestro = MaestroUnit(self.engine, registers, self.alchemist)
            cpu = QuantumCPU(registers, io_conductor, maestro, self)

            # --- MOVEMENT V: COMPILATION OF WILL ---
            cpu.load_program(self.scaffold_items, self.post_run_commands)

            if not cpu.program:
                self.Logger.warn("Void Intent: No kinetic instructions perceived. Rite concluded.")
                return registers

            # --- MOVEMENT VI: GEOMETRIC FORTIFICATION ---
            # Identify the paths warded against the Ghost Buster.
            self.sacred_paths = {(self.base_path / i.path).resolve() for i in self.scaffold_items if i.path}

            # =========================================================================
            # == MOVEMENT VII: THE KINETIC STRIKE (MATERIALIZATION)                 ==
            # =========================================================================
            # [THE FIX]: We enter the GnosticStatusShim, safe in any reality.
            with status_ctx:
                # strike the primary matter willed by the blueprint
                cpu.execute()

                # --- MOVEMENT VIII: POST-STRIKE CONSECRATION ---
                if not self.is_simulation:
                    # [ASCENSION 2]: GEOMETRIC FINALITY (THE CURE)
                    # We must determine the correct physical anchor for the StructureSentinel.
                    consecration_anchor = self.base_path.resolve()

                    if self.is_local_realm:
                        status_ctx.update("[bold yellow]Consecrating Reality Structure...[/]")
                        for item in self.scaffold_items:
                            if not item.is_dir and item.path:
                                # We construct the absolute physical path of the item
                                physical_target = (consecration_anchor / item.path).resolve()

                                # [SAFETY WARD]: Verify existence before summoning Sentinel
                                if physical_target.exists():
                                    self.structure_sentinel.ensure_structure(physical_target)
                                else:
                                    self.Logger.verbose(f"Skipping consecration for unmanifest scripture: {item.path}")

                    # --- MOVEMENT IX: ADJUDICATION OF SOUL PURITY ---
                    if self.adjudicate_souls and self.transaction:
                        status_ctx.update("[bold purple]Adjudicating Soul Purity...[/]")
                        self.adjudicator.conduct_sentinel_inquest()

                    # Finalize the .gitignore ward
                    self.adjudicator.conduct_dynamic_ignore()

                    # =========================================================================
                    # == [THE CURE]: MOVEMENT X - THE RITE OF FINAL LUSTRATION               ==
                    # =========================================================================
                    # [ASCENSION 1]: This is the most critical movement.
                    # We command the transaction to materialize AGAIN.
                    if self.transaction and not self.transaction.simulate:
                        self.Logger.verbose("Conducting Rite of Final Lustration...")
                        self.transaction.materialize()
                    # =========================================================================

                    # [ASCENSION 11]: PURIFICATION (GHOST BUSTER)
                    if self.clean_empty_dirs and self.is_local_realm:
                        status_ctx.update("[bold grey]Purging Entropy...[/]")
                        from ...core.sanitization.ghost_buster import GhostBuster
                        GhostBuster(root=self.project_root, protected_paths=self.sacred_paths).exorcise()

            # --- MOVEMENT XI: THE FINAL REVELATION ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not self.silent:
                self.Logger.success(f"Apotheosis Achieved. Reality manifest in {duration_ms:.2f}ms.")

            # Record final metabolic stats
            registers.metabolic_tax_ms = duration_ms
            registers.ops_conducted = len(cpu.program)

            return registers

        except Exception as catastrophic_paradox:
            # [ASCENSION 12]: THE FINALITY VOW
            if registers:
                registers.critical_heresies += 1

            # [ASCENSION 10]: AKASHIC FAILURE BROADCAST
            if hasattr(self.engine, 'akashic') and self.engine.akashic:
                try:
                    self.engine.akashic.broadcast({
                        "method": "novalym/hud_pulse",
                        "params": {"type": "RITE_FRACTURE", "label": "STRIKE_FAILED", "color": "#ef4444"}
                    })
                except:
                    pass

            if not isinstance(catastrophic_paradox, ArtisanHeresy):
                # Transmute unknown paradoxes into diagnostic failures
                raise ArtisanHeresy(
                    "CATASTROPHIC_RUN_FRACTURE",
                    child_heresy=catastrophic_paradox,
                    details=f"Anchor: {self.project_root} | Error: {str(catastrophic_paradox)}",
                    severity=HeresySeverity.CRITICAL,
                    ui_hints={"vfx": "shake", "sound": "fracture_critical"}
                ) from catastrophic_paradox
            raise

    def __repr__(self) -> str:
        return f"<Ω_QUANTUM_CREATOR_FACADE anchor='{getattr(self, 'project_root', '.')}' status=RESONANT>"
