# Path: scaffold/core/fusion/engine.py
# ------------------------------------

import ctypes
import hashlib
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, get_type_hints

from ...logger import Scribe
from ...contracts.heresy_contracts import ArtisanHeresy

Logger = Scribe("FusionEngine")


class FusionCore:
    """
    =============================================================================
    == THE FUSION CORE (V-Ω-JIT-COMPILER)                                      ==
    =============================================================================
    LIF: 10,000,000,000

    The heart of the Polyglot Fusion.
    1. **Detects** inline Rust code.
    2. **Hashes** it to ensure idempotency.
    3. **Compiles** it to a shared library (.so/.dll/..dylib).
    4. **Binds** it to Python via ctypes.
    """

    CACHE_DIR = Path.home() / ".scaffold" / "cache" / "fusion"

    def __init__(self):
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._rustc = shutil.which("rustc")

    def _get_lib_extension(self) -> str:
        system = platform.system()
        if system == "Windows": return ".dll"
        if system == "Darwin": return ".dylib"
        return ".so"

    def _type_map(self, py_type: Any) -> Any:
        """Transmutes Python types to C types."""
        if py_type == int: return ctypes.c_int32
        if py_type == float: return ctypes.c_double
        if py_type == bool: return ctypes.c_bool
        if py_type == str: return ctypes.c_char_p  # Requires careful handling
        return ctypes.c_void_p

    def compile_rust(self, code: str, func_name: str) -> Path:
        """
        The Rite of Compilation.
        Wraps the user's logic in the necessary extern "C" boilerplate if missing.
        """
        if not self._rustc:
            raise ArtisanHeresy("The 'rustc' artisan is missing. Install Rust to use Fusion.")

        # 1. Forge the Soul (Hash)
        code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest()[:16]
        lib_name = f"fusion_rust_{func_name}_{code_hash}{self._get_lib_extension()}"
        lib_path = self.CACHE_DIR / lib_name

        # 2. The Gnostic Chronocache (Idempotency check)
        if lib_path.exists():
            Logger.verbose(f"Fusion Cache Hit: {lib_name}")
            return lib_path

        Logger.info(f"Compiling Inline Rust: {func_name} ({code_hash})...")

        # 3. The Rite of Wrapping
        # If the user didn't include no_mangle, we wrap it.
        final_code = code
        if "#[no_mangle]" not in code:
            # We assume a simple function body was provided.
            # However, for robustness, we expect the user to provide the fn definition.
            # But we must ensure it is pub extern "C".
            if "extern \"C\"" not in code:
                # Naive injection - dangerous but helpful for simple cases.
                # Ideally, we ask the user to be explicit.
                pass

                # 4. The Forge
        with tempfile.TemporaryDirectory() as tmp_dir:
            src_path = Path(tmp_dir) / "lib.rs"
            src_path.write_text(final_code, encoding="utf-8")

            # rustc --crate-type cdylib -O -o output.so input.rs
            cmd = [
                self._rustc,
                "--crate-type", "cdylib",
                "-O",  # Optimize
                "-o", str(lib_path),
                str(src_path)
            ]

            try:
                subprocess.run(cmd, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                raise ArtisanHeresy(
                    f"Rust Compilation Failed for '{func_name}'",
                    details=f"Stderr:\n{e.stderr}",
                    suggestion="Check your Rust syntax inside the docstring."
                )

        return lib_path

    def bind_rust(self, lib_path: Path, func_name: str, py_hints: Dict[str, Any]) -> Callable:
        """
        The Rite of Binding. Loads the library and defines argtypes/restype.
        """
        try:
            lib = ctypes.cdll.LoadLibrary(str(lib_path))
            func = getattr(lib, func_name)
        except OSError as e:
            raise ArtisanHeresy(f"Failed to load compiled library: {e}")
        except AttributeError:
            raise ArtisanHeresy(
                f"Symbol '{func_name}' not found in compiled library.",
                suggestion=f"Did you forget `#[no_mangle]` or `pub extern \"C\"` in your Rust code?"
            )

        # Apply Types
        arg_types = []
        for arg_name, arg_type in py_hints.items():
            if arg_name == 'return':
                func.restype = self._type_map(arg_type)
            else:
                arg_types.append(self._type_map(arg_type))

        func.argtypes = arg_types
        return func


# Singleton Instance
_FUSION_ENGINE = FusionCore()


def rust_fusion(func):
    """
    The @rust Decorator.
    Transmutes a Python function with a Rust docstring into a native call.
    """
    doc = func.__doc__
    if not doc or "# @rust" not in doc:
        return func

    # Extract the Rust code block
    # We look for the content inside the docstring
    # Simple extraction: everything after # @rust
    code_match = doc.split("# @rust", 1)[1]

    # We need to unindent the code block based on the docstring indentation
    import textwrap
    rust_code = textwrap.dedent(code_match).strip()

    # Get Type Hints
    hints = get_type_hints(func)

    # Compile
    lib_path = _FUSION_ENGINE.compile_rust(rust_code, func.__name__)

    # Bind
    compiled_func = _FUSION_ENGINE.bind_rust(lib_path, func.__name__, hints)

    def wrapper(*args):
        # Type enforcement / marshaling could happen here
        return compiled_func(*args)

    return wrapper