# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/frameworks/strategies/django.py
# --------------------------------------------------------------------------------------------------------------------------------

import re
from pathlib import Path
from typing import Optional
from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case


class DjangoStrategy(WiringStrategy):
    name = "Django"

    def detect(self, content: str) -> Optional[str]:
        # Detect if this file defines an AppConfig or urlpatterns
        if "class" in content and "AppConfig" in content:
            # Extract config class name
            match = re.search(r"class\s+(\w+)\(AppConfig\):", content)
            return match.group(1) if match else None
        return None

    def find_target(self, root: Path, tx) -> Optional[Path]:
        # Look for settings.py
        candidates = list(root.rglob("settings.py"))
        for c in candidates:
            content = self.faculty._read(c, root, tx)
            if "INSTALLED_APPS" in content:
                return c
        return None

    def forge_injection(self, source_path: Path, component_var: str, target_content: str, root: Path) -> Optional[
        InjectionPlan]:
        try:
            rel = source_path.relative_to(root)
            # apps.py -> package dot path
            # src/my_app/apps.py -> src.my_app.apps.MyAppConfig
            mod = str(rel.with_suffix('')).replace('/', '.')
        except ValueError:
            return None

        app_config_path = f"{mod}.{component_var}"

        if app_config_path in target_content:
            return None

        # Django doesn't need imports for INSTALLED_APPS strings
        import_stmt = ""
        # The wiring statement isn't a simple line, it's a list append.
        # We handle this via the specific DjangoSurgeon in the Engine.

        return InjectionPlan(
            target_file=Path("unknown"),
            import_stmt="",
            wiring_stmt=app_config_path,  # Special payload for DjangoSurgeon
            anchor="INSTALLED_APPS",
            strategy_name=self.name
        )