# Path: scaffold/artisans/translocate_core/conductor/structure_sentinel/strategies/python_strategy/frameworks/strategies/fastapi.py
# ---------------------------------------------------------------------------------------------------------------------------------

import re
from pathlib import Path
from typing import Optional
from ..contracts import WiringStrategy, InjectionPlan
from .......utils import to_snake_case

class FastAPIStrategy(WiringStrategy):
    name = "FastAPI"

    def detect(self, content: str) -> Optional[str]:
        # Matches: router = APIRouter(...)
        match = re.search(r"^(\w+)\s*=\s*APIRouter\(", content, re.MULTILINE)
        return match.group(1) if match else None

    def find_target(self, root: Path, tx) -> Optional[Path]:
        # We look for the file initializing FastAPI
        return self.faculty.heuristics.find_best_match(root, ["FastAPI("], tx)

    def forge_injection(self, source_path: Path, component_var: str, target_content: str, root: Path) -> Optional[InjectionPlan]:
        try:
            rel = source_path.relative_to(root)
            mod = str(rel.with_suffix('')).replace('/', '.')
        except ValueError:
            return None

        alias = f"{source_path.stem}_router"
        prefix = f"/{to_snake_case(source_path.stem).replace('_', '-')}"
        tag = source_path.stem

        # Check for existence
        if f"include_router({alias}" in target_content or f"include_router({component_var}" in target_content:
            return None

        import_stmt = f"from {mod} import {component_var} as {alias}"
        wire_stmt = f"app.include_router({alias}, prefix=\"{prefix}\", tags=[\"{tag}\"])"

        return InjectionPlan(
            target_file=Path("unknown"), # Resolved by caller
            import_stmt=import_stmt,
            wiring_stmt=wire_stmt,
            anchor="app", # The variable name of the FastAPI instance
            strategy_name=self.name
        )