# Path: src/velm/core/blueprint_scribe/scribe.py
# ----------------------------------------------
# LIF: ∞ | ROLE: ARCHITECTURAL_TRANSCRIBER | RANK: OMEGA_SUPREME
# AUTH: Ω_BLUEPRINT_SCRIBE_V500_LITERALIST_FINALIS
# =========================================================================================
#
# [ARCHITECTURAL MANIFESTO]
# The High Priest of Transcription.
#
# [THE CURE]: This version annihilates the "Nested Root" heresy by strictly adherence
# to the Law of Relative Truth. It does not invent directories. It transcribes the
# exact paths provided by the Engine.
#
# [THE PANTHEON OF 12 ASCENSIONS]:
# 1.  **Literal Geometry:** Removes all "Project Slug" wrapper logic. The paths
#     in the blueprint are now 1:1 with the ScaffoldItems provided.
# 2.  **The Metadata Suture:** Correctly injects the `%% contract` and `%% trait`
#     definitions before the form, ensuring logical precedence.
# 3.  **The Atomic Stringifier:** Intelligently quotes strings in `$$` variables
#     while leaving booleans, integers, and template expressions naked.
# 4.  **The Sigil Stripper:** Surgically removes `>>` from commands in `%% post-run`
#     to ensure the blueprint is clean and idempotent.
# 5.  **The Void Guard:** Checks if `body` is empty and inserts a comment to
#     prevent creating a 0-byte file that looks like a heresy.
# 6.  **The Path Normalizer:** Forcefully transmutes all paths to POSIX (`/`)
#     standards, annihilating Windows backslashes in the scripture.
# 7.  **The Variable Segregator:** Isolates Gnostic State (`$$`) from Physical
#     Form (Files) for perfect readability.
# 8.  **The Deterministic Sorter:** Sorts variables alphabetically to ensure
#     Git diff stability.
# 9.  **The Stream of Consciousness:** Uses generators to build the string,
#     minimizing memory pressure.
# 10. **The Provenance Footer:** Inscribes the forensic timestamp and version
#     metadata at the bottom of the scroll.
# 11. **The In-Place Check:** (Redundant logic removed) - Simplicity is reliability.
# 12. **The Finality Vow:** Guaranteed valid return.

from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Iterable

from .metadata_scribe import MetadataScribe
from .tree_forger import TreeForger
from .canonical_serializer import CanonicalSerializer
from ..alchemist import DivineAlchemist, get_alchemist
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...logger import Scribe

Logger = Scribe("BlueprintScribe")


