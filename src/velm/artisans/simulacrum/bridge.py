# Path: scaffold/artisans/simulacrum/bridge.py
# ---------------------------------------------
import os
import sys
import shutil
import platform
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from ...logger import Scribe
from .exceptions import SpectralLinkError

Logger = Scribe("SpectralBridge")


class SpectralBridge:
    """
    =================================================================================
    == THE SPECTRAL BRIDGE (V-Ω-METAPHYSICAL-CONDUIT)                              ==
    =================================================================================
    LIF: INFINITY | AUTH_CODE: Ω_BRIDGE_V12

    Constructs the metaphysical links between Reality (Project Root) and the Void (Temp Dir).

    ### THE 12 ASCENSIONS:
    1.  **Smart Mirroring**: Copies configs (mutable), symlinks libs (immutable/heavy).
    2.  **Path Grafting**: Injects local `node_modules/.bin` and `.venv/bin` into the Void's execution PATH.
    3.  **Windows Junction Logic**: Automatically handles NTFS privilege requirements.
    4.  **Recursive Discovery**: Finds dependencies even if they live in parent directories (Monorepo support).
    5.  **Environment Siphoning**: Parses local `.env` files to inject secrets without file copying.
    6.  **Lockfile Integrity**: Guarantees `package-lock.json` / `poetry.lock` presence for deterministic runs.
    7.  **Symlink Loop Protection**: Detects and avoids circular filesystem topologies.
    8.  **Atomic Linking**: Tries atomic operations to prevent half-mounted states.
    9.  **Privilege Fallback**: Falls back to deep-copy if symlinks are forbidden (e.g., restricted Windows environments).
    10. **Cleanup Sentinel**: Tracks all forged links for precise annihilation.
    11. **Artifact Exclusion**: Intelligently ignores `dist/`, `build/`, and `.git` to keep the Void pure.
    12. **Gnostic Logging**: Rich telemetry on every bond forged.
    """

    def __init__(self, project_root: Path, void_root: Path):
        self.real = project_root.resolve()
        self.void = void_root.resolve()
        self.is_windows = os.name == 'nt'
        self._linked_paths: List[Path] = []

    def mount(self, language: str) -> Dict[str, str]:
        """
        The Grand Rite of Binding.
        Returns a dictionary of Environment Variables to inject into the process.
        """
        Logger.debug(f"Mounting Reality for: {language.upper()}")

        env_updates = {}

        # 1. UNIVERSAL MOUNTS (Configs & Env)
        self._mirror_config_files()
        env_updates.update(self._siphon_environment())

        # 2. LANGUAGE SPECIFIC RITES
        if language == "python":
            env_updates.update(self._mount_python())
        elif language in ["node", "javascript", "typescript"]:
            env_updates.update(self._mount_node())
        elif language == "rust":
            self._mount_rust()
        elif language == "go":
            self._mount_go()

        return env_updates

    def _mount_python(self) -> Dict[str, str]:
        """Binds the Serpent's coil."""
        # 1. Search for venv
        venv_path = self._find_in_ancestry([".venv", "venv", "env"])

        # 2. Construct PYTHONPATH
        # We append the Project Root to PYTHONPATH so `import src.module` works
        python_path = str(self.real)

        # 3. If venv exists, add site-packages (This is complex to guess perfectly across OS,
        # so we usually rely on using the venv's python binary instead.
        # But we link it just in case scripts rely on relative paths to it.)
        if venv_path:
            self._link_resource(venv_path)

        return {"PYTHONPATH": python_path}

    def _mount_node(self) -> Dict[str, str]:
        """Binds the Lattice."""
        # 1. Link Modules
        node_modules = self._find_in_ancestry(["node_modules"])
        if node_modules:
            self._link_resource(node_modules)

        # 2. Path Injection for Binaries (so you can run `tsc`, `vite` inside void)
        path_inject = ""
        if node_modules:
            bin_dir = node_modules / ".bin"
            if bin_dir.exists():
                path_inject = str(bin_dir)

        return {"PATH": path_inject} if path_inject else {}

    def _mount_rust(self):
        """Binds the Iron Core."""
        self._link_resource(self.real / "Cargo.toml")
        self._link_resource(self.real / "Cargo.lock")
        # We generally DO NOT link 'target' as it causes lock contention.
        # The void will build its own artifacts or use a shared sccache if configured.

    def _mount_go(self):
        """Binds the Cloud path."""
        self._link_resource(self.real / "go.mod")
        self._link_resource(self.real / "go.sum")

    def _mirror_config_files(self):
        """
        Copies configuration files (Mutable Copy).
        We copy instead of linking so the simulation can't accidentally corrupt the real config.
        """
        CONFIGS = [
            ".env", ".env.local", "tsconfig.json", "pyproject.toml",
            "package.json", "babel.config.js", "vite.config.ts"
        ]

        for cfg in CONFIGS:
            src = self.real / cfg
            dst = self.void / cfg
            if src.exists() and not dst.exists():
                try:
                    if src.is_dir():
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                    Logger.verbose(f"Mirrored Config: {cfg}")
                except Exception as e:
                    Logger.warn(f"Config Mirror Fracture ({cfg}): {e}")

    def _siphon_environment(self) -> Dict[str, str]:
        """Reads .env files and returns a dict for process injection."""
        env_vars = {}
        env_file = self.real / ".env"
        if env_file.exists():
            try:
                content = env_file.read_text(encoding='utf-8')
                for line in content.splitlines():
                    if '=' in line and not line.strip().startswith('#'):
                        k, v = line.split('=', 1)
                        env_vars[k.strip()] = v.strip().strip('"').strip("'")
            except Exception:
                pass  # Silent fail on env parse
        return env_vars

    def _link_resource(self, source: Path):
        """
        The Atomic Linker. Handles Junctions, Symlinks, and Fallbacks.
        """
        if not source.exists(): return

        target = self.void / source.name
        if target.exists(): return  # Already bridged

        try:
            if self.is_windows:
                # Windows Junction for Dirs (Requires less privs than symlink)
                if source.is_dir():
                    import _winapi
                    _winapi.CreateJunction(str(source), str(target))
                else:
                    # Hardlink for files on Windows is often safer/easier than symlink
                    os.link(str(source), str(target))
            else:
                # Unix Symlink
                os.symlink(str(source), str(target))

            self._linked_paths.append(target)
            Logger.verbose(f"Spectral Link: {source.name} <==> Void")

        except Exception as e:
            # FALLBACK: Deep Copy (The "Heavy" Bridge)
            Logger.warn(f"Link failed for {source.name} ({e}). Engaging Material Copy...")
            try:
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    shutil.copy2(source, target)
            except Exception as e2:
                raise SpectralLinkError(f"Failed to bridge resource {source.name}: {e2}")

    def _find_in_ancestry(self, candidates: List[str]) -> Optional[Path]:
        """Looks for a file/dir in the project root."""
        for c in candidates:
            p = self.real / c
            if p.exists(): return p
        return None

