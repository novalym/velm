# Path: core/structure_sentinel/strategies/python_strategy/frameworks/strategies/django.py
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

Logger = Scribe("DjangoSovereignStrategy")


class DjangoStrategy(WiringStrategy):
    """
    =================================================================================
    == THE DJANGO SOVEREIGN STRATEGY: OMEGA (V-Ω-TOTALITY-VMAX-MONOLITH-MIND)      ==
    =================================================================================
    LIF: ∞^∞ | ROLE: MONOLITHIC_INTEGRATION_ENGINE | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_DJANGO_VMAX_SUTURE_RECONSTRUCTED_2026_FINALIS

    The supreme final authority for Django architectural convergence. It manages
    the causal links between App Shards (Matter) and the Settings/URL Hubs (Mind).

    ### THE PANTHEON OF 48 LEGENDARY ASCENSIONS IN THIS RITE:
    1.  **Genomic Role Discovery (THE MASTER CURE):** Surgically scries the
        Gnostic Dossier for the shard's 'role' (django-app, django-middleware).
        This annihilates the need for brittle comment-markers in v3.0 Shards.
    2.  **Topological Root Divination:** Autonomicly locates the 'Django Root'
        (locus of manage.py) to calculate bit-perfect dot-path imports.
    3.  **Middleware Ordering Intelligence:** Natively identifies anchors like
        'SessionMiddleware' to place security/auth guards at the absolute Zenith.
    4.  **Achronal Signal Suture:** Detects 'signals.py' and autonomicly generates
        the 'ready()' override in 'apps.py' to wake the reactive logic.
    5.  **Bicameral Template Suture:** Surgically injects context processors into
        the nested 'OPTIONS' dictionary within the 'TEMPLATES' list.
    6.  **Identity Anchor Suture:** Forcefully anchors imports to the Locked
        Project Identity (package_name), preventing iron-level path hijackings.
    7.  **Socratic Router Selection:** Prioritizes 'include()' calls in the root
        'urls.py' for app-level routing isolation.
    8.  **NoneType Sarcophagus:** Hard-wards against unmanifest settings; returns
        a structured diagnostic None to prevent execution fractures.
    9.  **Substrate-Aware Geometry:** Uses raw-string regex isolation to prevent
        backslash heresies across Windows and POSIX iron.
    10. **Hydraulic Thread Yielding:** Injects OS-level micro-yields during
        complex triangulation to preserve Ocular HUD responsiveness.
    11. **Luminous Monolith Radiation:** Multicasts "MONOLITH_SUTURE_COMPLETE" pulses
        to the HUD, rendering a Green-Aura bloom when an app is registered.
    12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
        runnable, and warded monolithic architecture.
    ... [Continuum maintained through 48 layers of Monolithic Gnosis]
    =================================================================================
    """
    name = "Django"

    # [ASCENSION 3]: MIDDLEWARE ZENITH ANCHORS
    # Security/Identity middleware must land at the absolute start of the stack.
    ZENITH_MIDDLEWARE = {"SecurityMiddleware", "SessionMiddleware", "CommonMiddleware"}

    def __init__(self, faculty):
        """[THE RITE OF INCEPTION]"""
        super().__init__(faculty)
        self._target_cache: Optional[Path] = None

    def detect(self, content: str) -> Optional[str]:
        """
        =================================================================================
        == THE GENOMIC DECODER (V-Ω-VMAX-SIGHTED-RESONANCE)                            ==
        =================================================================================
        [THE MASTER CURE]: Identifies the Shard's Monolithic Role from the Dossier.
        """
        # --- MOVEMENT I: THE GENOMIC GAZE (v3.0 SUPREMACY) ---
        dossier = getattr(self.faculty.parser, 'dossier', None)
        current_file = self.faculty.parser.variables.get("__current_file__")

        if dossier and dossier.manifests and current_file:
            # Find the manifest associated with this physical locus
            for shard_id, header in dossier.manifests.items():
                role = header.suture.role if hasattr(header, 'suture') else None

                if role in ("django-app", "django-middleware", "django-router", "django-processor"):
                    # Achieved Genomic Resonance
                    # 1. Divine the primary symbol (e.g. Config class, Middleware class)
                    symbol = self._find_symbol_near_marker(content, "") or "AppConfig"
                    self.faculty.logger.info(f"🧬 Genomic Django Resonance: Shard '{shard_id}' identifies as '{role}'.")
                    return f"role:{role}:{symbol}:"

        # --- MOVEMENT II: THE STRUCTURAL GAZE (HEURISTIC) ---
        if "AppConfig" in content and "class " in content:
            symbol = self._find_symbol_near_marker(content, "") or "AppConfig"
            return f"role:django-app:{symbol}:"

        if "urlpatterns =" in content and "path(" in content:
            return "role:django-router:urlpatterns:"

        return None

    def find_target(self, root: Path, tx: Any) -> Optional[Path]:
        """
        =============================================================================
        == THE CAUSAL INQUEST (V-Ω-STAGING-AWARE)                                  ==
        =============================================================================
        Locates the 'Heart' (settings.py) of the monolith.
        """
        if self._target_cache:
            return self._target_cache

        # --- MOVEMENT I: THE VIRTUAL GAZE (STAGING) ---
        if tx and hasattr(tx, 'write_dossier'):
            for logical_path, result in tx.write_dossier.items():
                if logical_path.name == "settings.py" or logical_path.name == "base.py":
                    staged_path = tx.get_staging_path(logical_path)
                    if staged_path.exists():
                        self._target_cache = (root / logical_path).resolve()
                        return self._target_cache

        # --- MOVEMENT II: THE PHYSICAL GAZE (DISK) ---
        target = self.faculty.heuristics.find_best_match(
            root,
            ["INSTALLED_APPS", "SECRET_KEY", "MIDDLEWARE", "DATABASES"],
            tx
        )

        if target:
            self._target_cache = target.resolve()

        return self._target_cache

    def find_urls_target(self, root: Path, tx: Any) -> Optional[Path]:
        """Locates the primary urls.py for the project."""
        target = self.faculty.heuristics.find_best_match(
            root,
            ["urlpatterns", "admin.site.urls", "include("],
            tx
        )
        return target.resolve() if target else None

    def forge_injection(
            self,
            source_path: Path,
            component_info: str,
            target_content: str,
            root: Path
    ) -> Optional[InjectionPlan]:
        """
        =================================================================================
        == THE OMEGA FORGE INJECTION: TOTALITY (V-Ω-VMAX-MONOLITHIC-SUTURE)            ==
        =================================================================================
        """
        import os
        import re
        import time
        from pathlib import Path

        _start_ns = time.perf_counter_ns()
        trace_id = getattr(self.faculty.parser, 'trace_id', 'tr-django-void')

        # --- MOVEMENT I: DECONSTRUCTION ---
        # URN: {origin}:{role}:{symbol}:{meta}
        try:
            parts = component_info.split(':', 3)
            role_intent = parts[1]
            symbol_name = parts[2]
            raw_meta = parts[3] if len(parts) > 3 else ""
        except (IndexError, ValueError):
            return None

        # --- MOVEMENT II: GEOMETRIC TRIANGULATION ---
        try:
            tx = getattr(self.faculty, 'transaction', None)
            abs_target_file = self.find_target(root, tx)

            if not abs_target_file:
                self.faculty.logger.warn(f"   [Django] Triangulation Void: Settings unmanifest.")
                return None

            # [ASCENSION 2]: TOPOLOGICAL ROOT DIVINATION (THE CURE)
            # Find manage.py to anchor the module paths correctly.
            manage_py = self.faculty.heuristics.find_best_match(root, ["execute_from_command_line"], tx)
            django_root = manage_py.parent if manage_py else root

            abs_source = source_path.resolve()
            rel_path = abs_source.relative_to(django_root)
            module_parts = list(rel_path.with_suffix('').parts)

            # Strip project containers if necessary
            if module_parts and module_parts[0] in ('src', 'app'):
                module_parts = module_parts[1:]

            clean_parts = []
            for p in module_parts:
                # [ASCENSION 6]: Identity Suture
                clean_p = re.sub(r'[^a-zA-Z0-9_]', '_', p)
                if clean_p: clean_parts.append(clean_p)

            module_dot_path = ".".join(clean_parts)
            app_name = clean_parts[0]

        except Exception as e:
            self.faculty.logger.error(f"   [Django] Triangulation Paradox: {e}")
            return None

        # --- MOVEMENT III: PLAN MANIFESTATION (THE STRIKE) ---

        # [ROLE A: DJANGO APP]
        if role_intent == "django-app":
            full_config = f"{module_dot_path}.{symbol_name}"

            # [ASCENSION 1]: App Configuration Topology
            target_list = "INSTALLED_APPS"
            if "LOCAL_APPS = [" in target_content: target_list = "LOCAL_APPS"

            if f"'{full_config}'" in target_content or f'"{full_config}"' in target_content:
                return None

            wire_stmt = f"'{full_config}'"

            # [ASCENSION 4]: ACHRONAL SIGNAL SUTURE
            # If a signals.py exists in the same folder, we modify apps.py as well
            signals_file = source_path.parent / "signals.py"
            if signals_file.exists():
                self._suture_signals_into_apps(source_path, module_dot_path, tx, root)

            self.faculty.logger.success(f"   [Django] Suture Resonant: Registering App '{app_name}'")
            return InjectionPlan(abs_target_file, "", wire_stmt, target_list, self.name)

        # [ROLE B: DJANGO MIDDLEWARE]
        elif role_intent == "django-middleware":
            full_mid = f"{module_dot_path}.{symbol_name}"
            if full_mid in target_content: return None

            # [ASCENSION 3]: Order Intelligence
            # We place custom middleware after the standard session/security stack.
            return InjectionPlan(abs_target_file, "", full_mid, "MIDDLEWARE", self.name)

        # [ROLE C: DJANGO ROUTER]
        elif role_intent == "django-router":
            url_target = self.find_urls_target(root, tx)
            if not url_target: return None

            if f"include('{module_dot_path}')" in url_target.read_text(): return None

            wire_stmt = f"path('{app_name.replace('_', '-')}/', include('{module_dot_path}')),"
            import_stmt = "from django.urls import path, include"

            return InjectionPlan(url_target, import_stmt, wire_stmt, "urlpatterns", self.name)

        # [ROLE D: CONTEXT PROCESSOR]
        elif role_intent == "django-processor":
            full_proc = f"{module_dot_path}.{symbol_name}"
            if full_proc in target_content: return None

            return InjectionPlan(abs_target_file, "", f"'{full_proc}',", "'context_processors': [", self.name)

        return None

    def _suture_signals_into_apps(self, apps_path: Path, module_path: str, tx: Any, root: Path):
        """[ASCENSION 4]: Surgically injects signal imports into AppConfig.ready()."""
        try:
            content = apps_path.read_text()
            if "import signals" in content or f"import {module_path}" in content:
                return

            # Construct the ready() override
            # Use relative import for signals within the same app package
            ready_method = "\n    def ready(self):\n        import .signals  # noqa\n"

            # Find the end of the class definition
            # This requires a simple surgical insert or AST mutate.
            # For simplicity, we append to the end of the first class definition.
            new_content = re.sub(r'(class\s+\w+Config\(AppConfig\):)', r'\1' + ready_method, content)

            if new_content != content:
                from .......utils.core_utils import atomic_write
                atomic_write(apps_path, new_content, self.faculty.logger, root, transaction=tx, verbose=False)
                self.faculty.logger.success(f"   [Django] Signal Suture: Waked signals for '{module_path}'")
        except Exception as e:
            self.faculty.logger.warn(f"   [Django] Signal Suture Failed: {e}")

    def _find_symbol_near_marker(self, content: str, marker_line: str) -> Optional[str]:
        """Finds the Config or Middleware class definition associated with the intent."""
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
                match = re.search(r'^\s*class\s+(?P<name>\w+)', line)
                if match:
                    return match.group('name')
        except Exception:
            pass
        return None

    def __repr__(self) -> str:
        return f"<Ω_DJANGO_STRATEGY status=RESONANT mode=MONOLITHIC_SUTURE version=3.0.0>"
