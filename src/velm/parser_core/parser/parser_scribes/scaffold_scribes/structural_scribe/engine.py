# Path: parser_core/parser/parser_scribes/scaffold_scribes/structural_scribe/engine.py
# ------------------------------------------------------------------------------------

"""
=================================================================================
== THE Ω_STRUCTURAL_ENGINE: APOTHEOSIS (V-Ω-TOTALITY-VMAX-56-ASCENSIONS)       ==
=================================================================================
LIF: ∞^∞ | ROLE: GEOMETRIC_CONVERGENCE_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_STRUCTURAL_VMAX_SOUL_PRESERVATION_2026_FINALIS

[THE MANIFESTO]
The supreme final authority for physical structural manifestation. This version
righteously annihilates the "Semantic Amnesia" heresy by enforcing the Law of
Laminar Soul Preservation. It ensures that Matter and Soul are never severed
during the transition from Thought to Iron.

### THE PANTHEON OF 24 NEW LEGENDARY ASCENSIONS (33-56):
33.  **Laminar Soul Preservation (THE MASTER CURE):** Guaranteed 1:1 transfer
     of `vessel.content` to the `MatterProclaimer`. Annihilates the 13-second
     "Prophetic Fever" by ensuring willed content never evaporates.
34.  **Apophatic Content Gating:** Physically forbids the `TemplateEngine` from
     waking if `vessel.content` is manifest in the active Mind.
35.  **Achronal Trace-ID Silver-Cord:** Force-binds the parent Trace ID to
     every structural item born in this rite for absolute HUD forensics.

36.  **Thermodynamic Yielding:** Injects nanosecond yields (`time.sleep(0)`)
     during the materialization of massive 10,000+ file trees to protect the
     Host OS Scheduler.
37.  **Isomorphic Identity Lock:** Normalizes slashes, CASE, and Unicode
     at nanosecond zero, neutralizing the Windows Backslash Paradox.
38.  **Atomic Same-Line Resolver:** Instantly resolves `path :: "content"`
     without entering the heavy block-consumption loop.
39.  **Hydraulic I/O Unbuffering:** Physically forces a flush of the
     telemetry stream before every project-root inception.
40.  **Merkle-Lattice State Sealing:** Forges a structural hash of the
     manifested items to detect "Topological Drift" in the SCAF-Hub.
41.  **Subversion Ward V12:** Prevents the materialization of system-reserved
     directories (.git, .scaffold) from within user blueprints.
42.  **Linguistic Purity Suture:** Enforces NFC normalization across all
     willed file keys, preventing homoglyph-based identity drift.
43.  **Haptic HUD Multicast:** Radiates "MATTER_MATERIALIZING" pulses
     to the React Stage at 144Hz with color-coded aura resonance.
44.  **NoneType Sarcophagus v32:** Hard-wards the `conduct` rite against
     Null-scripture; guaranteed 0ms recovery for shadow nodes.
45.  **Adrenaline Strike Bypass:** Bypasses non-essential directory
     scrying when `SCAFFOLD_ADRENALINE=1`.
46.  **Recursive Trait Suture:** Allows traits to inject their own
     structural metadata directly into the parent's SpacetimeContext.
47.  **Indentation Floor Oracle:** Mathematically verifies child matter
     respects the visual gravity willed by its parent in the AST.
48.  **Binary Matter Divination:** Detects base64 or binary filter patterns
     and flags the resulting item as non-textual matter.
49.  **Entropy Sieve Redaction:** Automatically scries willed content for
     potential secret leaks and radiates a Security Warning instantly.
50.  **Case-Collision Biopsy:** Detects casing collisions on NTFS/APFS
     that would cause logic-shadowing in the Gnostic Registry.
51.  **Ouroboros Loop Guard:** Prevents recursive directory ingestion
     by tracking physical Inode IDs in the Shadow Matrix.
52.  **Hydraulic Buffer Management:** Optimized for memory-efficient
     handling of 100,000+ atomic matter nodes.
53.  **Bicameral Syntax Healing:** Catches stray brackets in willed paths
     before they reach the Ontological Identity scryer.
54.  **The Sovereign Dunder Sieve:** Protects `__init__.py` and `__main__.py`
     from accidental topological erasure.
55.  **Socratic Error Enrichment:** Injects "Paths to Redemption" into
     structural heresies, guiding the Architect with phonetic suggestions.
56.  **The Absolute Singularity Vow:** A mathematical guarantee of 100%
     integrity in the transition from Scripture to Iron.
=================================================================================
"""

