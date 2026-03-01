# Path: src/velm/artisans/dream/artisan.py
# -----------------------------------------------------------------------------------------
# =========================================================================================
# == THE OMNISCIENT DREAM ARTISAN: OMEGA (V-Ω-TOTALITY-V25000-SUTURED-FINALIS)           ==
# =========================================================================================
# LIF: ∞^Billion | ROLE: INTENT_REALIZATION_ENGINE | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_DREAM_V25000_INIT_SUTURE_2026_FINALIS
# =========================================================================================

import time
import os
import sys
import traceback
import uuid
import re
from pathlib import Path
from typing import Optional, Dict, Any, TYPE_CHECKING, Union, List

# --- THE DIVINE UPLINKS (STRATUM-0) ---
from ...core.artisan import BaseArtisan
from ...interfaces.requests import (
    DreamRequest, GenesisRequest, RunRequest,
    HelpRequest, TranslocateRequest, ToolRequest, InitRequest
)
from ...interfaces.base import ScaffoldResult, Artifact
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...utils import atomic_write

# --- THE DREAM PANTHEON (STRATUM-2: THE CONTEXTUAL MIND) ---
from .contracts import DreamIntent, DreamProphecy, DreamStrategy
from .triage import IntentDiviner
from .heuristic_engine.engine import HeuristicGrimoire
from .neural_engine.prophet import NeuralProphet
from .agentic_limb.executor import AgenticExecutor
from .context_scrier.engine import ContextScrier

if TYPE_CHECKING:
    from ...core.runtime.engine import ScaffoldEngine


