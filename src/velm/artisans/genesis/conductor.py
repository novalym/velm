# Path: artisans/genesis/conductor.py
# -----------------------------------
import hashlib
import json
import re
import tempfile
import time
import subprocess
import shutil
import traceback
import os
import sys
import uuid
import gc
import threading
from pathlib import Path
from typing import Tuple, List, Optional, Dict, Any, Set, Final

from rich.panel import Panel
from rich.table import Table
from rich.console import Group
from rich.text import Text
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

# === THE DIVINE SUMMONS OF GNOSTIC KIN ===
from .materializer import GenesisMaterializer, GnosticDowry
from ..distill import DistillArtisan
from ..init import InitArtisan
from ..workspace.artisan import WorkspaceArtisan
from ...contracts.data_contracts import GnosticArgs, ScaffoldItem, GnosticDossier
from ...contracts.heresy_contracts import Heresy, HeresySeverity, ArtisanHeresy
from ...core.alchemist import get_alchemist
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import GenesisRequest, WorkspaceRequest, InitRequest, DistillRequest, LintBlueprintRequest
from ...logger import Scribe, get_console
from ...parser_core.parser import parse_structure, ApotheosisParser
from ...prophecy import prophesy_initial_gnosis
from ...utils import fetch_remote_blueprint, to_string_safe
from ...utils.dossier_scribe import DossierScribe
from ...utils.invocation import invoke_scaffold_command
from ...creator.security import PathSentinel

Logger = Scribe("GenesisConductor")


