# === [scaffold/artisans/distill/core/oracle/propagator.py] - SECTION 1 of 1: The Omniscient Propagator ===
import time
from pathlib import Path
from typing import Set, Dict, List, Any, Optional
from collections import defaultdict

from .....logger import Scribe
from .contracts import OracleContext

# --- THE DIVINE SUMMONS OF SPECIALIST ENGINES ---
try:
    from .....core.cortex.data_flow import DataFlowEngine

    DATA_FLOW_AVAILABLE = True
except ImportError:
    DATA_FLOW_AVAILABLE = False

try:
    from ..causality.engine import CausalEngine
    from ..causality.contracts import CausalityProfile

    CAUSALITY_AVAILABLE = True
except ImportError:
    CAUSALITY_AVAILABLE = False

try:
    from ..tracer.engine import RuntimeWraith

    TRACER_AVAILABLE = True
except ImportError:
    TRACER_AVAILABLE = False

Logger = Scribe("OraclePropagator")


class OraclePropagator:
    """
    =================================================================================
    == THE GOD-ENGINE OF PROPAGATION (V-Ω-MULTI-VECTOR-GRAVITY)                    ==
    =================================================================================
    LIF: 10,000,000,000,000,000,000 (THE SIX-FOLD PATH)

    This artisan expands the initial set of Seed files into a complete, context-aware
    network of Gnosis. It orchestrates six distinct movements of expansion and pruning.
    """

    def __init__(self, root: Path, silent: bool = False):
        self.root = root
        self.silent = silent
        self.tracer = RuntimeWraith(root) if TRACER_AVAILABLE else None
        self.causality = CausalEngine(root, silent=True) if CAUSALITY_AVAILABLE else None

    def propagate(self, context: OracleContext):
        """The Grand Symphony of Expansion."""
        t0 = time.time()

        # Initialize the Trace with the Seeds
        context.traced_files = set(context.seed_files)

        # --- MOVEMENT I: THE DYNAMIC HOLOGRAM (PROPHECY VII) ---
        # If dynamic coverage data exists, it acts as the supreme filter.
        self._propagate_dynamic_hologram(context)

        # --- MOVEMENT II: THE RIVER OF DATA (PROPHECY VI) ---
        # Traces specific symbols (taint tracking).
        self._propagate_data_flow(context)

        # --- MOVEMENT III: THE CAUSAL WEB (STATIC GRAPH) ---
        # Expands based on imports and dependencies.
        # (Skipped if 'surgical' strategy is strictly enforced without depth)
        if context.profile.strategy != 'surgical' or context.profile.depth > 0:
            self._propagate_static_causality(context)

        # --- MOVEMENT IV: THE CHRONOMANCER'S WEB (GIT COHESION) ---
        # Pulls in files that historically change together.
        self._propagate_cohesion(context)

        # --- MOVEMENT V: THE SHADOW WEAVE (CONFIGURATION) ---
        # Links code to the config files they consume.
        self._propagate_configuration(context)

        # --- MOVEMENT VI: THE HEURISTIC OF THE VOID (SYMBOLIC PRUNING) ---
        # Calculates exactly which symbols are active within the traced files.
        self._propagate_active_symbols(context)

        duration = (time.time() - t0) * 1000
        context.record_stat('propagation_ms', duration)

        if not self.silent:
            Logger.info(f"Propagation complete. Reality expanded to {len(context.traced_files)} scriptures.")

    def _propagate_dynamic_hologram(self, context: OracleContext):
        """
        [PROPHECY VII] THE DYNAMIC HOLOGRAM.
        If coverage maps exist, they act as a Reality Anchor.
        Only code that was executed is considered 'Real'.
        """
        # Case A: Coverage Map (The New Way)
        if context.profile.coverage_map:
            covered_files = set(context.profile.coverage_map.keys())

            if not self.silent:
                Logger.info(f"Dynamic Hologram Active. Pruning reality to {len(covered_files)} covered files.")

            # The intersection of Intent (Seeds) and Reality (Coverage)
            # We keep seeds even if not covered, to provide context for "why it didn't run".
            context.traced_files = (context.traced_files & covered_files) | context.seed_files

            for f in context.traced_files:
                if f in covered_files:
                    context.add_reason(f, "Executed Code (Hologram)")
                    # Massive score boost for executed code
                    context.impact_scores[f] = 1000

        # Case B: Trace Command (Legacy Way - RuntimeWraith)
        elif context.profile.trace_command and self.tracer:
            Logger.info(f"Summoning Runtime Wraith for: {context.profile.trace_command}")
            result = self.tracer.trace(
                list(context.seed_files),
                context.profile.depth,
                context.memory,
                context.profile.strategy,
                context.profile.trace_command
            )
            # Add dynamically touched files
            for f in result.touched_files:
                if f not in context.traced_files:
                    context.traced_files.add(f)
                    context.impact_scores[f] = 100
                    context.add_reason(f, "Dynamic Trace Execution")
            context.runtime_state = result.runtime_state

    def _propagate_data_flow(self, context: OracleContext):
        """
        [PROPHECY VI] THE RIVER OF DATA.
        Traces variables/symbols from definition to usage across the cosmos.
        """
        if not context.profile.trace_data: return
        if not DATA_FLOW_AVAILABLE or not context.memory:
            Logger.warn("Data Flow Engine not available. The River is dry.")
            return

        df_engine = DataFlowEngine(context.memory)
        # trace_data is a list of symbols, e.g., ["user_password", "AuthService"]
        data_impact = df_engine.trace(context.profile.trace_data)

        for path, boost in data_impact.items():
            context.traced_files.add(path)
            context.impact_scores[path] = context.impact_scores.get(path, 0) + boost
            context.add_reason(path, "Data Flow Trace")

    def _propagate_static_causality(self, context: OracleContext):
        """
        [THE CAUSAL WEB]
        Standard static analysis (Imports/Exports).
        """
        if not self.causality or not context.memory: return

        seeds = list(context.traced_files)

        # [THE FIX] We correctly pass the directional flags to the Profile
        profile = CausalityProfile(
            max_depth=context.profile.depth,
            include_dependents=getattr(context.profile, 'include_dependents', True),
            include_dependencies=getattr(context.profile, 'include_dependencies', True)
        )

        base_scores = {f: 100 for f in seeds}

        impact_scores = self.causality.calculate_impact(
            context.memory, seeds, base_scores, profile
        )

        # Merge scores and expand trace
        for f, score in impact_scores.items():
            current_score = context.impact_scores.get(f, 0)
            context.impact_scores[f] = max(current_score, score)

            # If significant enough, add to trace
            if score > 10 and f not in context.traced_files:
                context.traced_files.add(f)
                context.add_reason(f, f"Static Causality (Score: {score})")

    def _propagate_cohesion(self, context: OracleContext):
        """
        [PROPHECY III] THE CHRONOMANCER'S WEB.
        Uses Git history to find files that are temporally entangled.
        """
        if not context.memory or not context.memory.co_change_graph: return

        # We look at the Seed files.
        for seed in list(context.seed_files):
            partners = context.memory.co_change_graph.get(seed, {})

            # Filter for strong temporal bonds (>5 co-edits)
            for partner, count in partners.items():
                if count > 5:
                    if partner not in context.traced_files:
                        context.traced_files.add(partner)
                        context.add_reason(partner, f"Temporal Cohesion with {seed} ({count} co-edits)")
                        # Moderate boost
                        context.impact_scores[partner] = context.impact_scores.get(partner, 0) + 20

    def _propagate_configuration(self, context: OracleContext):
        """
        [PROPHECY IV] THE SHADOW WEAVE.
        If a traced file uses a config key, pull in the config file.
        """
        if not context.memory: return

        config_files = [g for g in context.memory.inventory if g.category == 'config']

        for config in config_files:
            usage_map = config.ast_metrics.get("config_usage_map", {})
            if not usage_map: continue

            config_path_str = str(config.path).replace('\\', '/')

            # Check if any currently traced file consumes a key from this config
            is_relevant = False
            relevant_keys = []

            for key, consumers in usage_map.items():
                if any(c in context.traced_files for c in consumers):
                    is_relevant = True
                    relevant_keys.append(key)

            if is_relevant:
                if config_path_str not in context.traced_files:
                    context.traced_files.add(config_path_str)
                    context.add_reason(config_path_str, f"Config Provider ({', '.join(relevant_keys[:3])})")
                    context.impact_scores[config_path_str] = context.impact_scores.get(config_path_str, 0) + 30

    def _propagate_active_symbols(self, context: OracleContext):
        """
        [PROPHECY V] THE HEURISTIC OF THE VOID.
        Iterates through all 'Consumer' files.
        Finds what symbols they import/use.
        Marks those symbols as 'Active' in the 'Provider' files.
        """
        if not context.memory: return

        active_map: Dict[str, Set[str]] = defaultdict(set)

        # 1. Identify Consumers (Files currently in the trace)
        consumers = list(context.traced_files)

        for consumer_path in consumers:
            gnosis = context.memory.find_gnosis_by_path(Path(consumer_path))
            if not gnosis: continue

            # Gather used symbols
            used_symbols = set()

            # A. From Imports (File level)
            if gnosis.imported_symbols:
                used_symbols.update(gnosis.imported_symbols)

            # B. From AST (Block level - higher fidelity)
            if gnosis.ast_metrics:
                for block in gnosis.ast_metrics.get('functions', []) + gnosis.ast_metrics.get('classes', []):
                    deps = block.get('dependencies', {})
                    if isinstance(deps, dict):
                        used_symbols.update(deps.get('external', []))

            # 2. Map usages to Providers via Symbol Map
            for symbol in used_symbols:
                # Direct lookup
                provider_path = context.memory.symbol_map.get(symbol)

                # Fallback: Strip module parts (module.Func -> Func)
                if not provider_path and '.' in symbol:
                    short_name = symbol.split('.')[-1]
                    provider_path = context.memory.symbol_map.get(short_name)

                if provider_path:
                    provider_str = str(provider_path).replace('\\', '/')

                    # We only restrict files that are IN the trace.
                    if provider_str in context.traced_files:
                        # Extract simple name (class/func name) from FQN
                        simple_name = symbol.split('.')[-1]
                        active_map[provider_str].add(simple_name)

        # 3. Handle Seeds (The Focus)
        # If strategy is NOT surgical, Seeds are fully active (None).
        # If strategy IS surgical, Seeds are also restricted to what is used/requested.
        for seed in context.seed_files:
            if context.profile.strategy != 'surgical':
                # Mark as None to indicate "Show All"
                active_map[seed] = None
            else:
                # In surgical mode, we must ensure the seed has at least SOME active symbols.
                # If no one calls the seed, we default to "Show All" for the seed itself,
                # assuming the user wants to see what they focused on.
                if seed not in active_map:
                    active_map[seed] = None

        # 4. Update Context
        context.active_symbols_map = {Path(k): v for k, v in active_map.items()}

        if not self.silent and context.active_symbols_map:
            pruned_count = sum(1 for v in active_map.values() if v is not None)
            Logger.verbose(f"Symbolic propagation complete. Pruning dead code in {pruned_count} files.")