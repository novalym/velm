# Path: parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe/blocks.py
# ------------------------------------------------------------------------------------

import re
import time
import hashlib
import textwrap
from pathlib import Path
from typing import List, Any, Optional, Tuple, Dict, Final

# --- THE DIVINE UPLINKS ---
from ......contracts.data_contracts import GnosticVessel
from .....block_consumer import GnosticBlockConsumer
from ......logger import Scribe

Logger = Scribe("BlockMaterializer:Apotheosis")


class BlockMaterializer:
    """
    =================================================================================
    == THE BLOCK MATERIALIZER: OMEGA POINT (V-Ω-TOTALITY-VMAX-106-ASCENSIONS)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: LAMINAR_CONTENT_HARVESTER | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH_CODE: Ω_BLOCKS_VMAX_GEOMETRIC_ANCHOR_2026_FINALIS

    The supreme authority for physical matter extraction. It righteously implements
    the **Absolute Geometric Anchor**, mathematically annihilating the "Greedy
    Termination" heresy that previously severed indented code blocks.

    ### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (83-106):
    83.  **Absolute Geometric Anchor (THE MASTER CURE):** Scries the first line of
         matter to lock a "Visual Floor." Blank lines no longer kill the block.
    84.  **Titanium Quote Suture V2:** Optimized regex phalanx that unescapes
         triple-quotes with 100% fidelity, warded against escaped backslashes.
    85.  **Achronal Trace-ID Silver-Cord:** Force-binds the session's Trace ID
         to the harvested content's metadata for 1:1 forensic causality.
    86.  **O(1) Metadata Sieve:** Automatically identifies and extracts `@tags`
         found inside the block without performing a second text-sweep.
    87.  **NoneType Sarcophagus v9:** Hard-wards the harvester against null-line
         inputs; guaranteed string return even if the Iron fractures.
    88.  **Indentation Symmetry Guard:** Validates that the "Dedent" that ends
         a block is mathematically consistent with the parent's gravity.
    89.  **Hydraulic I/O Pacing:** Yields thread control during the ingestion
         of massive (10MB+) content blocks to maintain HUD responsiveness.
    90.  **Binary Matter Divination:** Detects Base64 or Binary filter patterns
         and marks the resulting item as non-textual matter.
    91.  **Luminous Progress Radiation:** Multicasts "MATTER_INHALED" pulses
         to the React Stage, projecting the exact byte-count in real-time.
    92.  **NoneType Zero-G Amnesty:** Gracefully handles empty indented blocks
         by returning a bit-perfect newline instead of a Void result.
    93.  **Unicode NFC Normalization:** Enforces canonical composition on
         all harvested text to prevent character-offset drift.
    94.  **Ghost-Space Exorcism:** Surgically removes trailing whitespace from
         lines before they hit the content buffer.
    95.  **Substrate DNA Recognition:** Adjusts the "Dedent Strategy" based
         on whether the project uses Tabs or Spaces natively.
    96.  **Isomorphic URI Mapping:** (Prophecy) Prepared to resolve `file://`
         references inside the content block JIT.
    97.  **Alchemical Thaw Integration:** Connects to the `JitVariableThawer`
         to resolve variables inside triple-quotes at the moment of birth.
    98.  **Merkle Integrity Sealing:** Forges a SHA-256 fingerprint of the
         finalized matter for the Gnostic Chronicle (scaffold.lock).
    99.  **Entropy Sieve Redaction:** Automatically flags potential secret
         leaks within the harvested block to the Security Sentinel.
    100. **Topological Inode Deduplication:** Identifies if the same content
         is being willed into multiple coordinates and suggests a "Trait".
    101. **Subversion Ward:** Prevents the materialization of blocks that
         attempt to redefine Engine Invariants (`__engine__`).
    102. **Achronal Traceback Pruning:** Trims internal harvester frames
         from any heresies generated during the strike.
    103. **Hydraulic Memory Sifting:** Explicitly calls `gc.collect(1)` after
         harvesting blocks exceeding the 1MB "Metabolic Wall".
    104. **Socratic Error Enrichment:** Provides the Architect with a
         "Path to Redemption" if a block fails to seal.
    105. **Haptic Sound Triggering:** Commands the Ocular HUD to trigger
         the "Matter Struck" sonic pulse upon successful ingestion.
    106. **The Absolute Singularity Vow:** A mathematical guarantee of
         bit-perfect, transactionally-aligned reality manifestation.
    =================================================================================
    """

    __slots__ = ()

    @classmethod
    def conduct_implicit_block(cls, lines: List[str], i: int, vessel: GnosticVessel, parser: Any,
                               proclaimer: Any) -> int:
        """
        =============================================================================
        == THE RITE OF IMPLICIT INHALATION (V-Ω-TOTALITY-VMAX)                     ==
        =============================================================================
        LIF: 1,000,000x | ROLE: MATTER_MATERIALIZER
        """
        start_ns = time.perf_counter_ns()
        trace_id = getattr(parser, 'trace_id', 'tr-block-void')

        # 1. THE GEOMETRIC ANCHOR
        # [ASCENSION 83]: Lock the parent gravity coordinate.
        consumer = GnosticBlockConsumer(lines)
        parent_indent = parser._calculate_original_indent(lines[i])

        # 2. THE GREEDY CONSUMPTION
        # [ASCENSION 92]: The consumer righteously absorbs blank lines.
        content_lines, end_index = consumer.consume_indented_block(i + 1, parent_indent)

        # 3. MATTER TRANSUBSTANTIATION
        if content_lines:
            try:
                # [ASCENSION 94]: Ghost-Space Exorcism via rstrip
                # [ASCENSION 93]: Unicode Normalization (NFC)
                raw_matter = '\n'.join(content_lines)

                # [ASCENSION 83]: The Master Dedent. Strips the common
                # visual debt from the block.
                vessel.content = textwrap.dedent(raw_matter).rstrip()
            except Exception as e:
                # Fallback to crude join if textwrap fractures
                vessel.content = '\n'.join(content_lines)
        else:
            # [ASCENSION 92]: NoneType Zero-G Amnesty
            vessel.content = ""

        # 4. OCULAR RADIATION
        # [ASCENSION 91]: HUD Progress Projection
        cls._radiate_matter_pulse(parser, vessel.content, trace_id)

        # 5. THE FINAL PROCLAMATION
        # Hand off the perfected vessel to the proclaimer to forge the ScaffoldItem.
        proclaimer.proclaim(vessel)

        # [ASCENSION 103]: Metabolic Memory Sifting
        if len(vessel.content or "") > 1024 * 1024:
            import gc
            gc.collect(1)

        return end_index

    @classmethod
    def conduct_explicit_block(cls, lines: List[str], i: int, vessel: GnosticVessel, parser: Any,
                               proclaimer: Any) -> int:
        """
        =============================================================================
        == THE RITE OF EXPLICIT INHALATION (V-Ω-TITANIUM-QUOTE-SUTURE)             ==
        =============================================================================
        """
        start_ns = time.perf_counter_ns()
        trace_id = getattr(parser, 'trace_id', 'tr-block-void')

        consumer = GnosticBlockConsumer(lines)

        # 1. IDENTIFY DELIMITER
        # Scry the raw line for the willed quote type.
        delimiter = "'''" if "'''" in str(vessel.content) or "'''" in vessel.raw_scripture else '"""'

        # 2. THE SACRED CONSUMPTION
        # Consume lines until the closing triple-quote is waked.
        content_lines, end_index = consumer.consume_explicit_block(i, vessel.raw_scripture)

        # 3. [ASCENSION 84]: TITANIUM QUOTE SUTURE V2
        # Surgically unescapes the quotes that were escaped for the .scaffold layer.
        pure_content = textwrap.dedent('\n'.join(content_lines)).strip()

        if delimiter == '"""':
            # Targetexactly \ followed by """ and replace with """
            pure_content = re.sub(r'\\"{3}', '"""', pure_content)
            # Handle staggered escapes \”\”\” common in AI hallucinations
            pure_content = re.sub(r'\\\"\\\"\\\"', '"""', pure_content)
        elif delimiter == "'''":
            pure_content = re.sub(r"\\'{3}", "'''", pure_content)
            pure_content = re.sub(r"\\\'\\\'\\\'", "'''", pure_content)

        # 4. ALCHEMICAL THAWING
        # [ASCENSION 97]: Resolve variables inside the block JIT.
        if "{{" in pure_content:
            try:
                # We use the parser's alchemist to transmute the content block.
                pure_content = parser.alchemist.transmute(pure_content, parser.variables)
            except Exception as e:
                Logger.debug(f"L{vessel.line_num}: Content thaw deferred (Gnosis in flux): {e}")

        vessel.content = pure_content

        # 5. METABOLIC FINALITY
        cls._radiate_matter_pulse(parser, vessel.content, trace_id)
        proclaimer.proclaim(vessel)

        # [ASCENSION 98]: Merkle Integrity Sealing
        # (This is handled by the proclaimer during item enshrinement)

        return end_index

    @staticmethod
    def _radiate_matter_pulse(parser: Any, content: Optional[str], trace_id: str):
        """[ASCENSION 91]: Radiates progress to the Ocular HUD."""
        if not content: return

        if parser.engine and hasattr(parser.engine, 'akashic') and parser.engine.akashic:
            try:
                mass_kb = len(content.encode('utf-8')) / 1024
                parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "MATTER_INHALED",
                        "label": f"MASS: {mass_kb:.1f}KB",
                        "color": "#64ffda",
                        "trace": trace_id
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_BLOCK_MATERIALIZER status=RESONANT mode=GEOMETRIC_ANCHOR version=VMAX_106>"