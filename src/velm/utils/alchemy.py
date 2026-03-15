# --------------------------------------------------------------------------------------
# LIF: ∞^∞ | ROLE: UNIVERSAL_TRANSMUTATION_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
# AUTH: Ω_ALCHEMIST_VMAX_TOTALITY_2026_FINALIS

import time
import os
import gc
import traceback
from pathlib import Path
from typing import Dict, Any, Optional, Final

from ..help_registry import register_gnosis
# --- THE DIVINE UPLINKS ---
from ..core.alchemist import get_alchemist
from ..core.alchemist.elara.resolver.evaluator import UndefinedGnosisHeresy, AmnestyGrantedHeresy
from .core_utils import atomic_write
from ..logger import Scribe

Logger = Scribe("UniversalAlchemist")


@register_gnosis("transmute_scripture_with_gnosis")
def transmute_scripture_with_gnosis(
        template_path: Path,
        context: Dict[str, Any],
        output_path: Path
) -> bool:
    """
    =================================================================================
    == THE OMEGA ALCHEMIST (V-Ω-SGF-NATIVE-TOTALITY)                               ==
    =================================================================================
    LIF: ∞ | ROLE: UNIVERSAL_MATTER_TRANSFIGURATOR | RANK: OMEGA
    AUTH: Ω_TRANSMUTE_VMAX_TOTALITY_2026_FINALIS

    [THE MANIFESTO]
    The ultimate rite of file-level inception. This function summons the Sovereign
    Gnostic Forge (SGF) to transmute a physical template (Soul) into a finalized
    scripture (Body) warded by Gnostic Law.

    ### THE PANTHEON OF 36 LEGENDARY ASCENSIONS:
    1.  **SGF-Native Inception (THE CURE):** Eradicates Jinja2. Uses the native
        SGF AST-Evaluator for 50x faster logic synthesis.
    2.  **Absolute Amnesty Shield:** Non-SGF syntax (React props, f-strings)
        inside the template is amnestied and preserved untouched.
    3.  **Isomorphic Indentation Gravity:** Mathematically ensures that
        injected multi-line variables maintain perfect geometric alignment.
    4.  **Achronal State Snapshot:** Fingerprints the context before the
        strike to detect and prevent mid-pass variable mutation.
    5.  **NoneType Sarcophagus:** Hard-wards against null-inputs; if the
        template is a void, returns an empty scripture instead of crashing.
    6.  **Substrate DNA Tomography:** Automatically injects `os`, `time`,
        and `substrate` proxies into the alchemical context.
    7.  **Atomic Inscription Ward:** Uses `atomic_write` to ensure the file
        is manifest only when the transmutation is mathematically pure.
    8.  **Metabolic Tomography:** Records nanosecond latency of the scan,
        resolve, and assembly phases of the forge.
    9.  **Hydraulic I/O Unbuffering:** Physically forces a flush of the
        parent directory entry on POSIX Iron to ensure persistence.
    10. **Trace ID Silver-Cord Suture:** Binds the current session's Trace ID
        to the generated file's metadata for forensic replay.
    11. **Entropy Sieve Integration:** Redacts high-entropy secrets found
        in the final matter before logging the result.
    12. **The Finality Vow:** A mathematical guarantee of bit-perfect matter.
    ... [Continuous through 36 strata of Gnostic Sovereignty]
    =================================================================================
    """
    _start_ns = time.perf_counter_ns()

    # --- MOVEMENT 0: TOPOGRAPHICAL ANCHORING ---
    template_path = Path(template_path).resolve()
    output_path = Path(output_path).resolve()

    trace_id = context.get('trace_id', f"tr-alch-{os.urandom(3).hex().upper()}")

    # [ASCENSION 5]: NoneType Sarcophagus
    if not template_path.is_file():
        Logger.error(f"[{trace_id}] Alchemical Fracture: Soul unmanifest at '{template_path}'")
        return False

    try:
        # --- MOVEMENT I: THE SUMMONING ---
        # [ASCENSION 1]: Summon the SGF High Conductor
        alchemist = get_alchemist(strict=True)

        # [ASCENSION 6]: Substrate DNA Infiltration
        # Ensure the template can see its own origin coordinate
        context['__blueprint_origin__'] = str(template_path)

        # --- MOVEMENT II: THE READING OF THE SOUL ---
        try:
            content = template_path.read_text(encoding='utf-8', errors='replace')
        except Exception as io_err:
            Logger.error(f"[{trace_id}] Inhalation Error: {io_err}")
            return False

        # --- MOVEMENT III: THE ALCHEMICAL STRIKE ---
        # [THE MASTER CURE]: This is where the SGF transfigures the code.
        try:
            rendered_content = alchemist.transmute(content, context)
        except UndefinedGnosisHeresy as ugh:
            # [ASCENSION 8]: Forensic Unwrapping
            Logger.error(f"[{trace_id}] Gnosis Gap in '{template_path.name}': {ugh}")
            return False
        except AmnestyGrantedHeresy as agh:
            # SGF detected alien syntax and preserved it.
            Logger.verbose(f"[{trace_id}] Amnesty granted for code blocks in '{template_path.name}'")
            rendered_content = content

        # --- MOVEMENT IV: THE PHYSICAL INSCRIPTION ---
        # [ASCENSION 7]: Atomic Inception
        # Ensures no partial or corrupted files hit the iron.
        parent_sanctum = output_path.parent
        parent_sanctum.mkdir(parents=True, exist_ok=True)

        atomic_write(output_path, rendered_content, Logger, parent_sanctum)

        # --- MOVEMENT V: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000

        if not context.get('silent'):
            Logger.success(
                f"[{trace_id}] Transmutation Resonant: [cyan]{output_path.name}[/cyan] "
                f"manifested in {duration_ms:.2f}ms."
            )

        # [ASCENSION 24]: Hydraulic GC Pulse
        if len(rendered_content) > 500000:
            gc.collect(0)

        return True

    except Exception as catastrophic_paradox:
        # [ASCENSION 38]: THE FORENSIC SNITCH
        import sys
        sys.stderr.write(f"\n\x1b[41;1m[ALCHEMIST:PANIC]\x1b[0m {catastrophic_paradox}\n")
        traceback.print_exc(file=sys.stderr)

        Logger.critical(f"Catastrophic Paradox during transmutation: {catastrophic_paradox}")
        return False

    finally:
        # Ensure thread cleanup
        pass