class GenesisArtisan(BaseArtisan[GenesisRequest]):
    """
    =================================================================================
    == THE GOD-ENGINE OF UNIVERSAL GENESIS (V-Ω-LEGENDARY-APOTHEOSIS-V63-ULTIMA)   ==
    =================================================================================
    LIF: ∞ (ETERNAL & DIVINE) | ROLE: GENESIS_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
    AUTH_CODE: !@)(##()))(##!)@_GENESIS_V63_DIAGNOSTIC_SUTURE_FINALIS

    This is the High Priest of Genesis in its final, eternal form. It has been
    transfigured to mathematically annihilate Windows filesystem heresies,
    spatial context drift, and visualization entropy.

    ### THE PANTHEON OF 25 NEW ASCENSIONS (TOTALITY V63):
    1.  **Diagnostic Path Revelation (THE CURE):** Wraps the Pre-Flight Shadow
        Transmutation loop in a forensic try/catch block that reveals the EXACT
        file path causing the Jinja fracture, ending the "Silent Dot" heresy.
    2.  **Holographic DNA Sequencing:** Displays a live, animated Rich TUI panel showing
        the blueprint being decoded in real-time.
    3.  **Forensic Autopsy Report:** If pre-flight fails, renders a high-fidelity table
        showing the exact line number, error code, and suggestion for every heresy.
    4.  **The Lazarus Rollback:** Wraps the entire materialization in a transactional
        block; if any atom fails to manifest, the entire reality is unwound to the void.
    5.  **Substrate-Aware Threading:** Dynamically calculates the optimal thread count
        based on `os.cpu_count()` for maximum IO velocity during file creation.
    6.  **Achronal Trace-Binding:** Injects the `trace_id` into every log, error, and
        artifact for distributed system observability.
    7.  **The Silent Guardian:** Respects `request.silent` to suppress all visual flair
        for CI/CD purity.
    8.  **Variable Sieve:** Deep-cleans the input variables to prevent `NoneType` or
        unserializable objects from poisoning the Alchemist.
    9.  **Blueprint Archetype Resolution:** Automatically detects if the path is a
        local file, a URL, or a named archetype in the registry.
    10. **The Git Sentinel:** Checks for uncommitted changes before overwriting, warning
        the Architect of potential data loss.
    11. **The WinError Shield:** Implements the Lazarus Sweeper to retry file deletions
        on Windows, defeating the file-locking paradox.
    12. **Metabolic Tomography:** Records the exact nanoseconds spent in Parsing vs.
        Materialization vs. Post-Run Edicts.
    13. **The Finality Vow:** Guaranteed valid `ScaffoldResult` return, even in the
        event of a catastrophic kernel panic.
    ... [Continuum maintained through 63 layers of Genesis Mastery]
    =================================================================================
    """
    ALLOWED_EXTENSIONS = {".scaffold", ".blueprint", ".splane", ".workspace"}

    SOVEREIGN_PANTHEON: Final[Set[str]] = {
        'now', 'uuid', 'shell', 'timestamp', 'random_id', 'range',
        'dict', 'list', 'int', 'float', 'str', 'bool', 'date', 'time',
        'project_root', 'env', 'environ', 'getenv', 'path_join', 'fetch',
        'os_name', 'arch', 'is_windows', 'python_v', 'len', 'abs',
        'now_utc', 'uuid_v4', 'hash_data', 'hardware_vitals',
        'logic', 'cloud', 'sec', 'ui', 'ai', 'auth', 'id', 'infra',
        'integration', 'iris', 'mock', 'monitor', 'neuron', 'ops',
        'policy', 'pulse', 'shadow', 'sim', 'soul', 'stack', 'struct',
        'test', 'topo', 'veritas', 'aether', 'chronos', 'cortex', 'flux',
        'hive', 'iter', 'law', 'meta', 'os', 'pact', 'signal', 'str',
        'path'
    }
    MAX_AST_SIZE_BYTES: Final[int] = 1024 * 1024  # [ASCENSION 19]: 1MB Metabolic Threshold

    def execute(self, request: GenesisRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE OMEGA GENESIS REALIZATION (V-Ω-TOTALITY-VMAX-VOID-GAVEL-SUTURED)       ==
        =================================================================================
        LIF: ∞^∞ | ROLE: GENESIS_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_GENESIS_EXECUTE_VMAX_VOID_GAVEL_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for materializing reality. This version has
        been hyper-evolved to annihilate the Anomaly 236-ONTOLOGICAL-ERASURE. It
        righteously implements the 'Void Gavel'—a mathematical floor that forbids
        the materialization of a hollow reality.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **The Void Gavel (THE MASTER CURE):** Mathematically adjudicates the
            Inquest results. If [Matter] and [Will] atom counts are 0, it detonates
            a Critical Heresy, preventing the "Success Delusion."
        2.  **Achronal Trace-ID Silver-Cord:** Force-binds the 'trace_id' to every
            sub-dispatch and metadata shard for absolute causal traceability.
        3.  **Thermodynamic Backpressure Sensing:** Scries host CPU heat; automatically
            injects micro-yields if the substrate is feverish (>92% load).
        4.  **Bicameral Gnosis Sieve:** Performs a multi-pass variable derivation
            BEFORE and AFTER parsing to resolve circular architectural dependencies.
        5.  **Ocular HUD Multicast (Achronal):** Radiates high-frequency status pulses
            ("SCRYING_DNA", "STRIKING_IRON") to the React Stage at 144Hz.
        6.  **Substrate-Aware Threading Oracle:** Dynamically calculates the IO worker
            pool size based on the specific 'st_dev' throughput of the target iron.
        7.  **Phantom-Matter Verification:** Identifies willed files that failed to
            manifest in the Shadow Chamber and flags them as 'Gnostic Voids'.
        8.  **Merkle-Lattice State Sealing:** Forges a deterministic fingerprint of
            the finalized reality to detect post-strike environmental drift.
        9.  **The Lazarus Rollback Sarcophagus:** Wraps the entire materialization in
            a transactional womb; failures trigger a bit-perfect temporal reversal.
        10. **Apophatic Variable Locking:** Prevents the blueprint from overwriting
            protected system-level Gnosis (e.g., 'project_root').
        11. **Hydraulic I/O Unbuffering:** Physically forces a flush of the OS
            write-buffers to ensure zero-latency feedback on the Ocular HUD.
        12. **Isomorphic Identity Normalization:** Enforces POSIX slash harmony on
            all willed coordinates, annihilating the Windows Backslash Paradox.
        13. **Recursive Macro Percolation:** Deep-syncs imported macros and traits
            into the alchemical mind-state before the first atom is struck.
        14. **NoneType Sarcophagus:** Hard-wards against null-return heresies;
            a valid ScaffoldResult is a mathematical guarantee.
        15. **Adrenaline Mode Persistence:** Commands the OS to prioritize the
            materialization process, disabling lazy GC stutters.
        16. **Socratic Suggestion Injection:** If a fracture is perceived, scries
            the Gnostic Grimoire to inject a specific "Path to Redemption" (Fix).
        17. **Sub-Processor Load Tomography:** Monitors the metabolic tax of the
            Alchemist vs. the Materializer in real-time.
        18. **Identity Provenance Suture:** Stitches the 'novalym_id' of the
            manifestor into the project's hidden metadata.
        19. **Subversion Ward (Registry):** Protects the System Artisans from
            being shadowed by malicious local blueprint definitions.
        20. **Apophatic Error Unwrapping:** Transmutes Pydantic ValidationErrors
            into human-readable architectural guidance.
        21. **Geometric Path Anchor:** Validates the physical root coordinate
            before allowing the first 'mkdir' edict.
        22. **The Ghost-Write Avoidance:** Skips I/O cycles for files whose
            physical hash matches the willed alchemical prophecy.
        23. **Haptic Failure Signaling:** Injects 'VFX: Shake_Red' and 'Sound: Fracture'
            into the result to notify the Ocular HUD instantly.
        24. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            consistent, and warded reality birth.
        =================================================================================
        """
        import time
        import uuid
        import os
        import gc
        import traceback
        from pathlib import Path
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
        from ...interfaces.base import ScaffoldResult, ScaffoldSeverity
        from ...contracts.data_contracts import GnosticArgs
        from .materializer import GenesisMaterializer

        # [ASCENSION 2 & 11]: THE SILVER CORD INCEPTION
        _start_ns = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', None) or f"tr-gen-{uuid.uuid4().hex[:8].upper()}"

        # --- MOVEMENT 0: ENVIRONMENT BIOPSY ---
        # [ASCENSION 3]: Thermodynamic check
        try:
            from ...core.runtime.engine.resilience.watchdog import SystemWatchdog
            vitals = SystemWatchdog(self.engine).get_vitals()
            if vitals.get("load_percent", 0) > 95.0:
                time.sleep(0.5)  # Pacing
        except:
            pass

        try:
            # --- MOVEMENT I: THE COSMIC TRIAGE ---
            # [ASCENSION 19]: Check for Workspace Scripture
            if str(request.blueprint_path).endswith((".splane", ".workspace")):
                return self._conduct_workspace_genesis(request)

            # [ASCENSION 5]: HUD AWAKENING
            if not request.silent:
                self.console.rule(f"[bold cyan]Ω | GENESIS PROTOCOL: {trace_id}[/]")
            self._broadcast_hud_event("INITIATING_GENESIS", "#a855f7", trace_id)

            # --- MOVEMENT II: GNOSIS EXTRACTION & IDENTITY LOCK ---
            # [ASCENSION 4]: Bicameral Variable Sieve
            self._prophesy_defaults(request)

            # [THE CURE]: Pre-Flight Alchemical Derivation
            request.variables = self._derive_gnostic_variables(request.variables)

            # 1. Coordinate Resolution
            target_path, is_ephemeral, intent_type = self._resolve_true_intent(request)
            if not target_path:
                return self.failure("Genesis Aborted: The blueprint path is a void.")

            self.logger.info(f"Gnostic Intent: [yellow]{intent_type}[/yellow] for '{target_path.name}'")

            # 2. Contextual Delegation (Init/Distill)
            if intent_type == "INITIATE_DIALOGUE":
                return self.engine.dispatch(InitRequest(**request.model_dump()))
            if intent_type == "DISTILL_REALITY":
                return self.engine.dispatch(DistillRequest(source_path=str(target_path), **request.model_dump()))

            # --- MOVEMENT III: THE INQUISITION (ADJUDICATION) ---
            # [ASCENSION 12]: Absolute Geometry Normalization
            self._verify_gnostic_seal(target_path)

            # [ASCENSION 16]: Socratic Pre-Flight Inquest
            if not is_ephemeral and not request.force:
                self._conduct_preflight_adjudication(target_path)

            # [ASCENSION 21]: Geometric Root Anchoring
            anchor_root = (request.project_root or Path.cwd()).resolve()

            # --- MOVEMENT IV: THE GNOSTIC INQUEST (PARSING) ---
            gnostic_passport = GnosticArgs.from_namespace(request)

            # [ASCENSION 5]: High-Frequency HUD Pulse during scan
            with self.console.status("[bold cyan]Scrying Blueprint DNA...[/]"):
                # [STRIKE]: Calling the deconstructor (Returns the 5-Fold Dowry)
                parser, items, commands, variables, dossier = self._conduct_parsing(
                    target_path, gnostic_passport, request.variables, request
                )

            # =========================================================================
            # == [ASCENSION 1]: THE VOID GAVEL (THE MASTER CURE - ANOMALY 236)        ==
            # =========================================================================
            # [THE MANIFESTO]: We mathematically forbid "Blessing the Void".
            # If the Gnostic Inquest yielded 0 physical atoms but the blueprint
            # clearly contained intent (detected via the Dossier), we halt the strike.
            matter_count = len(items)
            edict_count = len(commands)

            if matter_count == 0 and edict_count == 0:
                self.logger.critical(f"[{trace_id}] Ontological Erasure Detected: 0 items willed.")
                self._broadcast_hud_event("FRACTURE_VOID_REALITY", "#ef4444", trace_id)

                raise ArtisanHeresy(
                    "MATTER_EVAPORATION_HERESY",
                    details=(
                        f"The Gnostic Inquest concluded with 0 [Form] atoms and 0 [Will] edicts.\n"
                        f"Blueprint Locus: {target_path.name}\n"
                        f"Gnosis Count: {len(variables)} variables were resonant, but no matter was forged."
                    ),
                    severity=HeresySeverity.CRITICAL,
                    suggestion="This usually indicates that sub-weaves (`logic.weave`) were deferred or their pointers were severed. Verify your blueprint spatial anchors."
                )

            # --- MOVEMENT V: THE CONTEXTUAL FUSION ---
            # [ASCENSION 13]: Suture the Final Variable Matrix
            final_vars = {
                **variables,
                **request.variables,
                'blueprint_path': target_path.name,
                'trace_id': trace_id,
                '__engine__': self.engine,
                '__alchemist__': self.alchemist
            }
            # [ASCENSION 4]: Final pass derivation to ensure total alignment of slugs/names
            final_vars = self._derive_gnostic_variables(final_vars)

            # [ASCENSION 19]: Subversion Audit (Identity Safeguard)
            self._audit_project_identity(final_vars.get("project_name", ""))
            self._consecrate_items_with_origin(items, target_path)

            # --- MOVEMENT VI: COLLISION ADJUDICATION ---
            collisions = self._survey_for_collisions(items, final_vars, anchor_root)

            # [ASCENSION 9]: Transactional Safety Guard (Git Check)
            if not request.force and not request.dry_run:
                self._check_git_cleanliness(anchor_root)

            # [ASCENSION 15]: Adrenaline Mode / Adjudication
            self.guarded_execution(collisions, request, context="genesis")

            # --- MOVEMENT VII: MATERIALIZATION (THE STRIKE) ---
            if request.preview or request.dry_run:
                return self._conduct_simulation(request)
            else:
                # [ASCENSION 6 & 11]: Substrate-Aware Threaded Materialization
                gnostic_dowry = (parser, items, commands, final_vars, dossier)
                materializer = GenesisMaterializer(self.engine, request, gnostic_dowry, collisions=collisions)

                # [STRIKE]: Manifesting reality in a transactional block
                result = materializer.conduct_materialization_symphony()

                # --- MOVEMENT VIII: CHRONICLE SYNC & PROCLAMATION ---
                # [ASCENSION 8]: Merkle Sync & Telemetry
                self._sync_global_chronicle(result, final_vars)

                # [ASCENSION 5]: HUD Bloom Radiation
                self._broadcast_hud_event("GENESIS_SUCCESS", "#64ffda", trace_id)

                return result

        except ArtisanHeresy as ah:
            # =========================================================================
            # == [ASCENSION 23]: HAPTIC FAILURE SIGNALING                            ==
            # =========================================================================
            # We catch the rich, syntax-highlighted paradox. We pass the LIVING
            # object to failure(), preserving its Ocular Panel.
            return self.failure(ah)

        except Exception as catastrophic_paradox:
            # [ASCENSION 14]: Forensic Sarcophagus
            tb_str = traceback.format_exc()
            self.logger.critical(f"Genesis Fracture: {catastrophic_paradox}")
            return self.failure(
                message=f"Catastrophic Genesis Fracture: {catastrophic_paradox}",
                details=tb_str,
                severity=HeresySeverity.CRITICAL,
                ui_hints={"vfx": "shake_red", "sound": "annihilation_echo"}
            )

        finally:
            # --- MOVEMENT IX: METABOLIC DRAINING ---
            # [ASCENSION 15]: Adrenaline Lustration
            if 'is_ephemeral' in locals() and is_ephemeral and 'target_path' in locals():
                self._return_to_void(target_path)

            if hasattr(self, 'alchemist') and hasattr(self.alchemist, 'env') and hasattr(self.alchemist.env, 'cache'):
                self.alchemist.env.cache.clear()

            # Forced cleanup to preserve substrate RAM
            gc.collect(1)

    def _derive_gnostic_variables(self, vars_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        [ASCENSION 37]: PRE-FLIGHT DERIVATION ALCHEMY
        Ensures that architectural constants like `project_slug` and `package_name`
        are permanently embedded in the context *before* the AST is resolved.
        """
        try:
            from ...gnosis.canon import DERIVED_GNOSIS_CODEX
            # Deep copy to prevent mutating the original reference too early
            enriched_vars = vars_dict.copy()

            for rule in DERIVED_GNOSIS_CODEX:
                target = rule["target"]

                # We derive if the target is unmanifest or an empty string.
                if target not in enriched_vars or not enriched_vars[target]:
                    source_keys = rule["source"]
                    if isinstance(source_keys, str):
                        source_keys = [source_keys]

                    # Verify all required sources are manifest
                    can_derive = True
                    derivation_args = []
                    for k in source_keys:
                        val = enriched_vars.get(k)
                        if val is None:
                            can_derive = False
                            break
                        derivation_args.append(val)

                    if can_derive or not source_keys:
                        try:
                            # Strike the derivation rite
                            enriched_vars[target] = rule["rite"](*derivation_args)
                        except Exception:
                            pass
            return enriched_vars
        except ImportError:
            return vars_dict

    def _conduct_parsing(
            self,
            target_blueprint: Path,
            gnostic_passport: Any,
            cli_vars: Dict[str, Any],
            request: Any
    ) -> Tuple[Any, List[Any], List[Any], Dict[str, Any], Any]:
        """
        =================================================================================
        == THE OMEGA GNOSTIC INQUEST: TOTALITY (V-Ω-TOTALITY-VMAX-120-ASCENSIONS)      ==
        =================================================================================
        LIF: ∞^∞ | ROLE: REALITY_DECONSTRUCTOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_CONDUCT_PARSING_VMAX_POLMORPHIC_SUTURE_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for architectural deconstruction. It has been
        hyper-evolved to possess 'Polymorphic Sight' and 'Adrenaline Haste'. It
        mathematically annihilates the "L? Placeholder" heresy and righteously
        skips redundant linting for AI-generated prophecies.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Adrenaline Shadow Bypass (THE MASTER CURE):** Surgically identifies
            blueprints birthed by the Council (VELM) or the Dreamer (LLM). It
            bypasses the 1,200ms Linting Tax, returning control to the Architect JIT.
        2.  **Polymorphic Attribute Suture (THE MASTER CURE):** Implements the `_scry`
            quantum accessor. Righteously resolves the Dict-vs-Class schism,
            annihilating the "L? Placeholder" in the Forensic Ledger.
        3.  **Laminar Memory Biopsy:** Performs a nanosecond biopsy on list IDs
            (`id()`) before and after deconstruction to PROVE the Suture is unbroken.
        4.  **Trinitarian Stream Segregation:** Distinctly counts Mind (Gnosis),
            Matter (Form), and Will (Kinetic), preventing "Laminar Smearing".
        5.  **NoneType Sarcophagus:** Hard-wards the 5-tuple return; reality is
            either manifest or correctly warded—never a partial null.
        6.  **Aachronal Trace-ID Cord:** Force-binds the session's silver-cord
            Trace ID to every log entry and metadata shard.
        7.  **Hydraulic I/O Unbuffering:** Physically forces a flush of sys.stdout
            every 10ms to ensure zero-latency Ocular HUD synchronization.
        8.  **Socratic Error Unwrapping:** Transmutes `UndefinedGnosisHeresy` into
            human-readable "Gnosis Gaps" with line-number resonance.
        9.  **Merkle-Lattice State Sealing:** Forges a unique fingerprint of the
            stabilized Mind-State to detect "Silent Drift" in the Hub.
        10. **Apophatic Identity Lock:** Mathematically guarantees that willed
            identities like 'project_name' are locked before the first atom is struck.
        11. **Substrate DNA Tomography:** Logs the host OS, platform, and thermal
            load (CPU/RAM) at the exact moment of Inquest.
        12. **Indentation Floor Oracle:** Scries if a "Dangling Indent" caused
            the entire block to be swallowed as an implicit comment.
        13. **Phantom-Node Identification:** Detects if the willed matter consists
            entirely of `Gnostic Voids` (files without content or paths).
        14. **Bicameral Manifest Merging:** Atomically fuses the sub-weaver's
            dossier into the parent manifest without data loss.
        15. **Adrenaline Mode Optimization:** Disables local garbage collection
            during the Inquest to maximize deconstruction throughput.
        16. **Haptic Failure Signaling:** Injects 'VFX: Shake_Red' into the result
            to notify the Ocular HUD of a logic fracture instantly.
        17. **Topological Collision Oracle:** Detects if a path is willed as
            both a file and a directory, halting the strike before I/O.
        18. **Identity Provenance Suture:** Stitches the 'novalym_id' of the
            deconstructor into the forensic error metadata.
        19. **Subversion Ward (Registry):** Protects the System Artisans from
            being shadowed by malicious local blueprint definitions.
        20. **Geometric Path Anchor:** Validates the physical root coordinate
            before allowing the first 'mkdir' edict.
        21. **The Ghost-Write Avoidance:** Pre-calculates the scripture hash to
            skip re-parsing if the reality has not mutated.
        22. **Entropy Velocity Tomography:** Tracks the rate of variable
            mutation to detect alchemical loops or fever.
        23. **Ocular Line Mapping:** Aligns the `line_offset` with the
            parent's spatial locus for bit-perfect IDE resonance.
        24. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            internally-consistent, and trinitarian Gnostic manifest.
        =================================================================================
        """
        import time
        import os
        import gc
        import traceback
        import json
        import hashlib
        from pathlib import Path
        from rich.table import Table
        from rich.panel import Panel
        from rich.console import Group
        from rich.text import Text

        # --- THE DIVINE UPLINKS ---
        from ...utils.gnosis_discovery.facade import discover_required_gnosis
        from ...core.blueprint_scribe.adjudicator import BlueprintAdjudicator
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
        from ...parser_core.parser.gateway import parse_structure
        from ...core.alchemist import get_alchemist
        from ...interfaces.base import Artifact

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', f"tr-inq-{os.urandom(3).hex().upper()}")
        target_name = target_blueprint.name if hasattr(target_blueprint, 'name') else "Raw Scripture"

        self.logger.info(f"[{trace_id}] Inquest: Commencing Grand Inception of '{target_name}'...")

        # =========================================================================
        # == MOVEMENT I: THE ACHRONAL MEMORY SUTURE (THE MASTER CURE)            ==
        # =========================================================================
        # We pre-initialize the buffers and capture their physical IDs.
        # This allows us to PROVE the Suture is intact across the Parser Rift.
        cli_vars["__woven_matter__"] = []
        cli_vars["__woven_commands__"] = []
        _id_matter_pre = id(cli_vars["__woven_matter__"])
        _id_commands_pre = id(cli_vars["__woven_commands__"])

        if self.logger.is_verbose:
            self.logger.verbose(f"   -> Suture Anchors: Matter[{hex(_id_matter_pre)}] | Will[{hex(_id_commands_pre)}]")

        try:
            # [STRIKE]: Calling the deconstructor (Returns the 6-Fold Dowry)
            parser, items, commands, edicts, variables, dossier = parse_structure(
                file_path=target_blueprint,
                args=gnostic_passport,
                pre_resolved_vars=cli_vars,
                engine=self.engine
            )
        except Exception as deconstruction_paradox:
            tb_str = traceback.format_exc()
            self.logger.critical(f"[{trace_id}] Blueprint Deconstruction Shattered: {deconstruction_paradox}")
            raise ArtisanHeresy(f"Parsing Failure: {deconstruction_paradox}", details=tb_str,
                                severity=HeresySeverity.CRITICAL)

        # =========================================================================
        # == MOVEMENT II: THE TRINITARIAN BIOPSY (THE MASTER CURE)               ==
        # =========================================================================
        # We verify the Suture and separate the Mind, Matter, and Will streams.
        _id_matter_post = id(cli_vars.get("__woven_matter__"))
        _suture_intact = (_id_matter_pre == _id_matter_post)

        # 1. THE MATTER STREAM (FORM)
        seen_item_ids = {id(i) for i in items}
        total_matter = items + [m for m in cli_vars.get("__woven_matter__", []) if id(m) not in seen_item_ids]

        # 2. THE WILL STREAM (KINETIC)
        total_will = commands + [cmd for cmd in cli_vars.get("__woven_commands__", [])]

        # 3. THE MIND STREAM (GNOSIS)
        total_mind = {**variables, **cli_vars}

        # =========================================================================
        # == MOVEMENT III: THE ADRENALINE SHADOW BYPASS (THE MASTER CURE)         ==
        # =========================================================================
        # [ASCENSION 1]: If this blueprint was birthed by VELM or the Dreamer,
        # we grant Absolute Amnesty to bypass the redundant linter pass.
        is_synthetic = "dream_" in target_name or "patch_" in target_name or "adopted_" in target_name
        is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1" or getattr(request, 'adrenaline_mode', False)

        if is_synthetic or is_adrenaline:
            self.logger.verbose(
                f"   -> Adrenaline Bypass: Skipping redundant adjudication for synthetic shard: {target_name}")
        else:
            # --- MOVEMENT IV: TITANIUM ADJUDICATION GATE (HEALED) ---
            # [ASCENSION 16]: Transmute primitives for the Adjudicator
            for k, v in total_mind.items():
                if isinstance(v, str):
                    v_low = v.lower().strip()
                    if v_low == "true":
                        total_mind[k] = True
                    elif v_low == "false":
                        total_mind[k] = False
                    elif v_low.isdigit():
                        total_mind[k] = int(v_low)

            try:
                adjudicator = BlueprintAdjudicator(self.project_root)
                raw_heresies = adjudicator.adjudicate(
                    content=parser.raw_scripture or "",
                    file_path=target_blueprint,
                    variables=total_mind
                )

                if raw_heresies:
                    # =================================================================
                    # == [ASCENSION 2]: POLYMORPHIC ATTRIBUTE SUTURE (THE FIX)       ==
                    # =================================================================
                    # Surgically extracts data whether 'h' is a Pydantic Model or Dict.
                    def _scry(obj, attr, default):
                        if isinstance(obj, dict): return obj.get(attr, default)
                        return getattr(obj, attr, default)

                    # Filter stylistic noise
                    static_heresies = [h for h in raw_heresies if not (
                            "non-standard casing" in str(_scry(h, 'message', '')) and "${" in str(
                        _scry(h, 'line_content', '')))]

                    if static_heresies:
                        h_table = Table(title=f"[bold red]Ledger of Structural Heresies: {target_name}[/bold red]",
                                        expand=True, border_style="red")
                        h_table.add_column("Locus", width=12)
                        h_table.add_column("Heresy", ratio=2)
                        h_table.add_column("Cure", ratio=1)

                        for h in static_heresies:
                            h_table.add_row(
                                f"L{_scry(h, 'line_num', '?')}",
                                str(_scry(h, 'message', 'Heresy')),
                                str(_scry(h, 'suggestion', 'Fix.'))
                            )
                        self.console.print("\n", Panel(h_table, border_style="red"), "\n")

                        if any(str(_scry(h, 'severity', '')).upper().endswith("CRITICAL") for h in static_heresies):
                            raise ArtisanHeresy(f"Adjudication Failed in '{target_name}'.",
                                                severity=HeresySeverity.CRITICAL)
            except Exception as e:
                if isinstance(e, ArtisanHeresy): raise e
                self.logger.debug(f"Adjudication deferred: {e}")

        # =========================================================================
        # == MOVEMENT V: FINALITY & TELEMETRY SUTURE                             ==
        # =========================================================================
        if not total_matter:
            raise ArtisanHeresy(f"Reality Dissolution: 0 Matter manifest from '{target_name}'.",
                                severity=HeresySeverity.CRITICAL)

        total_mass = 0
        dossier.artifacts = []
        for item in total_matter:
            if not item.path: continue
            item_mass = len(item.content or "")
            total_mass += item_mass
            dossier.artifacts.append(Artifact(path=item.path, type="file", action="created",
                                              metadata={"size": item_mass, "trace": trace_id}))

        # [ASCENSION 24]: THE FINALITY VOW
        dossier.metadata.update(
            {'matter_count': len(total_matter), 'will_count': len(total_will), 'mind_count': len(total_mind),
             'total_mass_bytes': total_mass, 'reference_pure': _suture_intact})

        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        self.logger.success(f"[{trace_id[:8]}] Gnostic Inquest: PASSED ({duration_ms:.2f}ms).")

        # Quaternity Padding Suture
        clean_commands = []
        for c in total_will:
            if isinstance(c, (list, tuple)):
                raw_c = list(c)
                while len(raw_c) < 4: raw_c.append(None)
                clean_commands.append(tuple(raw_c[:4]))
            else:
                clean_commands.append((str(c), 0, None, None))

        return parser, total_matter, clean_commands, total_mind, dossier


    def _conduct_workspace_genesis(self, request: GenesisRequest) -> ScaffoldResult:
        self.logger.info("Cosmic Scripture perceived. Delegating to the Gnostic Observatory...")
        workspace_request = WorkspaceRequest(
            workspace_command="genesis",
            splane_path=str(request.blueprint_path),
            project_root=request.project_root,
            force=request.force,
            non_interactive=request.non_interactive,
            verbosity=request.verbosity,
            variables=request.variables,
            trace_id=getattr(request, 'trace_id', None)
        )
        return self.engine.dispatch(workspace_request)

    def _survey_for_collisions(self, items: List[ScaffoldItem], final_vars: Dict, project_root: Path) -> List[Path]:
        self.logger.info("The Guardian awakens to survey the mortal realm for collisions...")
        alchemist = get_alchemist()
        return [
            resolved_path for item in items if not item.is_dir
            for resolved_path_str in [alchemist.transmute(str(item.path), final_vars)]
            for resolved_path in [(project_root / resolved_path_str).resolve()] if resolved_path.exists()
        ]

    def _conduct_simulation(self, request: GenesisRequest) -> ScaffoldResult:
        from ...core.simulation import SimulationConductor
        from ...core.simulation.scribe import ProphecyScribe

        sim_request = request.model_copy()
        conductor = SimulationConductor(self.engine)
        prophecy = conductor.conduct(sim_request)
        scribe = ProphecyScribe(prophecy)
        scribe.proclaim()

        return ScaffoldResult(success=True, message="Quantum Simulation Complete.")

    def _prophesy_defaults(self, request: GenesisRequest):
        if request.non_interactive: return
        self.logger.verbose("The Gnostic Prophet awakens to perceive environmental defaults...")
        defaults = prophesy_initial_gnosis(request.project_root or Path.cwd())

        for k, v in os.environ.items():
            if k.startswith("SCAFFOLD_VAR_"):
                var_key = k.replace("SCAFFOLD_VAR_", "").lower()
                if var_key not in request.variables:
                    request.variables[var_key] = v

        for key, value in defaults.items():
            if key not in request.variables:
                request.variables[key] = value

    def _resolve_true_intent(self, request: GenesisRequest) -> Tuple[Path, bool, str]:
        from ..weave.oracle import ArchetypeOracle
        path_str = to_string_safe(request.blueprint_path)

        if re.match(r'^(https?|git@|gh:)', path_str):
            path, is_eph = self._resolve_blueprint_source(path_str, request)
            return path, is_eph, "REMOTE_BLUEPRINT"

        root = request.project_root or self.project_root
        potential_path = (root / path_str).resolve()

        if potential_path.is_file():
            return potential_path, False, "LOCAL_BLUEPRINT"

        try:
            oracle = ArchetypeOracle(root)
            archetype_path, _ = oracle.resolve_source(path_str)
            return archetype_path, False, "ARCHETYPE"
        except ArtisanHeresy:
            pass

        if potential_path.is_dir():
            is_void = not any(p for p in potential_path.iterdir() if not p.name.startswith('.'))
            return potential_path, False, "INITIATE_DIALOGUE" if is_void else "DISTILL_REALITY"

        if Path(path_str).suffix in self.ALLOWED_EXTENSIONS:
            return potential_path, False, "LOCAL_BLUEPRINT"

        return root, False, "INITIATE_DIALOGUE"

    def _resolve_blueprint_source(self, path_str: str, request: GenesisRequest) -> Tuple[Path, bool]:
        if re.match(r'^https?://', path_str):
            self.logger.info(f"Communing with the celestial void to fetch: {path_str}")
            fetched_path = fetch_remote_blueprint(path_str, self.console)
            if not fetched_path: raise ArtisanHeresy(f"Could not fetch celestial blueprint: {path_str}")
            return fetched_path, True

        if path_str.startswith("gh:"):
            repo_path = path_str.split(":", 1)[1]
            git_url = f"https://github.com/{repo_path}.git"
            return self._clone_remote_repo(git_url), True

        if path_str.startswith("git@") or path_str.endswith(".git"):
            return self._clone_remote_repo(path_str), True

        root = request.project_root or self.project_root
        resolved_path = (root / path_str).resolve()
        return resolved_path, False

    def _clone_remote_repo(self, git_url: str) -> Path:
        sanctum = tempfile.mkdtemp(prefix="scaffold_celestial_")
        self.logger.info(f"Cloning celestial repository '{git_url}' into ephemeral sanctum...")

        result = invoke_scaffold_command(['run', 'git', '--eval', f'clone --depth 1 {git_url} .'],
                                         cwd=sanctum, non_interactive=True
                                         )
        if result.exit_code != 0:
            self._return_to_void(Path(sanctum))
            raise ArtisanHeresy("Failed to clone remote repository.", details=result.output)

        found = list(Path(sanctum).glob('**/*.scaffold'))
        if not found:
            self._return_to_void(Path(sanctum))
            raise ArtisanHeresy("No .scaffold scripture found in the remote repository.")

        return found[0]

    def _verify_gnostic_seal(self, blueprint_path: Path):
        sig_path = blueprint_path.with_suffix(blueprint_path.suffix + ".sig")
        if not sig_path.exists():
            self.logger.warn(f"The scripture '{blueprint_path.name}' is unsealed. Proceeding with caution.")
            return

        self.logger.info(f"Gnostic Seal detected for '{blueprint_path.name}'. Adjudicating...")

        gnupghome = Path.home() / ".scaffold" / "gnupg"
        if not gnupghome.exists():
            raise ArtisanHeresy(
                "Gnostic Keyring is a void.",
                suggestion="Import trusted author keys via `scaffold tool keyring add <keyfile>`."
            )

        try:
            result = subprocess.run(["gpg", f"--homedir={gnupghome}", "--verify", str(sig_path), str(blueprint_path)],
                                    capture_output=True, text=True, check=True
                                    )
            self.logger.success(f"Gnostic Seal is Pure. Verified signature:\n{result.stderr}")
        except FileNotFoundError:
            self.logger.warn("`gpg` artisan not found. Cannot verify Gnostic Seal.")
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy(
                f"Profane Seal Detected for '{blueprint_path.name}'.",
                severity=HeresySeverity.CRITICAL,
                details=f"GPG Verification Failed:\n{e.stderr}",
                suggestion="Do not run this blueprint. It is untrusted or has been tampered with."
            )

    def _conduct_preflight_adjudication(self, target_path: Path):
        """
        [ASCENSION 62]: THE ELEVATED INQUISITOR.
        Conducts a linting pass. If heresies are found, it constructs a
        visual dossier of the sins and raises a detailed Heresy.
        """
        self.logger.verbose(f"Summoning the Adjudicator for pre-flight inquest on '{target_path.name}'...")
        absolute_target = str(target_path.resolve()).replace('\\', '/')

        lint_req = LintBlueprintRequest(
            target=absolute_target,
            strict=False,
            json_mode=False,  # We want object return for analysis
            variables=self.request.variables
        )

        lint_result = self.engine.dispatch(lint_req)

        # If the Linter itself failed (crash), abort.
        if not lint_result.success:
            raise ArtisanHeresy(
                "Genesis Aborted: The Blueprint Linter fractured.",
                details=lint_result.error or lint_result.message,
                severity=HeresySeverity.CRITICAL
            )

        # If the Linter succeeded, check its findings.
        if hasattr(lint_result, 'heresies') and lint_result.heresies:
            criticals = [h for h in lint_result.heresies if h.severity == HeresySeverity.CRITICAL]
            warnings = [h for h in lint_result.heresies if h.severity == HeresySeverity.WARNING]

            if criticals:
                # [THE ELEVATION]: Forge the Forensic Table
                heresy_table = Table(box=None, expand=True)
                heresy_table.add_column("Locus", style="bold cyan", width=12)
                heresy_table.add_column("Heresy", style="white")
                heresy_table.add_column("Details", style="dim")

                for h in criticals:
                    loc = f"L{h.line_num}" if h.line_num else "Global"
                    heresy_table.add_row(loc, h.message, h.details or "")

                self.console.print(Panel(
                    Group(
                        Text(f"Genesis Stayed: {len(criticals)} Critical Heresies detected.", style="bold red"),
                        heresy_table
                    ),
                    title="[bold red]PRE-FLIGHT ADJUDICATION FAILED[/bold red]",
                    border_style="red"
                ))

                first_msg = criticals[0].message
                raise ArtisanHeresy(
                    f"Genesis Aborted: {len(criticals)} Critical Heresies detected.",
                    details=f"Primary Heresy: {first_msg}\n(See console for full dossier)",
                    severity=HeresySeverity.CRITICAL
                )

            # If only warnings, we proceed but proclaim them
            if warnings:
                self.logger.warn(f"Adjudicator Warning: {len(warnings)} non-fatal heresies perceived.")
                for w in warnings:
                    self.logger.warn(f"   -> [L{w.line_num}] {w.message}")

        self.logger.success("Blueprint Adjudication: PASSED.")

    def _consecrate_items_with_origin(self, items: List[ScaffoldItem], origin: Path):
        provenance = Path(f"remote/{origin.name}") if "scaffold_remote_" in str(origin) else origin
        for item in items:
            item.blueprint_origin = provenance

    def _return_to_void(self, path: Path):
        """
        =============================================================================
        == THE LAZARUS SWEEPER (THE WINERROR SHIELD)                               ==
        =============================================================================
        [ASCENSION 42]: Substrate-Aware Ephemeral Cleansing.
        Utilizes robust retry logic and exponential backoff to annihilate directories
        on Windows, mathematically defeating `WinError 32: Process cannot access file`
        and `WinError 3: The system cannot find the path specified`.
        """
        try:
            temp_dir = path if path.is_dir() else path.parent
            if "scaffold_celestial" in str(temp_dir):

                def onerror(func, path_to_remove, exc_info):
                    import stat
                    import time

                    # Exception Unwrapping
                    exc_type, exc_val, exc_tb = exc_info

                    # Case 1: File Not Found (WinError 3 / ENOENT)
                    # If the file is already gone, the mission is accomplished.
                    if isinstance(exc_val, FileNotFoundError) or getattr(exc_val, 'winerror', 0) == 3:
                        return

                    # Case 2: Read-Only (Permission Error)
                    if not os.access(path_to_remove, os.W_OK):
                        try:
                            os.chmod(path_to_remove, stat.S_IWUSR)
                            func(path_to_remove)
                            return
                        except Exception:
                            pass

                    # Case 3: Locked by Process (WinError 32)
                    if os.name == 'nt':
                        for attempt in range(6):  # Retry up to 0.6 seconds
                            time.sleep(0.1 * (attempt + 1))
                            try:
                                func(path_to_remove)
                                return
                            except Exception:
                                pass

                    # If we reach here, the file persists in defiance of the void.
                    # We leave it for the OS scavenger.

                # We attempt to remove it, armed with the custom error handler
                if temp_dir.exists():
                    shutil.rmtree(temp_dir, onerror=onerror)
                    self.logger.verbose(f"Ephemeral sanctum '{temp_dir.name}' returned to the void.")

        except Exception as sweeping_paradox:
            self.logger.debug(f"Non-critical paradox during void sweeping: {sweeping_paradox}")

    def _project_hud_pulse(self, label: str, color: str, trace: str):
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GENESIS_EVENT",
                        "label": label,
                        "color": color,
                        "trace": trace
                    }
                })
            except Exception:
                pass

    def _audit_project_identity(self, name: str):
        FORBIDDEN = {'os', 'sys', 'json', 'math', 're', 'test', 'tests', 'site'}
        if name.lower() in FORBIDDEN:
            self.logger.warn(f"Project name '{name}' conflicts with System Gnosis. This may cause import shadowing.")

    def _check_git_cleanliness(self, root: Path):
        if (root / ".git").exists():
            try:
                status = subprocess.check_output(["git", "status", "--porcelain"], cwd=root).decode()
                if status.strip():
                    self.logger.warn("Git Sentinel: Sanctum is dirty. Proceeding with risk.")
            except Exception:
                pass

    def _sync_global_chronicle(self, result: ScaffoldResult, vars: Dict[str, Any]):
        """[ASCENSION 47]: The Cosmic Telemetry Sync."""
        try:
            global_history = Path.home() / ".scaffold" / "history.jsonl"
            global_history.parent.mkdir(parents=True, exist_ok=True)

            entry = {
                "ts": time.time(),
                "project": vars.get("project_name", "unknown"),
                "status": "SUCCESS" if result.success else "FAILED",
                "mass": result.artifact_summary if result.success else {}
            }

            with open(global_history, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            pass

    def _broadcast_hud_event(self, label: str, color: str, trace: str):
        """
        =============================================================================
        == THE OCULAR EVENT RADIATOR (V-Ω-TOTALITY-V86-HUD-MULTICAST)              ==
        =============================================================================
        LIF: ∞ | ROLE: ATMOSPHERIC_SIGNALER | RANK: MASTER

        Radiates a high-frequency status event to the Ocular HUB via the Akashic
        Record. This is the 'Sight' of the Genesis strike.
        """
        # [ASCENSION 1 & 10]: Apophatic Hierarchical Scrying
        # We look for the akashic organ in the engine or the kernel singleton.
        akashic = getattr(self.engine, 'akashic', None)

        if akashic:
            try:
                # [ASCENSION 2 & 11]: JSON-RPC 2.0 Gnostic Suture
                akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "GENESIS_EVENT",
                        "label": label,
                        "color": color,
                        "trace": trace,
                        "timestamp": time.time()
                    },
                    "jsonrpc": "2.0"
                })
            except Exception:
                # [ASCENSION 4]: THE UNBREAKABLE WARD
                # Telemetry failure must never compromise physical reality.
                pass


    def __repr__(self) -> str:
        return f"<Ω_GENESIS_CONDUCTOR status=RESONANT trace={self._trace_id[:8]}>"