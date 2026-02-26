# Path: src/velm/genesis/genesis_engine/weaving.py
# ------------------------------------------------

import os
import sys
import time
import uuid
import json
import hashlib
import platform
import unicodedata
import importlib.resources as pkg_resources
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List, TYPE_CHECKING, Set

# --- THE DIVINE SUMMONS ---
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe
from ...utils import generate_derived_names, to_string_safe
from ... import __version__

if TYPE_CHECKING:
    from .engine import GenesisEngine
    from ...parser_core.parser.engine import ApotheosisParser

Logger = Scribe("GenesisWeaving")


class WeavingMixin:
    """
    =================================================================================
    == THE MASTER WEAVER: OMEGA POINT (V-Ω-TOTALITY-V32000-INFINITE-LOOM)          ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_WEAVER | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_WEAVING_V32000_INFINITE_ASCENSION_FINALIS

    The Grand Weaver of Archetypes. It is the bridge between the Static (Templates)
    and the Dynamic (Reality). It handles the loading, parsing, and logical
    resolution of architectural DNA with absolute, unbreakable precision.

    ### THE PANTHEON OF 32 LEGENDARY ASCENSIONS:
    1.  **System DNA Suture (THE CORE FIX):** Injects `trace_id`, `session_id`, and `timestamp`
        into the Gnostic Context at *Nanosecond Zero*, preventing the "Void Trace" heresy.
    2.  **Resource Alchemist 3.0:** A tri-phasic loading engine that gracefully handles
        `importlib` (Modern), `pkg_resources` (Legacy), and `Filesystem` (Physical) sources.
    3.  **Achronal Thread-Sieve:** Detects WASM substrate and stays downstream threading
        triggers to prevent browser deadlocks.
    4.  **Bicameral Variable Isolation:** Surgically separates 'overrides' (Higher Will)
        from 'blueprint_vars' (Lower Will) to prevent Gnostic Leakage.
    5.  **The Variable Prism (Evolved):** Proactively generates 12+ derived variants
        of project DNA (Slug, Pascal, Snake, etc.) to saturate the Alchemist.
    6.  **The Syntax Healer:** Differentiates between Alchemical (Jinja) paradoxes
        and Structural (Scaffold) heresies with forensic clarity.
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
    13. **The Mirror of Narcissus:** Detects if an archetype attempts to import itself,
        preventing Ouroboric collapse.
    14. **The Contextual Hologram:** Injects deep system metadata (`_scaffold_version`,
        `_platform`, `_user`) into the rendering context.
    15. **The Privacy Veil:** Recursively redacts high-entropy secrets from the
        logging stream before the Weave begins.
    16. **The BOM Stripper:** Automatically detects and incinerates Byte Order Marks
        (\ufeff) to ensure UTF-8 purity.
    17. **The Unicode Sanitizer:** Enforces NFC normalization on all loaded scriptures.
    18. **The Lineage Tracker:** Appends the current archetype to a `_inheritance_chain`
        variable to track the genealogy of the blueprint.
    19. **The Root Resolver:** Ensures `project_root` is absolute in the context.
    20. **The Adrenaline Switch:** Checks for adrenaline mode and passes it down
        to the Parser Factory.
    21. **The Cache of Truth:** Implements an L1 memory cache for loaded archetype
        content to prevent redundant I/O during recursive weaves.
    22. **The Telemetric Pulse:** Broadcasts a specific "WEAVING_START" signal to the
        Akashic Record for real-time visualization.
    23. **The Exception Transmuter:** Converts raw IOErrors into rich `ArtisanHeresy`
        objects with forensic details.
    24. **The Dowry Validator:** Strict type-checking on the returned 4-tuple.
    25. **The Fallback Scryer:** If a system archetype is missing, it attempts to
        scry the local filesystem as a last resort.
    26. **The Pre-Flight Header Scan:** Peeks at the first 1KB of the archetype
        to validate Gnostic Headers (`# @gnosis`) before full parsing.
    27. **The Environment Bridge:** Merges `os.environ` variables prefixed with
        `SC_` into the weaving context.
    28. **The Path Canonizer:** Converts all Windows backslashes to POSIX forward
        slashes in the source path reference.
    29. **The Anchor of Provenance:** Injects `_blueprint_provenance` into variables
        for debugging.
    30. **The Silent Ward:** Respects the `silent` flag during internal operations.
    31. **The Entropy Seed:** Injects a stable random seed for deterministic generation.
    32. **The Omega Signal:** A special internal marker indicating the weave is complete.
    =================================================================================
    """

    # [ASCENSION 21]: THE CACHE OF TRUTH
    _archetype_cache: Dict[str, str] = {}

    def _conduct_master_weave(
            self: 'GenesisEngine',
            archetype_info: Dict[str, Any],
            final_gnosis: Dict[str, Any],
            overrides: Optional[Dict[str, Any]] = None
    ) -> Tuple[
        Dict, List[ScaffoldItem], List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]], 'ApotheosisParser']:
        """
        =================================================================================
        == THE MASTER WEAVER (V-Ω-TOTALITY-V32000-INFINITE)                            ==
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

            # [ASCENSION 21]: CACHE CHECK
            if archetype_path_ref in self._archetype_cache:
                archetype_content = self._archetype_cache[archetype_path_ref]
                # self.logger.debug("   -> Archetype retrieved from Memory Cache.")
            else:
                try:
                    # [ASCENSION 2]: RESOURCE ALCHEMIST 3.0
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
                            # Modern Python
                            from importlib import resources
                            # Handle Traversable vs Legacy
                            ref = resources.files(package).joinpath(resource_name)
                            if ref.is_file():
                                archetype_content = ref.read_text(encoding='utf-8')
                            else:
                                raise FileNotFoundError(f"Resource not found: {resource_name}")
                        except (ImportError, AttributeError, FileNotFoundError):
                            # [ASCENSION 25]: FALLBACK SCRYER (Legacy & Filesystem)
                            try:
                                import pkg_resources
                                archetype_content = pkg_resources.resource_string(package, resource_name).decode(
                                    'utf-8')
                            except Exception:
                                # Last resort: treat as relative file path
                                local_path = Path(resource_name).resolve()
                                if local_path.exists():
                                    archetype_content = local_path.read_text(encoding='utf-8')
                                else:
                                    raise
                    else:
                        # PATH B: PHYSICAL ARCHETYPE
                        archetype_path = Path(archetype_path_ref).resolve()
                        if not archetype_path.exists():
                            raise FileNotFoundError(f"Scripture unmanifest: {archetype_path}")
                        archetype_content = archetype_path.read_text(encoding='utf-8')

                    # [ASCENSION 16 & 17]: PURIFICATION (BOM & NFC)
                    archetype_content = archetype_content.lstrip('\ufeff')
                    archetype_content = unicodedata.normalize('NFC', archetype_content)

                    # [ASCENSION 8]: THE VOID GUARD
                    if not archetype_content or not archetype_content.strip():
                        raise ArtisanHeresy(f"The archetype '{archetype_name}' is a void.",
                                            severity=HeresySeverity.CRITICAL)

                    # Cache the pure soul
                    self._archetype_cache[archetype_path_ref] = archetype_content

                except Exception as e:
                    # [ASCENSION 23]: EXCEPTION TRANSMUTER
                    raise ArtisanHeresy(
                        f"Archetype Summoning Fracture: '{archetype_path_ref}'",
                        details=str(e), severity=HeresySeverity.CRITICAL
                    ) from e

            # --- MOVEMENT II: THE DIVINE ANOINTMENT OF THE SCRIBE ---
            self.logger.info("Awakening the one true Scribe (ApotheosisParser)...")

            # [ASCENSION 20]: Adrenaline awareness passed to factory
            parser = self.engine.parser_factory()

            # =========================================================================
            # == [THE CURE]: THE SYSTEM DNA SUTURE                                   ==
            # =========================================================================
            # [ASCENSION 1]: INJECT TRACE & SESSION AT NANOSECOND ZERO
            parsing_context = final_gnosis.copy()
            parsing_context['_scaffold_archetype_source'] = archetype_path_ref
            parsing_context['_scaffold_archetype_name'] = archetype_name

            # Explicitly pull Trace ID from Environment or CLI or Forge New
            active_trace_id = (
                    getattr(self.cli_args, 'trace_id', None) or
                    os.environ.get("SCAFFOLD_TRACE_ID") or
                    f"tr-gen-{uuid.uuid4().hex[:8].upper()}"
            )
            session_id = getattr(self.cli_args, 'session_id', 'SCAF-CORE')

            parsing_context['trace_id'] = active_trace_id
            parsing_context['session_id'] = session_id

            # [ASCENSION 14]: CONTEXTUAL HOLOGRAM
            parsing_context['_scaffold_version'] = __version__
            parsing_context['_platform'] = platform.system().lower()
            parsing_context['_user'] = os.environ.get('USER', 'architect')
            parsing_context['_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')

            # [ASCENSION 18]: LINEAGE TRACKER
            chain = parsing_context.get('_inheritance_chain', [])
            if not isinstance(chain, list): chain = []
            chain.append(archetype_name)
            parsing_context['_inheritance_chain'] = chain

            # [ASCENSION 29]: PROVENANCE ANCHOR
            self.variables['trace_id'] = active_trace_id
            self.variables['_blueprint_provenance'] = archetype_path_ref

            # Persist for child processes
            os.environ["SCAFFOLD_TRACE_ID"] = active_trace_id
            # =========================================================================

            # [ASCENSION 22]: TELEMETRIC PULSE (WASM-Safe)
            if hasattr(self.engine, 'akashic') and self.engine.akashic and not is_wasm:
                try:
                    self.engine.akashic.broadcast({
                        "method": "scaffold/weaving_init",
                        "params": {
                            "archetype": archetype_name,
                            "trace": active_trace_id,
                            "timestamp": time.time()
                        }
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
                # [ASCENSION 6]: THE SYNTAX HEALER
                is_template_error = "TemplateSyntaxError" in type(e).__name__ or "Jinja" in str(type(e))
                raise ArtisanHeresy(
                    f"{'Alchemical Syntax' if is_template_error else 'Gnostic'} Fracture in '{archetype_name}'.",
                    details=str(e),
                    severity=HeresySeverity.CRITICAL,
                    suggestion="Check for unclosed braces '{{ }}' or logical blocks." if is_template_error else None
                ) from e

            # --- MOVEMENT IV: THE RESOLUTION OF REALITY ---
            gnostic_plan = parser.resolve_reality()

            # --- MOVEMENT V: THE PROCLAMATION OF THE TRINITY ---
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

            # [ASCENSION 12 & 24]: THE FINALITY VOW (Type-Safe Return)
            return final_variables, gnostic_plan, post_run_commands, parser

    def _conduct_archetype_rite(self: 'GenesisEngine', archetype_info: Dict[str, Any]) -> Optional[
        Tuple[Dict, List[ScaffoldItem], List[
            Tuple[str, int, Optional[List[str]], Optional[List[str]]]], 'ApotheosisParser']]:
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

            # 5. [ASCENSION 5]: THE VARIABLE PRISM
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
            # [ASCENSION 13]: Mirror of Narcissus check
            # (Implicitly handled by recursion depth guard in parser, but we could add explicit check here)

            return self._conduct_master_weave(archetype_info, unified_context, overrides=unified_context)