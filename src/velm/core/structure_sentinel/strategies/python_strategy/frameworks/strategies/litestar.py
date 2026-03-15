# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/litestar.py
# ------------------------------------------------------------------------------------------

import re
import time
import os
import ast
import json
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union, Final

# --- THE DIVINE UPLINKS ---
from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case
from .......logger import Scribe

Logger = Scribe("LitestarSovereignStrategy")


class LitestarStrategy(WiringStrategy):
    """
    =================================================================================
    == THE LITESTAR SOVEREIGN STRATEGY: OMEGA (V-Ω-TOTALITY-VMAX-ASYNC-CORE)       ==
    =================================================================================
    LIF: ∞^∞ | ROLE: ASYNC_REALITY_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_LITESTAR_VMAX_SUTURE_RECONSTRUCTED_2026_FINALIS

    The supreme guardian of the Litestar substrate. It manages the causal
    links between Controllers, Dependencies, Middleware, and the Application Heart.
    =================================================================================
    """
    name = "Litestar"

    # [ASCENSION 20]: THE PHANTOM MARKER EXORCIST
    MARKER_REGEX: Final[re.Pattern] = re.compile(
        r'#\s*@scaffold:(?P<type>controller|router|middleware|plugin|dependency|lifecycle)(?:\((?P<meta>.*)\))?'
    )

    def __init__(self, faculty):
        """[THE RITE OF INCEPTION]"""
        super().__init__(faculty)
        self._target_cache: Optional[Path] = None

    def detect(self, content: str) -> Optional[str]:
        """
        =================================================================================
        == THE GENOMIC DECODER (V-Ω-VMAX-SIGHTED-RESONANCE)                            ==
        =================================================================================
        [THE MASTER CURE]: Identifies the Shard's Async Role from the Dossier autonomicly.
        """
        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY) ---
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            # Find the manifest associated with this physical locus
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None

                if role in ("litestar-controller", "litestar-router", "litestar-middleware", "litestar-plugin"):
                    # Achieved Genomic Resonance
                    # 1. Divine the primary variable symbol (e.g. controller or router)
                    symbol = self._find_symbol_near_marker(content, "") or "Handler"
                    self.faculty.logger.info(
                        f"🧬 Genomic Litestar Resonance: Shard '{shard_id}' identifies as '{role}'.")
                    return f"role:{role}:{symbol}:"

        # --- MOVEMENT II: THE GNOSTIC GAZE (v2.0 AMNESTY) ---
        for line in content.splitlines():
            match = self.MARKER_REGEX.search(line)
            if match:
                m_type = match.group('type')
                m_meta = match.group('meta') or ""
                symbol = self._find_symbol_near_marker(content, line)
                if symbol:
                    return f"legacy:{m_type}:{symbol}:{m_meta}"

        # --- MOVEMENT III: THE STRUCTURAL GAZE (HEURISTIC) ---
        # 1. Controller Detection
        if "class " in content and "Controller" in content:
            match = re.search(r"class\s+(?P<cls>\w+)", content)
            if match: return f"role:litestar-controller:{match.group('cls')}:"

        # 2. Router Detection
        if "Router(" in content:
            match = re.search(r"^(?P<var>\w+)\s*=\s*(?:\w+\.)?Router\(", content, re.MULTILINE)
            if match: return f"role:litestar-router:{match.group('var')}:"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE CAUSAL INQUEST (V-Ω-STAGING-AWARE)                                  ==
        =============================================================================
        Locates the 'Heart' (Litestar App Instance) of the project.
        """
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
                        if "Litestar(" in content:
                            abs_path = (root / logical_path).resolve()
                            self._target_cache = abs_path
                            return abs_path
                    except Exception:
                        pass

        # --- MOVEMENT II: THE PHYSICAL GAZE (DISK) ---
        target = self.faculty.heuristics.find_best_match(
            root,
            ["Litestar(", "route_handlers=[", "on_startup=[", "plugins=["],
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
        == THE OMEGA FORGE INJECTION: TOTALITY (V-Ω-VMAX-ASYNC-SUTURE)                 ==
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', 'tr-litestar-void')

        # --- MOVEMENT I: DECONSTRUCTION ---
        # URN: {origin}:{role}:{symbol}:{meta}
        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            raw_meta = parts[3] if len(parts) > 3 else ""
        except (IndexError, ValueError):
            return None

        if role_intent == "litestar-heart": return None

        # --- MOVEMENT II: GEOMETRIC TRIANGULATION ---
        try:
            tx = getattr(self.faculty, 'transaction', None)
            abs_target_file = self.find_target(root, tx)

            if not abs_target_file:
                self.faculty.logger.warn(f"   [Litestar] Triangulation Void: App Heart unmanifest.")
                return None

            # [ASCENSION 2]: RELATIONAL TRIANGULATION (THE CURE)
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
                # [ASCENSION 3]: Identity Suture
                clean_p = re.sub(r'[^a-zA-Z0-9_]', '_', p)
                if clean_p: clean_parts.append(clean_p)

            module_dot_path = ".".join(clean_parts)

            # [ASCENSION 16]: IDENTITY ALIASING
            safe_stem = re.sub(r'[^a-zA-Z0-9_]', '_', source_path.stem)
            alias = f"{safe_stem}_{symbol_name}"

        except Exception as e:
            self.faculty.logger.error(f"   [Litestar] Triangulation Paradox: {e}")
            return None

        # --- MOVEMENT III: IDENTITY ADJUDICATION ---
        # Find the variable holding the Litestar instance (app, server, etc.)
        instance_name = "app"
        instance_match = re.search(r"^(?P<var>[a-zA-Z_]\w*)\s*(?::\s*[\w\.]+)?\s*=\s*(?:\w+\.)?Litestar\(",
                                   target_content, re.MULTILINE)
        if instance_match:
            instance_name = instance_match.group("var")

        # --- MOVEMENT IV: PLAN MANIFESTATION (THE STRIKE) ---

        # 1. FORGE THE IMPORT
        import_stmt = f"from {leading_dots}{module_dot_path} import {symbol_name} as {alias}"

        # 2. IDEMPOTENCY CHECK
        if f" {alias}" in target_content or import_stmt in target_content:
            return None

        # 3. SURGICAL BRANCHING (ROLE-BASED)
        wire_stmt = ""
        anchor = instance_name

        # [ROLE A: CONTROLLER / HANDLER]
        if role_intent in ("litestar-controller", "litestar-router", "controller", "router"):
            wire_stmt = alias
            anchor = "route_handlers"

        # [ROLE B: MIDDLEWARE]
        elif role_intent in ("litestar-middleware", "middleware"):
            # [ASCENSION 6]: DefineMiddleware Suture
            wire_stmt = f"DefineMiddleware({alias})"
            anchor = "middleware"

        # [ROLE C: PLUGIN]
        elif role_intent in ("litestar-plugin", "plugin"):
            # [ASCENSION 7]: Plugin Inception
            wire_stmt = f"{alias}()"
            anchor = "plugins"

        # [ROLE D: LIFECYCLE]
        elif role_intent in ("lifecycle", "lifecycle-hook"):
            # [ASCENSION 8]: Lifecycle Suture
            wire_stmt = alias
            anchor = "on_startup" if "startup" in symbol_name.lower() else "on_shutdown"

        # [ROLE E: DEPENDENCY]
        elif role_intent == "dependency":
            # [ASCENSION 5]: Provide Suture
            key = symbol_name.lower().replace("provide_", "")
            wire_stmt = f"'{key}': Provide({alias})"
            anchor = "dependencies"

        # [ROLE F: GENERIC SUTURE]
        elif role_intent == "suture":
            wire_stmt = f"# [Autonomic Suture]\n{alias}({instance_name})"
            anchor = instance_name

        # --- MOVEMENT V: FINAL CHRONICLING ---
        if not wire_stmt: return None

        # [ASCENSION 22]: Trace ID Silver-Cord Suture
        wire_stmt = f"# [Trace: {trace_id}]\n{wire_stmt}"

        self.faculty.logger.success(
            f"   [Litestar] [bold cyan]Suture Resonant:[/] Grafted Role '[yellow]{role_intent}[/]' "
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

    def _find_symbol_near_marker(self, content: str, marker_line: str) -> Optional[str]:
        """Finds the class or function definition associated with the Litestar intent."""
        lines = content.splitlines()
        try:
            marker_index = -1
            if marker_line:
                for i, line in enumerate(lines):
                    if line.strip() == marker_line.strip():
                        marker_index = i
                        break

            start_scan = marker_index + 1 if marker_index != -1 else 0

            for i in range(start_scan, min(start_scan + 15, len(lines))):
                line = lines[i]
                # Match class Name, async def name, or var =
                match = re.search(r'^\s*(?:async\s+)?(?:def|class)\s+(?P<name>\w+)', line)
                if not match:
                    match = re.search(r'^\s*(?P<name>\w+)\s*=', line)

                if match:
                    return match.group('name')
        except Exception:
            pass
        return None

    def __repr__(self) -> str:
        return f"<Ω_LITESTAR_STRATEGY status=RESONANT mode=ASYNC_WIRING version=3.0.0>"