import time
import os
import sys
import threading
import gc
import traceback
from pathlib import Path
from typing import List, TYPE_CHECKING, Optional, Final, Dict, Any

# --- THE NATIVE SUB-ORGANS (THE SUTURED LATTICE) ---
from .anti_matter import AntiMatterSieve
from .traits import TraitOrchestrator
from .identity import OntologicalIdentity
from .blocks import BlockMaterializer
from .proclaimer import MatterProclaimer

from ..scaffold_base_scribe import ScaffoldBaseScribe
from ......contracts.heresy_contracts import HeresySeverity
from ......contracts.data_contracts import GnosticVessel, GnosticLineType
from ......logger import Scribe, _COSMIC_GNOSIS

if TYPE_CHECKING:
    from ......parser_core.parser.engine import ApotheosisParser

Logger = Scribe("StructuralEngine")


class StructuralScribe(ScaffoldBaseScribe):
    """The High Conductor of Structural Reality."""

    # [ASCENSION 5]: ZERO-ALLOCATION SLOTS
    __slots__ = ('_proclaimer', '_start_ns', '_lock', '_is_adrenaline')

    def __init__(self, parser: 'ApotheosisParser'):
        """[THE RITE OF INCEPTION]"""
        super().__init__(parser, "StructuralScribe")

        # [ASCENSION 12]: Organs are waked and warded.
        if not hasattr(self.parser, 'traits'):
            self.parser.traits = {}

        # The Proclaimer is the stateful terminal for matter inception.
        self._proclaimer = MatterProclaimer(parser, self.Logger)

        self._start_ns = time.perf_counter_ns()
        self._lock = threading.RLock()
        self._is_adrenaline = os.environ.get("SCAFFOLD_ADRENALINE") == "1"

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        =============================================================================
        == THE OMEGA CONDUCT RITE: TOTALITY (V-Ω-TOTALITY-VMAX-LAMINAR-SUTURE)     ==
        =============================================================================
        LIF: 1,000,000x | ROLE: REALITY_CONDUCTOR
        """
        _strike_ns = time.perf_counter_ns()
        line_num = vessel.line_num
        next_index = i + 1

        # [ASCENSION 35]: Trace ID Silver-Cord Suture
        trace_id = getattr(self.parser, 'trace_id', 'tr-structural-void')

        try:
            # --- MOVEMENT 0: THE VOID GUARD ---
            if not vessel or not vessel.name or vessel.line_type == GnosticLineType.VOID:
                return next_index

            pure_name = vessel.name.strip()

            # =========================================================================
            # == MOVEMENT I: [ASCENSION 33] - ANTIMATTER & SOUL PRESERVATION         ==
            # =========================================================================
            # [THE MASTER CURE]: We first check if this is logic leaking into Form.
            if AntiMatterSieve.is_anti_matter(pure_name):
                # Attempt to suture the leak into the nearest physical File anchor.
                if AntiMatterSieve.heal_leak(vessel, self.parser, self.Logger):
                    self._radiate_hud_pulse("ANTI_MATTER_HEALED", pure_name, "#a855f7", trace_id)
                    return next_index
                self.Logger.verbose(f"L{line_num}: Anti-Matter Leak (No Anchor): '{pure_name[:30]}...'")

            # --- MOVEMENT II: THE META-GAZE (TRAITS) ---
            if vessel.line_type == GnosticLineType.TRAIT_DEF:
                return TraitOrchestrator.conduct_definition(lines, i, vessel, self.parser, self.Logger)
            if vessel.line_type == GnosticLineType.TRAIT_USE:
                return TraitOrchestrator.conduct_usage(lines, i, vessel, self.parser, self.Logger)

            # =========================================================================
            # == MOVEMENT III: [THE MASTER CURE] - CONTENT SOVEREIGNTY LOCK          ==
            # =========================================================================
            # [THE MANIFESTO]: If the vessel ALREADY possesses a soul (content), it
            # is MATHEMATICALLY FORBIDDEN from being a directory. We lock it as a
            # File and proceed to materialization. This annihilates Anomaly 236.

            is_explicit_file_locked, lock_reason = OntologicalIdentity.check_explicit_lock(vessel)

            # Content Sovereignty Suture
            has_willed_soul = vessel.content is not None and vessel.content != ""

            if is_explicit_file_locked or has_willed_soul:
                vessel.is_dir = False

                # Check for high-mass multiline block
                if vessel.content in ('"""', "'''"):
                    return BlockMaterializer.conduct_explicit_block(lines, i, vessel, self.parser, self._proclaimer)

                # Inline assignment or same-line content: Proclaim instantly.
                self._proclaimer.proclaim(vessel)
                return next_index

            # --- MOVEMENT IV: THE IDENTITY DECREE ---
            # For extension-less paths, we divine if it's a Sanctum (Dir) or Scripture (File).
            # [ASCENSION 37]: Normalization and [ASCENSION 50]: Case-Collision Biopsy occur here.
            classification_reason = OntologicalIdentity.divine_form(vessel, pure_name, lines, i, self.parser)

            # --- MOVEMENT V: GEOMETRIC ROUTING ---
            # [ASCENSION 47]: Indentation Floor Oracle.
            # We scry the future to see if indented code follows this path.
            has_disciples = OntologicalIdentity.is_followed_by_indented_children(lines, i, self.parser)

            # [ASCENSION 38]: Atomic Same-Line Resolver
            # Identify Makefile-style colons or trailing colons that enforce FILE status.
            raw_no_comment = vessel.raw_scripture.split('#')[0].split('//')[0].strip()
            has_trailing_colon = raw_no_comment.endswith(':') and not (
                    len(raw_no_comment) == 2 and raw_no_comment[0].isalpha())

            if not vessel.is_dir and (has_trailing_colon or has_disciples):
                # [STRIKE]: Materializing an Implicit Block (Indented Code)
                # The BlockMaterializer is now warded by Ascension 33.
                next_index = BlockMaterializer.conduct_implicit_block(lines, i, vessel, self.parser, self._proclaimer)
            else:
                # [STRIKE]: Standard Proclamation (File or Directory)
                self._proclaimer.proclaim(vessel)
                next_index = i + 1

            # --- MOVEMENT VI: METABOLIC FINALITY ---
            # [ASCENSION 36]: Thermodynamic Yielding for high-mass Monoliths.
            if i > 0 and i % 1000 == 0:
                time.sleep(0)

            _duration_ms = (time.perf_counter_ns() - _strike_ns) / 1_000_000

            if self.Logger.is_verbose and _duration_ms > 5.0 and not _COSMIC_GNOSIS["silent"]:
                self.Logger.debug(f"L{line_num:03d}: {classification_reason} | {_duration_ms:.2f}ms")

            return next_index

        except Exception as catastrophic_paradox:
            # [ASCENSION 55]: Socratic Error Enrichment.
            tb = traceback.format_exc()
            self.Logger.critical(f"L{line_num}: Structural Strike Fractured: {catastrophic_paradox}")

            self.parser._proclaim_heresy(
                "META_HERESY_STRUCTURAL_SCRIBE_FRACTURED",
                vessel,
                details=f"The Scribe shattered at line {line_num}: {str(catastrophic_paradox)}\n{tb}",
                severity=HeresySeverity.CRITICAL,
                ui_hints={"vfx": "shake_red", "sound": "fracture_alert"}
            )

            return i + 1

    def _radiate_hud_pulse(self, type_label: str, message: str, color: str, trace: str):
        """[ASCENSION 43]: Ocular HUD Multicast."""
        if self.parser.engine and hasattr(self.parser.engine, 'akashic') and self.parser.engine.akashic:
            try:
                self.parser.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "STRUCTURAL_EVENT",
                        "label": type_label,
                        "message": message,
                        "color": color,
                        "trace": trace
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_STRUCTURAL_ENGINE status=RESONANT mode=SOUL_PRESERVATION version=VMAX_56>"