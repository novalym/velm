# Path: core/cortex/causal_linker/engine.py
# -----------------------------------------


"""
=================================================================================
== THE SOVEREIGN CAUSAL ASSEMBLER: OMEGA POINT (V-Ω-VMAX-LOCAL-SUPREMACY)      ==
=================================================================================
LIF: ∞^∞ | ROLE: ARCHITECTURAL_GENOME_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
AUTH: Ω_ASSEMBLER_VMAX_TOTALITY_2026_FINALIS

The supreme definitive authority for topological assembly. It orchestrates the
transformation of raw intent into a topologically sound Directed Acyclic Graph (DAG)
and finally into executable Gnostic Scripture. It is self-hydrating, Merkle-warded,
and righteously enforces the Law of Local Supremacy.
=================================================================================
"""
import threading
import os
import uuid
import json
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Any, Union, Optional, Final

# --- THE INTERNAL ORGANS ---
from .resolver import DependencyResolver
from .compiler import BlueprintCompiler
from .contracts import AssemblyManifest, ShardNode
from ..archetype_indexer.scanner import GnosticScanner
from ..archetype_indexer.extractor import SoulExtractor

# --- THE SOUL (DNA) ---
from ....contracts.data_contracts import ShardHeader

# --- CORE UPLINKS ---
from ....logger import Scribe
from ....contracts.heresy_contracts import ArtisanHeresy, HeresySeverity

Logger = Scribe("CausalAssembler")


