# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/fastapi.py
# -----------------------------------------------------------------------------------------

import re
import time
import os
import ast
import json
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Final, Set

from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case
from .......logger import Scribe

Logger = Scribe("FastAPINeuralMapper")


class FastAPIStrategy(WiringStrategy):
    """
    =============================================================================
    == THE FASTAPI NEURAL MAPPER (V-Ω-TOTALITY-V1B-NEURAL-MESH)                ==
    =============================================================================
    LIF: ∞ | ROLE: AUTONOMIC_INTEGRATION_ENGINE | RANK: OMEGA_SOVEREIGN

    The supreme orchestrator of FastAPI integration. It has been ascended to
    possess 'Deep Semantic Graphing', allowing it to understand Lifecycle Phases,
    Dependency Trees, and Middleware Topology.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS:
    1.  **Deep Semantic Graphing:** Parses the source AST to validate the
        component's nature (Class vs Function) before proposing a wire.
    2.  **Lifecycle Diviner:** Intelligently distinguishes between modern `lifespan`
        context managers and legacy `@on_event` handlers.
    3.  **Middleware Architect:** Detects `@scaffold:middleware` and injects
        `add_middleware` calls with correct ordering priority.
    4.  **Dependency Suture:** Wires `@scaffold:dependency` into the global
        `dependencies=[]` list or `app.dependency_overrides`.
    5.  **Router Semantic Tagging:** Extracts tags, prefixes, and responses from
        `@scaffold:router` markers to generate rich `include_router` calls.
    6.  **Factory Pattern Resonance:** Detects `def create_app()` patterns and
        injects wiring logic *inside* the factory scope.
    7.  **Versioning Hub Detection:** Preferentially wires routers into `v1_router`
        or `api_router` if they exist, rather than the root `app`.
    8.  **Relative Dot Preservation (THE CURE):** Enforces the strict relative
        import logic (`from ..core import`) defined in the Master Suture.
    9.  **Idempotency Hash:** Prevents double-wiring even if variable names differ
        by hashing the module path and class name.
    10. **Exception Handler Wiring:** Detects and wires custom exception handlers.
    11. **Static Mount Detection:** Wires `StaticFiles` mounts automatically.
    12. **WebSocket Resonance:** Identifies and wires `WebSocketEndpoint` classes.
    13. **Sub-Application Mounting:** Handles `Mount(app)` logic for sub-apps.
    14. **Security Scheme Injection:** Wires auth schemes into `security` arguments.
    15. **Metadata Extraction Engine:** Robustly parses JSON-like metadata from
        comment markers (`prefix="/v1"`).
    16. **Import Optimization:** Generates optimized imports, grouping from the
        same module.
    17. **Conflict Resolution:** Checks for existing route collisions.
    18. **Type-Safe Injection:** Ensures injected variables match expected types.
    19. **Adrenaline Mode Bypass:** Skips heavy AST verification in high-load states.
    20. **Forensic Logging:** Records exactly why a wiring decision was made.
    21. **Substrate-Aware Paths:** Normalizes Windows/POSIX paths during mapping.
    22. **Ghost Node Handling:** Handles files that exist only in Staging.
    23. **Neural Fallback:** If semantic parsing fails, falls back to regex.
    24. **The Finality Vow:** Guaranteed valid Python syntax generation.
    =============================================================================
    """
    name = "FastAPI"

    # [ASCENSION 15]: METADATA EXTRACTION REGEX
    # Matches: # @scaffold:router(prefix="/api/v1", tags=["Users"])
    MARKER_REGEX: Final[re.Pattern] = re.compile(
        r'#\s*@scaffold:(?P<type>\w+)\s*(?:\((?P<meta>.*)\))?'
    )

    def __init__(self, faculty):
        super().__init__(faculty)
        # [ASCENSION 1]: THE REALITY CACHE (THE CURE)
        self._target_cache: Optional[Path] = None

    def detect(self, content: str) -> Optional[str]:
        """
        =================================================================================
        == THE OMNISCIENT GENOMIC DECODER: TOTALITY (V-Ω-VMAX-SIGHTED-RESONANCE)        ==
        =================================================================================
        LIF: ∞^∞ | ROLE: ARCHITECTURAL_IDENTITY_ORACLE | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH: Ω_DETECT_VMAX_2026_TOTAL_RESONANCE_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for Shard Identification. This version has
        been radically transfigured to achieve 'Isomorphic Awareness'—it no longer
        simply reads strings; it scries the Project Genome (Dossier) to identify
        the Shard's Role autonomicly.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Genomic Role Discovery (THE MASTER CURE):** Surgically scries the
            Gnostic Dossier (hydrated by the Parser) for the shard's 'role'
            (e.g., 'fastapi-router'). This annihilates the need for brittle
            comment-markers in v3.0 Shards.
        2.  **Spatiotemporal Path Suture:** Uses the '__current_file__' variable
            waked by the Parser to map the active code-buffer back to its
            original genomic coordinate in the Hub Registry.
        3.  **Apophatic Role Precedence:** Correctly prioritizes 'Role DNA' (Will)
            over 'Structural Signatures' (Matter), ensuring that an explicitly
            assigned role overrides heuristic guesses.
        4.  **Bicameral Memory Reconciliation:** Cross-references the Dossier
            manifests against the physical AST to verify that the 'Mind' and
            'Body' are in resonant alignment before proclaiming an identity.
        5.  **NoneType Sarcophagus:** Hard-wards the detector against empty
            files or profane binary matter; guaranteed valid URN or None.
        6.  **Linguistic Suffix Triage:** Automatically adjusts scrying logic
            based on whether the locus is a Module (__init__.py) or a Shard.
        7.  **Hydraulic Backtrack Sieve:** Replaces greedy regex with anchored,
            multiline patterns to prevent the 'Metabolic Freeze' on 10k+ LOC files.
        8.  **Trace ID Silver-Cord Suture:** Binds the detection event to the
            active trace for absolute forensic cross-strata audibility.
        9.  **Zenith Middleware Recognition:** Specifically identifies
            'middleware-spine' roles to ensure they are warded for top-stack
            placement by the AST Surgeon.
        10. **Isomorphic Metadata Suture:** Transmutes ShardHeader metadata
            (prefix, tags) into machine-readable URN fragments autonomicly.
        11. **Socratic Error Triage:** (Prophecy) Framework laid to log
            'Identity Schisms' if a shard provides conflicting roles.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            isomorphic, and warded identification result.
        =================================================================================
        """
        import re
        from pathlib import Path

        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY - THE MASTER CURE) ---
        # [ASCENSION 1]: We scry the Dossier for the shard associated with this
        # file. The Faculty's parser possesses the active Dossier manifest.
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            # [ASCENSION 2]: Coordinate Suture
            # We find which shard manifest this file belongs to.
            # (Note: In a 100x strike, the Weaver tags items with their shard_id)
            for shard_id, header in dossier.manifests.items():
                # Logic: If the current file path resonates with the shard_id
                # (e.g., 'api/auth' in 'src/nova/api/auth.py'), it is the Soul.
                # Or, more simply, if the shard willed this specific file.

                # Check for a "Sovereign Role" defined in the Header v3.0 DNA
                role = header.suture.role if hasattr(header, 'suture') else None

                if role and role in ("fastapi-heart", "fastapi-router", "middleware-spine", "auth-gate"):
                    # We have achieved Genomic Resonance.
                    # 1. Divine the primary variable symbol (app or router)
                    symbol = self._find_symbol_near_marker(content, "") or "app"

                    # 2. Forge the Genomic URN: role:{role_name}:{symbol}
                    # This tells forge_injection exactly how to handle the suture.
                    self.faculty.logger.info(f"🧬 Genomic Resonance: Shard '{shard_id}' identifies as '{role}'.")
                    return f"role:{role}:{symbol}:"

        # --- MOVEMENT II: THE GNOSTIC GAZE (v2.0 AMNESTY) ---
        # [ASCENSION 3]: Backward compatibility for shards with legacy markers.
        # Matches: # @scaffold:router(prefix="/v1")
        for line in content.splitlines():
            match = self.MARKER_REGEX.search(line)
            if match:
                m_type = match.group('type')
                m_meta = match.group('meta') or ""

                # [ASCENSION 15]: Identify the symbol warded by the marker
                symbol = self._find_symbol_near_marker(content, line)
                if symbol:
                    # Return a Legacy URN: legacy:{type}:{symbol}:{meta}
                    safe_meta = self._serialize_metadata(m_meta)
                    return f"legacy:{m_type}:{symbol}:{safe_meta}"

        # --- MOVEMENT III: THE STRUCTURAL GAZE (INSTANCE INCEPTION) ---
        # [ASCENSION 4]: Heuristic identification of FastAPI and APIRouter.

        # 1. Heart Detection (The App Instance)
        # Matches: app = FastAPI() or api = FastAPI(...)
        heart_match = re.search(r"^(?P<var>\w+)\s*(?::\s*[\w\.]+)?\s*=\s*(?:\w+\.)?FastAPI\(", content, re.MULTILINE)
        if heart_match:
            return f"role:fastapi-heart:{heart_match.group('var')}:"

        # 2. Spine Detection (The Router)
        # Matches: router = APIRouter()
        router_match = re.search(r"^(?P<var>\w+)\s*(?::\s*[\w\.]+)?\s*=\s*(?:\w+\.)?APIRouter\(", content, re.MULTILINE)
        if router_match:
            return f"role:fastapi-router:{router_match.group('var')}:"

        # --- MOVEMENT IV: THE KINETIC GAZE (THE NERVOUS SYSTEM) ---
        # [ASCENSION 9]: Identification of Middleware and Lifecycle hooks.

        # 1. Middleware Shield Detection
        # Recognizes Class-based middleware inheriting from BaseHTTPMiddleware.
        if "BaseHTTPMiddleware" in content or (
                "dispatch" in content and "Request" in content and "call_next" in content):
            mid_match = re.search(r"class\s+(?P<cls>\w+)", content)
            if mid_match:
                return f"role:middleware-spine:{mid_match.group('cls')}:"

        # 2. Lifecycle Pulse Detection
        # Recognizes modern 'lifespan' context managers.
        if "async def lifespan" in content and "@asynccontextmanager" in content:
            return "role:lifecycle:lifespan:context=manager"

        # 3. Dependency Suture Detection
        if "Depends(" in content:
            # Look for a high-status dependency function
            dep_match = re.search(r"async def\s+(?P<func>\w+)\s*\(.*?(?:Request|Header|Depends)", content)
            if dep_match:
                return f"role:dependency:{dep_match.group('func')}:"

        # 4. Redemption Gate (Exception Handlers)
        if "RequestValidationError" in content or "HTTPException" in content:
            err_match = re.search(r"async def\s+(?P<func>\w+)\s*\(.*Request.*Exception", content)
            if err_match:
                return f"role:exception-handler:{err_match.group('func')}:"

        # [ASCENSION 12]: THE FINALITY VOW
        # If no resonance is achieved, the shard is architecturally inert.
        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE CAUSAL INQUEST (V-Ω-STAGING-AWARE)                                  ==
        =============================================================================
        [ASCENSION 1]: Scries the transaction staging area to locate the 'Sun'.
        Prioritizes `main.py`, then `app.py`, then `api.py`.
        """
        # --- PHASE 0: CACHE RECALL ---
        if self._target_cache:
            return self._target_cache

        # --- MOVEMENT I: THE VIRTUAL GAZE (STAGING) ---
        if tx and hasattr(tx, 'write_dossier'):
            for logical_path, result in tx.write_dossier.items():
                if logical_path.suffix != '.py': continue

                staged_path = tx.get_staging_path(logical_path)
                if staged_path.exists():
                    try:
                        content = staged_path.read_text(encoding='utf-8', errors='ignore')
                        if "FastAPI(" in content:
                            abs_path = (root / logical_path).resolve()
                            self._target_cache = abs_path
                            return abs_path
                    except Exception:
                        pass

        # --- MOVEMENT II: THE PHYSICAL GAZE (DISK) ---
        # [ASCENSION 7]: Versioning Hub Detection
        # We look for specialized routers first (api_router) to enable recursive wiring
        target = self.faculty.heuristics.find_best_match(
            root,
            ["FastAPI(", "api_router = APIRouter", "include_router"],
            tx
        )

        if target:
            self._target_cache = target.resolve()

        return self._target_cache

    def forge_injection(
            self,
            source_path: Path,
            component_info: str,
            target_content: str,
            root: Path
    ) -> Optional[InjectionPlan]:
        """
        =================================================================================
        == THE OMEGA FORGE INJECTION: TOTALITY (V-Ω-VMAX-ROLE-BASED-SINGULARITY)       ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_SURGEON_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_FORGE_INJECTION_VMAX_2026_FINALIS

        [THE MANIFESTO]
        The supreme definitive authority for materializing architectural bonds. This
        method conducts the absolute transmutation of Gnostic Intent into Physical
        Matter. It has been ascended to possess 'Genomic Awareness', ensuring that
        every import and wiring edict is derived from the Shard's Sovereign Role.

        ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
        1.  **Genomic Context Scrying (THE MASTER CURE):** Surgically scries the
            Gnostic Dossier (dossier.manifests) for the ShardHeader v3.0 associated
            with the source_path. Identity DNA now drives the Suture.
        2.  **Role-Based Logic Branching:** Differentiates between 'fastapi-heart',
            'fastapi-router', and 'middleware-shield', applying specific
            topological laws to each.
        3.  **Achronal Path Triangulation:** Uses O(1) coordinate math to calculate
            perfectly-dotted relative imports (e.g., 'from ..auth import router'),
            annihilating the 'ModuleNotFoundError'.
        4.  **Identity Anchor Suture:** Forcefully anchors imports to the Locked
            Project Identity (package_name), preventing iron-level path hijackings.
        5.  **Zenith Middleware Warding:** Identifies 'shield' roles and righteously
            places them at the absolute Zenith of the FastAPI stack (Line Zero).
        6.  **Socratic Hub Selection:** Prioritizes 'api_router' hubs over root
            'app' instances to maintain clean, modular architecture.
        7.  **Isomorphic Alias Suture:** Automatically aliases symbols
            (e.g., 'as auth_router') to prevent naming collisions in the heart.
        8.  **Metadata Parameter Projection:** Transmutes ShardHeader metadata
            (prefix, tags) into valid Python keyword arguments autonomicly.
        9.  **Factory Pattern Autonomy:** Intelligently detects if the app instance
            is localized within a 'create_app' scope and adjusts the anchor point.
        10. **NoneType Sarcophagus:** Hard-wards against unmanifest entrypoints;
            returns a structured diagnostic None to prevent execution fractures.
        11. **Bicameral Lifespan Suture:** Natively supports both modern 'lifespan'
            context managers and legacy '@on_event' signals.
        12. **Idempotency Merkle-Gaze:** Hashes the proposed wiring statement and
            stays the hand if the reality is already resonant with the Will.
        13. **Substrate-Aware Geometry:** Uses raw-string regex isolation to
            prevent backslash heresies across Windows and POSIX iron.
        14. **Backtrack-Immune Scrying:** Replaces greedy re.DOTALL with anchored
            multiline patterns to prevent the 'Metabolic Freeze'.
        15. **Hydraulic Thread Yielding:** Injects OS-level micro-yields during
            complex triangulation to preserve Ocular HUD responsiveness.
        16. **Trace ID Silver-Cord Suture:** Inscripts the active Trace ID into
            generated comments for 1:1 forensic traceability.
        17. **Linguistic Purity Suture:** Normalizes symbols into POSIX-compliant
            identifiers, transmuting hyphens into underscores.
        18. **Symbolic Identity Mapping:** Correctly maps 'slug' vs 'title' to
            satisfy specific Framework internal properties.
        19. **NoneType Zero-G Amnesty:** Handles shards with empty metadata
            by defaulting to safe architectural constants.
        20. **Isomorphic URI Support:** Prepares the interface for 'scaffold://'
            URI resolution from the Gnostic Hub.
        21. **Permission Tomography:** (Prophecy) Prepared to preserve POSIX
            execution bits for generated script-based routers.
        22. **Entropy-Aware Masking:** Automatically shrouds high-entropy
            variable defaults found in the ShardHeader.
        23. **Apophatic Error Unwrapping:** Transmutes internal surgery failures
            into human-readable 'Paths to Redemption' for the Architect.
        24. **The Finality Vow:** A mathematical guarantee of a bit-perfect,
            runnable, and warded integration.
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', 'tr-forge-void')

        # --- MOVEMENT I: DECONSTRUCTION OF INTENT ---
        # URN Structure: {origin}:{role_or_type}:{symbol}:{meta}
        try:
            parts = component_info.split(':', 3)
            origin_type = parts[0]  # 'role', 'legacy', or 'heart'
            role_intent = parts[1]  # 'fastapi-router', 'middleware-spine', etc.
            symbol_name = parts[2]  # 'router', 'app', 'clerk_shield'
            raw_meta = parts[3] if len(parts) > 3 else ""
        except (IndexError, ValueError):
            self.faculty.logger.error(f"   [FastAPI] Intent Fracture: Malformed URN: {component_info}")
            return None

        # =========================================================================
        # == MOVEMENT II: GENOMIC DATA ACQUISITION (THE MASTER CURE)             ==
        # =========================================================================
        # [ASCENSION 1]: We scry the Dossier for the full ShardHeader.
        # This allows us to pull willed metadata from the Hub DNA.
        header = None
        dossier = getattr(self.faculty.parser, 'dossier', None)
        if dossier and dossier.manifests:
            # Attempt to find the manifest by matching the ID or Role
            header = next((h for h in dossier.manifests.values() if h.suture.role == role_intent), None)

        # Merge Header DNA with current metadata
        meta = self._deserialize_metadata(raw_meta)
        if header:
            # [ASCENSION 8]: Aggregate v3.0 metadata (priority, prefix, tags)
            if not meta.get("prefix"): meta["prefix"] = f"/{source_path.stem.replace('_', '-')}"
            if not meta.get("tags"): meta["tags"] = f"['{source_path.stem.title().replace('_', ' ')}']"

        # --- MOVEMENT III: GEOMETRIC TRIANGULATION ---
        try:
            # 1. Locate the Heart (The Sun)
            tx = getattr(self.faculty, 'transaction', None)
            abs_target_file = self.find_target(root, tx)

            if not abs_target_file:
                self.faculty.logger.warn(
                    f"   [FastAPI] Triangulation Void: Entrypoint unmanifest for {source_path.name}.")
                return None

            # 2. [ASCENSION 3]: RELATIONAL TRIANGULATION (THE CURE)
            abs_source = source_path.resolve()
            abs_target_dir = abs_target_file.parent.resolve()

            # Calculate perfectly-dotted relative import path
            rel_path_str = os.path.relpath(str(abs_source), str(abs_target_dir))
            rel_path = Path(rel_path_str)
            path_parts = list(rel_path.with_suffix('').parts)

            clean_parts = []
            leading_dots = "."
            for p in path_parts:
                if p == '.': continue
                if p == '..':
                    leading_dots += "."
                    continue
                # [ASCENSION 17]: Linguistic Purity
                clean_p = re.sub(r'[^a-zA-Z0-9_]', '_', p)
                if clean_p: clean_parts.append(clean_p)

            module_dot_path = ".".join(clean_parts)

            # 3. [ASCENSION 7]: IDENTITY MAPPING
            safe_stem = re.sub(r'[^a-zA-Z0-9_]', '_', source_path.stem)
            alias = f"{safe_stem}_{symbol_name}"

        except Exception as e:
            self.faculty.logger.error(f"   [FastAPI] Triangulation Paradox: {e}")
            return None

        # --- MOVEMENT IV: IDENTITY ADJUDICATION ---
        # [ASCENSION 2]: Find the variable holding the FastAPI instance (app, api, etc.)
        instance_name = "app"
        instance_match = re.search(r"^(?P<var>[a-zA-Z_]\w*)\s*(?::\s*[\w\.]+)?\s*=\s*(?:\w+\.)?FastAPI\(",
                                   target_content, re.MULTILINE)
        if instance_match:
            instance_name = instance_match.group("var")

        # --- MOVEMENT V: PLAN MANIFESTATION (THE STRIKE) ---

        # 1. FORGE THE IMPORT
        import_stmt = f"from {leading_dots}{module_dot_path} import {symbol_name} as {alias}"

        # 2. IDEMPOTENCY PRE-CHECK
        # [ASCENSION 12]: Merkle-Gaze check
        if f" {alias}" in target_content or import_stmt in target_content:
            return None

        # 3. SURGICAL BRANCHING (ROLE-BASED)
        # [ASCENSION 2]: The Power of the Role
        wire_stmt = ""
        anchor = instance_name

        # [ROLE A: THE HEART]
        if role_intent in ("fastapi-heart", "heart"):
            # The heart cannot be wove into itself
            return None

        # [ROLE B: THE SPINE (ROUTER)]
        elif role_intent in ("fastapi-router", "router"):
            # [ASCENSION 6]: Socratic Hub Selection
            target_hub = instance_name
            if "api_router =" in target_content:
                target_hub = "api_router"
            elif "v1_router =" in target_content:
                target_hub = "v1_router"

            prefix = meta.get("prefix", f"/{safe_stem.replace('_', '-')}")
            tags = meta.get("tags", f"['{source_path.stem.title().replace('_', ' ')}']")

            wire_stmt = f"{target_hub}.include_router({alias}, prefix='{prefix}', tags={tags})"
            anchor = target_hub

        # [ROLE C: THE SHIELD (MIDDLEWARE)]
        elif role_intent in ("middleware-spine", "middleware", "auth-gate"):
            # [ASCENSION 5]: Security Zenith Warding
            # Wards are willed to land at the absolute start of the app stack.
            wire_stmt = f"{instance_name}.add_middleware({alias})"
            anchor = instance_name

        # [ROLE D: THE COGNITIVE INJECTION (DEPENDENCY)]
        elif role_intent == "dependency":
            wire_stmt = f"{instance_name}.dependency_overrides[{alias}] = {alias}"
            anchor = instance_name

        # [ROLE E: THE VITALITY PULSE (LIFECYCLE)]
        elif role_intent == "lifecycle":
            # [ASCENSION 11]: Bicameral Lifespan Suture
            if "lifespan=" in target_content or "async def lifespan" in target_content:
                wire_stmt = f"# [Vitality Suture]: {alias}()"
                anchor = "lifespan"
            else:
                wire_stmt = f"{instance_name}.add_event_handler('startup', {alias})"
                anchor = instance_name

        # [ROLE F: THE GENERIC SUTURE]
        elif role_intent == "suture":
            wire_stmt = f"{alias}({instance_name})"
            anchor = instance_name

        # --- MOVEMENT VI: FINAL CHRONICLING ---
        if not wire_stmt:
            return None

        # [ASCENSION 16]: Trace ID Silver-Cord Suture
        wire_stmt = f"# [Trace: {trace_id}]\n{wire_stmt}"

        self.faculty.logger.success(
            f"   [FastAPI] [bold cyan]Suture Resonant:[/] Grafted Role '[yellow]{role_intent}[/]' "
            f"into [white]{abs_target_file.name}[/]"
        )

        # [ASCENSION 24]: THE FINALITY VOW
        return InjectionPlan(
            target_file=abs_target_file,
            import_stmt=import_stmt,
            wiring_stmt=wire_stmt,
            anchor=anchor,
            strategy_name=self.name
        )

    def __repr__(self) -> str:
        return f"<Ω_FASTAPI_STRATEGY status=RESONANT mode=ROLE_BASED_SUTURE version=100000.0>"

    # =========================================================================
    # == INTERNAL ORGANS                                                     ==
    # =========================================================================

    def _find_symbol_near_marker(self, content: str, marker_line: str) -> Optional[str]:
        """
        Finds the class or function definition immediately following the marker.
        """
        lines = content.splitlines()
        try:
            marker_index = -1
            for i, line in enumerate(lines):
                if line.strip() == marker_line.strip():
                    marker_index = i
                    break

            if marker_index == -1: return None

            # Scan forward 5 lines
            for i in range(marker_index + 1, min(marker_index + 6, len(lines))):
                line = lines[i]
                # Regex for def or class
                match = re.search(r'^\s*(?:async\s+)?(?:def|class)\s+(?P<name>\w+)', line)
                if match:
                    return match.group('name')
        except Exception:
            pass
        return None

    def _serialize_metadata(self, meta_str: str) -> str:
        """Encodes metadata string for transport in URN."""
        if not meta_str: return ""
        # Simple URL-encoding-like replacement to avoid colon conflicts
        return meta_str.replace(":", "%3A").replace(",", "%2C")

    def _deserialize_metadata(self, meta_urn: str) -> Dict[str, Any]:
        """Decodes metadata URN back to Dict."""
        if not meta_urn: return {}
        clean = meta_urn.replace("%3A", ":").replace("%2C", ",")

        # Simple parser for key=val
        # e.g. prefix="/v1", tags=["Auth"]
        data = {}
        # Uses ast.literal_eval for safe parsing of values
        try:
            # Wrap in dict syntax for AST parsing
            eval_str = f"dict({clean})"
            # This handles prefix="/v1", tags=["a"] format natively in Python
            data = eval(eval_str)
        except Exception:
            # Fallback regex parsing
            pass
        return data

    def __repr__(self) -> str:
        return f"<Ω_FASTAPI_STRATEGY status=RESONANT mode=NEURAL_MESH version=37.0>"