# Path: scaffold/artisans/simulacrum/runtimes/go.py
# -------------------------------------------------
import os
import shutil
import re
from pathlib import Path
from typing import List, Dict, Optional

from .base import BaseRuntime, RuntimeConfig
from ..exceptions import VoidCollapseError
from ....logger import Scribe

Logger = Scribe("GoRuntime")


class GoRuntime(BaseRuntime):
    """
    =================================================================================
    == THE GO RUNTIME (V-Ω-IRON-GOPHER-ASCENDED)                                   ==
    =================================================================================
    LIF: INFINITY | AUTH_CODE: Ω_GO_RUNTIME_V12

    Executes Go logic within the Void Sanctum, maintaining full module awareness.
    """

    def prepare_source(self, content: str, void_path: Path, filename: str) -> Path:
        """
        [ELEVATION 3]: AUTOMATIC WRAPPING & INJECTION
        Ensures the code is a valid Go program.
        """
        # 1. Handle Package Declaration
        if not re.search(r"^\s*package\s+", content, re.MULTILINE):
            content = f"package main\n\n{content}"
            Logger.verbose("Injected 'package main' into Void Scripture.")

        # 2. Handle Main Function Wrapper
        if "package main" in content and "func main()" not in content:
            # We wrap the content in main, but try to keep imports outside
            # This is a heuristic wrap
            lines = content.splitlines()
            imports = []
            logic = []
            in_import_block = False

            for line in lines:
                if line.startswith("import"):
                    imports.append(line)
                    if "(" in line and ")" not in line: in_import_block = True
                elif in_import_block:
                    imports.append(line)
                    if ")" in line: in_import_block = False
                elif not line.startswith("package "):
                    logic.append(line)

            content = f"{lines[0]}\n" + "\n".join(imports) + "\n\nfunc main() {\n" + "\n".join(logic) + "\n}"
            Logger.verbose("Wrapped logic in 'func main()'.")

        # 3. Apply Build Tags (Elevation 5)
        content = f"// +build gnostic_void\n\n{content}"

        script_path = void_path / filename
        script_path.write_text(content, encoding="utf-8")
        return script_path

    def configure(self, void_path: Path) -> RuntimeConfig:
        """
        The Strategic Configuration Rite.
        """
        # 1. Toolchain Discovery (Elevation 8)
        go_bin = shutil.which("go")
        if not go_bin:
            # Check standard GOROOT fallbacks
            goroot = os.environ.get("GOROOT")
            if goroot:
                ext = ".exe" if os.name == 'nt' else ""
                candidate = Path(goroot) / "bin" / f"go{ext}"
                if candidate.exists():
                    go_bin = str(candidate)

        if not go_bin:
            raise VoidCollapseError("The 'go' toolchain is not manifest in this reality.")

        # 2. Module Identity Resonance (Elevation 1)
        # We need to know the module name so imports like `import "my-project/src/utils"` work.
        module_name = self._divine_module_name()

        # 3. Environment Fusion (Elevation 2 & 6)
        env = {
            "GO111MODULE": "on",
            "GOPATH": os.environ.get("GOPATH", ""),
            # Siphon caches to prevent re-downloads
            "GOCACHE": os.environ.get("GOCACHE", str(Path.home() / ".cache" / "go-build")),
            "GOMODCACHE": os.environ.get("GOMODCACHE", os.path.join(os.environ.get("GOPATH", ""), "pkg", "mod")),
        }

        # 4. Command Selection
        # We use 'go run' for simplicity, but enforce module mode.
        args = ["run"]

        # [ELEVATION 4]: Vendor Awareness
        if (self.project_root / "vendor").exists():
            args.append("-mod=vendor")
            Logger.verbose("Engaging -mod=vendor strategy.")

        # [ELEVATION 11]: Fast Build Optimization
        # -ldflags="-s -w" reduces binary size and overhead
        # args.extend(["-ldflags", "-s -w"])

        return RuntimeConfig(
            binary=go_bin,
            args=args,
            extension="go",
            entry_point_name="main.go",
            env_inject=env
        )

    def _divine_module_name(self) -> str:
        """Reads the project's go.mod to find the module identity."""
        go_mod = self.project_root / "go.mod"
        if go_mod.exists():
            try:
                content = go_mod.read_text(encoding='utf-8')
                match = re.search(r"^module\s+(.+)$", content, re.MULTILINE)
                if match:
                    name = match.group(1).strip()
                    Logger.debug(f"Module Resonance: {name}")
                    return name
            except Exception:
                pass
        return "gnostic/void"