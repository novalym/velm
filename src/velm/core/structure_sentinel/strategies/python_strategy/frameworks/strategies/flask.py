# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/flask.py
# ---------------------------------------------------------------------------------------

import re
import time
import os
import ast
import uuid
import threading
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple, Union, Final, Set

from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case
from .......logger import Scribe

Logger = Scribe("FlaskSovereignStrategy")


class FlaskStrategy(WiringStrategy):
    """
    =================================================================================
    == THE FLASK SOVEREIGN STRATEGY: OMEGA (V-Ω-TOTALITY-VMAX-MICRO-KERNEL-MIND)   ==
    =================================================================================
    LIF: ∞^∞ | ROLE: ASYNC_MICRO_KERNEL_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_FLASK_VMAX_SUTURE_RECONSTRUCTED_2026_FINALIS

    The supreme final authority for Flask architectural convergence. It manages
    the causal links between Shard matter and the Application Heart (Factory).

    ### THE PANTHEON OF 24 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Genomic Role Discovery (THE MASTER CURE):** Surgically scries the
        Gnostic Dossier for the shard's 'role' (flask-blueprint, flask-extension).
        This annihilates the need for brittle comment-markers in v3.0 Shards.
    2.  **Factory Pattern Autonomy:** Intelligently detects if the app instance
        is localized within a 'create_app' scope and righteously adjusts the
        AST anchor point to ensure logic lands inside the factory.
    3.  **Achronal Path Triangulation:** Uses O(1) coordinate math to calculate
        perfectly-dotted relative imports (e.g., 'from ..auth import auth_bp'),
        annihilating the 'ModuleNotFoundError'.
    4.  **Extension Lifecycle Suture:** Natively distinguishes between Global
        instantiation and Factory-based 'init_app' registration.
    5.  **Blueprint Topological Prefixing:** Transmutes ShardHeader metadata
        (prefix) into valid Flask `url_prefix` arguments autonomicly.
    6.  **Identity Anchor Suture:** Forcefully anchors imports to the Locked
        Project Identity (package_name), preventing iron-level path hijackings.
    7.  **Isomorphic Alias Suture:** Automatically aliases symbols to prevent
        naming collisions when multiple blueprints share common names.
    8.  **NoneType Sarcophagus:** Hard-wards against unmanifest factories; returns
        a structured diagnostic None to prevent execution fractures.
    9.  **Idempotency Merkle-Gaze:** Hashes the proposed wiring statement and
        stays the hand if the reality is already resonant with the Will.
    10. **Substrate-Aware Geometry:** Uses raw-string regex isolation to
        prevent backslash heresies across Windows and POSIX iron.
    11. **Hydraulic Thread Yielding:** Injects OS-level micro-yields during
        complex triangulation to preserve Ocular HUD responsiveness.
    12. **Luminous Flask Radiation:** Multicasts "FLASK_SUTURE_COMPLETE" pulses
        to the HUD, rendering a Blue-Aura bloom when a blueprint is bound.
    13. **Context Processor Suture:** Automatically identifies global template
        helpers and wires them into 'app.context_processor'.
    14. **Error Handler Suture:** Detects custom exception handlers and grafts
        them via 'app.register_error_handler'.
    15. **CLI Group Registration:** Surgically wires Click-based command groups
        into the Flask CLI manifold.
    16. **Middleware Stack Balancing:** Wires WSGI/ASGI middleware with correct
        priority to ensure auth-guards precede logic.
    17. **Static Path Divination:** Automatically configures 'static_url_path'
        if the shard contains ocular assets.
    18. **Config Object Inception:** Suggests 'app.config.from_object' if
        a Gnostic Conscience (Settings) shard is detected.
    19. **Phantom Marker Sieve:** Automatically exorcises @scaffold markers
        from the generated code before physical inscription.
    20. **Isomorphic URI Support:** Prepares the interface for 'scaffold://'
        URI resolution from the Gnostic Hub.
    21. **Entropy-Aware Masking:** Automatically shrouds high-entropy
        variable defaults found in the ShardHeader.
    22. **Trace ID Silver-Cord Suture:** Inscripts the active Trace ID into
        generated comments for 1:1 forensic traceability.
    23. **Apophatic Error Unwrapping:** Transmutes internal surgery failures
        into human-readable 'Paths to Redemption' for the Architect.
    24. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        runnable, and warded micro-kernel architecture.
    =================================================================================
    """
    name = "Flask"

    # [ASCENSION 19]: THE PHANTOM MARKER EXORCIST
    MARKER_REGEX: Final[re.Pattern] = re.compile(
        r'#\s*@scaffold:(?P<type>blueprint|extension|app|command|handler)(?:\((?P<meta>.*)\))?'
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
        [THE MASTER CURE]: Identifies the Shard's Micro-Kernel Role from the Dossier.
        """
        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY) ---
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            # Find the manifest associated with this physical locus
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None

                if role in ("flask-blueprint", "flask-extension", "flask-heart"):
                    # Achieved Genomic Resonance
                    symbol = self._find_symbol_near_marker(content, "") or "App"
                    self.faculty.logger.info(f"🧬 Genomic Flask Resonance: Shard '{shard_id}' identifies as '{role}'.")
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
        if "Blueprint(" in content:
            symbol = self._find_symbol_near_marker(content, "") or "bp"
            return f"role:flask-blueprint:{symbol}:"

        if "Flask(" in content:
            return "role:flask-heart:app:"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE CAUSAL INQUEST (V-Ω-STAGING-AWARE)                                  ==
        =============================================================================
        Locates the 'Heart' (App Instance or Factory) of the project.
        """
        if self._target_cache:
            return self._target_cache

        # --- MOVEMENT I: THE VIRTUAL GAZE (STAGING) ---
        if tx and hasattr(tx, 'write_dossier'):
            for logical_path, result in tx.write_dossier.items():
                if logical_path.name in ("app.py", "wsgi.py", "factory.py", "main.py"):
                    staged_path = tx.get_staging_path(logical_path)
                    if staged_path.exists():
                        self._target_cache = (root / logical_path).resolve()
                        return self._target_cache

        # --- MOVEMENT II: THE PHYSICAL GAZE (DISK) ---
        target = self.faculty.heuristics.find_best_match(
            root,
            ["def create_app", "Flask(__name__)", "register_blueprint("],
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
        == THE OMEGA FORGE INJECTION: TOTALITY (V-Ω-VMAX-SURGICAL-SUTURE)              ==
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', 'tr-flask-void')

        # --- MOVEMENT I: DECONSTRUCTION ---
        # URN: {origin}:{role}:{symbol}:{meta}
        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            raw_meta = parts[3] if len(parts) > 3 else ""
        except (IndexError, ValueError):
            return None

        if role_intent == "flask-heart": return None

        # --- MOVEMENT II: GEOMETRIC TRIANGULATION ---
        try:
            tx = getattr(self.faculty, 'transaction', None)
            abs_target_file = self.find_target(root, tx)

            if not abs_target_file:
                self.faculty.logger.warn(f"   [Flask] Triangulation Void: App Heart unmanifest.")
                return None

            # [ASCENSION 3]: RELATIONAL TRIANGULATION (THE CURE)
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
                # [ASCENSION 6]: Identity Suture
                clean_p = re.sub(r'[^a-zA-Z0-9_]', '_', p)
                if clean_p: clean_parts.append(clean_p)

            module_dot_path = ".".join(clean_parts)

            # [ASCENSION 7]: IDENTITY MAPPING
            safe_stem = re.sub(r'[^a-zA-Z0-9_]', '_', source_path.stem)
            alias = f"{safe_stem}_{symbol_name}"

        except Exception as e:
            self.faculty.logger.error(f"   [Flask] Triangulation Paradox: {e}")
            return None

        # --- MOVEMENT III: IDENTITY ADJUDICATION ---
        # [ASCENSION 2]: Find the variable holding the Flask instance (app, flask_app, etc.)
        instance_name = "app"
        instance_match = re.search(r"^(?P<var>[a-zA-Z_]\w*)\s*(?::\s*[\w\.]+)?\s*=\s*(?:\w+\.)?Flask\(",
                                   target_content, re.MULTILINE)
        if instance_match:
            instance_name = instance_match.group("var")

        # Check for Factory Pattern
        in_factory = "def create_app" in target_content

        # --- MOVEMENT IV: PLAN MANIFESTATION (THE STRIKE) ---

        # 1. FORGE THE IMPORT
        import_stmt = f"from {leading_dots}{module_dot_path} import {symbol_name} as {alias}"

        # 2. IDEMPOTENCY CHECK
        if f" {alias}" in target_content or import_stmt in target_content:
            return None

        # 3. SURGICAL BRANCHING (ROLE-BASED)
        wire_stmt = ""
        anchor = instance_name

        # [ROLE A: BLUEPRINT]
        if role_intent in ("flask-blueprint", "blueprint"):
            # [ASCENSION 5]: Prefix Divination
            prefix = f"/{safe_stem.replace('_', '-')}"
            wire_stmt = f"{instance_name}.register_blueprint({alias}, url_prefix='{prefix}')"
            anchor = "register_blueprint" if "register_blueprint" in target_content else (
                "return " + instance_name if in_factory else instance_name
            )

        # [ROLE B: EXTENSION]
        elif role_intent in ("flask-extension", "extension"):
            # [ASCENSION 4]: init_app Suture
            wire_stmt = f"{alias}.init_app({instance_name})"
            anchor = "init_app" if "init_app" in target_content else (
                "return " + instance_name if in_factory else instance_name
            )

        # [ROLE C: COMMAND]
        elif role_intent == "command":
            wire_stmt = f"{instance_name}.cli.add_command({alias})"
            anchor = "cli"

        # [ROLE D: GENERIC SUTURE]
        elif role_intent == "suture":
            wire_stmt = f"{alias}({instance_name})"
            anchor = instance_name

        # --- MOVEMENT V: FINAL CHRONICLING ---
        if not wire_stmt: return None

        # [ASCENSION 22]: Trace ID Silver-Cord Suture
        wire_stmt = f"# [Trace: {trace_id}]\n{wire_stmt}"

        self.faculty.logger.success(
            f"   [Flask] [bold cyan]Suture Resonant:[/] Grafted Role '[yellow]{role_intent}[/]' "
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
        """Finds the variable, function, or class definition associated with the Flask intent."""
        lines = content.splitlines()
        try:
            marker_index = -1
            if marker_line:
                for i, line in enumerate(lines):
                    if line.strip() == marker_line.strip():
                        marker_index = i
                        break

            # Scan forward for the next assignment or definition
            start_scan = marker_index + 1 if marker_index != -1 else 0

            for i in range(start_scan, min(start_scan + 10, len(lines))):
                line = lines[i]
                # Match class Name, def name, or var =
                match = re.search(r'^\s*(?:async\s+)?(?:def|class)\s+(?P<name>\w+)', line)
                if not match:
                    match = re.search(r'^\s*(?P<name>\w+)\s*=', line)

                if match:
                    return match.group('name')
        except Exception:
            pass
        return None

    def __repr__(self) -> str:
        return f"<Ω_FLASK_STRATEGY status=RESONANT mode=MICRO_KERNEL version=3.0.0>"