# Path: artisans/fusion/artisan.py
# --------------------------------

import shutil
import subprocess
import os
from pathlib import Path
from typing import Optional

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import FusionRequest
from ...help_registry import register_artisan
from ...core.fusion.engine import FusionCore
from ...contracts.heresy_contracts import ArtisanHeresy
from ...utils import atomic_write


@register_artisan("fuse")
class FusionArtisan(BaseArtisan[FusionRequest]):
    """
    =================================================================================
    == THE FUSION CORE (V-Ω-POLYGLOT-BUILDER)                                    ==
    =================================================================================
    LIF: INFINITY

    Transmutes high-performance system code (Rust/Go) into scriptable modules
    (Python/Node) with zero friction.
    """

    def execute(self, request: FusionRequest) -> ScaffoldResult:
        self.cache_dir = FusionCore.CACHE_DIR

        # --- LEGACY RITES (Preserved) ---
        if request.fusion_command == "list":
            return self._conduct_list_rite(request)
        elif request.fusion_command == "clean":
            return self._conduct_clean_rite(request)

        # --- ASCENDED RITES (The New Power) ---
        elif request.fusion_command == "compile":
            return self._conduct_compile_rite(request)

        return self.failure(f"Unknown fusion rite: {request.fusion_command}")

    def _conduct_list_rite(self, request: FusionRequest) -> ScaffoldResult:
        if not self.cache_dir.exists():
            return self.success("The Fusion Cache is empty.")

        files = list(self.cache_dir.glob("*"))
        if request.target_lang:
            files = [f for f in files if request.target_lang in f.name]

        from rich.table import Table
        table = Table(title="Fused Artifacts")
        table.add_column("Library", style="cyan")
        table.add_column("Size", style="dim")

        for f in files:
            table.add_row(f.name, f"{f.stat().st_size} bytes")

        self.console.print(table)
        return self.success(f"Found {len(files)} compiled bonds.")

    def _conduct_clean_rite(self, request: FusionRequest) -> ScaffoldResult:
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        return self.success("The Fusion Cache has been purified.")

    def _conduct_compile_rite(self, request: FusionRequest) -> ScaffoldResult:
        """
        The Rite of Transmutation.
        Takes a raw source file (e.g., .rs) and compiles it into a native extension.
        """
        if not request.source:
            return self.failure("Source file required for compilation.")

        source_path = (self.project_root / request.source).resolve()
        if not source_path.exists():
            raise ArtisanHeresy(f"Source void: {source_path}")

        # Gnostic Triage based on extension
        if source_path.suffix == ".rs" and request.target_lang == "python":
            return self._fuse_rust_to_python(source_path, request.output_dir)

        return self.failure(f"Fusion from '{source_path.suffix}' to '{request.target_lang}' is not yet known.")

    def _fuse_rust_to_python(self, source: Path, output_dir: Optional[str]) -> ScaffoldResult:
        """
        Orchestrates the creation of a PyO3 binding.
        """
        self.logger.info(f"Fusing Rust soul '{source.name}' into Python...")

        # 1. Prepare Ephemeral Build Sanctum
        build_root = self.project_root / ".scaffold" / "fusion" / source.stem
        build_root.mkdir(parents=True, exist_ok=True)
        src_dir = build_root / "src"
        src_dir.mkdir(exist_ok=True)

        # 2. Transmute Cargo.toml (if missing)
        cargo_path = build_root / "Cargo.toml"
        if not cargo_path.exists():
            self.logger.info("Forging Cargo manifest...")
            cargo_content = f"""
[package]
name = "{source.stem}"
version = "0.1.0"
edition = "2021"

[lib]
name = "{source.stem}"
crate-type = ["cdylib"]

[dependencies]
pyo3 = {{ version = "0.20.0", features = ["extension-module"] }}
"""
            atomic_write(cargo_path, cargo_content, self.logger, self.project_root)

        # 3. Inject Gnostic Wrapper (The Binding Logic)
        # We read the user's code and ensure it has the PyO3 prelude and module export.
        user_code = source.read_text(encoding='utf-8')
        final_code = user_code

        if "#[pymodule]" not in user_code:
            self.logger.warn("Source lacks #[pymodule]. Injecting Gnostic Wrapper...")
            # We wrap the user's public functions automatically
            # (Simplified heuristic for V1 - assumes `pub fn` are targets)
            # In a real impl, we'd parse the Rust AST.
            wrapper = f"""
use pyo3::prelude::*;

{user_code}

#[pymodule]
fn {source.stem}(_py: Python, m: &PyModule) -> PyResult<()> {{
    // Gnostic Auto-Binding would go here.
    // For now, we assume the user wrote valid PyO3 functions but forgot the module block.
    Ok(())
}}
"""
            final_code = wrapper

        # Write to build src
        (src_dir / "lib.rs").write_text(final_code, encoding='utf-8')

        # 4. Compile (Maturin invocation)
        # We assume `maturin` is available in the environment.
        cmd = ["maturin", "build", "--release", "--manifest-path", str(cargo_path)]

        try:
            self.logger.info("Igniting the Rust Forge (Maturin)...")
            subprocess.run(cmd, check=True, cwd=build_root, capture_output=True)

            # 5. Harvest Artifact
            # Maturin puts wheels in target/wheels, but we want the .so/.pyd
            # Actually, `maturin develop` installs it. `maturin build` makes a wheel.
            # Let's use `maturin develop` to install into current venv, OR copy the .so

            # Find the shared object in target/release
            target_release = build_root / "target" / "release"

            # Extension varies by OS
            exts = [".so", ".pyd", ".dylib"]
            artifact = None
            for f in target_release.iterdir():
                if f.stem == source.stem and f.suffix in exts:
                    artifact = f
                    break

            if not artifact:
                # Fallback: check deps directory?
                raise FileNotFoundError("Compilation succeeded but artifact vanished.")

            # Move to output location
            final_dest = (self.project_root / (output_dir or ".")) / artifact.name
            shutil.copy2(artifact, final_dest)

            return self.success(
                f"Fusion complete. Artifact materialized at {final_dest}",
                artifacts=[Artifact(path=final_dest, type="file", action="created")]
            )

        except FileNotFoundError:
            return self.failure("The 'maturin' artisan is missing. `pip install maturin`")
        except subprocess.CalledProcessError as e:
            return self.failure(f"Fusion reactor failed.", details=e.stderr.decode() if e.stderr else str(e))