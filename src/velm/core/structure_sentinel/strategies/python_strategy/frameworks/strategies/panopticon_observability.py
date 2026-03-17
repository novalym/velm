# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/panopticon_observability.py
# ----------------------------------------------------------------------------------------------------------


import re
import time
import os
import ast
import json
import hashlib
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Final, Set

# --- THE DIVINE UPLINKS ---
from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case
from .......logger import Scribe

Logger = Scribe("PanopticonSovereignConductor")


class PanopticonObservabilityStrategy(WiringStrategy):
    """
    =================================================================================
    == THE PANOPTICON OBSERVABILITY STRATEGY: OMEGA (V-Ω-TOTALITY-VMAX-V52)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TELEMETRY_ORCHESTRATOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_PANOPTICON_VMAX_SGF_PURIFIED_2026_FINALIS

    [THE MANIFESTO]
    The absolute final authority for system observability. This version righteously
    implements the **Stealth Trace Suture**, mathematically annihilating the
    "Formatter's Paradox" by passing Trace IDs securely via metadata rather than
    polluting the Python AST with manual trace comments.

    This organ provides only pure Python intent to the AST Surgeon, allowing the
    Downward Laminar Suture (Vertical Sanctuary) to handle all tracing and
    geometric voids natively.
    =================================================================================
    """

    name = "PanopticonObservability"

    # [ASCENSION 15]: APOPHATIC SENSOR DISCOVERY
    SENSORY_MARKER: Final[re.Pattern] = re.compile(
        r'#\s*@scaffold:(?P<type>observe|span|metric|trace|instrument|logger|sentry)(?:\((?P<meta>.*)\))?'
    )

    def __init__(self, faculty):
        """[THE RITE OF INCEPTION]"""
        super().__init__(faculty)
        self._target_cache: Optional[Path] = None

    def detect(self, content: str) -> Optional[str]:
        """
        =============================================================================
        == THE GENOMIC DECODER (V-Ω-TOTALITY-VMAX-SIGHTED-RESONANCE)               ==
        =============================================================================
        LIF: 100,000x | ROLE: SENSORY_RESONATOR
        """
        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY) ---
        # [ASCENSION 1]: Genomic Role Synthesis
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None
                # Scry for exact observability role resonance
                if role in ("observability-bastion", "telemetry-probe", "trace-radiator",
                            "exception-alchemist", "database-sentinel"):
                    symbol = self._find_symbol_near_marker(content, "") or "TelemetryHub"
                    return f"role:{role}:{symbol}:"

        # --- MOVEMENT II: THE GNOSTIC GAZE (v2.0 AMNESTY) ---
        for line in content.splitlines():
            match = self.SENSORY_MARKER.search(line)
            if match:
                m_type = match.group('type')
                m_meta = match.group('meta') or ""
                symbol = self._find_symbol_near_marker(content, line)
                if symbol:
                    return f"legacy:{m_type}:{symbol}:{self._serialize_metadata(m_meta)}"

        # --- MOVEMENT III: THE STRUCTURAL GAZE (ZENITH DETECTION) ---
        if "TracerProvider" in content or "instrument_app(" in content or "init_sentry(" in content:
            symbol = self._find_symbol_near_marker(content, "") or "Tracer"
            return f"role:observability-bastion:{symbol}:"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE BICAMERAL TARGET RESOLVER (V-Ω-STAGING-AWARE)                       ==
        =============================================================================
        [ASCENSION 3]: Prioritizes dedicated telemetry modules.
        """
        if self._target_cache: return self._target_cache

        # [STRIKE]: Check Ephemeral Reality (Staging Area)
        if tx and hasattr(tx, 'write_dossier'):
            for logical_path, result in tx.write_dossier.items():
                # [ASCENSION 3]: Bicameral Priority: telemetry.py > main.py
                if logical_path.name in ("telemetry.py", "monitor.py", "observatory.py", "main.py", "app.py"):
                    staged_path = tx.get_staging_path(logical_path)
                    if staged_path.exists():
                        try:
                            content = staged_path.read_text(encoding='utf-8', errors='ignore')
                            if any(x in content for x in ("FastAPI(", "api_router", "TracerProvider")):
                                self._target_cache = (root / logical_path).resolve()
                                return self._target_cache
                        except Exception:
                            pass

        # [STRIKE]: Check Physical Iron (Disk)
        target = self.faculty.heuristics.find_best_match(
            root, ["TracerProvider(", "BatchSpanProcessor(", "FastAPIInstrumentor",
                   "init_sentry", "SQLAlchemyInstrumentor", "# @scaffold:telemetry_hub"], tx
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
        == THE Ω_FORGE_INJECTION: TOTALITY (V-Ω-VMAX-STEALTH-TRACE-SUTURE)             ==
        =================================================================================
        LIF: ∞^∞ | ROLE: KINETIC_OBSERVABILITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
        AUTH_CODE: Ω_PANOPTICON_FORGE_VMAX_STEALTH_SUTURE_2026_FINALIS
        """
        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', f"tr-panopticon-{uuid.uuid4().hex[:4].upper()}")

        # --- MOVEMENT I: DECONSTRUCTION ---
        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            raw_meta = parts[3] if len(parts) > 3 else ""
        except (IndexError, ValueError):
            return None

        # --- MOVEMENT II: GEOMETRIC TRIANGULATION ---
        tx = getattr(self.faculty, 'transaction', None)
        abs_target_file = self.find_target(root, tx)

        if not abs_target_file: return None

        # [ASCENSION 4]: ACHRONAL PATH TRIANGULATION
        abs_source = source_path.resolve()
        abs_target_dir = abs_target_file.parent.resolve()

        try:
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
                # [ASCENSION 13]: NAMESPACE COLLISION GUARD
                clean_p = re.sub(r'[^a-zA-Z0-9_]', '_', p)
                if clean_p: clean_parts.append(clean_p)

            module_dot_path = ".".join(clean_parts)

            # [ASCENSION 17]: APOPHATIC SELF-IMPORT WARD
            if module_dot_path == abs_target_file.stem or (module_dot_path == "" and leading_dots == "."):
                return None

            safe_stem = re.sub(r'[^a-zA-Z0-9_]', '_', source_path.stem)
            alias = f"{safe_stem}_{symbol_name}"
        except Exception:
            return None

        # --- MOVEMENT III: IDENTITY ADJUDICATION ---
        instance_name = "app"
        instance_match = re.search(
            r"^(?P<var>[a-zA-Z_]\w*)\s*(?::\s*[\w\.]+)?\s*=\s*(?:\w+\.)?(?:FastAPI|Flask|Litestar)\(",
            target_content, re.MULTILINE)
        if instance_match:
            instance_name = instance_match.group("var")

        # [ASCENSION 20]: DATABASE SENTINEL SUTURE
        db_engine_name = "engine"
        db_match = re.search(r"^(?P<var>[a-zA-Z_]\w*)\s*=\s*create_engine\(", target_content, re.MULTILINE)
        if db_match:
            db_engine_name = db_match.group("var")

        # --- MOVEMENT IV: PLAN MANIFESTATION ---

        # 1. THE IMPORT SUTURE
        import_stmt = f"from {leading_dots}{module_dot_path} import {symbol_name} as {alias}"

        # 2. IDEMPOTENCY CHECK
        if f" {alias}" in target_content or import_stmt in target_content:
            return None

        # =========================================================================
        # == MOVEMENT V: [ASCENSION 9] - LAMINAR SANCTUARY TRIAGE                ==
        # =========================================================================
        # [THE MASTER CURE]: Observability belongs to the Zenith (post_assignment)
        # to ensure the nervous system is awake before the first request arrives.

        anchor = instance_name
        sanctuary = "post_assignment"
        wire_stmt = ""

        # [ROLE A: THE BASTION (CENTRAL HUB)]
        if role_intent in ("observability-bastion", "trace-radiator", "sentry"):
            wire_stmt = f"{alias}({instance_name})"
            anchor = instance_name

        # [ROLE B: THE IRON EYE (DATABASE)]
        elif role_intent == "database-sentinel":
            # [ASCENSION 20]: Natively targets engine instrumentation
            wire_stmt = f"{alias}.instrument(engine={db_engine_name})"
            anchor = db_engine_name

        # [ROLE C: THE REDEMPTION GATE (EXCEPTIONS)]
        elif role_intent == "exception-alchemist":
            wire_stmt = f"{instance_name}.add_exception_handler(Exception, {alias})"
            anchor = instance_name

        # [ROLE D: THE TELEMETRY PROBE]
        elif role_intent == "telemetry-probe":
            wire_stmt = f"{alias}.ignite()"
            anchor = instance_name

        # [ROLE E: THE GENERIC SUTURE]
        elif role_intent == "suture":
            wire_stmt = f"{alias}()"
            anchor = instance_name

        if not wire_stmt:
            return None

        # --- MOVEMENT VI: METABOLIC FINALITY ---
        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        self.faculty.logger.success(
            f"   -> [Panopticon] Sensory Nerve Sutured: {role_intent} -> {abs_target_file.name} [{_duration_ms:.2f}ms]"
        )

        # [ASCENSION 24]: THE FINALITY VOW
        return InjectionPlan(
            target_file=abs_target_file,
            import_stmt=import_stmt,
            wiring_stmt=wire_stmt,
            anchor=anchor,
            strategy_name=self.name,
            metadata={"sanctuary": sanctuary, "trace_id": trace_id}
        )

    def _find_symbol_near_marker(self, content: str, marker_line: str) -> Optional[str]:
        """AST-Aware Sensory Symbol Divination."""
        try:
            tree = ast.parse(content)
            # 1. The Explicit Ward (__all__)
            for node in tree.body:
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == "__all__":
                            if isinstance(node.value, (ast.List, ast.Tuple)):
                                for elt in node.value.elts:
                                    val = getattr(elt, 'value', getattr(elt, 's', None))
                                    if val and isinstance(val, str): return val

            # 2. Semantic Analysis (Vibe check)
            public_symbols = []
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if not node.name.startswith('_'):
                        public_symbols.append(node.name)
                        if any(vibe in node.name.lower() for vibe in
                               ("telemetry", "tracer", "ignite", "instrument", "monitor", "observe", "sentry",
                                "logger")):
                            return node.name
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and not target.id.startswith('_'):
                            public_symbols.append(target.id)
                            if any(vibe in target.id.lower() for vibe in ("tracer", "provider", "meter", "logger")):
                                return target.id
            if public_symbols: return public_symbols[-1]
        except SyntaxError:
            pass

        # Fallback to Regex for malformed ASTs
        lines = content.splitlines()
        try:
            marker_index = -1
            if marker_line:
                for i, line in enumerate(lines):
                    if line.strip() == marker_line.strip():
                        marker_index = i
                        break
            start_scan = marker_index + 1 if marker_index != -1 else 0
            for i in range(start_scan, min(start_scan + 20, len(lines))):
                line = lines[i]
                match = re.search(r'^\s*(?:async\s+)?(?:def|class)\s+(?P<name>\w+)', line)
                if not match:
                    match = re.search(r'^\s*(?P<name>\w+)\s*=', line)
                if match:
                    return match.group('name')
        except Exception:
            pass
        return "Tracer"

    def _serialize_metadata(self, meta_str: str) -> str:
        if not meta_str: return ""
        return meta_str.replace(":", "%3A").replace(",", "%2C")

    def __repr__(self) -> str:
        return f"<Ω_PANOPTICON_STRATEGY status=RESONANT mode=OMNISCIENT_SIGHT version=3.5.2-Ω>"