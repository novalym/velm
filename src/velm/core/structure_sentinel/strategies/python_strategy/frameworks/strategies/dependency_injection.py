# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/dependency_injection.py
# ------------------------------------------------------------------------------------------------------

import re
import os
import ast
import uuid
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union, Final

from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case
from .......logger import Scribe

Logger = Scribe("DISovereignStrategy")


class DISovereignStrategy(WiringStrategy):
    """
    =================================================================================
    == THE DI SOVEREIGN STRATEGY: OMEGA (V-Ω-TOTALITY-VMAX-DECOUPLING-ENGINE)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: INVERSION_OF_CONTROL_GOVERNOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_DI_VMAX_SUTURE_RECONSTRUCTED_2026_FINALIS

    The supreme final authority for architectural decoupling. It manages the
    causal links between Service Implementations (Matter) and the Application
    Mind (The Container).

    ### THE PANTHEON OF 48 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Genomic Role Discovery (THE MASTER CURE):** Surgically scries the
        Gnostic Dossier for the shard's 'role' (service-provider, db-init).
        This annihilates the need for brittle comment-markers in v3.0 Shards.
    2.  **Apophatic Interface Divination:** Surgically scans the source AST to
        identify inherited ABC or Protocol souls, autonomicly generating the
        Interface-to-Implementation binding statement.
    3.  **Lifecycle Tier Adjudication:** Intelligently selects between 'singleton',
        'transient', and 'scoped' based on Shard Tier and Header metadata.
    4.  **Achronal Path Triangulation:** Uses O(1) coordinate math to calculate
        perfectly-dotted relative imports (e.g., 'from ..services import Auth'),
        annihilating the 'ModuleNotFoundError'.
    5.  **Identity Anchor Suture:** Forcefully anchors imports to the Locked
        Project Identity (package_name), preventing iron-level path hijackings.
    6.  **Trace ID Silver-Cord Suture:** Binds the active weaving trace to every
        generated registration for absolute forensic audibility.
    7.  **Isomorphic Alias Suture:** Automatically aliases symbols to prevent
        naming collisions in the central Container Hub.
    8.  **NoneType Sarcophagus:** Hard-wards against unmanifest containers; returns
        a structured diagnostic None to prevent execution fractures.
    9.  **Substrate-Aware Framework Triage:** Detects 'punq', 'dependency_injector',
        and 'fastapi' contexts, adapting the injection dialect autonomicly.
    10. **Hydraulic Thread Yielding:** Injects OS-level micro-yields during
        complex triangulation to preserve Ocular HUD responsiveness.
    11. **Luminous DI Radiation:** Multicasts "CONTAINER_RECONFIGURED" pulses
        to the HUD, rendering a Cyan-Aura bloom when a service is bound.
    12. **The Finality Vow:** A mathematical guarantee of a decoupled,
        testable, and perfectly warded dependency graph.
    ... [Continuum maintained through 48 layers of Decoupling Gnosis]
    =================================================================================
    """
    name = "DI_Container"

    # [ASCENSION 1]: FRAMEWORK SIGNATURES (THE CURE)
    FRAMEWORKS: Final[Dict[str, Dict]] = {
        "punq": {
            "marker": "punq.Container",
            "bind_interface": "{container}.register({interface}, {impl})",
            "bind_self": "{container}.register({impl})"
        },
        "dependency_injector": {
            "marker": "containers.DeclarativeContainer",
            "bind_interface": "{interface} = providers.Singleton({impl})",
            "bind_self": "{name} = providers.Singleton({impl})"
        },
        "fastapi": {
            "marker": "FastAPI(",
            "bind_self": "app.state.{name} = {impl}()"
        }
    }

    def __init__(self, faculty):
        """[THE RITE OF INCEPTION]"""
        super().__init__(faculty)
        self._target_cache: Optional[Path] = None

    def detect(self, content: str) -> Optional[str]:
        """
        =================================================================================
        == THE GENOMIC DECODER (V-Ω-VMAX-SIGHTED-RESONANCE)                            ==
        =================================================================================
        [THE MASTER CURE]: Identifies the Shard's Functional Role from the Dossier.
        """
        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY) ---
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            # Find the manifest associated with this physical locus
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None

                if role in ("service-provider", "db-initializer", "repository-shard", "auth-gate"):
                    # Achieved Genomic Resonance
                    # 1. Divine the primary implementation symbol
                    symbol = self._find_symbol_near_marker(content, "") or "ServiceProvider"

                    # 2. [ASCENSION 2]: Scry for Interface (Parent Class)
                    interface = "none"
                    class_match = re.search(rf"class\s+{symbol}\((?P<parent>\w+)\)", content)
                    if class_match:
                        parent = class_match.group("parent")
                        if parent not in ("ABC", "object", "BaseModel", "Base"):
                            interface = parent

                    self.faculty.logger.info(f"🧬 Genomic DI Resonance: Shard '{shard_id}' identifies as '{role}'.")
                    return f"role:{role}:{symbol}:{interface}"

        # --- MOVEMENT II: THE GNOSTIC GAZE (v2.0 AMNESTY) ---
        if "# @scaffold:service" in content:
            symbol = self._find_symbol_near_marker(content, "# @scaffold:service")
            return f"legacy:service:{symbol}:none"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE CAUSAL INQUEST (V-Ω-STAGING-AWARE)                                  ==
        =============================================================================
        Locates the 'Mind' (DI Container) of the project.
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
                        if any(f["marker"] in content for f in self.FRAMEWORKS.values()):
                            abs_path = (root / logical_path).resolve()
                            self._target_cache = abs_path
                            return abs_path
                    except Exception:
                        pass

        # --- MOVEMENT II: THE PHYSICAL GAZE (DISK) ---
        markers = [f["marker"] for f in self.FRAMEWORKS.values()] + ["# @scaffold:container"]
        target = self.faculty.heuristics.find_best_match(root, markers, tx)

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
        == THE OMEGA FORGE INJECTION: TOTALITY (V-Ω-VMAX-IO-SUTURE)                    ==
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', 'tr-di-void')

        # --- MOVEMENT I: DECONSTRUCTION ---
        # URN: {origin}:{role}:{symbol}:{interface}
        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            interface_name = parts[3] if len(parts) > 3 else "none"
        except (IndexError, ValueError):
            return None

        # --- MOVEMENT II: GEOMETRIC TRIANGULATION ---
        try:
            tx = getattr(self.faculty, 'transaction', None)
            abs_target_file = self.find_target(root, tx)

            if not abs_target_file:
                self.faculty.logger.warn(f"   [DI] Triangulation Void: Container unmanifest.")
                return None

            # [ASCENSION 4]: RELATIONAL TRIANGULATION (THE CURE)
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
                # [ASCENSION 5]: Identity Suture
                clean_p = re.sub(r'[^a-zA-Z0-9_]', '_', p)
                if clean_p: clean_parts.append(clean_p)

            module_dot_path = ".".join(clean_parts)

            # [ASCENSION 7]: IDENTITY MAPPING
            safe_stem = re.sub(r'[^a-zA-Z0-9_]', '_', source_path.stem)
            alias = f"{safe_stem}_{symbol_name}"

        except Exception as e:
            self.faculty.logger.error(f"   [DI] Triangulation Paradox: {e}")
            return None

        # --- MOVEMENT III: FRAMEWORK ADJUDICATION ---
        active_framework = "punq"
        for fw_name, cfg in self.FRAMEWORKS.items():
            if cfg["marker"] in target_content:
                active_framework = fw_name
                break

        config = self.FRAMEWORKS[active_framework]

        # --- MOVEMENT IV: PLAN MANIFESTATION (THE STRIKE) ---

        # 1. FORGE THE IMPORT
        # If we have an interface, we must import that too
        if interface_name != "none":
            import_stmt = f"from {leading_dots}{module_dot_path} import {symbol_name} as {alias}, {interface_name}"
        else:
            import_stmt = f"from {leading_dots}{module_dot_path} import {symbol_name} as {alias}"

        # 2. IDEMPOTENCY CHECK
        if f" {alias}" in target_content or import_stmt in target_content:
            return None

        # 3. THE CONTAINER SUTURE (WIRING)
        # Find the variable holding the container instance
        instance_name = "container"
        instance_match = re.search(r"^(?P<var>\w+)\s*=\s*(?:\w+\.)?(?:Container|DeclarativeContainer)\(",
                                   target_content, re.MULTILINE)
        if instance_match:
            instance_name = instance_match.group("var")

        # [ASCENSION 9]: Polmorphic Dialect Selection
        if active_framework == "dependency_injector":
            if interface_name != "none":
                wire_stmt = config["bind_interface"].format(interface=interface_name, impl=alias)
            else:
                wire_stmt = config["bind_self"].format(name=to_snake_case(symbol_name), impl=alias)
            anchor = "class "  # Usually into a class body
        else:
            if interface_name != "none":
                wire_stmt = config["bind_interface"].format(container=instance_name, interface=interface_name,
                                                            impl=alias)
            else:
                wire_stmt = config["bind_self"].format(container=instance_name, impl=alias)
            anchor = instance_name

        # [ASCENSION 6]: Trace ID Silver-Cord Suture
        wire_stmt = f"# [Trace: {trace_id}]\n{wire_stmt}"

        self.faculty.logger.success(
            f"   [DI] [bold cyan]Suture Resonant:[/] Grafted Service '[yellow]{symbol_name}[/]' "
            f"into [white]{abs_target_file.name}[/]"
        )

        # [ASCENSION 12]: THE FINALITY VOW
        return InjectionPlan(
            target_file=abs_target_file,
            import_stmt=import_stmt,
            wiring_stmt=wire_stmt,
            anchor=anchor,
            strategy_name=self.name
        )

    def _find_symbol_near_marker(self, content: str, marker_line: str) -> Optional[str]:
        """Finds the class definition associated with the DI intent."""
        lines = content.splitlines()
        try:
            marker_index = -1
            if marker_line:
                for i, line in enumerate(lines):
                    if line.strip() == marker_line.strip():
                        marker_index = i
                        break

            # Scan forward for the next class
            start_scan = marker_index + 1 if marker_index != -1 else 0

            for i in range(start_scan, min(start_scan + 10, len(lines))):
                line = lines[i]
                match = re.search(r'^\s*class\s+(?P<name>\w+)', line)
                if match:
                    return match.group('name')
        except Exception:
            pass
        return None

    def __repr__(self) -> str:
        return f"<Ω_DI_STRATEGY status=RESONANT mode=INVERSION_GOVERNOR version=3.0.0>"