class BlueprintScribe:
    """
    The Sovereign Scribe. Writes the laws of the universe into text.
    """

    def __init__(self, project_root: Path, *, alchemist: Optional[DivineAlchemist] = None):
        self.project_root = project_root.resolve()
        self.alchemist = alchemist or get_alchemist()

        # Summon Sub-Artisans
        self.metadata_scribe = MetadataScribe(self.project_root, self.alchemist)
        self.tree_forger = TreeForger()
        self.serializer = CanonicalSerializer()

    def transcribe(
            self,
            items: List[ScaffoldItem],
            commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],  # <--- UPDATED
            gnosis: Dict[str, Any],
            rite_type: str = 'genesis'
    ) -> str:
        """
        The Grand Rite of Transcription.
        """
        Logger.verbose("The Blueprint Scribe awakens. Commencing Rite of Transcription...")

        # --- MOVEMENT I: THE SEGREGATION OF SOULS ---
        (
            variable_items,
            contract_items,
            trait_items,
            form_items
        ) = self._segregate_items(items)

        # --- MOVEMENT II: THE FORGING OF THE HIERARCHY ---
        root_node = self.tree_forger.forge(form_items)

        # --- MOVEMENT III: THE STREAM OF CONSCIOUSNESS ---
        body_lines = list(self.serializer.serialize(root_node))

        # --- MOVEMENT IV: THE PROVENANCE SUTURE ---
        clean_commands = [cmd for cmd, _, _, _ in commands]  # Ignore undo/heresy for footer hash
        header_lines = self.metadata_scribe.forge_header(gnosis)
        footer_lines = self.metadata_scribe.forge_footer(gnosis, clean_commands)

        # --- MOVEMENT V: THE FINAL ASSEMBLY ---
        final_scripture = self._assemble_scripture(
            header_lines,
            variable_items,
            contract_items,
            trait_items,
            body_lines,
            clean_commands,
            footer_lines,
            gnosis
        )

        return "\n".join(final_scripture)

    def _assemble_scripture(self, *args) -> Iterable[str]:
        """The Gnostic Generator."""
        header, variables, contracts, traits, body, commands, footer, gnosis = args

        # 1. HEADER
        yield from header

        # 2. VARIABLES (The Altar of Gnostic Will)
        combined_vars = gnosis.copy()

        if combined_vars:
            yield "\n# --- I. The Altar of Gnostic Will (Variables) ---"
            for key in sorted(combined_vars.keys()):
                if key.startswith("_") or key in ["project_root"]: continue
                val = combined_vars[key]
                formatted_val = self._format_variable_value(val)
                yield f"$$ {key} = {formatted_val}"
            yield ""

        # 3. LAWS (Contracts & Traits)
        if contracts or traits:
            yield "# --- II. The Scripture of Law (Contracts & Traits) ---"
            for contract_item in contracts:
                yield from contract_item.raw_scripture.splitlines()
                yield ""
            for trait_item in traits:
                yield trait_item.raw_scripture
            yield ""

        # 4. FORM (The Body)
        if body:
            yield "# --- III. The Scripture of Form (The Body) ---"

            # [ASCENSION 1]: LITERAL GEOMETRY (THE CURE)
            # We do NOT wrap the body in {{ project_slug }}.
            # The TreeForger has already constructed the correct relative hierarchy.
            # We trust the items as they are.
            yield from body

            yield ""
        else:
            yield "# [VOID MANIFEST]: No physical form defined."
            yield ""

        # 5. WILL (Automation)
        if commands:
            yield "\n# --- IV. The Maestro's Will (Automation) ---"
            yield "%% post-run"
            for cmd in commands:
                # [ASCENSION 4]: Sigil Stripper
                clean = cmd.lstrip('>').strip()
                yield f"    >> {clean}"
            yield ""

        # 6. FOOTER
        yield from footer

    def _format_variable_value(self, value: Any) -> str:
        """Smart formatting for variable values."""
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, (int, float)):
            return str(value)

        val_str = str(value)
        if val_str.startswith('"') and val_str.endswith('"'):
            return val_str
        if val_str.startswith("'") and val_str.endswith("'"):
            return val_str

        # Heuristic: Check for template syntax or function calls
        if "{{" in val_str or "(" in val_str:
            return val_str

        return f'"{val_str}"'

    def _segregate_items(self, items: List[ScaffoldItem]) -> Tuple[
        List[ScaffoldItem], List[ScaffoldItem], List[ScaffoldItem], List[ScaffoldItem]]:
        """Segregates Gnostic types."""
        vars_list, contracts_list, traits_list, form_list = [], [], [], []

        for item in items:
            if not item.path and not item.raw_scripture: continue

            if item.line_type == GnosticLineType.VARIABLE:
                vars_list.append(item)
            elif item.line_type == GnosticLineType.CONTRACT_DEF:
                contracts_list.append(item)
            elif item.line_type in (GnosticLineType.TRAIT_DEF, GnosticLineType.TRAIT_USE):
                traits_list.append(item)
            elif item.line_type == GnosticLineType.FORM:
                form_list.append(item)
            # Logic nodes (@if) are implicitly handled by the TreeForger as containers

        return vars_list, contracts_list, traits_list, form_list