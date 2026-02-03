# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/frameworks/strategies/flask.py
# -------------------------------------------------------------------------------------------------------------------------------

import re
from pathlib import Path
from typing import Optional
from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case

class FlaskStrategy(WiringStrategy):
    name = "Flask"

    def detect(self, content: str) -> Optional[str]:
        match = re.search(r"^(\w+)\s*=\s*Blueprint\(", content, re.MULTILINE)
        return match.group(1) if match else None

    def find_target(self, root: Path, tx) -> Optional[Path]:
        return self.faculty.heuristics.find_best_match(root, ["Flask(__name__)"], tx)

    def forge_injection(self, source_path: Path, component_var: str, target_content: str, root: Path) -> Optional[InjectionPlan]:
        try:
            rel = source_path.relative_to(root)
            mod = str(rel.with_suffix('')).replace('/', '.')
        except ValueError: return None

        alias = f"{source_path.stem}_bp"
        prefix = f"/{to_snake_case(source_path.stem).replace('_', '-')}"

        if f"register_blueprint({alias}" in target_content:
            return None

        import_stmt = f"from {mod} import {component_var} as {alias}"
        wire_stmt = f"app.register_blueprint({alias}, url_prefix=\"{prefix}\")"

        return InjectionPlan(
            target_file=Path("unknown"),
            import_stmt=import_stmt,
            wiring_stmt=wire_stmt,
            anchor="app",
            strategy_name=self.name
        )