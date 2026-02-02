import sys
import shutil
from pathlib import Path
from .base import BaseRuntime, RuntimeConfig


class PythonRuntime(BaseRuntime):
    def configure(self, void_path: Path) -> RuntimeConfig:
        # 1. Detect Virtual Environment
        venv_python = None
        for venv_name in [".venv", "venv", "env"]:
            if os.name == 'nt':
                candidate = self.project_root / venv_name / "Scripts" / "python.exe"
            else:
                candidate = self.project_root / venv_name / "bin" / "python"

            if candidate.exists():
                venv_python = str(candidate)
                break

        # 2. Select Binary
        binary = venv_python or sys.executable

        # 3. Inject PYTHONPATH
        # This is critical for `from src import X` to work
        # We add the Void Root AND the Project Root
        python_path = f"{str(self.project_root)}{os.pathsep}{str(void_path)}"

        return RuntimeConfig(
            binary=binary,
            args=["-u"],  # Unbuffered
            extension="py",
            entry_point_name="main.py",
            env_inject={
                "PYTHONPATH": python_path,
                "PYTHONUNBUFFERED": "1"
            }
        )