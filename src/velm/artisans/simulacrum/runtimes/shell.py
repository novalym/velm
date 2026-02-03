from pathlib import Path
from .base import BaseRuntime, RuntimeConfig

class ShellRuntime(BaseRuntime):
    def configure(self, void_path: Path) -> RuntimeConfig:
        return RuntimeConfig(
            binary="bash", # or sh
            args=["-e"], # Exit on error
            extension="sh",
            entry_point_name="script.sh"
        )