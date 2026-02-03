# Path: scaffold/core/ignition/diviner/heuristics/systems_inquisitor.py
# --------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_SYSTEMS_INQUISITOR_V1

from pathlib import Path
from typing import Tuple, List
from .base import BaseInquisitor
from ...contracts import IgnitionAura


class SystemsInquisitor(BaseInquisitor):
    """Perceives the soul of Systems Languages (Rust/Go/C++)."""

    def analyze(self, root: Path) -> Tuple[IgnitionAura, float, List[str]]:
        # RUST
        if (root / "Cargo.toml").exists():
            return IgnitionAura.CARGO, 1.0, ["Rust Cargo manifest present."]

        # GO
        if (root / "go.mod").exists():
            return IgnitionAura.GO_MOD, 1.0, ["Go Module manifest present."]

        # C++ / C
        if (root / "CMakeLists.txt").exists():
            return IgnitionAura.GENERIC, 0.8, ["C++ CMake manifest present."]

        return IgnitionAura.GENERIC, 0.0, []