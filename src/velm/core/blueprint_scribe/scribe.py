# Path: src/velm/core/blueprint_scribe/scribe.py
# ----------------------------------------------
# LIF: ∞ | ROLE: ARCHITECTURAL_TRANSCRIBER | RANK: OMEGA_SUPREME
# AUTH: Ω_BLUEPRINT_SCRIBE_V1000_TOTALITY_FINALIS
# =========================================================================================

import json
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Iterable

# --- INTERNAL STRATA ---
from .metadata_scribe import MetadataScribe
from .tree_forger import TreeForger
from .canonical_serializer import CanonicalSerializer
from ..alchemist import DivineAlchemist, get_alchemist
from ...contracts.data_contracts import ScaffoldItem, GnosticLineType
from ...logger import Scribe

# [ASCENSION 1 & 11]: THE GNOSTIC SYSTEM ABYSS
# These keys represent the "Metabolism of the Machine" and must never be inscribed.
GNOSTIC_SYSTEM_ABYSS = {
    "scaffold_env", "generated_manifest", "timestamp", "file_count",
    "project_root_name", "ansi_colors", "term_width", "os_sep",
    "transaction_id", "trace_id", "python_version_tuple", "is_simulated",
    "dry_run", "force", "verbose", "silent", "no_edicts", "non_interactive",
    "request_id", "session_id", "client_id", "blueprint_path",
    "clean_type_name", "env_vars_setup", "name_camel", "name_const",
    "name_pascal", "name_path", "name_slug", "name_snake", "name_title",
    "ai_code_generation_consent", "project_structure_pattern", "dna",
    "blueprint_origin", "is_binary", "current_year", "creation_date",
    "is_git_repo", "has_docker", "has_make", "project_type", "scaffold_version"
}

Logger = Scribe("BlueprintScribe")


