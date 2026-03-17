# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/fastapi.py
# -----------------------------------------------------------------------------------------

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
from ..contracts import InjectionPlan, WiringStrategy
from .......utils import to_snake_case
from .......logger import Scribe

Logger = Scribe("FastAPISovereignConductor")


class FastAPIStrategy(WiringStrategy):
    """
    =================================================================================
    == THE FASTAPI SOVEREIGN CONDUCTOR: TOTALITY (V-Ω-LIFECYCLE-APOTHEOSIS-V99)    ==
    =================================================================================
    LIF: ∞^∞ | ROLE: AUTONOMIC_INTEGRATION_ENGINE_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_FASTAPI_VMAX_MATRYOSHKA_SINGULARITY_2026_FINALIS

    [THE MANIFESTO]
    The supreme definitive authority for FastAPI structural and metabolic resonance.
    This version righteously implements the **Matryoshka Lifespan Suture**,
    mathematically annihilating the "Empty Vigil" heresy. It dynamically wraps
    the `app.router.lifespan_context` at runtime, ensuring infinite composability.
    =================================================================================
    """

    name = "FastAPI"

    MARKER_REGEX: Final[re.Pattern] = re.compile(
        r'#\s*@scaffold:(?P<type>router|middleware|heart|dependency|lifespan_manager|lifecycle|exception_handler|static_mount)(?:\((?P<meta>.*)\))?'
    )

    def __init__(self, faculty):
        super().__init__(faculty)
        self._target_cache: Optional[Path] = None

    def detect(self, content: str) -> Optional[str]:
        """
        =============================================================================
        == THE GENOMIC DECODER (V-Ω-TOTALITY-VMAX-SIGHTED-RESONANCE)               ==
        =============================================================================
        LIF: 100,000x | ROLE: IDENTITY_RESONATOR
        """
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None

                # [THE MASTER CURE]: Detect the new Matryoshka Role
                if role in ("lifespan-manager", "lifecycle-context"):
                    symbol = self._find_symbol_near_marker(content, "") or "shard_lifespan"
                    return f"role:lifespan-manager:{symbol}:"

                if role in ("lifecycle-init", "db-initializer", "neural-warming", "metabolic-start"):
                    symbol = self._find_symbol_near_marker(content, "") or "ignite"
                    return f"role:lifecycle-init:{symbol}:"

                if role in ("lifecycle-exit", "db-shutdown", "metabolic-stop"):
                    symbol = self._find_symbol_near_marker(content, "") or "extinguish"
                    return f"role:lifecycle-exit:{symbol}:"

                if role in ("fastapi-router", "middleware-spine", "auth-gate", "exception-alchemist"):
                    symbol = self._find_symbol_near_marker(content, "") or "app"
                    return f"role:{role}:{symbol}:"

        for line in content.splitlines():
            match = self.MARKER_REGEX.search(line)
            if match:
                m_type = match.group('type')
                m_meta = match.group('meta') or ""
                symbol = self._find_symbol_near_marker(content, line)
                if symbol:
                    if m_type == "lifecycle" and "@asynccontextmanager" in content:
                        return f"legacy:lifespan-manager:{symbol}:{self._serialize_metadata(m_meta)}"
                    return f"legacy:{m_type}:{symbol}:{self._serialize_metadata(m_meta)}"

        # [ASCENSION 2]: Naked Shard Clairvoyance
        if "FastAPI(" in content:
            heart_match = re.search(r"^(?P<var>[a-zA-Z_]\w*)\s*=\s*FastAPI\(", content, re.MULTILINE)
            if heart_match: return f"role:fastapi-heart:{heart_match.group('var')}:"

        if "@asynccontextmanager" in content and "async def " in content and "(app" in content:
            symbol = self._find_symbol_near_marker(content, "@asynccontextmanager")
            if symbol: return f"role:lifespan-manager:{symbol}:"

        if "async def ignite(app" in content or "def ignite(app" in content:
            return "role:lifecycle-init:ignite:"
        if "async def extinguish(app" in content or "def extinguish(app" in content:
            return "role:lifecycle-exit:extinguish:"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        if self._target_cache: return self._target_cache

        if tx and hasattr(tx, 'write_dossier'):
            for logical_path, result in tx.write_dossier.items():
                if logical_path.name in ("main.py", "app.py", "api.py", "entry.py"):
                    staged_path = tx.get_staging_path(logical_path)
                    if staged_path.exists():
                        try:
                            content = staged_path.read_text(encoding='utf-8', errors='ignore')
                            if "FastAPI(" in content or "lifespan" in content:
                                self._target_cache = (root / logical_path).resolve()
                                return self._target_cache
                        except Exception:
                            pass

        target = self.faculty.heuristics.find_best_match(
            root, ["FastAPI(", "api_router = APIRouter", "async def lifespan", "include_router"], tx
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
        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', f"tr-fastapi-{uuid.uuid4().hex[:4].upper()}")

        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            raw_meta = parts[3] if len(parts) > 3 else ""
        except (IndexError, ValueError):
            return None

        tx = getattr(self.faculty, 'transaction', None)
        abs_target_file = self.find_target(root, tx)

        if not abs_target_file: return None

        abs_source = source_path.resolve()
        abs_target_dir = abs_target_file.parent.resolve()

        try:
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
                clean_p = re.sub(r'[^a-zA-Z0-9_]', '_', p)
                if clean_p: clean_parts.append(clean_p)

            module_dot_path = ".".join(clean_parts)
            target_stem = abs_target_file.stem
            if module_dot_path == target_stem or (module_dot_path == "" and leading_dots == "."):
                return None

            safe_stem = re.sub(r'[^a-zA-Z0-9_]', '_', source_path.stem)
            alias = f"{safe_stem}_{symbol_name}"
        except Exception:
            return None

        instance_name = "app"
        instance_match = re.search(r"^(?P<var>[a-zA-Z_]\w*)\s*(?::\s*[\w\.]+)?\s*=\s*(?:\w+\.)?FastAPI\(",
                                   target_content, re.MULTILINE)
        if instance_match:
            instance_name = instance_match.group("var")

        import_stmt = f"from {leading_dots}{module_dot_path} import {symbol_name} as {alias}"

        if f" {alias}" in target_content or import_stmt in target_content:
            return None

        anchor = instance_name
        sanctuary = "post_assignment"
        wire_stmt = ""

        # =========================================================================
        # == [ASCENSION 1]: THE MATRYOSHKA LIFESPAN SUTURE (THE OMEGA CURE)      ==
        # =========================================================================
        if role_intent in ("lifespan-manager", "lifecycle-context"):
            # We import asynccontextmanager cleanly with an alias to prevent namespace collision
            import_stmt += "\nfrom contextlib import asynccontextmanager as _suture_asynccontextmanager"

            wire_stmt = (
                f"_base_lifespan_{alias} = {instance_name}.router.lifespan_context\n"
                f"@_suture_asynccontextmanager\n"
                f"async def _compound_lifespan_{alias}(app):\n"
                f"    async with {alias}(app):\n"
                f"        async with _base_lifespan_{alias}(app) as state:\n"
                f"            yield state\n"
                f"{instance_name}.router.lifespan_context = _compound_lifespan_{alias}"
            )
            anchor = instance_name
            sanctuary = "post_assignment"

        elif role_intent == "lifecycle-init":
            wire_stmt = f"await {alias}({instance_name})"
            anchor = "Initialize DB Pools"
            sanctuary = "lifespan_setup"

        elif role_intent == "lifecycle-exit":
            wire_stmt = f"await {alias}({instance_name})"
            anchor = "Graceful shutdown"
            sanctuary = "lifespan_teardown"

        elif role_intent in ("fastapi-router", "router"):
            prefix = f"/{source_path.stem.replace('_', '-')}"
            wire_stmt = f"{instance_name}.include_router({alias}, prefix='{prefix}')"
            sanctuary = "post_assignment"

        elif role_intent in ("middleware-spine", "middleware", "auth-gate"):
            wire_stmt = f"{instance_name}.add_middleware({alias})"
            sanctuary = "post_assignment"

        elif role_intent == "exception-handler":
            wire_stmt = f"{instance_name}.add_exception_handler(Exception, {alias})"
            sanctuary = "post_assignment"

        if not wire_stmt:
            return None

        _duration_ms = (time.perf_counter_ns() - _start_ns) / 1_000_000
        self.faculty.logger.success(
            f"   -> [FastAPI] Vitality Sutured: {role_intent} -> {abs_target_file.name} [{_duration_ms:.2f}ms]"
        )

        return InjectionPlan(
            target_file=abs_target_file,
            import_stmt=import_stmt,
            wiring_stmt=wire_stmt,
            anchor=anchor,
            strategy_name=self.name,
            metadata={"sanctuary": sanctuary, "trace_id": trace_id}
        )

    def _find_symbol_near_marker(self, content: str, marker_line: str) -> Optional[str]:
        try:
            tree = ast.parse(content)
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if not node.name.startswith('_'):
                        if any(vibe in node.name.lower() for vibe in
                               ("router", "ignite", "extinguish", "lifespan", "app", "handler", "database")):
                            return node.name
        except:
            pass
        return "app"

    def _serialize_metadata(self, meta_str: str) -> str:
        if not meta_str: return ""
        return meta_str.replace(":", "%3A").replace(",", "%2C")

    def __repr__(self) -> str:
        return f"<Ω_FASTAPI_STRATEGY status=RESONANT mode=MATRYOSHKA_SUTURE version=3.6.0-Ω>"