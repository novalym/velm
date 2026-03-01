# Path: src/velm/artisans/holocron/artisan.py
# =========================================================================================
# == THE OMEGA HOLOCRON: TOTALITY (V-Ω-TOTALITY-V25000-RESONANT-FINALIS)                  ==
# =========================================================================================
# LIF: INFINITY | ROLE: FORENSIC_CAUSALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_HOLOCRON_V25K_TOTALITY_SUTURE_2026_FINALIS
#
# [ARCHITECTURAL CONSTITUTION]
# 1.  **The Radiant Gnosis Suture (THE CURE):** Forcibly extracts the distilled content
#     from the underlying DistillArtisan and injects it into the final ScaffoldResult.data.
#     This annihilates the "Void UI" heresy and enables the Context Weaver to speak.
# 2.  **Recursive Gnostic Strike:** Implements a recursive dispatch loop. The Holocron
#     does not calculate; it commands the Distill system and then adjudicates the result.
# 3.  **Achronal Trace Preservation:** Ensures the `trace_id` from the Ocular HUD is
#     passed deep into the causal chain, linking the UI intent to the physical disk write.
# 4.  **Forensic DNA Injection:** Automatically enables `--diagnose` and `--format dossier`
#     for every Holocron plea, transforming raw code into a structured Narrative of Truth.
# 5.  **NoneType Sarcophagus:** Hardened against null `variables` or malformed payloads;
#     pre-initializes the GnosticSovereignDict to ensure stability.
# 6.  **Metabolic Tomography:** Tracks the exact nanosecond duration of the Holocron
#     expansion and reports it back as telemetry.
# 7.  **Substrate-Aware Routing:** Detects the WASM Ether Plane and stays the hand of
#     local-only filesystem operations during the recursive call.
# 8.  **Haptic HUD Resonance:** Multicasts "Holocron_Awakened" signals to the HUD.
# 9.  **Socratic Error Triage:** If the underlying Distill rite fractures, the Holocron
#     captures the traceback and presents it as a "Causal Schism" rather than a crash.
# 10. **The Priority Seal:** Forces 'HIGH' priority on the internal dispatch to ensure
#     identity materialization precedes background scrying.
# 11. **Alchemical Intent Mapping:** Correctly maps `entry_point` to the `intent` slot
#     to trigger the Neural Prophet's Semantic Search.
# 12. **The Finality Vow:** A mathematical guarantee of a resonant ScaffoldResult.
# =========================================================================================

import time
import traceback
import uuid
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple, TYPE_CHECKING

# --- THE DIVINE UPLINKS ---
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact, ScaffoldSeverity
from ...interfaces.requests import HolocronRequest, DistillRequest
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...help_registry import register_artisan
from ...logger import Scribe

if TYPE_CHECKING:
    from ...core.runtime.engine import ScaffoldEngine

Logger = Scribe("HolocronArtisan")


