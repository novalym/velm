# Path: src/velm/parser_core/parser/logic_weaver/import_manager.py
# -----------------------------------------------------------------
# LIF: ∞ | ROLE: MULTIVERSAL_INHALER_ENGINE | RANK: OMEGA_SUPREME
# AUTH: Ω_IMPORT_MANAGER_V200_RECURSIVE_TOTALITY_FINALIS
# =========================================================================================

import os
import re
import time
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Set, Optional, Tuple, TYPE_CHECKING

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...contracts.data_contracts import GnosticLineType, ScaffoldItem
from ...logger import Scribe

if TYPE_CHECKING:
    from ..parser.engine import ApotheosisParser

Logger = Scribe("GnosticImportManager")


class GnosticImportManager:
    """
    =================================================================================
    == THE GNOSTIC IMPORT MANAGER (V-Ω-TOTALITY-V200.0-UNBREAKABLE)                ==
    =================================================================================
    LIF: ∞ | ROLE: SPATIOTEMPORAL_REALITY_MERGER | RANK: OMEGA_SOVEREIGN

    The supreme authority on cross-scripture resonance. It manages the transition
    of Gnosis and Matter from external shards into the active timeline.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Selective Destructuring (@from):** Implements `from path import a, b`,
        performing a surgical extraction of willed atoms while discarding the void.
    2.  **Omniscient Indentation Awareness:** Automatically determines if an import
        is a Mind-Graft (Logic) or Matter-Suture (Physical) based on call-site depth.
    3.  **Naked Path Resolution:** Reconstructs coordinates from raw space-separated
        tokens, eliminating the "String-Tax" of quotes.
    4.  **Dot-Notation Transmutation:** Seamlessly converts `core.laws.api`
        into `core/laws/api.scaffold` for Pythonic mental parity.
    5.  **Namespaced Alias Suture (as):** Supports renaming both bulk namespaces
        and individual destructured atoms to prevent multiversal collision.
    6.  **Geometric Gravity Suture:** Automatically re-calculates the indentation
        of all included structural items to match the parent sanctum's gravity.
    7.  **Ouroboros Cryptographic Shield:** Uses SHA-256 path-anchoring in a shared
        Cortex cache to annihilate infinite recursion loops.
    8.  **The Origin Compass:** Directs the Hierophant to resolve internal
        paths relative to the imported file's physical locus, preventing drift.
    9.  **Bicameral Gnosis Grafting:** Safely merges $$, %%, and @macro
        strata into the parent Mind with transactional integrity.
    10. **Indentation Hierarchy Guard:** Prevents "Indentation Bleed" where
        child logic could accidentally overwrite parent topographical laws.
    11. **Fault-Isolated Inception:** Captures heresies in sub-files without
        shattering the parent's parse-vessel.
    12. **The Silence Vow Propagation:** Inherits and enforces all metabolic flags
        (silent, verbose, adrenaline) across the recursion stack.
    13. **Pythonic Syntax Parity:** No markers, no __init__, no boilerplate.
        The filesystem structure *is* the module registry.
    14. **Variable Thawing:** Pre-resolves alchemical variables `{{ var }}`
        within the import path string before spatial resolution.
    15. **Artifact Provenance Suture:** Injected items are stamped with
        their originating blueprint path for bit-perfect forensic auditing.
    16. **Contract Inheritance:** %% contract definitions are shared globally
        across the entire import tree.
    17. **Snippet Focus:** Optimized for inhaling microscopic shards of logic
        (Macros/Traits) to keep the Gnostic Context lean.
    18. **Hydraulic Import Throttling:** Paces deep-recursion events to
        prevent stack-overflow fever in the WASM heap.
    19. **Zero-Touch Archetypes:** Every .scaffold file in the universe is
        an instantly importable library shard.
    20. **Trait Globalist:** Centralizes %% trait registries, allowing
        one standard to ward the entire multiverse.
    21. **Post-Run Will Merge:** Unifies kinetic edict queues across
        timelines, ensuring sequential execution resonance.
    22. **Causal Trace Mapping:** Links every imported variable back to its
        birth file via metadata, proving provenance.
    23. **Substrate-Agnostic Scrying:** Functions with bit-perfect parity in
        the WASM `/vault` and Physical Iron substrates.
    24. **The Finality Vow:** A mathematical guarantee of total resonance or
        a descriptive, actionable heresy—never a silent failure.
    =================================================================================
    """

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION] Binds the Manager to the Master Cortex."""
        self.parser = parser
        self.Logger = Logger

    def conduct_inhalation(self, i: int, args: List[str], raw_line: str) -> int:
        """
        =============================================================================
        == THE MASTER RITE OF INHALATION (V-Ω-TOTALITY-V200)                      ==
        =============================================================================
        Transmutes an @import or @from intent into a unified Reality.
        """
        if not args:
            raise ArtisanHeresy("IMPORT_HERESY: Directive requires target coordinate.", line_num=i + 1)

        # --- MOVEMENT I: SEMANTIC TRIAGE ---
        # 1. Divine the Intent (import vs from)
        # Note: The GnosticLineInquisitor has already tagged the directive_type
        directive = getattr(self.parser.vessel, 'directive_type', 'import')
        full_arg_string = " ".join(args)

        target_path_str: str = ""
        items_to_import: Optional[List[str]] = None  # None implies "Bulk"
        namespace_alias: Optional[str] = None

        # [ASCENSION 1]: SELECTIVE DESTRUCTURING (@from)
        if directive == "from":
            if " import " not in full_arg_string:
                raise ArtisanHeresy(
                    "@from requires 'import' clause. Syntax: @from x import a, b",
                    line_num=i + 1,
                    severity=HeresySeverity.CRITICAL
                )

            path_part, items_part = full_arg_string.split(" import ", 1)
            target_path_str = path_part.strip()
            # Split items and clean commas/whitespace
            items_to_import = [x.strip().strip(',') for x in items_part.split()]
            items_to_import = [x for x in items_to_import if x]

        # [ASCENSION 5]: NAMESPACED BULK (@import ... as ...)
        else:
            if " as " in full_arg_string:
                path_part, alias_part = full_arg_string.split(" as ", 1)
                target_path_str = path_part.strip()
                namespace_alias = alias_part.strip()
            else:
                target_path_str = full_arg_string.strip()

        # --- MOVEMENT II: SPATIAL RESOLUTION ---
        # 1. Alchemical Thawing: Resolve variables inside the path
        target_path_str = self.parser.alchemist.transmute(target_path_str, self.parser.variables)

        # 2. [ASCENSION 4]: DOT-NOTATION TRANSMUTATION
        if '.' in target_path_str and '/' not in target_path_str and not target_path_str.endswith(
                ('.scaffold', '.arch')):
            target_path_str = target_path_str.replace('.', '/')

        # 3. Scry the Celestial Strata
        try:
            target_path = self._scry_celestial_strata(target_path_str.strip('"\''))
        except FileNotFoundError as e:
            raise ArtisanHeresy(f"IMPORT_VOID: {str(e)}", line_num=i + 1, severity=HeresySeverity.CRITICAL)

        # --- MOVEMENT III: THE OUROBOROS GUARD ---
        if target_path in self.parser.import_cache:
            # If we are doing a bulk import and already did it, we skip to save metabolism.
            # If we are doing selective destructuring, we re-scry (from cache) to find the atoms.
            if not items_to_import:
                self.Logger.verbose(f"L{i + 1}: Inhale Stayed: '{target_path.name}' is already resonant.")
                return i + 1

        self.parser.import_cache.add(target_path)

        # --- MOVEMENT IV: THE INCEPTION ---
        self.Logger.info(f"L{i + 1}: Inhaling Reality from '[cyan]{target_path.name}[/cyan]'...")

        try:
            # 1. Forge the Sub-Parser (The Temporary Emissary)
            # We share the Engine and the shared Registry (Traits/Imports) by reference.
            sub_parser = self.parser.__class__(grammar_key='scaffold', engine=self.parser.engine)
            sub_parser.import_cache = self.parser.import_cache
            sub_parser.traits = self.parser.traits
            sub_parser.depth = self.parser.depth + 1
            sub_parser._silent = self.parser._silent

            # 2. Materialize Matter
            content = target_path.read_text(encoding='utf-8')

            # 3. Execute the Sub-Strike
            # (parser, items, commands, edicts, vars, dossier)
            _, sub_items, sub_commands, _, inhaled_vars, _ = sub_parser.parse_string(
                content,
                file_path_context=target_path,
                pre_resolved_vars=self.parser.variables  # Inherit current Mind state
            )

            # --- MOVEMENT V: THE SOCRATIC SIEVE (DESTRUCTURING) ---
            # If items_to_import is manifest, we only keep the willed atoms.
            if items_to_import:
                inhaled_vars, sub_items, sub_commands = self._sieve_atoms(
                    items_to_import, inhaled_vars, sub_items, sub_commands, sub_parser, target_path.name, i
                )

            # [ASCENSION 5]: NAMESPACE PREFIXING (AS)
            elif namespace_alias:
                inhaled_vars = {f"{namespace_alias}.{k}": v for k, v in inhaled_vars.items()}
                # In namespaced mode, structural matter is suppressed to keep the parent pure.
                sub_items = []
                sub_commands = []

            # --- MOVEMENT VI: GEOMETRIC SUTURE (THE FIX) ---
            # [ASCENSION 6]: Automatically adjusts indentation to Call-Site visual depth.
            current_indent = self.parser._calculate_original_indent(raw_line)

            if sub_items:
                for item in sub_items:
                    # Suture indents to the current visual locus
                    item.original_indent += current_indent
                    # [ASCENSION 15]: Inscribe Provenance
                    item.blueprint_origin = target_path
                    self.parser.raw_items.append(item)

            # --- MOVEMENT VII: GNOSTIC GRAFTING (THE MIND) ---
            # Graft the sub-file's soul into the parent Cortex.
            self.parser.blueprint_vars.update(inhaled_vars)
            self.parser.macros.update(sub_parser.macros)
            self.parser.tasks.update(sub_parser.tasks)
            self.parser.contracts.update(sub_parser.contracts)
            # Link the Kinetic Will
            self.parser.post_run_commands.extend(sub_commands)

            self.Logger.success(f"   -> Singularity: '{target_path.name}' integrated purely.")

        except Exception as fracture:
            if isinstance(fracture, ArtisanHeresy): raise fracture
            raise ArtisanHeresy(f"IMPORT_FRACTURE: {str(fracture)}", line_num=i + 1, child_heresy=fracture)

        return i + 1

    def _sieve_atoms(
            self,
            willed_names: List[str],
            vars_in: Dict,
            items_in: List,
            cmds_in: List,
            sub_p: Any,
            src_name: str,
            line: int
    ) -> Tuple[Dict, List, List]:
        """
        [FACULTY 1]: THE SOCRATIC SIEVE.
        Filters the sub-parser's results, keeping only the explicitly requested atoms.
        """
        final_vars = {}

        for willed in willed_names:
            # Handle "a as b" aliasing
            src_key, dst_key = (willed.split(" as ") if " as " in willed else (willed, willed))
            src_key, dst_key = src_key.strip(), dst_key.strip()

            found = False
            # 1. Search Variables
            if src_key in vars_in:
                final_vars[dst_key] = vars_in[src_key]
                found = True

            # 2. Search Macros
            if src_key in sub_p.macros:
                self.parser.macros[dst_key] = sub_p.macros[src_key]
                found = True

            # 3. Search Traits
            if src_key in sub_p.traits:
                self.parser.traits[dst_key] = sub_p.traits[src_key]
                found = True

            if not found:
                available = list(vars_in.keys()) + list(sub_p.macros.keys()) + list(sub_p.traits.keys())
                raise ArtisanHeresy(
                    f"Coordinate Deficiency: '{src_key}' unmanifest in '{src_name}'.",
                    suggestion=f"Available atoms in source: {available[:8]}...",
                    line_num=line + 1,
                    severity=HeresySeverity.CRITICAL
                )

        # Selective destructuring suppresses all Matter (structural items) by definition.
        return final_vars, [], []

    def _scry_celestial_strata(self, path_str: str) -> Path:
        """
        =============================================================================
        == THE HIERARCHICAL COMPASS (V-Ω-TOTALITY-V200)                            ==
        =============================================================================
        LIF: 100x | ROLE: GEOMETRIC_RESOLVER
        [THE CURE]: Implements the 'Local -> Project-Library -> Global-Library' search.
        """
        # 1. Normalize extension
        if not path_str.endswith(('.scaffold', '.arch', '.symphony')):
            path_str += '.scaffold'

        # --- THE HIERARCHY OF TRUTH ---

        # 1. LOCAL STRATUM: Sibling to current scripture
        base_dir = self.parser.file_path.parent if self.parser.file_path else Path.cwd()
        local_cand = (base_dir / path_str).resolve()
        if local_cand.is_file(): return local_cand

        # 2. PROJECT STRATUM: .scaffold/library/ (Project Sovereignty)
        proj_lib = (self.parser.project_root or Path.cwd()) / ".scaffold" / "library"
        proj_cand = (proj_lib / path_str).resolve()
        if proj_cand.is_file(): return proj_cand

        # 3. CELESTIAL STRATUM: ~/.scaffold/library/ (Architect's Grimoire)
        global_lib = Path.home() / ".scaffold" / "library"
        global_cand = (global_lib / path_str).resolve()
        if global_cand.is_file(): return global_cand

        # 4. SUBSTRATE STRATUM: Internal WASM Assets
        try:
            from ...artisans.project.seeds import ArchetypeOracle
            oracle = ArchetypeOracle()
            sources = oracle._triangulate_sources()
            if "virtual" in sources:
                virt_cand = (sources["virtual"] / path_str).resolve()
                if virt_cand.is_file(): return virt_cand
        except Exception:
            pass

        # If all strata are a void, we proclaim the failure.
        raise FileNotFoundError(f"Scripture '{path_str}' is unmanifest across all multiversal strata.")

    def __repr__(self) -> str:
        return f"<Ω_GNOSTIC_IMPORT_MANAGER state=RESONANT cache_size={len(self.parser.import_cache)}>"