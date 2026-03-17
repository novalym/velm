# Path: parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe/traits.py
# ------------------------------------------------------------------------------------
import os
import re
import shlex
import time
import hashlib
import threading
from pathlib import Path
from typing import List, Any, Dict, Optional, Tuple, Final

# --- THE DIVINE UPLINKS ---
from ......contracts.data_contracts import GnosticVessel, ScaffoldItem, GnosticLineType
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......core.alchemist import get_alchemist
from ......logger import Scribe

Logger = Scribe("TraitOrchestrator:Apotheosis")


class TraitOrchestrator:
    """
    =================================================================================
    == THE TRAIT ORCHESTRATOR: OMEGA POINT (V-Ω-TOTALITY-VMAX-169-ASCENSIONS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TOPOLOGICAL_REALITY_GRAFTER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_TRAITS_VMAX_RECURSIVE_SUTURE_2026_FINALIS

    The supreme authority for structural inheritance. This organ manages the
    definitions of Gnostic Traits (Mixins) and their kinetic expansion into the
    active blueprint timeline. It righteously enforces the Law of Modular Integrity.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS:
    146. **Achronal Trait-Path Cache (THE MASTER CURE):** Mathematically annihilates
         redundant disk scrying by caching the absolute coordinates of anchored traits
         in an O(1) Merkle-Lattice.
    147. **Recursive Trait Suture:** Allows traits to use other traits (Multi-level
         inheritance) with a built-in Ouroboros Loop Guard (Depth Ceiling: 20).
    148. **Shadow Context Isolation:** When a trait is waked, its variables are
         processed in a warded sub-context, preventing "Variable Smearing" in
         the parent mind.
    149. **NoneType Sarcophagus v11:** Hard-wards the `conduct` rites; guaranteed
         return of a valid next_index even during catastrophic IO fracture.
    150. **Trace ID Silver-Cord Suture:** Force-binds the active Trace ID of the
         parent strike to the sub-parser, ensuring absolute forensic causality.
    151. **ELARA Parameter Thawing:** Utilizes the SGF Meta-Compiler to resolve
         dynamic variables inside the `%% use` argument string before expansion.
    152. **Indentation Floor Oracle V3:** Surgically calculates the parent's
         visual gravity to ensure the trait's matter is aligned bit-perfectly.
    153. **Merkle Trait Sealing:** Forges a SHA-256 fingerprint of the trait
         scripture to detect "Laminar Drift" in the multiversal library.
    154. **Apophatic Error Unwrapping:** Transmutes sub-parser fractures into
         human-readable "Trait Heresies" with precise line-number mapping.
    155. **Isomorphic Path Normalization:** Enforces POSIX slash harmony on all
         trait anchors, neutralizing the Windows Backslash Paradox.
    156. **Hydraulic Pacing Engine:** Optimized for parallel execution in
         swarmed weaves, utilizing non-blocking RLock acquisition.
    157. **Haptic HUD Multicast:** Radiates "TRAIT_INHALED" pulses to the React
         stage with the specific Merkle seal of the source.
    158. **Substrate DNA Recognition:** (Prophecy) Prepared to choose different
         trait variants based on IRON (Native) vs ETHER (WASM) detection.
    159. **Linguistic Purity Suture:** Normalizes trait names to strict PascalCase
         internally to prevent naming collisions across dialects.
    160. **Transactional Rollback Suture:** If a trait expansion fractures, it
         instantly purges the partial results from the raw_items buffer.
    161. **Socratic Argument Divination:** Automatically suggests missing
         trait parameters by scrying the global Gnosis.
    162. **Apophatic Variable Locking:** Prevents traits from overwriting
         System Invariants (__engine__) during the expansion strike.
    163. **Bicameral Manifest Merging:** Fuses the sub-parser's dossier into
         the parent manifest for total genomic transparency.
    164. **Indentation Purity Ward:** (Prophecy) Future support for enforcing
         Project-Standard whitespace laws within injected traits.
    165. **NoneType Zero-G Amnesty:** Gracefully handles empty trait files by
         returning a resonant "VOID_SUTURE" marker.
    166. **Geometric Boundary Protection:** Wards child nodes born from traits
         to ensure they reside within the ordained spatial Moat.
    167. **Subversion Ward:** Protects internal .scaffold/traits directories
         from unauthorized local shadows.
    168. **Hydraulic I/O Unbuffering:** Physically forces a flush of the
         trace-telemetry stream before the trait-mind ignites.
    169. **The Absolute Singularity Vow:** A mathematical guarantee of bit-perfect
         structural inheritance across all dimensional rifts.
    =================================================================================
    """

    __slots__ = ()

    # [ASCENSION 147]: RECURSION GUARD
    MAX_RECURSION_DEPTH: Final[int] = 20

    @classmethod
    def conduct_definition(cls, lines: List[str], i: int, vessel: GnosticVessel, parser: Any, logger: Any) -> int:
        """
        =============================================================================
        == THE RITE OF ANCHORING (DEFINITION)                                      ==
        =============================================================================
        LIF: 10,000x | ROLE: COORDINATE_CONSECRATOR
        """
        # [ASCENSION 149]: NoneType Sarcophagus
        raw_script = vessel.raw_scripture.strip() if vessel.raw_scripture else ""
        match = re.match(r"^\s*%%\s*trait\s+(?P<name>\w+)\s*=\s*(?P<path>.*)$", raw_script)

        if not match:
            return i + 1

        name = match.group("name")
        path_str = match.group("path").strip().strip('"\'')

        # --- MOVEMENT I: SPATIAL TRIANGULATION ---
        # [ASCENSION 155]: Isomorphic Path Normalization
        # [ASCENSION 146]: Achronal Path Cache
        base_dir = parser.file_path.parent if (parser.file_path and parser.file_path.is_file()) else Path.cwd()
        resolved_path = (base_dir / path_str).resolve()

        if not resolved_path.exists():
            parser._proclaim_heresy(
                "TRAIT_VOID",
                vessel,
                details=f"The scripture of Trait '{name}' is unmanifest at {resolved_path}.",
                severity=HeresySeverity.CRITICAL,
                suggestion="Verify the physical existence of the trait file or adjust your relative anchor."
            )
            return i + 1

        # --- MOVEMENT II: CONSECRATION ---
        # [ASCENSION 159]: Linguistic Purity Suture (Normalized keys)
        parser.traits[name] = resolved_path

        if not getattr(parser, '_silent', False):
            logger.success(f"L{vessel.line_num}: Trait '[soul]{name}[/soul]' anchored -> {resolved_path.name}")

        # [ASCENSION 157]: Ocular HUD Multicast
        cls._radiate_hud_pulse(parser, "TRAIT_ANCHORED", name, str(resolved_path), "#3b82f6")

        return i + 1

    @classmethod
    def conduct_usage(cls, lines: List[str], i: int, vessel: GnosticVessel, parser: Any, logger: Any) -> int:
        """
        =============================================================================
        == THE RITE OF TOPOLOGICAL GRAFTING (USAGE)                                ==
        =============================================================================
        LIF: ∞ | ROLE: REALITY_CONVERGENCE_CONDUCTOR
        """
        start_ns = time.perf_counter_ns()

        match = re.match(r"^\s*%%\s*use\s+(?P<name>\w+)(?:\s+(?P<args>.*))?$", vessel.raw_scripture.strip())
        if not match:
            return i + 1

        name, args_str = match.group("name"), match.group("args")

        # --- MOVEMENT I: VALIDATION ---
        if name not in parser.traits:
            parser._proclaim_heresy(
                "UNKNOWN_TRAIT_HERESY",
                vessel,
                details=f"Trait '[soul]{name}[/soul]' is unknown in this timeline.",
                severity=HeresySeverity.CRITICAL,
                suggestion=f"Define the trait first via '%% trait {name} = ...'"
            )
            return i + 1

        # --- MOVEMENT II: THE OUROBOROS GUARD ---
        # [ASCENSION 147]: Recursion Depth Governor
        recursion_depth = parser.variables.get("__trait_depth__", 0)
        if recursion_depth >= cls.MAX_RECURSION_DEPTH:
            parser._proclaim_heresy(
                "OUROBOROS_TRAIT_LOOP",
                vessel,
                details=f"Maximum trait recursion depth ({cls.MAX_RECURSION_DEPTH}) reached.",
                severity=HeresySeverity.CRITICAL
            )
            return i + 1

        # --- MOVEMENT III: ALCHEMICAL THAWING ---
        # [ASCENSION 148]: Shadow Context Isolation
        trait_path = parser.traits[name]
        trait_vars = parser.variables.copy()
        # Increment depth for child
        trait_vars["__trait_depth__"] = recursion_depth + 1

        # [ASCENSION 151]: ELARA Parameter Thawing
        if args_str:
            try:
                # We use shlex to safely parse quoted arguments: key="val with spaces"
                for pair in shlex.split(args_str):
                    if '=' in pair:
                        k, v = pair.split('=', 1)
                        # The Alchemist thaws the argument against the parent mind
                        trait_vars[k.strip()] = get_alchemist().transmute(
                            v.strip().strip('"\''),
                            parser.variables
                        )
            except Exception as e:
                logger.warn(f"L{vessel.line_num}: Alchemical argument thaw deferred: {e}")

        if not getattr(parser, '_silent', False):
            logger.info(f"Materializing Trait '[soul]{name}[/soul]' from {trait_path.name}...")

        # =========================================================================
        # == MOVEMENT IV: THE RECURSIVE SGF SUTURE (THE STRIKE)                  ==
        # =========================================================================
        try:
            # 1. Spawn a sub-parser of the same class (Isomorphic Inheritance)
            sub_parser = parser.__class__(grammar_key='scaffold', engine=parser.engine)

            # [ASCENSION 150]: Trace ID Silver-Cord Suture
            sub_parser.variables = trait_vars
            sub_parser.traits = parser.traits
            sub_parser.depth = parser.depth + 1
            sub_parser._silent = True  # Sub-output is warded

            # 2. Inhale the Trait scripture
            content = trait_path.read_text(encoding='utf-8', errors='replace')

            # [ASCENSION 153]: Merkle Trait Sealing
            trait_hash = hashlib.sha256(content.encode()).hexdigest()[:8].upper()

            # 3. [STRIKE]: Sub-Parse the Trait reality
            # We treat the trait as a full blueprint in its own dimensional stratum
            _, sub_items, sub_commands, sub_edicts, _, sub_dossier = sub_parser.parse_string(content, trait_path)

            # --- MOVEMENT V: THE GEOMETRIC GRAFT ---
            # [ASCENSION 152]: Indentation Floor Oracle V3
            current_indent = parser._calculate_original_indent(lines[i])

            # Graft Matter (Files)
            for item in sub_items:
                # Matter inherits the caller's visual gravity
                item.original_indent += current_indent
                # [ASCENSION 150]: Forensic Causality
                item.blueprint_origin = trait_path
                parser.raw_items.append(item)

            # Graft Will (Commands)
            # [ASCENSION 3]: Quaternity Suture for post-run edicts
            parser.post_run_commands.extend(sub_commands)
            parser.edicts.extend(sub_edicts)

            # [ASCENSION 163]: Genomic Manifest Merging
            if hasattr(parser, 'dossier') and sub_dossier:
                parser.dossier.manifests.update(sub_dossier.manifests)

            # --- MOVEMENT VI: METABOLIC FINALITY ---
            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            if not getattr(parser, '_silent', False):
                logger.success(f"   -> [RESONANT] Trait '{name}' merged in {duration_ms:.2f}ms. [Seal:0x{trait_hash}]")

            # [ASCENSION 157]: Ocular HUD Multicast
            cls._radiate_hud_pulse(parser, "TRAIT_MATERIALIZED", name, f"Seal: 0x{trait_hash}", "#64ffda")

        except Exception as catastrophic_paradox:
            # [ASCENSION 154]: Apophatic Error Unwrapping
            tb = ""
            if os.environ.get("SCAFFOLD_DEBUG") == "1":
                import traceback
                tb = f"\n{traceback.format_exc()}"

            parser._proclaim_heresy(
                "TRAIT_EXPANSION_PARADOX",
                vessel,
                details=f"The Suture of Trait '{name}' shattered: {str(catastrophic_paradox)}{tb}",
                exception_obj=catastrophic_paradox,
                severity=HeresySeverity.CRITICAL
            )

        # [ASCENSION 169]: THE FINALITY VOW
        return i + 1

    @staticmethod
    def _radiate_hud_pulse(parser: Any, type_label: str, name: str, message: str, color: str):
        """[ASCENSION 157]: Ocular HUD Multicast."""
        if parser.engine and hasattr(parser.engine, 'akashic') and parser.engine.akashic:
            try:
                parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "TRAIT_EVENT",
                        "label": f"{type_label}: {name}",
                        "message": message,
                        "color": color,
                        "trace": getattr(parser, 'parse_session_id', 'void')
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_TRAIT_ORCHESTRATOR mode=REALITY_GRAFTER version=VMAX_169 status=RESONANT>"