# Path: artisans/dream/neural_engine/prophet.py
# ---------------------------------------------


import time
import logging
from pathlib import Path
from typing import Tuple, Optional, Dict, Any, List, Final

# --- THE DIVINE UPLINKS ---
from ....core.ai.engine import AIEngine
from ....core.ai.contracts import NeuralPrompt
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ....logger import Scribe
from .constitution import forge_system_prompt
from .validator import NeuralInquisitor

Logger = Scribe("Dream:NeuralProphet")


class NeuralProphet:
    """
    =================================================================================
    == THE OMEGA NEURAL PROPHET (V-Ω-TOTALITY-VMAX-24-ASCENSIONS)                  ==
    =================================================================================
    LIF: ∞^∞ | ROLE: ARCHITECTURAL_COMPILER_PRIME | RANK: OMEGA_SOVEREIGN
    AUTH: Ω_PROPHET_VMAX_TOTALITY_2026_FINALIS

    The Generative Heart of the Dream Artisan. It bridges the gap between Human
    Intent and Gnostic Scripture (.scaffold) with absolute precision.
    """

    MAX_HEALING_CYCLES: Final[int] = 3
    RETRY_BACKOFF_BASE: Final[float] = 1.6

    def __init__(self, engine):
        """[THE RITE OF BINDING]"""
        self.engine = engine
        self.ai = AIEngine.get_instance()
        self.inquisitor = NeuralInquisitor(engine=self.engine)

    def forge_blueprint(self, intent: str, root: Path, model_hint: str = "smart") -> Tuple[str, float]:
        """
        [THE RITE OF GENESIS - PURE]
        Forges a custom blueprint from raw ether.
        """
        return self._commune(intent, "GENESIS_PURE", {}, model_hint)

    def forge_hybrid_blueprint(
            self,
            intent: str,
            root: Path,
            hub_index_str: str,
            model_hint: str = "smart"
    ) -> Tuple[str, float]:
        """
        [ASCENSION 1]: THE RITE OF HYBRID GENESIS.
        The Exoskeleton Strategy. Uses SCAF-Hub to weave established reality.
        """
        # [THE MASTER CURE]: IDENTITY LOCK SUTURE
        # We explicitly command the AI to use the dynamic 'package_name' variable.
        hybrid_context = (
            f"### SCAF-HUB REGISTRY (AVAILABLE SHARDS):\n"
            f"{hub_index_str}\n\n"
            f"### CRITICAL ARCHITECTURAL DIRECTIVES:\n"
            f"1. **DO NOT** write boilerplate if a Shard exists. Use `{{{{ logic.weave('shard_id') }}}}`.\n"
            f"2. **IDENTITY LOCK:** You MUST use the `{{{{ package_name }}}}` variable for all inner package paths.\n"
            f"3. NEVER hardcode folder names like 'app' or 'omega_citadel'.\n"
            f"4. Example: src/{{{{ package_name }}}}/api/routes.py :: \"\"\" ... \"\"\"\n"
        )

        return self._commune(intent, "GENESIS_HYBRID", {"project_context": hybrid_context}, model_hint)

    def forge_evolution(
            self,
            intent: str,
            context: Dict[str, Any],
            hub_index_str: str = "",
            model_hint: str = "smart"
    ) -> Tuple[str, float]:
        """
        [ASCENSION 7]: THE RITE OF EVOLUTION (MUTATION).
        Analyzes the existing organism and generates a surgical patch.
        """
        Logger.info(f"🧬 The Neural Prophet is analyzing the host DNA for evolution...")

        project_type = context.get("project_type", "generic")
        files = ", ".join(context.get("file_structure", []))

        evolution_context = (
            f"### CURRENT REALITY MATRIX:\n"
            f"- Type: {project_type}\n"
            f"- Topography: {files}\n"
            f"\n"
            f"### EVOLUTION DIRECTIVE:\n"
            f"1. Generate a `.scaffold` patch that adds the requested features.\n"
            f"2. Use `+=` to append to configs, or create new files in `src/{{{{ package_name }}}}/`.\n"
            f"3. WEAVE existing shards via `{{{{ logic.weave('id') }}}}` where applicable.\n"
            f"4. Available Shards:\n{hub_index_str}\n"
        )

        return self._commune(intent, "EVOLUTION", {"project_context": evolution_context}, model_hint)

    def _commune(
            self,
            intent: str,
            mode: str,
            extra_context: Dict[str, str],
            model_hint: str = "smart"
    ) -> Tuple[str, float]:
        """
        =============================================================================
        == THE SHARED COMMUNION LOGIC (V-Ω-TOTALITY-HEALED)                        ==
        =============================================================================
        LIF: 100x | ROLE: NEURAL_STRIKE_CONDUCTOR
        """
        start_time = time.time()
        trace_id = getattr(self.engine.context, 'session_id', 'tr-neural-void')

        # 1. FORGE THE CONSTITUTION
        system_prompt = forge_system_prompt()

        # 2. FORGE THE PLEA
        full_query = f"## ARCHITECT'S INTENT ({mode}):\n{intent}\n"
        if "project_context" in extra_context:
            full_query += f"\n## CONTEXTUAL GNOSIS:\n{extra_context['project_context']}\n"
        full_query += "\n## COMMAND:\nForge the .scaffold blueprint now. Output ONLY raw code."

        # [ASCENSION 16]: TOKEN ECONOMY
        token_budget = 8000 if mode != "GENESIS_PURE" else 4000

        prompt = NeuralPrompt(
            user_query=full_query,
            system_instruction=system_prompt,
            model_hint=model_hint,  # [SUTURED]: Propagated from conductor
            max_tokens_override=token_budget,
            use_rag=True
        )

        attempts = 0
        total_cost = 0.0
        last_error = ""

        # =========================================================================
        # == THE SELF-HEALING SEMANTIC LOOP (ASCENSION 2)                        ==
        # =========================================================================
        while attempts <= self.MAX_HEALING_CYCLES:
            attempts += 1
            try:
                # [STRIKE]: The Neural Communion
                revelation = self.ai.active_provider.commune(prompt)

                # [ASCENSION 3]: Metabolic Tomography
                total_cost += revelation.cost_usd

                # [ASCENSION 8]: THE PHANTOM SIEVE
                clean_content = self.inquisitor.purify(revelation.content)

                # [ASCENSION 23]: THE SHADOW PARSE VERIFICATION
                # Physically attempts to parse the response before returning to Architect.
                is_valid, error_msg = self.inquisitor.adjudicate(clean_content)

                if is_valid:
                    duration = time.time() - start_time
                    Logger.success(
                        f"✨ Prophecy Resonant ({mode}). "
                        f"Model: {revelation.model_used} | "
                        f"Cost: ${total_cost:.4f} | "
                        f"Cycles: {attempts}"
                    )
                    return clean_content, total_cost

                # --- FRACTURE DETECTED: INITIATE HEALING ---
                Logger.warn(f"Prophecy Fractured (Cycle {attempts}): {error_msg}")
                last_error = error_msg

                # [THE CURE]: Feed the parser error back to the Mind as a constraint.
                error_feedback = (
                    f"\n\n### SYSTEM ERROR - SYNTAX FRACTURE:\n"
                    f"Your previous output contained a structural error:\n"
                    f"Error: {error_msg}\n"
                    f"\n"
                    f"### CORRECTION DIRECTIVE:\n"
                    f"Regenerate the blueprint fixing this error. Ensure valid `path :: \"content\"` syntax.\n"
                    f"Output ONLY the corrected .scaffold code."
                )
                prompt.user_query += error_feedback

                # [ASCENSION 15]: Exponential Backoff
                time.sleep(self.RETRY_BACKOFF_BASE ** attempts)

            except Exception as transmission_fracture:
                Logger.error(f"Neural Transmission Failed: {transmission_fracture}")
                if any(x in str(transmission_fracture).lower() for x in ("auth", "quota", "connection")):
                    raise ArtisanHeresy(f"Neural Link Severed: {transmission_fracture}",
                                        severity=HeresySeverity.CRITICAL)
                last_error = str(transmission_fracture)

        # [ASCENSION 6]: THE NONE-TYPE SARCOPHAGUS
        raise ArtisanHeresy(
            f"The Neural Prophet failed to manifest a resonant blueprint after {self.MAX_HEALING_CYCLES} cycles.",
            details=f"Last Forensic Heresy: {last_error}",
            severity=HeresySeverity.CRITICAL,
            suggestion="Simplify the architectural plea or check SCAF-Hub availability."
        )

    def __repr__(self) -> str:
        return f"<Ω_NEURAL_PROPHET status=RESONANT mode=VMAX_24_ASCENSIONS capacity=LIF_INFINITY>"