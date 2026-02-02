import shutil
from pathlib import Path
from .base import BaseRuntime, RuntimeConfig


class RustRuntime(BaseRuntime):
    def configure(self, void_path: Path) -> RuntimeConfig:
        # We assume the Bridge has linked Cargo.toml
        return RuntimeConfig(

            # ALTERNATIVE: Use `cargo script` (unstable) or just stick to `rust-script`.
            # Let's default to a simple rustc for V1 to ensure it works without complex setup.
            binary="rustc",
            args=["--crate-name", "simulation", "-o", str(void_path / "sim.exe" if os.name == 'nt' else "sim")],
            extension="rs",
            entry_point_name="main.rs"
        )

    def prepare_source(self, content: str, void_path: Path, filename: str) -> Path:
        # Wrap in main if missing
        if "fn main" not in content:
            content = f"fn main() {{\n{content}\n}}"
        return super().prepare_source(content, void_path, filename)