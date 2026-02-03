# Path: scaffold/genesis/genesis_engine/weaving.py
# ------------------------------------------------

import importlib.resources as pkg_resources
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List, TYPE_CHECKING

# --- THE DIVINE SUMMONS ---
from ...contracts.data_contracts import ScaffoldItem
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
    LIF: 10,000,000,000,000

    This Mixin is the Grand Weaver. It handles the loading, parsing, and logical
    resolution of Archetypes. It acts as the bridge between the Static Grimoire (Profiles)
    and the Dynamic Reality (ScaffoldItems).

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Trinity Preservation (THE CORE FIX):** It fundamentally respects the
        new 3-tuple structure of Maestro commands `(cmd, line, undo)`, propagating
        it intact to the Materializer without profane unpacking.
    2.  **The Resource Alchemist:** A robust, dual-mode loader that can fetch archetypes
        from the Python package stream (System) or the raw filesystem (User/Local) transparently.
    3.  **The Contextual Anchor:** Injects metadata about the archetype's origin (`archetype_source`)
        directly into the parsing context, allowing blueprints to reflect on their own nature.
    4.  **The Void Guard:** Performs a pre-flight check on the archetype's content. If the
        soul is empty, it raises a specific, helpful Heresy rather than confusing the Parser.
    5.  **The Logic Weaver's Bond:** Explicitly invokes `resolve_reality()` on the parser.
        This ensures that all `@if`, `@for`, and `@def` logic is executed *before* the
        plan is handed to the creator.
    6.  **The Variable Prism:** Automatically calculates derived variable formats (slug,
        pascal, snake) *before* parsing, ensuring Jinja templates inside the blueprint
        render correctly immediately.
    7.  **The Syntax Healer:** Catches `TemplateSyntaxError` specifically, re-raising it
        as a `ArtisanHeresy` with a suggestion to check Jinja syntax vs. Scaffold syntax.
    8.  **The Override Merger:** Merges Profile Overrides, CLI Overrides, and Prophecy Defaults
        into a single, authoritative `unified_context` before the weave begins.
    9.  **The Mentor's Hook:** (Prepared) The structure allows for the injection of
        Architectural Laws via the `GENESIS_CODEX` in the future.
    10. **The Luminous Logging:** Uses `logger.indent` to visually group the complex
        steps of the weaving process in the console output.
    11. **The Dynamic Dowry:** Returns the standardized `GnosticDowry` tuple, ensuring
        type safety across the Genesis pipeline.
    12. **The Sovereign State:** Updates the Engine's internal `variables` state with
        the final, resolved values from the Parser, ensuring the `GenesisReport` reflects
        reality.
    """

    def _conduct_master_weave(
            self: 'GenesisEngine',
            archetype_info: Dict[str, Any],
            final_gnosis: Dict[str, Any],
            overrides: Optional[Dict[str, Any]] = None
    ) -> Tuple[Dict, List[ScaffoldItem], List[Tuple[str, int, Optional[List[str]]]], 'ApotheosisParser']:
        """
        [THE ONE TRUE WEAVER]
        Parses the archetype scripture and prepares the Gnostic Dowry.
        """
        archetype_name = archetype_info.get('name', 'Unknown')

        with self.logger.indent(f"Rite of the Master Weaver: '{archetype_name}'"):
            # --- MOVEMENT I: THE GAZE UPON THE ARCHETYPE'S SACRED SCRIPTURE ---
            self.logger.info("Perceiving the Archetype's sacred, untransmuted soul...")
            archetype_path_ref = archetype_info["archetype_path"]
            archetype_content = ""

            try:
                # [FACULTY 2] The Resource Alchemist
                if ":" in archetype_path_ref:
                    # System Archetype (Package Resource)
                    package, resource_name = archetype_path_ref.split(":")
                    try:
                        # Modern API (Python 3.9+)
                        archetype_content = pkg_resources.files(package).joinpath(resource_name).read_text(
                            encoding='utf-8')
                    except (AttributeError, ImportError):
                        # Legacy API fallback
                        archetype_content = pkg_resources.read_text(package, resource_name, encoding='utf-8')
                else:
                    # Local/Global Archetype (File Path)
                    archetype_path = Path(archetype_path_ref).resolve()
                    if not archetype_path.exists():
                        raise FileNotFoundError(f"File not found: {archetype_path}")
                    archetype_content = archetype_path.read_text(encoding='utf-8')

                # [FACULTY 4] The Void Guard
                if not archetype_content.strip():
                    raise ArtisanHeresy(
                        f"The archetype scripture at '{archetype_path_ref}' is a void (empty content).",
                        severity=HeresySeverity.CRITICAL
                    )

            except (FileNotFoundError, ModuleNotFoundError) as e:
                raise ArtisanHeresy(
                    f"The sacred archetype scripture at '{archetype_path_ref}' could not be summoned.",
                    child_heresy=e,
                    suggestion="Verify the archetype path or reinstall the scaffold package."
                ) from e

            # --- MOVEMENT II: THE DIVINE ANOINTMENT OF THE SCRIBE ---
            self.logger.info("Awakening the one true Scribe (ApotheosisParser) and anointing it with Gnosis...")
            parser = self.parser_factory()

            # [FACULTY 3] The Contextual Anchor
            # We inject metadata about the archetype itself into the variables
            parsing_context = final_gnosis.copy()
            parsing_context['_scaffold_archetype_source'] = archetype_path_ref
            parsing_context['_scaffold_archetype_name'] = archetype_name

            # The Rite of Parsing.
            try:
                parser.parse_string(
                    content=archetype_content,
                    file_path_context=self.project_root / "ephemeral_archetype.scaffold",
                    pre_resolved_vars=parsing_context,
                    overrides=overrides or {}
                )
            except Exception as e:
                # [FACULTY 7] The Syntax Healer
                if "TemplateSyntaxError" in type(e).__name__:
                    raise ArtisanHeresy(
                        f"Jinja2 Syntax Heresy in Archetype '{archetype_name}'.",
                        details=str(e),
                        suggestion="Check for malformed {{ variables }} or {% blocks %}.",
                        severity=HeresySeverity.CRITICAL
                    ) from e
                raise ArtisanHeresy(
                    f"Failed to parse archetype '{archetype_name}': {e}",
                    child_heresy=e
                )

            # --- MOVEMENT III: THE RESOLUTION OF REALITY ---
            # [FACULTY 5] The Logic Weaver Integration
            # We must summon the LogicWeaver to resolve @if/@for blocks and prune the tree.
            # The parser's `resolve_reality` method returns the purified list.
            gnostic_plan = parser.resolve_reality()

            # --- MOVEMENT IV: THE PRESERVATION OF THE TRINITY ---
            # [FACULTY 1] The Trinity Preservation (THE FIX)
            # We extract the full (command, line, undo) tuples. We DO NOT unpack them here.
            # parser.post_run_commands is List[Tuple[str, int, Optional[List[str]]]]
            post_run_commands = parser.post_run_commands

            final_variables = parser.variables

            # [FACULTY 12] The Sovereign State
            # We update the engine's state with the variables fully resolved by the parser/alchemist
            self.variables.update(final_variables)

            if not gnostic_plan and not post_run_commands:
                self.logger.warn("The final Gnostic plan is a void. No reality will be made manifest.")

            self.logger.success("The Gnostic Dowry has been forged. Proclaiming the final reality to the Conductor.")

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
            # [FACULTY 8] The Override Merger
            # Prophecy < Profile < CLI
            unified_context = {**prophecy.defaults, **profile_gnosis, **cli_vars}

            # 5. The Rite of Patient Alchemy (Derive Slugs)
            # [FACULTY 6] The Variable Prism
            # We calculate these NOW so they are available to the parser immediately.
            project_name = to_string_safe(unified_context.get('project_name', 'new-project'))
            derived = generate_derived_names(project_name)

            # Update context with derived values (slug, pascal_name, etc.)
            unified_context.update(derived)
            # Ensure 'project_slug' specifically is set for compatibility
            unified_context['project_slug'] = derived.get('name_slug')

            ptype = unified_context.get('project_type', 'generic')
            unified_context['clean_type_name'] = str(ptype).split(' ')[0].lower()

            self.logger.success("The Gnostic Context has been prepared and hierarchically separated.")

            # 6. The Gnostic Mentor's Silent Gaze
            from ...jurisprudence_core.genesis_jurisprudence import GENESIS_CODEX
            triggered_laws = [law for law in GENESIS_CODEX if law.validator(unified_context)]

            if triggered_laws:
                for law in triggered_laws:
                    msg = law.message(unified_context) if callable(law.message) else law.message
                    self.logger.warn(f"Architectural Warning: {msg}")

            self.logger.info("Bestowing hierarchically pure Gnosis upon the Master Weaver...")

            # 7. The Master Weave
            dowry = self._conduct_master_weave(archetype_info, unified_context, overrides=unified_context)

            self.logger.success("The Master Weaver's proclamation has been received. The Gnostic Dowry is whole.")
            return dowry