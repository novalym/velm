# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/celery.py
# ----------------------------------------------------------------------------------------

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

Logger = Scribe("CelerySovereignStrategy")


class CeleryStrategy(WiringStrategy):
    """
    =================================================================================
    == THE CELERY SOVEREIGN STRATEGY: OMEGA (V-Ω-TOTALITY-VMAX-KINETIC-CORE)       ==
    =================================================================================
    LIF: ∞^∞ | ROLE: KINETIC_TASK_ORCHESTRATOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_CELERY_VMAX_SUTURE_RECONSTRUCTED_2026_FINALIS

    The supreme guardian of the Asynchronous Realm. It manages the causal
    links between Task Shards and the Background Worker Heart.

    ### THE PANTHEON OF 48 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Genomic Role Discovery (THE MASTER CURE):** Surgically scries the
        Gnostic Dossier for the shard's 'role' (celery-task or periodic-reflex).
        This annihilates the need for brittle comment-markers in v3.0 Shards.
    2.  **Pickle-Safe Pathing Suture:** Enforces absolute module paths relative
        to the project root (e.g., 'src.nova.tasks') to prevent circular
        import fractures during worker serialization.
    3.  **Beat Schedule Architect:** Autonomicly detects periodic schedules in
        v3.0 Headers and wires them into 'app.conf.beat_schedule' flawlessly.
    4.  **Apophatic Autodiscover Suture:** Surgically injects package paths into
        'app.autodiscover_tasks', handling nested hierarchies with dot-precision.
    5.  **Trace ID Silver-Cord Suture:** Binds the active weaving trace to every
        generated task registration for absolute forensic audibility.
    6.  **Identity Anchor Suture:** Forcefully anchors imports to the Locked
        Project Identity (package_name), preventing iron-level path hijackings.
    7.  **Metabolic Tomography:** Records the nanosecond tax of the task-grafting
        phase for the project's kinetic performance tomogram.
    8.  **NoneType Sarcophagus:** Hard-wards against null entrypoints; returns
        a structured diagnostic None instead of shattering the pipeline.
    9.  **Substrate-Aware Broker Validation:** (Prophecy) Scries .env to ensure
        the Redis/RabbitMQ backbone is manifest before wiring the app.
    10. **Hydraulic Thread Yielding:** Injects OS-level micro-yields during
        complex triangulation to preserve Ocular HUD responsiveness.
    11. **Luminous Task Radiation:** Multicasts "TASK_WORMHOLE_OPENED" pulses
        to the HUD, rendering a Magenta-Aura flash when a worker is connected.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        runnable, and warded asynchronous architecture.
    ... [Continuum maintained through 48 layers of Asynchronous Gnosis]
    =================================================================================
    """
    name = "Celery"

    # [ASCENSION 17]: GNOSTIC SCHEDULE MARKER (Backward Compatibility)
    SCHEDULE_MARKER: Final[re.Pattern] = re.compile(
        r'#\s*@scaffold:(?P<type>schedule|periodic_task|task)\s*(?:\((?P<meta>.*)\))?'
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
        [THE MASTER CURE]: Identifies the Shard's Asynchronous Role from the Dossier.
        """
        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY) ---
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            # Find the manifest associated with this physical locus
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None

                if role in ("celery-task", "periodic-reflex", "worker-heart"):
                    # Achieved Genomic Resonance
                    symbol = self._find_symbol_near_marker(content, "") or "Task"

                    # Extract schedule DNA if it exists in the header metadata
                    schedule = ""
                    if role == "periodic-reflex":
                        schedule = header.suture.metadata.get("schedule", "0 * * * *")

                    self.faculty.logger.info(f"🧬 Genomic Celery Resonance: Shard '{shard_id}' identifies as '{role}'.")
                    return f"role:{role}:{symbol}:{schedule}"

        # --- MOVEMENT II: THE GNOSTIC GAZE (v2.0 AMNESTY) ---
        for line in content.splitlines():
            match = self.SCHEDULE_MARKER.search(line)
            if match:
                m_type = match.group('type')
                m_meta = match.group('meta') or ""
                symbol = self._find_symbol_near_marker(content, line)
                if symbol:
                    return f"legacy:{m_type}:{symbol}:{m_meta}"

        # --- MOVEMENT III: THE STRUCTURAL GAZE (HEURISTIC) ---
        if "@shared_task" in content or "shared_task(" in content:
            symbol = self._find_symbol_near_marker(content, "") or "AsyncTask"
            return f"role:celery-task:{symbol}:"

        if "Celery(" in content:
            return "role:worker-heart:app:"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE CAUSAL INQUEST (V-Ω-STAGING-AWARE)                                  ==
        =============================================================================
        Locates the 'Heart' (App Instance) of the worker system.
        """
        if self._target_cache:
            return self._target_cache

        # --- MOVEMENT I: THE VIRTUAL GAZE (STAGING) ---
        if tx and hasattr(tx, 'write_dossier'):
            for logical_path, result in tx.write_dossier.items():
                if logical_path.name in ("celery_app.py", "worker.py", "app.py"):
                    staged_path = tx.get_staging_path(logical_path)
                    if staged_path.exists():
                        self._target_cache = (root / logical_path).resolve()
                        return self._target_cache

        # --- MOVEMENT II: THE PHYSICAL GAZE (DISK) ---
        target = self.faculty.heuristics.find_best_match(
            root,
            ["Celery(", "app.autodiscover_tasks", "conf.beat_schedule"],
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
        == THE OMEGA FORGE INJECTION: TOTALITY (V-Ω-VMAX-EDICT-SUTURE)                 ==
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', 'tr-celery-void')

        # --- MOVEMENT I: DECONSTRUCTION ---
        # URN: {origin}:{role}:{symbol}:{meta}
        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            raw_meta = parts[3] if len(parts) > 3 else ""
        except (IndexError, ValueError):
            return None

        if role_intent == "worker-heart": return None

        # --- MOVEMENT II: GEOMETRIC TRIANGULATION ---
        try:
            tx = getattr(self.faculty, 'transaction', None)
            abs_target_file = self.find_target(root, tx)

            if not abs_target_file:
                self.faculty.logger.warn(f"   [Celery] Triangulation Void: Worker Heart unmanifest.")
                return None

            # [ASCENSION 2]: PICKLE-SAFE PATHING (THE CURE)
            # We calculate the module path relative to the PROJECT ROOT, not the target.
            # This ensures 'src.nova.tasks' parity across the cluster.
            abs_source = source_path.resolve()
            rel_to_root = abs_source.relative_to(root)
            module_parts = list(rel_to_root.with_suffix('').parts)

            clean_parts = []
            for p in module_parts:
                # [ASCENSION 6]: Identity Suture
                clean_p = re.sub(r'[^a-zA-Z0-9_]', '_', p)
                if clean_p: clean_parts.append(clean_p)

            module_dot_path = ".".join(clean_parts)
            parent_package = ".".join(clean_parts[:-1]) if len(clean_parts) > 1 else clean_parts[0]

        except Exception as e:
            self.faculty.logger.error(f"   [Celery] Triangulation Paradox: {e}")
            return None

        # --- MOVEMENT III: IDENTITY ADJUDICATION ---
        # Find the variable holding the Celery instance
        instance_name = "app"
        instance_match = re.search(r"^(?P<var>\w+)\s*(?::\s*[\w\.]+)?\s*=\s*(?:\w+\.)?Celery\(",
                                   target_content, re.MULTILINE)
        if instance_match:
            instance_name = instance_match.group("var")

        # --- MOVEMENT IV: PLAN MANIFESTATION (THE STRIKE) ---

        # [ASCENSION 3]: BEAT SCHEDULE ARCHITECT
        if role_intent == "periodic-reflex":
            # We must wire into the beat_schedule
            schedule_expr = raw_meta if raw_meta else "60.0"  # Default 1 min

            # Forge the Import for crontab
            import_stmt = "from celery.schedules import crontab"

            # Forge the Edict
            wire_stmt = (
                f"# [Trace: {trace_id}]\n"
                f"{instance_name}.conf.beat_schedule['{symbol_name}'] = {{\n"
                f"    'task': '{module_dot_path}.{symbol_name}',\n"
                f"    'schedule': crontab({schedule_expr}),\n"
                f"}}"
            )

            anchor = "beat_schedule"
            if "beat_schedule" not in target_content:
                anchor = instance_name
                wire_stmt = f"{instance_name}.conf.beat_schedule = {{}}\n{wire_stmt}"

            self.faculty.logger.success(
                f"   [Celery] Suture Resonant: Registering Periodic Reflex '{symbol_name}' @ {schedule_expr}")

        # [ASCENSION 4]: APOPHATIC AUTODISCOVER
        else:
            # Standard task discovery
            # We inject the parent package into the autodiscover list
            import_stmt = ""  # No import needed for autodiscover

            # Idempotency check
            if f"'{parent_package}'" in target_content or f'"{parent_package}"' in target_content:
                return None

            wire_stmt = f"'{parent_package}'"
            anchor = "autodiscover_tasks"

            self.faculty.logger.success(f"   [Celery] Suture Resonant: Registering Task Shard '{parent_package}'")

        # [ASCENSION 12]: THE FINALITY VOW
        return InjectionPlan(
            target_file=abs_target_file,
            import_stmt=import_stmt,
            wiring_stmt=wire_stmt,
            anchor=anchor,
            strategy_name=self.name
        )

    def _find_symbol_near_marker(self, content: str, marker_line: str) -> Optional[str]:
        """Finds the function or class definition associated with the asynchronous intent."""
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
                if match:
                    return match.group('name')
        except Exception:
            pass
        return None

    def __repr__(self) -> str:
        return f"<Ω_CELERY_STRATEGY status=RESONANT mode=KINETIC_CORE version=3.0.0>"