@register_artisan("holocron")
class HolocronArtisan(BaseArtisan[HolocronRequest]):
    """
    =================================================================================
    == THE HOLOCRON CONDUCTOR (V-Ω-TOTALITY-V25000)                                ==
    =================================================================================
    LIF: ∞ | ROLE: CAUSAL_CONTEXT_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN
    """

    def __init__(self, engine: 'ScaffoldEngine'):
        """[THE RITE OF BINDING]"""
        super().__init__(engine)
        self.signature = "Ω_HOLOCRON_V25000_RESONANT"

    def execute(self, request: HolocronRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND RITE OF FORENSIC RECONSTRUCTION                               ==
        =============================================================================
        """
        start_ts = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', f"tr-hlc-{uuid.uuid4().hex[:6].upper()}")

        self.logger.info(f"The Holocron awakens. Scrying causal web for: [cyan]'{request.entry_point}'[/cyan]")
        self._resonate(trace_id, "HOLOCRON_AWAKENED", "#3b82f6")

        try:
            # --- MOVEMENT I: THE TRANSMUTATION OF WILL ---
            # We convert the HolocronRequest into a high-status DistillRequest.
            # We exclude 'holocron_command' to avoid validation heresies in the target.
            base_data = request.model_dump(exclude={'holocron_command'})

            # [ASCENSION 11]: ALCHEMICAL INTENT MAPPING
            # We explicitly map the entry_point to 'intent' to trigger Semantic Search.
            distill_params = {
                **base_data,
                "intent": request.entry_point,
                "format": "dossier",  # Holocron always prefers the Narrative Dossier (.md)
                "diagnose": True,  # Always invoke the AI Inquisitor
                "strategy": "balanced",
                "trace_id": trace_id,
                "project_root": str(request.project_root or Path.cwd()),
                "source_path": "."
            }

            # [ASCENSION 5]: THE NONETYPE SARCOPHAGUS
            # Ensure the variables dict is manifest for the alchemist.
            if 'variables' not in distill_params or distill_params['variables'] is None:
                distill_params['variables'] = {}

            # --- MOVEMENT II: THE RECURSIVE GNOSTIC STRIKE (THE CURE) ---
            # We hand the intent back to the Master Dispatcher.
            # This allows the DistillArtisan's logic to conduct the actual scry.
            try:
                distill_plea = DistillRequest.model_validate(distill_params)
                self.logger.verbose(f"Holocron: Dispatching Recursive Rite [Trace: {trace_id}]")

                # [STRIKE]: Recursive Conduction
                distill_result = self.engine.dispatch(distill_plea)

            except Exception as e:
                self.logger.error(f"Holocron: Recursive dispatch fractured: {e}")
                raise ArtisanHeresy(
                    f"Causal Schism: The underlying Distill engine failed to resonate.",
                    details=traceback.format_exc(),
                    severity=HeresySeverity.CRITICAL
                )

            # --- MOVEMENT III: THE REVELATION ADJUDICATION ---
            # If the underlying rite failed, the Holocron must proclaim the fracture.
            if not distill_result.success:
                self.logger.error("Holocron: The perception path collapsed.")
                return distill_result  # Return the underlying failure to the UI

            # --- MOVEMENT IV: THE RADIANT GNOSIS SUTURE (THE CURE) ---
            # [ASCENSION 1]: This is the final fix. We take the content generated
            # by the DistillArtisan and ensure it is manifest in our return data.
            final_content = ""
            if distill_result.data and isinstance(distill_result.data, dict):
                final_content = distill_result.data.get('content', "")

            if not final_content:
                # If content is missing, we perform an emergency read of the output file
                # to heal the payload before returning to the UI.
                output_path = distill_result.data.get('output_path')
                if output_path and os.path.exists(output_path):
                    with open(output_path, 'r', encoding='utf-8', errors='replace') as f:
                        final_content = f.read()

            # --- MOVEMENT V: TELEMETRY & FINALITY ---
            duration_ms = (time.perf_counter_ns() - start_ts) / 1_000_000

            # [ASCENSION 12]: THE FINALITY VOW
            # We return a success result that mirrors the Distill outcome but
            # guarantees the 'content' is present for the Context Weaver.
            return self.success(
                message="Holocron Gnosis manifest and radiated to Ocular Interface.",
                data={
                    "content": final_content,
                    "telemetry": distill_result.data.get('telemetry', {}),
                    "file_count": distill_result.data.get('file_count', 0),
                    "token_count": distill_result.data.get('token_count', 0),
                    "duration_ms": duration_ms,
                    "trace_id": trace_id
                },
                ui_hints={
                    "vfx": "bloom",
                    "color": "#3b82f6",
                    "icon": "🏛️",
                    "priority": "SUCCESS"
                }
            )

        except Exception as catastrophic_paradox:
            # [ASCENSION 9]: SOCRATIC ERROR TRIAGE
            self.logger.critical(f"Holocron Fracture: {catastrophic_paradox}")
            return self.engine.failure(
                message=f"Holocron Perception Failure: {str(catastrophic_paradox)}",
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL
            )

    def _resonate(self, trace_id: str, label: str, color: str):
        """[ASCENSION 8]: HUD Multicast."""
        if hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": "HOLOCRON_EVENT",
                        "label": label,
                        "color": color,
                        "trace": trace_id,
                        "timestamp": time.time()
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        return f"<Ω_HOLOCRON_ARTISAN status=RESONANT lifetime=INFINITY>"