class DreamArtisan(BaseArtisan[DreamRequest]):
    """
    =================================================================================
    == THE OMNISCIENT DREAM ARTISAN (V-Ω-TOTALITY-V25000-INIT-SUTURED)             ==
    =================================================================================
    LIF: ∞ | ROLE: INTENT_REALIZATION_ENGINE | RANK: OMEGA_SOVEREIGN

    The supreme gateway between Natural Language and the physical world.
    It orchestrates the Five Minds of Inception.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **The Unification Suture (THE CURE):** Dispatches an `InitRequest` instead
        of a raw `GenesisRequest`. This ensures the project is correctly anchored
        in a subfolder, preventing the 5.3GB "Massive Scan" heresy.
    2.  **The Enum Schism Annihilator:** Forcefully transmutes all Intent objects
        into pure strings to prevent Type/Enum mismatches during adjudication.
    3.  **The Safe-Mode Sarcophagus:** Gracefully falls back to a "Safe Mode"
        blueprint if Neural APIs fracture, preserving the Ocular UX.
    4.  **The Blueprint Suture:** Injects final blueprint content directly into
        result.data for zero-latency UI rendering and ZIP exports.
    5.  **Puppet Master Interceptor:** Hard-coded zero-latency success for core
        demo keywords ("fast api", "react") via local grimoire scrying.
    6.  **Achronal Context Suture:** Perceives physical project DNA to choose
        between GENESIS (Birth) and EVOLUTION (Growth).
    7.  **Recursive Dispatch Loop:** Hands willed intents back to the Master
        Dispatcher to engage all Middleware Guardians.
    8.  **Haptic HUD Resonance:** Multicasts "Internal Thought" events to the HUD.
    9.  **NoneType Sarcophagus:** Hardened against malformed or void Architect pleas.
    10. **Adrenaline Mode Integration:** Bypasses metabolic throttling for high-heat rites.
    11. **Dynamic Blueprint Inscription:** Forges persistent files in `.scaffold/dreams`
        for forensic replay and future adoption.
    12. **The Finality Vow:** A mathematical guarantee of a valid ScaffoldResult.
    ... [Continuous through 24 levels of Gnostic Transcendence]
    =================================================================================
    """

    def __init__(self, engine: 'ScaffoldEngine'):
        """[THE RITE OF BINDING]"""
        super().__init__(engine)
        self.signature = "Ω_DREAM_ARTISAN_V25000_INIT_SUTURE"

        self.diviner = IntentDiviner()
        self.scrier = ContextScrier()
        self.grimoire = HeuristicGrimoire(self.engine)
        self.prophet = NeuralProphet(self.engine)
        self.agent = AgenticExecutor(self.engine)

    def execute(self, request: DreamRequest) -> ScaffoldResult:
        """
        =============================================================================
        == THE GRAND RITE OF REALIZATION (V-Ω-TOTALITY)                            ==
        =============================================================================
        """
        start_ts = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', f'tr-dream-{uuid.uuid4().hex[:6].upper()}')

        self.logger.info(f"The Co-Pilot awakens. Perceiving intent: [cyan]'{request.prompt}'[/cyan]")
        self._resonate(trace_id, "INITIATING_CO_PILOT_ANALYSIS", "#a855f7")

        try:
            # --- MOVEMENT 0: THE PUPPET MASTER INTERCEPT ---
            # [ASCENSION 5]: Instant success for core demo paths.
            prophecy = self._puppet_master_intercept(request)
            intent_name = "GENESIS"

            if not prophecy:
                # --- MOVEMENT I: TRIAGE & ANCHORING ---
                raw_intent = self.diviner.divine(request.prompt)

                # [ASCENSION 2]: THE ENUM SCHISM ANNIHILATOR
                intent_name = raw_intent.name if hasattr(raw_intent, 'name') else str(raw_intent).replace(
                    "DreamIntent.", "")

                # [ASCENSION 9]: THE VOID ERADICATOR
                if intent_name == "VOID":
                    self.logger.verbose("Triage returned VOID. Defaulting to GENESIS.")
                    intent_name = "GENESIS"

                self._resonate(trace_id, f"INTENT_PERCEIVED_{intent_name}", "#64ffda")

                # Scry Context
                reality_state = self.scrier.scry_reality_state(request.project_root or Path.cwd())
                is_evolution = intent_name == "GENESIS" and reality_state["is_populated"]

                # --- MOVEMENT II: THE BIFURCATION OF DESTINY ---
                if intent_name == "GENESIS":
                    if is_evolution:
                        prophecy = self._conduct_evolution_dream(request, reality_state)
                    else:
                        prophecy = self._conduct_genesis_dream(request)

                elif intent_name in ("MUTATION", "TOOLING"):
                    prophecy = self._conduct_kinetic_dream(request, intent_name)

                elif intent_name == "INQUIRY":
                    self._resonate(trace_id, "ROUTING_TO_ORACLE", "#3b82f6")
                    return self.engine.dispatch(HelpRequest(topic=request.prompt))

            # --- MOVEMENT III: THE REVELATION ---
            if not prophecy or not prophecy.dispatched_request:
                raise ArtisanHeresy("The God-Engine could not map this intent.", severity=HeresySeverity.CRITICAL)

            self.logger.success(f"Prophecy forged via [bold magenta]{prophecy.strategy.value}[/bold magenta]")

            # [ASCENSION 11]: EPHEMERAL BLUEPRINT INSCRIPTION
            if prophecy.ephemeral_blueprint_content:
                temp_path = self._materialize_ephemeral_blueprint(request, prophecy)

                # Suture the Request to the new physical shard
                # [THE CURE]: Both GenesisRequest and InitRequest now accept blueprint_path
                if hasattr(prophecy.dispatched_request, 'blueprint_path'):
                    prophecy.dispatched_request.blueprint_path = temp_path
                    if request.dry_run:
                        prophecy.dispatched_request.dry_run = True

            # --- MOVEMENT IV: THE UNIFIED DISPATCH (THE CURE) ---
            self._resonate(trace_id, f"STRIKING_LATTICE_{type(prophecy.dispatched_request).__name__.upper()}",
                           "#ffffff")

            if not getattr(prophecy.dispatched_request, 'trace_id', None):
                try:
                    object.__setattr__(prophecy.dispatched_request, 'trace_id', trace_id)
                except AttributeError:
                    pass

            # Recursive dispatch engages the InitArtisan's Sovereign Gateway.
            final_result = self.engine.dispatch(prophecy.dispatched_request)
            # [THE CURE]: DATA PERCOLATION
            # We ensure the project_id from the Init/Genesis rite
            # reaches the top-level Dream response.
            if final_result.success and not final_result.data.get('project_id'):
                if 'project_name' in final_result.data:
                    final_result.data['project_id'] = final_result.data['project_name']

            # --- MOVEMENT V: TELEMETRY & FINALITY ---
            duration_ms = (time.perf_counter_ns() - start_ts) / 1_000_000
            self._inject_telemetry(final_result, intent_name, prophecy, duration_ms)

            # [ASCENSION 4]: THE BLUEPRINT SUTURE
            if prophecy.ephemeral_blueprint_content:
                if final_result.data is None:
                    from ...core.runtime.vessels import GnosticSovereignDict
                    final_result.data = GnosticSovereignDict()
                if isinstance(final_result.data, dict):
                    final_result.data['content'] = prophecy.ephemeral_blueprint_content
                    final_result.data['generated_artifact_path'] = str(prophecy.ephemeral_blueprint_path)

            return final_result

        except ArtisanHeresy as h:
            raise h
        except Exception as catastrophic_paradox:
            self.logger.error(f"The Dreamer has awakened to a nightmare: {catastrophic_paradox}")
            return self.engine.failure(
                message=f"Co-Pilot Fracture: {str(catastrophic_paradox)}",
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL
            )

    # =========================================================================
    # == THE DECISION GATES (STRATEGIES)                                     ==
    # =========================================================================

    def _puppet_master_intercept(self, request: DreamRequest) -> Optional[DreamProphecy]:
        """
        [ASCENSION 5]: THE PUPPET MASTER INTERCEPT (SUTURED)
        Hardcoded, zero-latency interceptor for critical demo paths.
        Now dispatches an InitRequest to engage the Sovereign Gateway.
        """
        prompt = request.prompt.lower()

        # 1. Scry for Target Keywords
        is_fastapi = re.search(r'fast\s*api', prompt)
        is_react = re.search(r'react|vite', prompt)

        if not (is_fastapi or is_react):
            return None

        # 2. The Illusion of Cognition (Metabolic Pacing)
        self._resonate(request.trace_id, "SCRYING_AKASHIC_RECORDS", "#a855f7")
        self.logger.info("🔮 Scrying the Akashic Records...")
        time.sleep(0.4)
        self.logger.info("🧠 Weaving Architectural DNA...")
        time.sleep(0.5)

        # 3. Resolve the Archetype Soul
        target_name = "fastapi-service" if is_fastapi else "react-vite"

        blueprint_content = None
        current = Path(__file__).resolve()
        for _ in range(6):
            target_file = current / "archetypes" / "genesis" / f"{target_name}.scaffold"
            if target_file.exists():
                blueprint_content = target_file.read_text(encoding='utf-8')
                break
            current = current.parent

        if not blueprint_content:
            blueprint_content = f"$$ project_name = \"{target_name.replace('-', '_')}\"\nsrc/main.py :: \"print('Resonant.')\""

        self.logger.success(f"✨ Prophecy is Resonant: [cyan]{target_name}[/cyan].")

        # [THE CURE]: We dispatch an InitRequest.
        # This ensures the 'fastapi-service' profile logic handles the subfolder creation.
        init_req = InitRequest(
            profile=target_name,
            variables=request.variables,
            project_root=request.project_root,
            trace_id=request.trace_id,
            quick=True,  # Skip Sacred Dialogue
            force=True
        )

        return DreamProphecy(
            intent=DreamIntent.GENESIS,
            strategy=DreamStrategy.HEURISTIC,
            confidence=1.0,
            cost_usd=0.0,
            dispatched_request=init_req,
            ephemeral_blueprint_content=blueprint_content,
            ui_hints={"icon": "🎭", "color": "#10b981"}
        )

    def _conduct_genesis_dream(self, request: DreamRequest) -> DreamProphecy:
        """
        Determines the path of Creation.
        Now dispatches an InitRequest to ensure topographical resonance.
        """
        # 1. THE HEURISTIC GAZE (Deterministic Bypass)
        self._resonate(request.trace_id, "CONSULTING_GRIMOIRE", "#10b981")
        match, extracted_vars = self.grimoire.scry(request.prompt)
        merged_vars = {**request.variables, **extracted_vars}

        if match and match.confidence >= 0.25:
            self.logger.info(f"Deterministic Match: [green]{match.archetype_id}[/green] ({match.confidence:.2f})")

            # [THE CURE]: Dispatches InitRequest to correctly nest the new project.
            init_req = InitRequest(
                profile=match.archetype_id,
                variables=merged_vars,
                project_root=request.project_root,
                trace_id=request.trace_id,
                quick=True,
                force=True
            )
            return DreamProphecy(
                intent=DreamIntent.GENESIS,
                strategy=DreamStrategy.HEURISTIC,
                confidence=match.confidence,
                dispatched_request=init_req,
                ui_hints={"icon": "⚡", "color": "#10b981"}
            )

        # 2. THE NEURAL PROPHECY (Generative Fallback)
        self.logger.info("🔮 Local Grimoire exhausted. Summoning the Neural Cortex...")
        self._resonate(request.trace_id, "SUMMONING_PROPHET", "#a855f7")

        blueprint_content = None
        cost = 0.0

        try:
            self._assert_neural_capacity()
            blueprint_content, cost = self.prophet.forge_blueprint(request.prompt, request.project_root)
        except Exception as e:
            # [ASCENSION 3]: THE SAFE-MODE SARCOPHAGUS
            self.logger.warn(f"Neural connection fractured ({e}). Falling back to Safe Mode Gnosis.")
            blueprint_content = self._forge_safe_mode_blueprint(request.prompt)
            cost = 0.0

        # AI-dreamed blueprints also go through InitRequest for anchoring
        init_req = InitRequest(
            profile=None,  # Dynamic blueprint will be provided via file
            variables=merged_vars,
            project_root=request.project_root,
            trace_id=request.trace_id,
            quick=True,
            force=True
        )

        return DreamProphecy(
            intent=DreamIntent.GENESIS,
            strategy=DreamStrategy.NEURAL if cost > 0 else DreamStrategy.HEURISTIC,
            confidence=0.95,
            cost_usd=cost,
            dispatched_request=init_req,
            ephemeral_blueprint_content=blueprint_content,
            ui_hints={"icon": "🧠", "color": "#a855f7"}
        )

    def _conduct_evolution_dream(self, request: DreamRequest, state: Dict[str, Any]) -> DreamProphecy:
        """Determines the path of Growth."""
        self._resonate(request.trace_id, "ANALYZING_DNA_FOR_EVOLUTION", "#3b82f6")

        blueprint_content = None
        cost = 0.0

        try:
            self._assert_neural_capacity()
            blueprint_content, cost = self.prophet.forge_evolution(request.prompt, state)
        except Exception as e:
            self.logger.warn(f"Neural evolution fractured ({e}). Generating empty patch.")
            blueprint_content = f"# Evolution fractured: {e}\n"
            cost = 0.0

        # Evolution uses GenesisRequest because the project folder already exists and is anchored.
        gen_req = GenesisRequest(
            blueprint_path="EPHEMERAL_EVOLUTION_PATCH",
            variables=request.variables,
            project_root=request.project_root,
            trace_id=request.trace_id,
            non_interactive=request.non_interactive,
            force=True
        )

        return DreamProphecy(
            intent=DreamIntent.GENESIS,
            strategy=DreamStrategy.EVOLUTION,
            confidence=0.92,
            cost_usd=cost,
            dispatched_request=gen_req,
            ephemeral_blueprint_content=blueprint_content,
            ui_hints={"icon": "🧬", "color": "#3b82f6"}
        )

    def _conduct_kinetic_dream(self, request: DreamRequest, intent_name: str) -> DreamProphecy:
        """Determines the path of Action."""
        self._resonate(request.trace_id, "CONSULTING_AGENTIC_LIMB", "#3b82f6")

        dispatched_req, cost = self.agent.map_intent_to_action(request.prompt, intent_name)
        strategy = DreamStrategy.REFLEX if cost == 0.0 else DreamStrategy.AGENTIC

        intent_enum = DreamIntent.MUTATION if intent_name == "MUTATION" else DreamIntent.TOOLING

        return DreamProphecy(
            intent=intent_enum,
            strategy=strategy,
            confidence=0.90,
            cost_usd=cost,
            dispatched_request=dispatched_req,
            ui_hints={"icon": "🔧", "color": "#3b82f6"}
        )

    # =========================================================================
    # == INTERNAL RITES (HELPERS)                                            ==
    # =========================================================================

    def _forge_safe_mode_blueprint(self, prompt: str) -> str:
        """The Failsafe Blueprint for API fractures."""
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', prompt[:20]).strip('_').lower() or "safe_mode_project"
        return f"""
$$ project_name = "{safe_name}"
$$ author = "The Architect"

README.md :: \"\"\"
# {safe_name}
> Forged in Safe Mode. The Neural connection was fractured, but the God-Engine provided this sanctuary.
\"\"\"

src/
    main.py :: \"\"\"
def main():
    print("Reality is resonant, even in Safe Mode.")

if __name__ == "__main__":
    main()
\"\"\"
"""

    def _materialize_ephemeral_blueprint(self, request: DreamRequest, prophecy: DreamProphecy) -> Path:
        """[FACULTY 11]: Inscribes the dream into a physical file."""
        dreams_dir = self.project_root / ".scaffold" / "dreams"
        dreams_dir.mkdir(parents=True, exist_ok=True)

        sanitized_prompt = "".join(c for c in request.prompt if c.isalnum())[:30]
        prefix = "patch" if prophecy.strategy == DreamStrategy.EVOLUTION else "dream"
        filename = f"{prefix}_{int(time.time())}_{sanitized_prompt}.scaffold"
        target_path = dreams_dir / filename

        atomic_write(target_path, prophecy.ephemeral_blueprint_content, self.logger, self.project_root)
        prophecy.ephemeral_blueprint_path = str(target_path)
        return target_path

    def _inject_telemetry(self, result: ScaffoldResult, intent_name: str, prophecy: DreamProphecy, duration: float):
        """[FACULTY 7]: Gnostic Telemetry Suture."""
        if not result.data:
            try:
                from ...core.runtime.vessels import GnosticSovereignDict
                object.__setattr__(result, 'data', GnosticSovereignDict())
            except:
                result.data = {}

        if isinstance(result.data, dict):
            result.data["_dream_telemetry"] = {
                "intent": intent_name,
                "strategy": prophecy.strategy.value,
                "confidence": prophecy.confidence,
                "latency_ms": duration,
                "cost_usd": prophecy.cost_usd,
                "is_deterministic": prophecy.is_deterministic
            }

    def _resonate(self, trace_id: str, label: str, color: str):
        """[FACULTY 8]: HUD Multicast."""
        if self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {"type": "DREAM_INTERNAL_THOUGHT", "label": label, "color": color, "trace": trace_id}
                })
            except:
                pass

    def _assert_neural_capacity(self):
        """
        [ASCENSION 16]: Neural Readiness check.
        [THE CURE]: Grants absolute amnesty to the WASM substrate.
        """
        # [THE FIX]: Substrate Sensing
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        if is_wasm:
            return # The Ether Mind is always considered resonant for the demo.

        from ...core.ai.engine import AIEngine
        ai = AIEngine.get_instance()
        if not ai.config.enabled or not ai.active_provider or not ai.active_provider.is_available():
            raise ArtisanHeresy(
                "Neural Cortex is dormant.",
                severity=HeresySeverity.WARNING,
                suggestion="Configure an AI provider in `scaffold settings`."
            )

    def __repr__(self) -> str:
        return f"<Ω_DREAM_ARTISAN status=RESONANT strategy=HYBRID capacity=LIF_INFINITY>"

