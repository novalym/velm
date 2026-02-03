# Path: scaffold/artisans/bridge/artisan.py
# -----------------------------------------

from pathlib import Path
from typing import Dict, Any

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import BridgeRequest
from ...help_registry import register_artisan
from ...inquisitor import get_treesitter_gnosis
from ...utils import atomic_write, to_snake_case


@register_artisan("bridge")
class BridgeArtisan(BaseArtisan[BridgeRequest]):
    """
    =============================================================================
    == THE POLYGLOT BRIDGE (V-Ω-PYO3-AUTOMATOR)                                ==
    =============================================================================
    LIF: 10,000,000,000

    Automates the painful ritual of binding Rust to Python.
    1. Scans the Rust struct.
    2. Forges `lib.rs` with `#[pyclass]`.
    3. Forges `Cargo.toml` with `pyo3` + `maturin`.
    4. Forges `pyproject.toml` for the build system.
    """

    def execute(self, request: BridgeRequest) -> ScaffoldResult:
        if request.source_lang != "rust" or request.target_lang != "python":
            return self.failure("Only Rust -> Python bridging is currently supported in this epoch.")

        entry_path = (self.project_root / request.entry_point).resolve()
        if not entry_path.exists():
            return self.failure(f"Source scripture '{entry_path.name}' is a void.")

        self.logger.info(f" forging the bridge between {entry_path.name} and Python...")

        # 1. Gnostic Analysis (Extract Struct/Impl)
        content = entry_path.read_text(encoding='utf-8')
        gnosis = get_treesitter_gnosis(entry_path, content)

        if "error" in gnosis:
            return self.failure(f"Could not perceive Rust structure: {gnosis['error']}")

        # 2. Forge the Rust Lib (The Shim)
        lib_content = self._forge_rust_lib(gnosis, entry_path.stem)

        # 3. Forge the Manifests
        cargo_content = self._forge_cargo_toml(entry_path.stem)
        pyproject_content = self._forge_pyproject_toml(entry_path.stem)

        # 4. Inscription
        artifacts = []

        # We create a new crate directory
        crate_name = f"{to_snake_case(entry_path.stem)}_bridge"
        crate_root = self.project_root / "crates" / crate_name
        crate_src = crate_root / "src"
        crate_src.mkdir(parents=True, exist_ok=True)

        res_lib = atomic_write(crate_src / "lib.rs", lib_content, self.logger, self.project_root)
        artifacts.append(Artifact(path=res_lib.path, type="file", action="created"))

        res_cargo = atomic_write(crate_root / "Cargo.toml", cargo_content, self.logger, self.project_root)
        artifacts.append(Artifact(path=res_cargo.path, type="file", action="created"))

        res_py = atomic_write(crate_root / "pyproject.toml", pyproject_content, self.logger, self.project_root)
        artifacts.append(Artifact(path=res_py.path, type="file", action="created"))

        return self.success(
            f"Bridge forged in 'crates/{crate_name}'. Use 'maturin develop' to activate.",
            artifacts=artifacts
        )

    def _forge_rust_lib(self, gnosis: Dict, module_name: str) -> str:
        """Generates the PyO3 binding code."""
        # This is a template logic. In V-Omega we construct it intelligently.
        # We need to expose the Structs found in gnosis.

        structs = [c['name'] for c in gnosis.get('classes', [])]  # In Rust inquisitor, structs map to classes

        lines = [
            "use pyo3::prelude::*;",
            f"mod {module_name};",  # Assuming original file is moved/linked here
            f"use {module_name}::*;",
            ""
        ]

        # Wrap structs
        for struct in structs:
            lines.append(f"#[pyclass]")
            lines.append(f"struct Py{struct} {{ inner: {struct} }}")
            lines.append("")

        # Module definition
        lines.append("#[pymodule]")
        lines.append(f"fn {module_name}(_py: Python, m: &PyModule) -> PyResult<()> {{")
        for struct in structs:
            lines.append(f"    m.add_class::<Py{struct}>()?;")
        lines.append("    Ok(())")
        lines.append("}")

        return "\n".join(lines)

    def _forge_cargo_toml(self, name: str) -> str:
        return f"""
[package]
name = "{name}"
version = "0.1.0"
edition = "2021"

[lib]
name = "{name}"
crate-type = ["cdylib"]

[dependencies]
pyo3 = {{ version = "0.20.0", features = ["extension-module"] }}
"""

    def _forge_pyproject_toml(self, name: str) -> str:
        return f"""
[build-system]
requires = ["maturin>=1.0,<2.0"]
build-backend = "maturin"

[project]
name = "{name}"
requires-python = ">=3.7"
classifiers = [
    "Programming Language :: Rust",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy",
]
"""

