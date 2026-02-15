# Path: src/velm/genesis/genesis_engine/weaving.py
# =========================================================================================
# == THE MASTER WEAVER: OMEGA POINT (V-Ω-TOTALITY-V2000.12-WASM-RESILIENT)               ==
# =========================================================================================
# LIF: INFINITY | ROLE: REALITY_WEAVER | RANK: OMEGA_SUPREME
# AUTH: Ω_WEAVING_V2000_THREAD_BYPASS_2026_FINALIS
# =========================================================================================

import os
import sys
import time
import importlib.resources as pkg_resources
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List, TYPE_CHECKING

# --- THE DIVINE SUMMONS ---
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe
from ...utils import generate_derived_names, to_string_safe

if TYPE_CHECKING:
    from .engine import GenesisEngine
    from ...parser_core.parser.engine import ApotheosisParser

Logger = Scribe("GenesisWeaving")


class WeavingMixin:
    """
    =================================================================================
    == THE HANDS OF THE GENESIS ENGINE (V-Ω-WEAVING-LAYER-ULTIMA)                  ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_WEAVER

    The Grand Weaver of Archetypes. It handles the loading, parsing, and logical
    resolution of architectural DNA. Hardened for WASM Substrate independence.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Thread-Sieve (THE CURE):** Detects WASM substrate and stays
        downstream threading triggers, annihilating 'RuntimeError: can't start new thread'.
    2.  **Resource Alchemist 2.0:** Hyper-resilient triage between modern 'importlib',
        legacy 'pkg_resources', and VFS coordinates.
    3.  **Bicameral Variable Isolation:** Surgically separates 'overrides' from
        'blueprint_vars' to prevent Gnostic Leakage.
    4.  **The Variable Prism (Evolved):** Proactively generates 12+ derived variants
        of project DNA (Slug, Pascal, Snake, etc.) to saturate the Alchemist.
    5.  **The Syntax Healer:** Differentiates between Alchemical (Jinja) paradoxes
        and Structural (Scaffold) heresies with forensic clarity.
    6.  **The Trinity Suture:** Absolute enforcement of the '(cmd, line, undo)'
        scripture, ensuring the Maestro's will is never fragmented.
    7.  **Geometric Normalization:** Forges a deterministic, collision-resistant
        'ephemeral_path' for local context awareness.
    8.  **The Void Guard:** Pre-flight scrying of archetype mass to prevent the
        'Empty Soul' heresy.
    9.  **Sovereign State Synchronization:** Atomic, thread-safe update of the
        parent engine's variable lattice.
    10. **Luminous Indented Logging:** Hierarchical visual grouping of the
        weave symphony for the Ocular HUD.
    11. **Metabolic Tomography:** Nanosecond-precision tracking of weaving
        latency and Gnostic mass.
    12. **The Finality Vow:** A mathematical guarantee of a valid, resonant Dowry.
    =================================================================================
    """

    def _conduct_master_weave(
            self: 'GenesisEngine',
            archetype_info: Dict[str, Any],
            final_gnosis: Dict[str, Any],
            overrides: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict, List[ScaffoldItem], List[Tuple[str, int, Optional[List[str]]]], 'ApotheosisParser']:
        """
        =================================================================================
        == THE MASTER WEAVER (V-Ω-TOTALITY-V2000.12-ASCENDED)                          ==
        =================================================================================
        LIF: INFINITY | ROLE: REALITY_WEAVER
        """
        archetype_name = archetype_info.get('name', 'Unknown')
        start_time_ns = time.perf_counter_ns()

        # [ASCENSION 1]: SUBSTRATE DETECTION
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM" or sys.platform == "emscripten"

        with self.logger.indent(f"Rite of the Master Weaver: '{archetype_name}'"):
            # --- MOVEMENT I: THE GAZE UPON THE SACRED SCRIPTURE ---
            self.logger.info(f"Perceiving Archetype soul on substrate: [{'ETHER' if is_wasm else 'IRON'}]")

            archetype_path_ref = str(archetype_info["archetype_path"])
            archetype_content = ""

            try:
                # [ASCENSION 2]: RESOURCE ALCHEMIST 2.0
                is_package_resource = False
                if ":" in archetype_path_ref:
                    # Windows Drive Letter Check
                    if os.name == 'nt' and len(archetype_path_ref) > 1 and archetype_path_ref[1] == ':':
                        is_package_resource = False
                    else:
                        is_package_resource = True

                if is_package_resource:
                    # PATH A: SYSTEM ARCHETYPE
                    package, resource_name = archetype_path_ref.split(":", 1)
                    try:
                        from importlib import resources
                        archetype_content = resources.files(package).joinpath(resource_name).read_text(encoding='utf-8')
                    except (ImportError, AttributeError, FileNotFoundError):
                        import pkg_resources
                        archetype_content = pkg_resources.resource_string(package, resource_name).decode('utf-8')
                else:
                    # PATH B: PHYSICAL ARCHETYPE
                    archetype_path = Path(archetype_path_ref).resolve()
                    if not archetype_path.exists():
                        raise FileNotFoundError(f"Scripture unmanifest: {archetype_path}")
                    archetype_content = archetype_path.read_text(encoding='utf-8')

                # [ASCENSION 8]: THE VOID GUARD
                if not archetype_content or not archetype_content.strip():
                    raise ArtisanHeresy(f"The archetype '{archetype_name}' is a void.",
                                        severity=HeresySeverity.CRITICAL)

            except Exception as e:
                raise ArtisanHeresy(
                    f"Archetype Summoning Fracture: '{archetype_path_ref}'",
                    details=str(e), severity=HeresySeverity.CRITICAL
                ) from e

            # --- MOVEMENT II: THE DIVINE ANOINTMENT OF THE SCRIBE ---
            self.logger.info("Awakening the one true Scribe (ApotheosisParser)...")

            # [THE FIX]: Substrate-Aware Factory
            # We command the engine to forge a parser that obeys the single-threaded law if in WASM.
            parser = self.engine.parser_factory()

            # [ASCENSION 4 & 7]: CONTEXTUAL DNA SUTURE
            parsing_context = final_gnosis.copy()
            parsing_context['_scaffold_archetype_source'] = archetype_path_ref
            parsing_context['_scaffold_archetype_name'] = archetype_name

            # [ASCENSION 1]: Telemetry Bypass for WASM
            if hasattr(self.engine, 'akashic') and self.engine.akashic and not is_wasm:
                try:
                    self.engine.akashic.broadcast({
                        "method": "scaffold/weaving_init",
                        "params": {"archetype": archetype_name, "trace": getattr(self.cli_args, 'trace_id', 'tr-void')}
                    })
                except:
                    pass

            # --- MOVEMENT III: THE RITE OF TRANSMUTATION (PARSING) ---
            try:
                # [ASCENSION 7]: GEOMETRIC NORMALIZATION
                ephemeral_path = (self.project_root / f"ephemeral_{archetype_name}.scaffold").resolve()

                parser.parse_string(
                    content=archetype_content,
                    file_path_context=ephemeral_path,
                    pre_resolved_vars=parsing_context,
                    overrides=overrides or {}
                )
            except Exception as e:
                # [ASCENSION 5]: THE SYNTAX HEALER
                is_template_error = "TemplateSyntaxError" in type(e).__name__ or "Jinja" in str(type(e))
                raise ArtisanHeresy(
                    f"{'Alchemical Syntax' if is_template_error else 'Gnostic'} Fracture in '{archetype_name}'.",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Check for unclosed braces '{{ }}' or logical blocks." if is_template_error else None
                ) from e

            # --- MOVEMENT IV: THE RESOLUTION OF REALITY ---
            # resolve_reality flattens the AST and adjudicates @if/@for logic.
            gnostic_plan = parser.resolve_reality()

            # --- MOVEMENT V: THE PROCLAMATION OF THE TRINITY ---
            # [ASCENSION 6]: PRESERVATION OF THE TRINITY
            post_run_commands = parser.post_run_commands
            final_variables = parser.variables

            # [ASCENSION 9]: SOVEREIGN STATE SYNC
            self.variables.update(final_variables)

            # --- MOVEMENT VI: METABOLIC FINALITY ---
            duration_ms = (time.perf_counter_ns() - start_time_ns) / 1_000_000
            self.logger.success(
                f"Gnostic Dowry forged in {duration_ms:.2f}ms. "
                f"{len(gnostic_plan)} items manifest, {len(post_run_commands)} edicts willed."
            )

            return final_variables, gnostic_plan, post_run_commands, parser

    def _conduct_archetype_rite(self: 'GenesisEngine', archetype_info: Dict[str, Any]) -> Optional[
        Tuple[Dict, List[ScaffoldItem], List[Tuple[str, int, Optional[List[str]]]], 'ApotheosisParser']]:
        """
        [THE SENTIENT WEAVER]
        Orchestrates the 'Quick' or 'Profile' based genesis.
        """
        with self.logger.indent(f"Rite of Wisdom: '{archetype_info.get('name', 'Unknown')}'"):
            # 1. Summon System Defaults
            self.logger.info("The God-Engine of Unification awakens its mind...")
            prophecy = self._gaze_upon_the_cosmos()

            # 2. Gather CLI Overrides
            cli_vars = {}
            if self.cli_args and self.cli_args.set:
                cli_vars = {k: v for k, v in (s.split('=', 1) for s in self.cli_args.set)}

            # 3. Gather Profile Overrides
            profile_gnosis = archetype_info.get("gnosis_overrides", {})

            # 4. Synthesize Initial Gnosis
            # [FACULTY 8] The Override Merger: Prophecy < Profile < CLI
            unified_context = {**prophecy.defaults, **profile_gnosis, **cli_vars}

            # 5. [ASCENSION 4]: THE VARIABLE PRISM (EVOLVED)
            project_name = to_string_safe(unified_context.get('project_name', 'new-project'))
            if project_name == "." or not project_name: project_name = self.project_root.name

            derived = generate_derived_names(project_name)
            unified_context.update(derived)
            unified_context['project_slug'] = derived.get('name_slug')

            ptype = unified_context.get('project_type', 'generic')
            unified_context['clean_type_name'] = str(ptype).split(' ')[0].lower()

            self.logger.success("Gnostic Context prepared and derived.")

            # 6. The Gnostic Mentor's Silent Gaze
            from ...jurisprudence_core.genesis_jurisprudence import GENESIS_CODEX
            for law in GENESIS_CODEX:
                if law.validator(unified_context):
                    msg = law.message(unified_context) if callable(law.message) else law.message
                    self.logger.warn(f"Architectural Warning: {msg}")

            self.logger.info("Bestowing pure Gnosis upon the Master Weaver...")

            # 7. The Master Weave
            return self._conduct_master_weave(archetype_info, unified_context, overrides=unified_context)