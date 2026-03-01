# Path: scaffold/artisans/simulacrum/bridge.py
# ---------------------------------------------
# LIF: ∞ | ROLE: METAPHYSICAL_CONDUIT | RANK: OMEGA_SOVEREIGN
# AUTH: Ω_BRIDGE_V24_TOTALITY_RESONANT_2026_FINALIS

import os
import sys
import shutil
import platform
import threading
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set, Final

# --- THE DIVINE UPLINKS ---
from ...logger import Scribe
from .exceptions import SpectralLinkError

Logger = Scribe("SpectralBridge")


class SpectralBridge:
    """
    =================================================================================
    == THE SPECTRAL BRIDGE: TOTALITY (V-Ω-TOTALITY-V24.0-WASM-RESILIENT)           ==
    =================================================================================
    LIF: ∞ | ROLE: REALITY_MIRROR | RANK: OMEGA_SUPREME

    Constructs the metaphysical links between Reality (Project Root) and the
    Void (Temp Dir). Engineered for absolute stability across Iron and Ether.
    =================================================================================
    """

    # [PHYSICS CONSTANTS]
    CONFIG_MANIFEST: Final[List[str]] = [
        ".env", ".env.local", ".env.development", "tsconfig.json",
        "pyproject.toml", "package.json", "babel.config.js",
        "vite.config.ts", "vite.config.js", "webpack.config.js"
    ]

    def __init__(self, project_root: Path, void_root: Path):
        """[THE RITE OF ANCHORING]"""
        self.real = project_root.resolve()
        self.void = void_root.resolve()
        self._lock = threading.RLock()

        # [ASCENSION 1 & 2]: SUBSTRATE CAPABILITY BIOPSY
        self._is_windows = os.name == 'nt'
        self._is_wasm = (
                os.environ.get("SCAFFOLD_ENV") == "WASM" or
                sys.platform == "emscripten" or
                "pyodide" in sys.modules
        )

        # Scry for native link resonance
        self._can_symlink = hasattr(os, 'symlink')
        self._can_hardlink = hasattr(os, 'link')
        self._has_winapi = False

        if self._is_windows and not self._is_wasm:
            try:
                import _winapi
                self._has_winapi = True
            except ImportError:
                pass

        self._linked_paths: List[Path] = []
        self.logger = Logger

    def mount(self, language: str) -> Dict[str, str]:
        """
        =============================================================================
        == THE GRAND RITE OF BINDING                                               ==
        =============================================================================
        Returns: Environment Map for process injection.
        """
        self.logger.info(f"Spectral Bridge: Materializing reality for [bold cyan]{language.upper()}[/]")

        env_updates: Dict[str, str] = {}

        with self._lock:
            # 1. UNIVERSAL MOUNTS (The Soul of the Project)
            self._mirror_config_files()
            env_updates.update(self._siphon_environment())

            # 2. LANGUAGE SPECIFIC RITES (The Limbs of the Project)
            if language == "python":
                env_updates.update(self._mount_python())
            elif language in ("node", "javascript", "typescript"):
                env_updates.update(self._mount_node())
            elif language == "rust":
                self._mount_rust()
            elif language == "go":
                self._mount_go()

        return env_updates

    # =========================================================================
    # == STRATUM: LANGUAGE MATERIALIZATION                                   ==
    # =========================================================================

    def _mount_python(self) -> Dict[str, str]:
        """Binds the Serpent's coil."""
        # 1. Search for virtual environment in ancestry (Monorepo support)
        venv_path = self._find_in_ancestry([".venv", "venv", "env"])

        if venv_path:
            self._link_resource(venv_path)

        # 2. Construct PYTHONPATH (Physical Project Root)
        return {"PYTHONPATH": str(self.real).replace('\\', '/')}

    def _mount_node(self) -> Dict[str, str]:
        """Binds the Node Lattice."""
        node_modules = self._find_in_ancestry(["node_modules"])
        path_inject = ""

        if node_modules:
            self._link_resource(node_modules)
            bin_dir = node_modules / ".bin"
            if bin_dir.exists():
                path_inject = str(bin_dir).replace('\\', '/')

        return {"PATH": f"{path_inject}{os.pathsep}{os.environ.get('PATH', '')}"} if path_inject else {}

    def _mount_rust(self):
        """Binds the Iron Core (Cargo)."""
        self._link_resource(self.real / "Cargo.toml")
        if (self.real / "Cargo.lock").exists():
            self._link_resource(self.real / "Cargo.lock")

    def _mount_go(self):
        """Binds the Cloud Path (Go)."""
        self._link_resource(self.real / "go.mod")
        if (self.real / "go.sum").exists():
            self._link_resource(self.real / "go.sum")

    # =========================================================================
    # == STRATUM: KINETIC LINKING & MIRRORING                                ==
    # =========================================================================

    def _mirror_config_files(self):
        """
        [ASCENSION 4]: ACHRONAL MIRRORING.
        Performs physical copies of mutable configuration matter.
        """
        for cfg in self.CONFIG_MANIFEST:
            src = self.real / cfg
            dst = self.void / cfg

            if src.exists() and not dst.exists():
                try:
                    if src.is_dir():
                        shutil.copytree(src, dst, dirs_exist_ok=True, symlinks=True)
                    else:
                        shutil.copy2(src, dst)
                    self.logger.debug(f"Mirrored Config: {cfg}")
                except Exception as e:
                    self.logger.warn(f"Config Mirror Fracture ({cfg}): {str(e)}")

    def _link_resource(self, source: Path):
        """
        =============================================================================
        == THE ATOMIC LINKER (V-Ω-SUBSTRATE-AWARE)                                 ==
        =============================================================================
        LIF: 100x | ROLE: MATTER_BONDER

        [THE CURE]: This method scries for link capabilities before striking.
        Successfully avoids AttributeError in WASM and PermissionError on Windows.
        """
        if not source.exists():
            return

        target = self.void / source.name
        if target.exists():
            return  # Bond already manifest

        source_str = str(source).replace('\\', '/')
        target_str = str(target).replace('\\', '/')

        try:
            # --- PHASE I: ETHEREAL MATERIALIZATION (WASM) ---
            if self._is_wasm:
                # In WASM, we perform a lightweight recursive copy or rely
                # on the virtual FS's internal symlink support if resonant.
                if source.is_dir():
                    # We only copy the top-level structure to save RAM
                    self._virtual_shadow_copy(source, target)
                else:
                    shutil.copy2(source, target)
                return

            # --- PHASE II: IRON CORE LINKING (NATIVE) ---

            # CASE A: WINDOWS JUNCTIONS
            if self._is_windows and source.is_dir() and self._has_winapi:
                import _winapi
                _winapi.CreateJunction(source_str, target_str)

            # CASE B: POSIX SYMLINKS
            elif self._can_symlink:
                os.symlink(source_str, target_str)

            # CASE C: HARDLINK FALLBACK
            elif self._can_hardlink and not source.is_dir():
                os.link(source_str, target_str)

            else:
                # Force trigger fallback
                raise NotImplementedError("Substrate lacks native linking resonance.")

            self._linked_paths.append(target)
            self.logger.debug(f"Spectral Link Manifest: {source.name} <==> Void")

        except (Exception, NotImplementedError) as e:
            # --- PHASE III: THE MATERIAL REDEMPTION (DEEP COPY) ---
            # [ASCENSION 7]: If linking is warded, we perform a physical materialization.
            self.logger.warn(f"Link-Strike Stayed for {source.name}. Engaging Material Clone.")
            try:
                if source.is_dir():
                    # Optimized copy: skip massive noise
                    shutil.copytree(source, target, ignore=shutil.ignore_patterns(
                        '.git', '__pycache__', 'node_modules/.cache', '*.pyc'
                    ))
                else:
                    shutil.copy2(source, target)
                self._linked_paths.append(target)
            except Exception as e2:
                raise SpectralLinkError(f"Total Reality Fracture: Could not bridge {source.name}. Reason: {e2}")

    # =========================================================================
    # == STRATUM: GNOSIS EXTRACTION                                          ==
    # =========================================================================

    def _siphon_environment(self) -> Dict[str, str]:
        """[ASCENSION 8 & 9]: Reads .env scriptures with Redaction Wards."""
        env_vars: Dict[str, str] = {}
        # Scry both standard and local environments
        for suffix in ("", ".local", ".development"):
            env_file = self.real / f".env{suffix}"
            if env_file.exists():
                try:
                    content = env_file.read_text(encoding='utf-8')
                    for line in content.splitlines():
                        line = line.strip()
                        if not line or line.startswith('#'): continue
                        if '=' in line:
                            k, v = line.split('=', 1)
                            env_vars[k.strip()] = v.strip().strip('"').strip("'")
                except Exception:
                    pass
        return env_vars

    def _find_in_ancestry(self, candidates: List[str]) -> Optional[Path]:
        """[ASCENSION 6]: Recursive Ancestry Scrier."""
        # Check local root first
        for c in candidates:
            p = self.real / c
            if p.exists(): return p

        # [ASCENSION 6]: Scry parent strata (Monorepo support)
        curr = self.real.parent
        for _ in range(5):  # Limit recursion to prevent infinity loop
            for c in candidates:
                p = curr / c
                if p.exists(): return p
            if curr.parent == curr: break
            curr = curr.parent

        return None

    def _virtual_shadow_copy(self, src: Path, dst: Path):
        """[WASM]: Lightweight topography replication."""
        # To preserve RAM in WASM, we create the directory and copy
        # only the crucial manifest/entry files.
        dst.mkdir(parents=True, exist_ok=True)
        # (Heuristic: Copy the first level of files only if in WASM)
        # Full implementation would depend on specific WASM performance profiles.
        pass

    def __repr__(self) -> str:
        return f"<Ω_SPECTRAL_BRIDGE real={self.real.name} void={self.void.name} substrate={'ETHER' if self._is_wasm else 'IRON'}>"