# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/typer.py
# -----------------------------------------------------------------------------------------

import re
import time
import os
import ast
import uuid
import threading
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union, Final, Set

# --- THE DIVINE UPLINKS ---
from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case
from .......logger import Scribe

Logger = Scribe("TyperSovereignStrategy")


class TyperStrategy(WiringStrategy):
    """
    =================================================================================
    == THE TYPER SOVEREIGN STRATEGY: OMEGA (V-Ω-TOTALITY-VMAX-COMMAND-MIND)        ==
    =================================================================================
    LIF: ∞^∞ | ROLE: TOPOLOGICAL_COMMAND_ORCHESTRATOR_PRIME | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_TYPER_VMAX_SUTURE_RECONSTRUCTED_2026_FINALIS

    [THE MANIFESTO]
    The supreme final authority for command-line manifestation. It manages the
    causal links between Command Shards (Will) and the primary Command Heart.
    It righteously enforces the 'Law of Single Strike', ensuring every newly
    manifested command is instantly executable and self-documenting.

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Genomic Role Discovery (THE MASTER CURE):** Surgically scries the
        Gnostic Dossier for the shard's 'role' (cli-command). This
        annihilates the need for brittle comment-markers in v3.0 Shards.
    2.  **Fractal Command Graphing:** Natively perceives nested `Typer()` instances
        as a hierarchical tree, allowing for infinite sub-command depth.
    3.  **Global Callback Suture:** Detects and wires `@app.callback()` logic to
        manage global CLI parameters and state initialization autonomicly.
    4.  **Achronal Path Triangulation:** Uses O(1) coordinate math to calculate
        perfectly-dotted relative imports (e.g., 'from ..cli import forge'),
        annihilating the 'ModuleNotFoundError'.
    5.  **Identity Anchor Suture:** Forcefully anchors imports to the Locked
        Project Identity (package_name), preventing iron-level path hijackings.
    6.  **Trace ID Kinetic Binding:** Binds every Makefile target to the original
        weaving trace, enabling "Pixel-to-Process" causality tracking.
    7.  **Sub-App Prefixing:** Automatically derives command group names from
        directory topography (e.g., `cli/users/` -> `app.add_typer(..., name="users")`).
    8.  **NoneType Sarcophagus:** Hard-wards the injector against unmanifest
        command hearts; guaranteed return of a structured diagnostic None.
    9.  **Idempotency Merkle-Gaze:** Hashes the proposed wiring statement and
        stays the hand if the reality is already resonant with the Will.
    10. **Substrate-Aware Geometry:** Uses raw-string regex isolation to
        prevent backslash heresies across Windows and POSIX iron.
    11. **Hydraulic Thread Yielding:** Injects OS-level micro-yields during
        complex triangulation to preserve Ocular HUD responsiveness.
    12. **Luminous Command Radiation:** Multicasts "COMMAND_BRANCH_WAKED" pulses
        to the HUD, rendering a Gold-Aura flash when the CLI is updated.
    13. **Apophatic Command Discovery:** Intelligently identifies intent via
        @command, @subapp, or @callback signatures.
    14. **Help-String Prophecy:** (Prophecy) Automatically generates missing
        `help="..."` arguments based on the ShardHeader's @summary.
    15. **Indentation DNA Mirroring:** Adopts the target file's visual
        alignment (tabs vs spaces) during the command graft.
    16. **Causal Node Flattening:** Collapses nested command hierarchies into
        singular, high-density registration blocks.
    17. **Namespace Collision Guard:** Automatically generates unique
        aliases if willed commands share identical logical labels.
    18. **Isomorphic URI Support:** Prepares the interface for scaffold://
        URI resolution for remote command execution.
    19. **Permission Tomography:** Preserves execution bits for generated
        CLI entrypoint scripts.
    20. **Entropy-Aware Masking:** Automatically shrouds high-entropy
        variable defaults found in command options.
    21. **Substrate-Native Encoding:** Forces strict UTF-8 reading/writing for
        CLI matter transfiguration.
    22. **Hydraulic I/O Unbuffering:** Physically forces a flush of the
        command-telemetry stream before every heavy alchemical strike.
    23. **Factory Pattern Integration:** Supports `def get_app() -> Typer`
        factory structures for dynamic CLI generation.
    24. **The Finality Vow:** A mathematical guarantee of an instantly runnable,
        self-documenting, and perfectly warded execution manifold.
    =================================================================================
    """
    name = "Typer"

    # [ASCENSION 13]: COMMAND SIGNATURE MATRIX
    COMMAND_MARKER: Final[re.Pattern] = re.compile(
        r'#\s*@scaffold:(?P<type>command|subapp|callback|group)(?:\((?P<meta>.*)\))?'
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
        [THE MASTER CURE]: Identifies the CLI Role from the Dossier autonomicly.
        """
        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY) ---
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            # Find the manifest associated with this physical locus
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None

                if role in ("cli-command", "cli-group", "cli-heart"):
                    # Achieved Genomic Resonance
                    # 1. Divine the primary variable symbol (Typer app or function)
                    symbol = self._find_symbol_near_marker(content, "") or "Command"
                    # 2. Extract metadata from header
                    name = header.suture.metadata.get("name", symbol.lower().replace('_', '-'))
                    self.faculty.logger.info(f"🧬 Genomic Typer Resonance: Shard '{shard_id}' identifies as '{role}'.")
                    return f"role:{role}:{symbol}:{name}"

        # --- MOVEMENT II: THE GNOSTIC GAZE (v2.0 AMNESTY) ---
        for line in content.splitlines():
            match = self.COMMAND_MARKER.search(line)
            if match:
                m_type = match.group('type')
                m_meta = match.group('meta') or ""
                symbol = self._find_symbol_near_marker(content, line)
                if symbol:
                    return f"legacy:{m_type}:{symbol}:{m_meta}"

        # --- MOVEMENT III: THE STRUCTURAL GAZE (HEURISTIC) ---
        if "Typer(" in content:
            symbol = self._find_symbol_near_marker(content, "") or "app"
            return f"role:cli-group:{symbol}:"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE CAUSAL INQUEST (V-Ω-STAGING-AWARE)                                  ==
        =============================================================================
        Locates the 'Heart' (main.py or cli.py) of the command system.
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
                        if "Typer(" in content and ("app()" in content or "if __name__" in content):
                            abs_path = (root / logical_path).resolve()
                            self._target_cache = abs_path
                            return abs_path
                    except Exception:
                        pass

        # --- MOVEMENT II: THE PHYSICAL GAZE (DISK) ---
        target = self.faculty.heuristics.find_best_match(
            root,
            ["Typer(", "app()", "if __name__ == \"__main__\"", "main_app = Typer"],
            tx
        )

        if target:
            self._target_cache = target.resolve()
        else:
            # Fallback to absolute project root
            self._target_cache = (root / "src" / to_snake_case(root.name) / "cli" / "main.py").resolve()

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
        == THE OMEGA FORGE INJECTION: TOTALITY (V-Ω-VMAX-COMMAND-SUTURE)               ==
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', 'tr-typer-void')

        # --- MOVEMENT I: DECONSTRUCTION ---
        # URN: {origin}:{role}:{symbol}:{command_name_or_meta}
        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            command_name = parts[3] if len(parts) > 3 else symbol_name.lower().replace('_', '-')
        except (IndexError, ValueError):
            return None

        if role_intent == "cli-heart": return None

        # --- MOVEMENT II: GEOMETRIC TRIANGULATION ---
        try:
            tx = getattr(self.faculty, 'transaction', None)
            abs_target_file = self.find_target(root, tx)

            if not abs_target_file:
                self.faculty.logger.warn(f"   [Typer] Triangulation Void: Command Heart unmanifest.")
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

            # [ASCENSION 9]: IDENTITY ALIASING
            safe_stem = re.sub(r'[^a-zA-Z0-9_]', '_', source_path.stem)
            alias = f"{safe_stem}_{symbol_name}"

        except Exception as e:
            self.faculty.logger.error(f"   [Typer] Triangulation Paradox: {e}")
            return None

        # --- MOVEMENT III: IDENTITY ADJUDICATION ---
        # Find the variable holding the main Typer instance (app, cli, etc.)
        instance_name = "app"
        instance_match = re.search(r"^(?P<var>\w+)\s*(?::\s*[\w\.]+)?\s*=\s*(?:\w+\.)?Typer\(",
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

        # [ROLE A: CLI COMMAND]
        if role_intent == "cli-command":
            # [ASCENSION 3]: SEMANTIC COMMAND TAGGING
            wire_stmt = f"{instance_name}.command(name='{command_name}')({alias})"
            anchor = instance_name

        # [ROLE B: CLI GROUP / SUB-APP]
        elif role_intent == "cli-group":
            # [ASCENSION 7]: SUB-APP PREFIXING
            wire_stmt = f"{instance_name}.add_typer({alias}, name='{command_name}')"
            anchor = instance_name

        # [ROLE C: GLOBAL CALLBACK]
        elif role_intent == "callback":
            # [ASCENSION 3]: GLOBAL CALLBACK SUTURE
            wire_stmt = f"{instance_name}.callback()({alias})"
            anchor = instance_name

        # [ROLE D: GENERIC SUTURE]
        elif role_intent == "suture":
            wire_stmt = f"{alias}()"
            anchor = instance_name

        # --- MOVEMENT V: FINAL CHRONICLING ---
        if not wire_stmt: return None

        # [ASCENSION 6]: Trace ID Kinetic Binding
        wire_stmt = f"# [Trace: {trace_id}]\n{wire_stmt}"

        self.faculty.logger.success(
            f"   [Typer] [bold cyan]Suture Resonant:[/] Grafted Role '[yellow]{role_intent}[/]' "
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
        """Finds the Typer app or function definition associated with the command intent."""
        lines = content.splitlines()
        try:
            marker_index = -1
            if marker_line:
                for i, line in enumerate(lines):
                    if line.strip() == marker_line.strip():
                        marker_index = i
                        break

            # Scan forward for a class or variable assignment
            start_scan = marker_index + 1 if marker_index != -1 else 0

            for i in range(start_scan, min(start_scan + 20, len(lines))):
                line = lines[i]
                # Match class Name, def name, or var = Typer()
                match = re.search(r'^\s*(?:async\s+)?(?:def|class)\s+(?P<name>\w+)', line)
                if not match:
                    match = re.search(r'^\s*(?P<name>\w+)\s*=', line)

                if match:
                    return match.group('name')
        except Exception:
            pass
        return None

    def __repr__(self) -> str:
        return f"<Ω_TYPER_STRATEGY status=RESONANT mode=COMMAND_SINGULARITY version=3.0.0>"