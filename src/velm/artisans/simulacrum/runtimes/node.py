# Path: scaffold/artisans/simulacrum/runtimes/node.py
# -------------------------------------------------
# LIF: INFINITY | AUTH_CODE: ()@()@ | ROLE: LATTICE_INTERPRETER
# =================================================================================

import shutil
import os
import json
import subprocess
import sys
from pathlib import Path
from .base import BaseRuntime, RuntimeConfig
from ....logger import Scribe

Logger = Scribe("NodeRuntime")


class NodeRuntime(BaseRuntime):
    """
    =================================================================================
    == THE NODE RUNTIME (V-Ω-NODE-22-ZENITH-FINAL)                                 ==
    =================================================================================
    """

    def configure(self, void_path: Path) -> RuntimeConfig:
        # [ELEVATION 1]: VERSION & SUBSTRATE SCRYING
        node_version = self._get_node_version()
        is_esm = self._is_esm()
        local_bin = (self.project_root / "node_modules" / ".bin").resolve()
        ext = ".cmd" if os.name == 'nt' else ""

        # [ELEVATION 2]: TSX PRIORITY (The Modern Standard)
        # tsx is immune to Node 22's loader paradoxes.
        # We look for it in the project, then the system.
        tsx_bin = shutil.which("tsx" + ext, path=str(local_bin)) or shutil.which("tsx")

        if tsx_bin:
            Logger.info("Zenith Logic: Engaging TSX Reality Driver.")
            return RuntimeConfig(
                binary=str(tsx_bin),
                args=[],
                extension="ts",
                entry_point_name="index.ts",
                env_inject={
                    "PATH": self._inject_path([str(local_bin)]),
                    "NODE_NO_WARNINGS": "1"
                }
            )

        # [ELEVATION 3]: THE LOADER PATH DIVINATION (FALLBACK)
        # We manually anchor the loader to avoid 'ERR_PACKAGE_PATH_NOT_EXPORTED'
        loader_path = self._divine_loader_path()
        node_bin = shutil.which("node" + ext) or "node"

        args = []
        env = {
            "NODE_ENV": "development",
            "TS_NODE_TRANSPILE_ONLY": "true",
            "NODE_NO_WARNINGS": "1",
            "PATH": self._inject_path([str(local_bin)])
        }

        if is_esm and loader_path:
            # [ELEVATION 4]: THE NODE 22 IMPORT RITE
            loader_uri = Path(loader_path).as_uri()
            if node_version >= 22:
                # Node 22 requires URI registration to handle .ts extensions
                args = ["--loader", loader_uri]
            else:
                args = ["--loader", loader_uri]
            Logger.info(f"Loader Anchored: {loader_uri}")
        else:
            # [ELEVATION 5]: CJS/LEGACY PIVOT
            ts_node = shutil.which("ts-node" + ext, path=str(local_bin)) or shutil.which("ts-node")
            if ts_node:
                return RuntimeConfig(binary=str(ts_node), args=[], extension="ts", entry_point_name="index.ts",
                                     env_inject=env)

        return RuntimeConfig(
            binary=node_bin,
            args=args,
            extension="ts",
            entry_point_name="index.ts",
            env_inject=env
        )

    def _divine_loader_path(self) -> str | None:
        """[FACULTY 3]: Hunts for the physical esm.mjs soul."""
        candidates = [
            self.project_root / "node_modules" / "ts-node" / "esm.mjs",
            self.project_root / "node_modules" / "ts-node" / "dist" / "esm.mjs",
            self.project_root / "node_modules" / "ts-node" / "register" / "esm.mjs"
        ]
        for c in candidates:
            if c.exists(): return str(c.resolve())
        return None

    def _get_node_version(self) -> int:
        try:
            output = subprocess.check_output(["node", "--version"], text=True)
            return int(output.strip().lstrip('v').split('.')[0])
        except:
            return 22

    def _is_esm(self) -> bool:
        pkg = self.project_root / "package.json"
        if pkg.exists():
            try:
                return json.loads(pkg.read_text(encoding='utf-8')).get("type") == "module"
            except:
                pass
        return True

    def prepare_source(self, content: str, void_path: Path, filename: str) -> Path:
        """[ELEVATION 8]: CONFIGURATION SHADOWING."""
        for cfg in ["package.json", "tsconfig.json"]:
            src = self.project_root / cfg
            if src.exists():
                shutil.copy2(src, void_path / cfg)

        script_path = void_path / filename
        # [ELEVATION 11]: UTF-8 INSCRIPTION
        script_path.write_text(content, encoding="utf-8")
        return script_path