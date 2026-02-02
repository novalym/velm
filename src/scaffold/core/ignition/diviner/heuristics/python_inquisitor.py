# Path: scaffold/core/ignition/diviner/heuristics/python_inquisitor.py
# -------------------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_PYTHON_INQUISITOR_V1

from pathlib import Path
from typing import Tuple, List
from .base import BaseInquisitor
from ...contracts import IgnitionAura


class PythonInquisitor(BaseInquisitor):
    """
    =============================================================================
    == THE PYTHON INQUISITOR (V-Ω-SERPENT-INFERENCE)                           ==
    =============================================================================
    Detects Python frameworks via manifest scanning and entrypoint forensics.
    """

    def analyze(self, root: Path) -> Tuple[IgnitionAura, float, List[str]]:
        pyproject = root / "pyproject.toml"
        requirements = root / "requirements.txt"

        has_python_matter = pyproject.exists() or requirements.exists() or any(root.glob("*.py"))

        if not has_python_matter:
            return IgnitionAura.GENERIC, 0.0, []

        # [ASCENSION 9]: SEMANTIC KEYWORD RESONANCE
        # Scan entrypoints for imports
        for entry in ["main.py", "app.py", "api.py", "wsgi.py", "asgi.py"]:
            p = root / entry
            if p.exists():
                content = self.read_manifest_safe(p)
                if "fastapi" in content.lower():
                    return IgnitionAura.FASTAPI, 0.98, [f"FastAPI signature in {entry}"]
                if "flask" in content.lower():
                    return IgnitionAura.FLASK, 0.95, [f"Flask signature in {entry}"]
                if "streamlit" in content.lower():
                    return IgnitionAura.STREAMLIT, 0.99, [f"Streamlit signature in {entry}"]
                if "django" in content.lower():
                    return IgnitionAura.DJANGO, 0.95, [f"Django signature in {entry}"]

        if pyproject.exists():
            content = self.read_manifest_safe(pyproject).lower()
            if "fastapi" in content: return IgnitionAura.FASTAPI, 0.9, ["Poetry/FastAPI detected."]
            return IgnitionAura.PYTHON_SCRIPT, 0.6, ["Python pyproject.toml found."]

        return IgnitionAura.PYTHON_SCRIPT, 0.3, ["Generic Python files present."]