class CausalAssembler:
    """
    The High Conductor of Topological Assembly.
    The single point of truth for forging the Causal DAG.
    """

    def __init__(self, engine: Any):
        """
        [THE RITE OF INCEPTION: APOPHATIC VELOCITY]
        Initializes the facade. Performs zero I/O at birth; materializes
        memory JIT during the first assembly plea.
        """
        self.engine = engine
        self.registry_path = Path.home() / ".scaffold" / "registry" / "index.json"

        # --- STRATUM: MEMORY ---
        self._grimoire: List[ShardNode] = []
        self._last_merkle_root: str = "0xVOID"
        self._last_load_ts: float = 0.0
        self._resolver: Optional[DependencyResolver] = None

        # --- ORGANS ---
        self.compiler = BlueprintCompiler()

        # [ASCENSION 13]: Hydraulic Lock to prevent rehydration races
        self._hydration_lock = threading.RLock()

    def _rehydrate_if_drifted(self):
        """
        =============================================================================
        == THE RITE OF REHYDRATION (V-Ω-TOTALITY-LOCAL-SUPREMACY-CURE)             ==
        =============================================================================
        [THE CURE]: Achieves Local Supremacy. It actively scries the physical iron
        for V3.0 Headers *before* consulting the Celestial Hub. This guarantees
        that local capabilities are perfectly parsed and never overwritten by
        stale remote caches.
        """
        # [ASCENSION 17]: Thermodynamic Backpressure Sensing
        if hasattr(self.engine, 'watchdog') and self.engine.watchdog.get_vitals().get("load_percent", 0) > 92.0:
            time.sleep(0.01)  # Yield to cooler threads

        with self._hydration_lock:
            # We perform the scan if the cache is empty or we haven't scried in 10s
            if self._grimoire and (time.time() - self._last_load_ts < 10.0):
                return

            start_ns = time.perf_counter_ns()
            Logger.info(f"🔄 [ASSEMBLER] Rehydrating Causal Spine from Local Iron & Celestial Hub...")

            # =========================================================================
            # == 1. THE IRON CENSUS (Local Physical Shards)                         ==
            # =========================================================================
            # [ASCENSION 1]: Local Iron Supremacy.
            # We use the GnosticScanner to find every .scaffold file in the core.
            scanner = GnosticScanner(self.engine.project_root if self.engine else Path.cwd(), engine=self.engine)
            extractor = SoulExtractor()

            new_grimoire = []
            local_ids = set()

            for path in scanner.scan():
                try:
                    # Resolve ID based on directory context (e.g., system/python-core)
                    # We look at the parent folder name to categorize.
                    category = path.parent.name
                    rel_id = f"{category}/{path.stem}" if category != "shards" else path.stem

                    # [STRIKE]: Extract the full V3.0 Genomic DNA
                    header, _ = extractor.extract(path, rel_id)

                    # Transmute into a DAG ShardNode with full metadata
                    node = ShardNode(
                        id=header.id,
                        version=header.version,
                        tier=header.tier,
                        summary=header.summary,
                        vibe=header.vibe,
                        provides=header.provides,
                        requires=header.requires,
                        metabolism=header.metabolism,
                        substrate=header.substrate,
                        suture=header.suture,
                        resonance_score=1.0  # Local shards are high-status
                    )
                    new_grimoire.append(node)
                    local_ids.add(header.id)
                except Exception as e:
                    Logger.debug(f"   -> Skipping malformed local shard {path.name}: {e}")

            # =========================================================================
            # == 2. THE CELESTIAL CENSUS (Remote Hub)                                ==
            # =========================================================================
            # We only merge remote shards if they provide capabilities not manifest on Iron.
            if self.registry_path.exists():
                try:
                    raw_json = self.registry_path.read_text('utf-8')
                    data = json.loads(raw_json)

                    for s_data in data.get("registry", []):
                        sid = s_data.get('id')
                        # [THE MOAT]: Local sovereignty overrides remote aether.
                        if sid not in local_ids:
                            try:
                                new_grimoire.append(ShardNode.model_validate(s_data))
                            except Exception:
                                pass
                except Exception as e:
                    Logger.warn(f"   -> Celestial Hub scry fractured: {e}")

            # --- THE SINGULARITY BINDING ---
            self._grimoire = new_grimoire

            # [ASCENSION 15]: Re-materialize the Resolver with the new truth
            self._resolver = DependencyResolver(self._grimoire)

            # Update temporal and cryptographic anchors
            self._last_merkle_root = hashlib.sha256(str(len(new_grimoire)).encode()).hexdigest()
            self._last_load_ts = time.time()

            duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
            Logger.success(f"✅ Spine Resonant. {len(self._grimoire)} shards manifest in {duration_ms:.2f}ms.")
            self._multicast_hud("DAG_REHYDRATION_COMPLETE", "#64ffda")

    def assemble_reality(self, intent: str, semantic_hits: List[Dict[str, Any]],
                         willed_gnosis: Optional[Dict[str, Any]] = None) -> AssemblyManifest:
        """
        =============================================================================
        == THE GRAND RITE OF ASSEMBLY (V-Ω-TOTALITY-VMAX-GENOMIC-SUTURE)           ==
        =============================================================================
        Input: Raw intents elected by the SemanticResolver.
        Output: A bit-perfect, topologically sorted AssemblyManifest scripture.
        """
        start_ns = time.perf_counter_ns()

        # [ASCENSION 5]: Trace ID Cord Binding
        trace_id = (willed_gnosis or {}).get("trace_id") or os.environ.get(
            "GNOSTIC_TRACE_ID") or f"tr-asm-{uuid.uuid4().hex[:6].upper()}"

        # 1. THE AWAKENING
        self._rehydrate_if_drifted()

        if not self._resolver:
            self._resolver = DependencyResolver(self._grimoire)

        Logger.info(f"🧩 [ASSEMBLER] Initiating Autonomic Causal Linking for Trace: {trace_id}")

        # --- MOVEMENT I: TOPOLOGICAL RESOLUTION ---
        # The resolver builds the DAG and performs the Tarjan-Kahn auto-healing sort.
        manifest = self._resolver.resolve(semantic_hits)
        manifest.trace_id = trace_id

        # =========================================================================
        # == MOVEMENT II: THE GENOMIC SUTURE (THE MASTER CURE)                   ==
        # =========================================================================
        # [ASCENSION 2]: We populate the manifest with full V3.0 DNA.
        # This allows the Motor Cortex (Parser) to aggregate metabolic mass.
        grimoire_map: Dict[str, ShardNode] = {s.id: s for s in self._grimoire}

        for node in manifest.ordered_shards:
            header_dna = grimoire_map.get(node.id)
            if header_dna:
                # [STRIKE]: Suture the full genomic data into the manifest dictionary.
                manifest.manifests[node.id] = header_dna

        # --- MOVEMENT III: BLUEPRINT COMPILATION ---
        if manifest.is_executable and manifest.ordered_shards:
            engine_vars = getattr(self.engine, 'variables', {})

            # [ASCENSION 18]: Sovereign Variable Suture
            # We strictly merge the Architect's Willed Gnosis over the Engine defaults
            final_vars = {**engine_vars, **(willed_gnosis or {})}

            # [STRIKE]: The Compiler transmutes the DAG into a .scaffold manifest
            manifest.compiled_blueprint = self.compiler.compile(
                ordered_shards=manifest.ordered_shards,
                primary_intent=intent,
                existing_vars=final_vars,
                shard_manifests=manifest.manifests
            )

            # [ASCENSION 12]: Merkle Seal Finality
            manifest.seal_manifest()

            Logger.success(f"✨ Gnostic Scripture forged with {len(manifest.ordered_shards)} atoms. [RESONANT]")
        else:
            # [ASCENSION 7]: Socratic Gap Diagnosis
            for gap in manifest.unresolved_requirements:
                Logger.warn(f"   -> [GNOSTIC_VOID] {gap}")
            for conflict in manifest.conflicts:
                Logger.error(f"   -> [CAUSAL_CONFLICT] {conflict}")

            # [ASCENSION 21]: Haptic Failure Signaling
            manifest.ui_hints.update({"vfx": "shake_red", "aura": "#ef4444"})

        # --- MOVEMENT IV: METABOLIC FINALITY ---
        duration_ms = (time.perf_counter_ns() - start_ns) / 1_000_000
        manifest.latency_ms = duration_ms

        return manifest

    def _multicast_hud(self, type_label: str, color: str):
        """[ASCENSION 16]: Radiates the assembly pulse to the Ocular HUD."""
        if self.engine and hasattr(self.engine, 'akashic') and self.engine.akashic:
            try:
                self.engine.akashic.broadcast({
                    "method": "novalym/hud_pulse",
                    "params": {
                        "type": type_label,
                        "label": "CAUSAL_ASSEMBLER",
                        "color": color,
                        "trace": getattr(self.engine.context, 'session_id', 'tr-unbound')
                    }
                })
            except Exception:
                pass

    def __repr__(self) -> str:
        status = "RESONANT" if self._grimoire else "DORMANT"
        return f"<Ω_CAUSAL_ASSEMBLER status={status} shards={len(self._grimoire)}>"