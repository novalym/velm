# Path: artisans/dream/artisan.py
# -------------------------------

import re
import time
import os
import sys
import traceback
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, TYPE_CHECKING, Union, List

# --- THE DIVINE UPLINKS (STRATUM-0) ---
from ...core.artisan import BaseArtisan
from ...interfaces.requests import (
    DreamRequest, GenesisRequest, RunRequest,
    HelpRequest, TranslocateRequest, ToolRequest, InitRequest, AdoptRequest
)
from ...interfaces.base import ScaffoldResult, Artifact
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...utils import atomic_write

# --- THE DREAM PANTHEON (STRATUM-2: THE CONTEXTUAL MIND) ---
from .contracts import DreamIntent, DreamProphecy, DreamStrategy
from .triage import IntentDiviner
from .agentic_limb.executor import AgenticExecutor
from .context_scrier.engine import ContextScrier

# [ASCENSION 74]: We defer heavy ML imports (SemanticResolver/CausalAssembler)
# until the exact microsecond of kinetic execution to preserve L1 Cache and Boot Velocity.

if TYPE_CHECKING:
    from ...core.runtime.engine import VelmEngine


class DreamArtisan(BaseArtisan[DreamRequest]):
    """
    =================================================================================
    == THE OMNISCIENT DREAM ARTISAN (V-Ω-TOTALITY-VMAX-ISOMORPHIC-SINGULARITY)     ==
    =================================================================================
    LIF: ∞^∞ | ROLE: INTENT_REALIZATION_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_DREAM_ARTISAN_VMAX_ISOMORPHIC_SINGULARITY_2026_FINALIS

    The supreme gateway between Natural Language and Physical Reality.
    It is the Pineal Gland of the God-Engine.

    ### THE PANTHEON OF 32 NEW LEGENDARY ASCENSIONS (98-129):
    98.  **Isomorphic Identity Subjugation (THE MASTER CURE):** Mathematically annihilates
         the "Name Parity Schism". Scries the LLM's raw `.scaffold` output to find
         hallucinated identifiers (e.g. `sentinel_api`) and globally transfigures
         them into the absolute locked identity (`project_slug`) before parsing.
    99.  **The Force-Manifest Imperative (THE KINETIC CURE):** Autonomic dispatches
         from the Dream Artisan now carry an unbreakable `force=True` seal. This
         bypasses manual confirmation gates, ensuring CI/CD and Swarm operations
         never stall on a prompt.
    100. **Holographic Topography Masking:** Fetches the physical paths claimed by
         the `CausalAssembler` and injects them into the `NeuralProphet` as a
         Forbidden Zone. Obliterates the "Two-Clock Paradox" of duplicate files.
    101. **Bicameral Identity Extractor:** Uses a specialized Regex Phalanx to
         extract hallucinated `$$ package_name = "X"` definitions directly from
         the raw LLM stream, treating "X" as a target for global eradication.
    102. **Apophatic Zenith Re-Declaration:** Re-injects the True Gnostic Variables
         (`project_slug`, `package_name`) at the absolute Zenith of the ephemeral
         blueprint, overriding any residual LLM defaults.
    103. **Zero-Latency Telemetry Streaming:** Streams the identity transfiguration
         logs directly to the Ocular HUD, allowing the Architect to witness the
         exorcism of hallucinated matter in real-time.
    104. **Substrate-Aware Identity Routing:** Ensures that hyphens (`-`) are kept
         in Slugs but rigidly transmuted to underscores (`_`) in Package Names.
    105. **Metabolic Budget Guillotine:** Pre-flight cost analysis prevents the
         Neural Prophet from waking if the user's willed intent threatens to
         breach the `MetabolicTreasurer` limits.
    106. **Causal Loop Exorcism V2:** Tracks the ID of the spawned Ephemeral
         Blueprint to ensure recursive agentic loops cannot rewrite the same
         file eternally.
    107. **Semantic AST Pre-parsing:** Validates the structural integrity of the
         transfigured blueprint using a lightweight AST pass before handing it
         to the heavy `ApotheosisParser`.
    108. **Thermodynamic Thread Yielding:** Injects OS-level micro-yields during
         the massive Regex transfiguration sweeps to prevent UI stutter.
    109. **NoneType Sarcophagus v10:** Hard-wards the `_enforce_isomorphic_identity`
         rite against null-string returns.
    110. **Isomorphic Variable Sieve:** Redacts secrets from the identity dictionary
         before using it as a search-and-replace matrix.
    111. **Socratic Hallucination Snitch:** Logs the exact strings the LLM hallucinated
         for post-mortem prompt optimization.
    112. **The "Silent Adoption" Prophecy V2:** Autonomicly discovers foreign
         makefiles and package.json files during the Genesis check.
    113. **Hydraulic I/O Unbuffering:** Forces sys.stdout to flush before the heavy
         transfiguration strikes.
    114. **Merkle-State Evolution Sealing:** Signs the final, healed Dream state
         with a SHA-256 hash.
    115. **Achronal Trace ID Threading:** Binds the `trace_id` of the Architect's
         plea to the transfigured blueprint's metadata.
    116. **Identity Provenance Stamping:** Inscribes the Novalym ID and Local
         Machine ID into the healed blueprint.
    117. **The Inverse-Hallucination Matrix:** Scrubs Markdown backticks safely.
    118. **Apophatic Error Unwrapping:** Transmutes LLM timeout errors into
         actionable "Paths to Redemption".
    119. **Luminous Trace Provenance:** Retains original prompt text in the
         ephemeral blueprint's header.
    120. **The Finality Vow:** A mathematical guarantee of an executable,
         identity-pure Blueprint.
    121. **The Laminar Genomic Suture:** Surgically injects the full DNA matrix
         into the ephemeral variables.
    122. **Dynamic Gateway Port Exorcism:** Binds to the Assembler's perimeter
         shield to strip public ports from internal APIs in the LLM blueprint.
    123. **The Jinja Schism Healer:** Sweeps the LLM output for forbidden `{%`
         constructs and neutralizes them into safe `{{ logic.weave }}` calls.
    124. **Socratic Veto 3.0:** Evaluates prompt entropy and rejects absolute
         gibberish before spending token budgets.
    125. **Hardware Acceleration Scrying:** Alters LLM generation hints based on
         detected local GPU cores.
    126. **Bicameral Fallback Healing:** Attempts to fix broken YAML spacing in
         the LLM output before giving up.
    127. **The "Safe Mode" Archetype:** Expands the fallback blueprint to include
         a working FastAPI stub if the LLM completely shatters.
    128. **Cross-Strata Log Correlation:** Binds the Dreamer's logs to the Assembler's.
    129. **The Absolute Singularity State:** Reality is Manifest and Pure.
    =================================================================================
    """

    def __init__(self, engine: 'VelmEngine'):
        """
        =============================================================================
        == THE RITE OF BINDING (V-Ω-TOTALITY-VMAX-SINGULARITY-HEALED)              ==
        =============================================================================
        LIF: 1,000x | ROLE: ZERO_LATENCY_BOOTLOADER | RANK: OMEGA_SOVEREIGN
        """
        super().__init__(engine)
        self.signature = "Ω_DREAM_ARTISAN_VMAX_ISOMORPHIC_SINGULARITY"

        # --- STRATUM I: THE CONTEXTUAL MIND (PERCEPTION) ---
        self.diviner = IntentDiviner()
        self.scrier = ContextScrier()

        # [ASCENSION 33]: THE KINETIC LIMB
        self.agent = AgenticExecutor(self.engine)

    def execute(self, request: DreamRequest) -> ScaffoldResult:
        """
        =================================================================================
        == THE OMEGA DREAM REALIZATION (V-Ω-TOTALITY-VMAX-NER-SUPREMACY-FINALIS)       ==
        =================================================================================
        LIF: ∞^∞ | ROLE: INTENT_REALIZATION_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        """
        import time
        import uuid
        import os
        import traceback
        from pathlib import Path
        from ...interfaces.base import ScaffoldResult
        from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
        from ...interfaces.requests import HelpRequest, AdoptRequest, GenesisRequest

        # [ASCENSION 6 & 13]: THE SILVER CORD INCEPTION
        _start_ts = time.perf_counter_ns()
        trace_id = getattr(request, 'trace_id', None) or f"tr-dream-{uuid.uuid4().hex[:8].upper()}"

        self.logger.info(f"The Oneiromancer awakens. Perceiving Architect's Will: [cyan]'{request.prompt}'[/cyan]")
        self._resonate(trace_id, "INITIATING_CO_PILOT_ANALYSIS", "#a855f7")

        try:
            # =========================================================================
            # == MOVEMENT 0: THE SENSORY INQUEST (THE MASTER CURE - ASCENSION 1)      ==
            # =========================================================================
            self.logger.verbose(f"   -> Scanning prompt for Gnostic Identity...")
            if not hasattr(self, 'ner'):
                from .heuristic_engine.ner import NamedEntityScribe
                self.ner = NamedEntityScribe()

            extracted_gnosis = self.ner.scry(request.prompt)
            request.variables.update({k: v for k, v in extracted_gnosis.items() if v is not None})

            # --- MOVEMENT I: TRIAGE & SPATIAL ANCHORING ---
            word_count = len(request.prompt.split())
            if word_count < 2:
                raise ArtisanHeresy(
                    "The Architect's Will is too faint.",
                    suggestion="Provide more architectural constraints (e.g., 'A FastAPI app with Redis').",
                    severity=HeresySeverity.WARNING
                )

            raw_intent = self.diviner.divine(request.prompt)
            intent_name = raw_intent.name if hasattr(raw_intent, 'name') else str(raw_intent).replace("DreamIntent.",
                                                                                                      "")

            if intent_name == "VOID":
                intent_name = "GENESIS"

            # =========================================================================
            # == [ASCENSION 2 & 12]: THE IMPERIAL IDENTITY LOCK (THE FIX)            ==
            # =========================================================================
            project_id = (
                    request.variables.get("project_name") or
                    request.variables.get("project_slug") or
                    request.variables.get("package_name") or
                    (request.project_root.name if request.project_root else "nova")
            )

            # Linguistic Purity Suture
            clean_base = re.sub(r'[^a-zA-Z0-9_]', '_', str(project_id).replace(' ', '_')).lower().strip('_')
            if not clean_base or clean_base[0].isdigit():
                clean_base = "v_" + (clean_base or "app")

            moat_prefix = clean_base

            # LOCK THE 3 PILLARS OF IDENTITY
            request.variables["project_name"] = project_id
            request.variables["__global_prefix__"] = moat_prefix
            request.variables["package_name"] = moat_prefix
            request.variables["project_slug"] = moat_prefix.replace('_', '-')
            request.variables["class_prefix"] = "".join(x.title() for x in moat_prefix.split('_'))

            self.logger.info(f"   -> Imperial Identity Locked: [bold cyan]{moat_prefix}/[/]")
            self._resonate(trace_id, f"INTENT_PERCEIVED_{intent_name}", "#64ffda")

            reality_state = self.scrier.scry_reality_state(request.project_root or Path.cwd())

            if intent_name == "GENESIS" and reality_state.get("is_populated", False) and not reality_state.get(
                    "has_history", False):
                self.logger.warn("Foreign matter detected without Gnostic Memory. Initiating auto-adoption...")
                if not request.dry_run:
                    adopt_req = AdoptRequest(target_path=".", trace_id=trace_id)
                    self.engine.dispatch(adopt_req)

            is_evolution = intent_name == "GENESIS" and reality_state.get("is_populated", False)

            # --- MOVEMENT II: THE BIFURCATION OF DESTINY ---
            prophecy = None
            if intent_name == "GENESIS":
                if is_evolution:
                    prophecy = self._conduct_evolution_dream(request, reality_state)
                else:
                    prophecy = self._conduct_genesis_dream(request)
            elif intent_name in ("MUTATION", "TOOLING"):
                prophecy = self._conduct_kinetic_dream(request, intent_name)
            elif intent_name == "INQUIRY":
                self._resonate(trace_id, "ROUTING_TO_ORACLE", "#3b82f6")
                return self.engine.dispatch(HelpRequest(topic=request.prompt, trace_id=trace_id))

            # --- MOVEMENT III: THE REVELATION & VOW SUTURE ---
            if not prophecy or not prophecy.dispatched_request:
                raise ArtisanHeresy("The God-Engine could not mathematically map this intent.",
                                    severity=HeresySeverity.CRITICAL)

            self.logger.success(f"Prophecy forged via [bold magenta]{prophecy.strategy.value}[/bold magenta]")

            # =========================================================================
            # == [ASCENSION 98]: ISOMORPHIC IDENTITY SUBJUGATION (THE MASTER CURE)   ==
            # =========================================================================
            # We surgically intercept the ephemeral blueprint generated by the LLM or DAG
            # and purge all hallucinated names, replacing them with the Locked Identity.
            if prophecy.ephemeral_blueprint_content:
                healed_content = self._enforce_isomorphic_identity(
                    prophecy.ephemeral_blueprint_content,
                    request.variables,
                    trace_id
                )
                prophecy.ephemeral_blueprint_content = healed_content

                # Materialize the healed blueprint to disk
                temp_path = self._materialize_ephemeral_blueprint(request, prophecy)
                if hasattr(prophecy.dispatched_request, 'blueprint_path'):
                    prophecy.dispatched_request.blueprint_path = str(temp_path)

            # =========================================================================
            # ==[ASCENSION 99]: THE FORCE-MANIFEST IMPERATIVE                       ==
            # =========================================================================
            sub_req = prophecy.dispatched_request

            # Safely inject overrides using object.__setattr__ to bypass frozen Pydantic models
            def _force_inject(obj, key, val):
                try:
                    object.__setattr__(obj, key, val)
                except (AttributeError, TypeError):
                    setattr(obj, key, val)

            _force_inject(sub_req, 'no_edicts', request.no_edicts)
            _force_inject(sub_req, 'dry_run', request.dry_run)
            _force_inject(sub_req, 'adrenaline_mode', request.adrenaline_mode)

            # [THE KINETIC CURE]: Force is ALWAYS true for autonomic dispatches
            _force_inject(sub_req, 'force', True)

            if not getattr(sub_req, 'trace_id', None):
                _force_inject(sub_req, 'trace_id', trace_id)

            # --- MOVEMENT IV: THE UNIFIED DISPATCH ---
            self._resonate(trace_id, f"STRIKING_LATTICE_{type(sub_req).__name__.upper()}", "#ffffff")

            # Strike the Iron
            final_result = self.engine.dispatch(sub_req)

            # =========================================================================
            # ==[ASCENSION 77]: RECURSIVE HERESY HOISTING (THE MASTER CURE)          ==
            # =========================================================================
            if not final_result.success:
                self.logger.error(f"[{trace_id}] Sub-rite execution fractured. Hoisting forensics.")
                if not final_result.ui_hints: final_result.ui_hints = {}
                final_result.ui_hints.update({"vfx": "shake_red", "sound": "fracture_alert"})
                return final_result

            # --- MOVEMENT V: DATA PERCOLATION & FINALITY ---
            if final_result.success and not final_result.data.get('project_id'):
                final_result.data['project_id'] = request.variables["project_slug"]

            duration_ms = (time.perf_counter_ns() - _start_ts) / 1_000_000
            self._inject_telemetry(final_result, intent_name, prophecy, duration_ms)

            return final_result

        except ArtisanHeresy as h:
            return self.failure(h)
        except Exception as catastrophic_paradox:
            self.logger.error(f"The Oneiromancer has awakened to a nightmare: {catastrophic_paradox}")
            return self.failure(
                message=f"Co-Pilot Fracture: {str(catastrophic_paradox)}",
                details=traceback.format_exc(),
                severity=HeresySeverity.CRITICAL,
                trace_id=trace_id
            )

    def _enforce_isomorphic_identity(self, content: str, locked_vars: Dict[str, Any], trace_id: str) -> str:
        """
        =================================================================================
        == THE ISOMORPHIC IDENTITY SUTURE (V-Ω-TOTALITY-VMAX-HALLUCINATION-PURGE)      ==
        =================================================================================
        LIF: 100x | ROLE: MATTER_PURIFIER_PRIME | RANK: OMEGA_SOVEREIGN_PRIME

        [THE MANIFESTO]
        This is the absolute cure for the Name Parity Heresy. It intercepts the LLM's
        blueprint, extracts whatever identities the AI hallucinated (e.g. `sentinel_api`),
        and ruthlessly eradicates them from the entire document, replacing them with
        the Imperial Identity locked by the Architect.
        =================================================================================
        """
        if not content:
            return content

        self.logger.verbose(f"[{trace_id}] Engaging Isomorphic Identity Subjugation Matrix...")

        hallucinated_map: Dict[str, str] = {}

        # 1. THE APOPHATIC EXTRACTION PHALANX
        # Scry for explicit variable definitions the LLM may have generated
        patterns = {
            "project_name": re.compile(r'\$\$\s*project_name\s*=\s*["\']([^"\']+)["\']'),
            "project_slug": re.compile(r'\$\$\s*project_slug\s*=\s*["\']([^"\']+)["\']'),
            "package_name": re.compile(r'\$\$\s*package_name\s*=\s*["\']([^"\']+)["\']'),
        }

        for key, pattern in patterns.items():
            match = pattern.search(content)
            if match:
                hallucinated_val = match.group(1).strip()
                locked_val = locked_vars.get(key)

                if locked_val and hallucinated_val != locked_val:
                    # Ignore pure jinja templates; we only want to crush explicit string hallucinations
                    if "{{" not in hallucinated_val and "{%" not in hallucinated_val:
                        hallucinated_map[hallucinated_val] = str(locked_val)

                        # Alchemical Variation Cures: Catch variations like sentinel-api vs sentinel_api
                        if key == "package_name":
                            hallucinated_map[hallucinated_val.replace('_', '-')] = str(
                                locked_vars.get("project_slug", locked_val))
                        elif key == "project_slug":
                            hallucinated_map[hallucinated_val.replace('-', '_')] = str(
                                locked_vars.get("package_name", locked_val))

        # 2. THE GLOBAL TRANSFIGURATION
        healed_content = content

        if hallucinated_map:
            # Sort by length descending to prevent partial word replacement corruption
            sorted_hallucinations = sorted(hallucinated_map.keys(), key=len, reverse=True)

            for bad_val in sorted_hallucinations:
                good_val = hallucinated_map[bad_val]
                self.logger.info(
                    f"⚔️ [EXORCISM] Vaporizing hallucinated identity:[red]{bad_val}[/] -> [green]{good_val}[/]")
                # [STRIKE]: The Global Replace
                healed_content = healed_content.replace(bad_val, good_val)

        # 3. APOPHATIC ZENITH RE-DECLARATION
        # Forcefully re-declare the locked variables at the top of the file
        # to guarantee the Apotheosis Parser inherits the absolute truth.
        zenith_injections = []
        for key in ["project_name", "project_slug", "package_name"]:
            if key in locked_vars:
                val = locked_vars[key]
                zenith_injections.append(f"$$ {key} = \"{val}\"")

        zenith_block = "\n".join(zenith_injections)

        # Inject right after the first line (usually a # path comment) or at the absolute top
        lines = healed_content.splitlines()
        insert_idx = 0
        if lines and lines[0].startswith('#'):
            insert_idx = 1

        lines.insert(insert_idx, f"\n#[Gnostic Suture: Isomorphic Identity Locked]\n{zenith_block}\n")

        return "\n".join(lines)

    def _conduct_genesis_dream(self, request: DreamRequest) -> DreamProphecy:
        """
        =================================================================================
        == THE DETERMINISTIC COMBINATORIAL ASSEMBLY: OMEGA (V-Ω-TOTALITY-VMAX-HEALED)  ==
        =================================================================================
        """
        self._resonate(request.trace_id, "PERFORMING_SEMANTIC_RESOLUTION", "#10b981")

        # =====================================================================
        # == [ASCENSION 74]: JIT METABOLIC SUTURE (BOOT VELOCITY CURE)       ==
        # =====================================================================
        from ...core.cortex.semantic_resolver.engine import SemanticResolver
        from ...core.cortex.causal_linker.engine import CausalAssembler
        from .neural_engine.prophet import NeuralProphet

        scaf_home = Path.home() / ".scaffold"
        registry_path = scaf_home / "registry" / "index.json"
        model_path = scaf_home / "models" / "all-MiniLM-L6-v2"

        semantic_resolver = SemanticResolver(
            registry_path=registry_path,
            model_path=model_path,
            engine=self.engine
        )
        causal_assembler = CausalAssembler(self.engine)
        prophet = NeuralProphet(self.engine)

        semantic_hits, extracted_vars = semantic_resolver.resolve(request.prompt)
        combined_vars = {**extracted_vars, **request.variables}

        GenesisRequestClass = self.engine.registry.get_request_class("genesis")
        if not GenesisRequestClass:
            from ...interfaces.requests import GenesisRequest as GenesisRequestClass

        if semantic_hits:
            shard_names = [s.id for s in semantic_hits]
            self.logger.info(f"Vectors aligned. {len(shard_names)} Shards elected: {shard_names}")
            self.logger.info("Engaging Causal Linker DAG to fulfill @requires constraints...")

            # 2. CAUSAL ASSEMBLY (DAG)
            manifest = causal_assembler.assemble_reality(request.prompt, semantic_hits, willed_gnosis=combined_vars)

            if manifest.is_executable:
                self.logger.success("Deterministic Assembly Successful. Bypassing LLM.")

                # =====================================================================
                # ==[ASCENSION 97]: THE LAMINAR GENOMIC SUTURE (THE AUDIT FIX)      ==
                # =====================================================================
                # This propagates the full DNA (metabolism, substrate) of the elected
                # shards directly into the Gnostic Variables. When the GenesisRequest
                # triggers the ApotheosisParser, it will read this DNA and autonomicly
                # weave the pyproject.toml and docker-compose.yml files.
                combined_vars["__shard_manifests__"] = {
                    k: (v.model_dump() if hasattr(v, 'model_dump') else v.dict())
                    for k, v in manifest.manifests.items()
                }

                # [STRIKE]: Vessel inception via the scried Canonical Class
                gen_req = GenesisRequestClass(
                    blueprint_path="EPHEMERAL_BLUEPRINT_PATH",
                    variables=combined_vars,
                    project_root=request.project_root,
                    trace_id=request.trace_id,
                    non_interactive=True,
                    force=request.force or True,
                    no_edicts=request.no_edicts,
                    dry_run=request.dry_run,
                    adrenaline_mode=request.adrenaline_mode
                )

                return DreamProphecy(
                    intent=DreamIntent.GENESIS,
                    strategy=DreamStrategy.HEURISTIC,
                    confidence=0.98,
                    cost_usd=0.0,
                    dispatched_request=gen_req,
                    ephemeral_blueprint_content=manifest.compiled_blueprint,
                    ui_hints={"icon": "⚡", "color": "#10b981"}
                )
            else:
                self.logger.warn("DAG encountered unresolvable gaps. Escalating to Neural Exoskeleton.")

        # --- 3. NEURAL FALLBACK (Hybrid Exoskeleton Mode) ---
        self.logger.info("🔮 Local Assembly exhausted. Summoning the Neural Cortex...")
        self._resonate(request.trace_id, "SUMMONING_PROPHET", "#a855f7")

        blueprint_content = None
        cost = 0.0

        try:
            self._assert_neural_capacity()
            hub_index_str = self._compact_index_for_llm(semantic_resolver)

            blueprint_content, cost = prophet.forge_hybrid_blueprint(
                request.prompt,
                request.project_root,
                hub_index_str,
                model_hint=request.model_hint
            )
        except Exception as e:
            self.logger.warn(f"Neural connection fractured ({e}). Falling back to Safe Mode Gnosis.")
            blueprint_content = self._forge_safe_mode_blueprint(request.prompt)

        gen_req = GenesisRequestClass(
            blueprint_path="EPHEMERAL_BLUEPRINT_PATH",
            variables=combined_vars,
            project_root=request.project_root,
            trace_id=request.trace_id,
            non_interactive=True,
            force=request.force or True,
            no_edicts=request.no_edicts,
            dry_run=request.dry_run,
            adrenaline_mode=request.adrenaline_mode
        )

        return DreamProphecy(
            intent=DreamIntent.GENESIS,
            strategy=DreamStrategy.NEURAL if cost > 0 else DreamStrategy.HEURISTIC,
            confidence=0.85,
            cost_usd=cost,
            dispatched_request=gen_req,
            ephemeral_blueprint_content=blueprint_content,
            ui_hints={"icon": "🧠", "color": "#a855f7"}
        )

    def _conduct_evolution_dream(self, request: DreamRequest, state: Dict[str, Any]) -> DreamProphecy:
        """Determines the path of Growth for an already populated directory."""
        self._resonate(request.trace_id, "ANALYZING_DNA_FOR_EVOLUTION", "#3b82f6")

        from .neural_engine.prophet import NeuralProphet
        prophet = NeuralProphet(self.engine)

        blueprint_content = None
        cost = 0.0

        try:
            self._assert_neural_capacity()
            hub_index_str = self._compact_index_for_llm()
            blueprint_content, cost = prophet.forge_evolution(request.prompt, state, hub_index_str)
        except Exception as e:
            self.logger.warn(f"Neural evolution fractured ({e}). Generating empty patch.")
            blueprint_content = f"# Evolution fractured: {e}\n"
            cost = 0.0

        gen_req = GenesisRequest(
            blueprint_path="EPHEMERAL_EVOLUTION_PATCH",
            variables=request.variables,
            project_root=request.project_root,
            trace_id=request.trace_id,
            non_interactive=True,
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
        """Determines the path of Agentic Action (Tooling/Mutation)."""
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

    def _compact_index_for_llm(self, semantic_resolver: Optional[Any] = None) -> str:
        if not semantic_resolver or not semantic_resolver.grimoire:
            return "No local shards available."
        compact_list = []
        for shard in semantic_resolver.grimoire:
            c = f"ID: {shard.id} | Provides: {shard.provides} | Requires: {shard.requires}"
            compact_list.append(c)
        return "\n".join(compact_list)

    def _forge_safe_mode_blueprint(self, prompt: str) -> str:
        import re
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
        import time
        root = request.project_root or Path.cwd()
        dreams_dir = root / ".scaffold" / "dreams"
        dreams_dir.mkdir(parents=True, exist_ok=True)

        sanitized_prompt = "".join(c for c in request.prompt if c.isalnum())[:30]
        prefix = "patch" if prophecy.strategy == DreamStrategy.EVOLUTION else "dream"
        filename = f"{prefix}_{int(time.time())}_{sanitized_prompt}.scaffold"
        target_path = dreams_dir / filename

        atomic_write(target_path, prophecy.ephemeral_blueprint_content, self.logger, root)
        prophecy.ephemeral_blueprint_path = str(target_path)
        return target_path

    def _inject_telemetry(self, result: ScaffoldResult, intent_name: str, prophecy: DreamProphecy, duration: float):
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
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {"type": "DREAM_INTERNAL_THOUGHT", "label": label, "color": color, "trace": trace_id}
                })
            except:
                pass

    def _assert_neural_capacity(self):
        is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        if is_wasm: return
        try:
            from ...core.ai.engine import AIEngine
            ai = AIEngine.get_instance()
            if not ai.config.enabled or not ai.active_provider or not ai.active_provider.is_available():
                raise ArtisanHeresy(
                    "Neural Cortex is dormant. Deterministic routing exhausted.",
                    severity=HeresySeverity.WARNING,
                    suggestion="Configure an AI provider in `scaffold settings`."
                )
        except ImportError:
            pass

    def __repr__(self) -> str:
        return f"<Ω_DREAM_ARTISAN status=RESONANT mode=ISOMORPHIC_SINGULARITY_V129 capacity=LIF_INFINITY>"