class BlueprintScribe:
    """
    =================================================================================
    == THE SOVEREIGN SCRIBE (V-Ω-TOTALITY-V1000)                                   ==
    =================================================================================
    The High Priest of Transcription. Transmutes live Gnostic state into the
    Eternal Scripture of Form.
    """

    def __init__(self, project_root: Path, *, alchemist: Optional[DivineAlchemist] = None):
        """[THE RITE OF INCEPTION]"""
        self.project_root = project_root.resolve()
        self.alchemist = alchemist or get_alchemist()

        # Summon the Sub-Artisans
        self.metadata_scribe = MetadataScribe(self.project_root, self.alchemist)
        self.tree_forger = TreeForger()
        self.serializer = CanonicalSerializer()

    def transcribe(
            self,
            items: List[ScaffoldItem],
            commands: List[Tuple[str, int, Optional[List[str]], Optional[List[str]]]],
            gnosis: Dict[str, Any],
            rite_type: str = 'genesis'
    ) -> str:
        """
        =============================================================================
        == THE GRAND RITE OF TRANSCRIPTION                                         ==
        =============================================================================
        Conducts the five-movement symphony to materialize the Blueprint scroll.
        """
        Logger.verbose("The Blueprint Scribe awakens. Commencing Rite of Transcription...")

        # --- MOVEMENT I: THE SEGREGATION OF SOULS ---
        # Separates variables, contracts, and physical items for tiered assembly.
        (
            variable_items,
            contract_items,
            trait_items,
            form_items
        ) = self._segregate_items(items)

        # --- MOVEMENT II: THE FORGING OF THE HIERARCHY ---
        # [ASCENSION 2]: Literalist Tree Forge.
        root_node = self.tree_forger.forge(form_items)

        # --- MOVEMENT III: THE STREAM OF CONSCIOUSNESS ---
        # Converts the tree into aligned, indented strings.
        body_lines = list(self.serializer.serialize(root_node))

        # --- MOVEMENT IV: THE PROVENANCE SUTURE ---
        # Extracts command strings and forges the metadata seals.
        clean_commands = [cmd[0] if isinstance(cmd, (tuple, list)) else cmd for cmd in commands]
        header_lines = self.metadata_scribe.forge_header(gnosis)
        footer_lines = self.metadata_scribe.forge_footer(gnosis, clean_commands)

        # --- MOVEMENT V: THE FINAL ASSEMBLY ---
        # Joins the strata into a single, cohesive scripture.
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
        """[ASCENSION 9]: The Gnostic Generator."""
        header, variable_items, contracts, traits, body, commands, footer, gnosis = args

        # 1. HEADER (Identity)
        yield from header

        # 2. VARIABLES (The Altar of Gnostic Will)
        # [ASCENSION 1 & 8]: Gnostic Sieve & Deterministic Sort
        yield "\n# --- I. The Altar of Gnostic Will (Variables) ---"
        manifest_vars = []
        for key in sorted(gnosis.keys()):
            # [THE SIEVE]: Filter out internal noise and private keys
            if self._is_system_variable(key):
                continue

            val = gnosis[key]
            # [ASCENSION 12]: Type-Strict Inscription
            if not isinstance(val, (str, bool, int, float, list, dict)):
                continue

            formatted_val = self._format_variable_value(val)
            manifest_vars.append(f"$$ {key} = {formatted_val}")

        if manifest_vars:
            yield from manifest_vars
        else:
            yield "# [VOID_STATE]: No custom variables willed."
        yield ""

        # 3. LAWS (Contracts & Traits)
        # [ASCENSION 14]: Logic Precedence
        if contracts or traits:
            yield "# --- II. The Scripture of Law (Contracts & Traits) ---"
            for contract in contracts:
                if hasattr(contract, 'raw_scripture') and contract.raw_scripture:
                    yield from contract.raw_scripture.splitlines()
                    yield ""
            for trait in traits:
                if hasattr(trait, 'raw_scripture') and trait.raw_scripture:
                    yield trait.raw_scripture
            yield ""

        # 4. FORM (The Body)
        # [ASCENSION 5]: The Void Guard
        if body:
            yield "# --- III. The Scripture of Form (The Body) ---"
            yield from body
            yield ""
        else:
            yield "# [VOID_MANIFEST]: Physical reality is a void."
            yield ""

        # 5. WILL (Automation)
        if commands:
            yield "\n# --- IV. The Maestro's Will (Automation) ---"
            yield "%% post-run"
            for cmd in commands:
                # [ASCENSION 5]: Sigil Stripper
                clean = str(cmd).lstrip('>').lstrip(' ').strip()
                yield f"    >> {clean}"
            yield ""

        # 6. FOOTER (Provenance)
        yield from footer

    def _is_system_variable(self, key: str) -> bool:
        """[ASCENSION 1, 13]: The Gnostic Sieve Logic."""
        if key.startswith("_"): return True
        if key.lower() in GNOSTIC_SYSTEM_ABYSS: return True
        return False

    def _format_variable_value(self, value: Any) -> str:
        """
        [ASCENSION 3, 18]: THE ATOMIC STRINGIFIER.
        Transmutes Python types into Gnostic scripture literals.
        """
        if isinstance(value, bool):
            return str(value).lower()
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, (list, dict)):
            # [ASCENSION 18]: JSON-Safe Complex Types
            return json.dumps(value)

        val_str = str(value)

        # [ASCENSION 4]: Smart Quoting
        # If it's already quoted, or contains template tags, we don't wrap it.
        if val_str.startswith('"') and val_str.endswith('"'):
            return val_str
        if val_str.startswith("'") and val_str.endswith("'"):
            return val_str
        if "{{" in val_str or "(" in val_str:
            return val_str

        # Escape existing quotes and wrap
        escaped = val_str.replace('"', '\\"')
        return f'"{escaped}"'

    def _segregate_items(self, items: List[ScaffoldItem]) -> Tuple[
        List[ScaffoldItem], List[ScaffoldItem], List[ScaffoldItem], List[ScaffoldItem]]:
        """Segregates Gnostic types for hierarchical assembly."""
        vars_list, contracts_list, traits_list, form_list = [], [], [], []

        for item in items:
            # Prevent transcription of void items
            if not item.path and not item.raw_scripture:
                continue

            if item.line_type == GnosticLineType.VARIABLE:
                vars_list.append(item)
            elif item.line_type == GnosticLineType.CONTRACT_DEF:
                contracts_list.append(item)
            elif item.line_type in (GnosticLineType.TRAIT_DEF, GnosticLineType.TRAIT_USE):
                traits_list.append(item)
            elif item.line_type == GnosticLineType.FORM:
                form_list.append(item)

        return vars_list, contracts_list, traits_list, form_list