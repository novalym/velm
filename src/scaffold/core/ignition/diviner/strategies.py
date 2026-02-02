# Path: scaffold/core/ignition/diviner/strategies.py
# --------------------------------------------------
# LIF: INFINITY // AUTH_CODE: @)(!@(!()@ // Ω_STRATEGIES_SINGULARITY_V122_FINAL
# SYSTEM: IDEABOX QUANTUM // MODULE: IGNITION.DIVINER
# -------------------------------------------------------------------------------------

import os
import sys
import shutil
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple

# --- THE DIVINE SUMMONS: INTERNAL GNOSTIC CLUSTER ---
from ..contracts import (
    ExecutionPlan,
    IgnitionAura,
    BiologicalSupport,
    NetworkPhysics,
    Protocol,
    HardwareConstraint
)
from ..sentinel.priest import ToolchainSentinel
from ....logger import Scribe

Logger = Scribe("StrategyArchitect")


class IgnitionStrategy(ABC):
    """
    =================================================================================
    == THE ANCESTRAL MIND OF ACTION (V-Ω-CONTRACT)                                 ==
    =================================================================================
    The base contract for all Reality Transmutations.
    """

    def __init__(self, root: Path):
        self.root = root.resolve()

    @abstractmethod
    def forge(self, port: int, custom_command: Optional[str] = None) -> ExecutionPlan:
        """Transmutes a perceived Aura into a kinetic ExecutionPlan."""
        pass

    def _resolve_binary(self, bin_name: str) -> str:
        """[ASCENSION 1]: ISOMORPHIC BINARY RESOLVER."""
        # 1. Check local project shims first (Project-Relative Authority)
        for sub in ["node_modules/.bin", ".venv/bin", "venv/bin", ".venv/Scripts"]:
            ext = ".cmd" if os.name == 'nt' else ""
            local_bin = self.root / sub / f"{bin_name}{ext}"
            if local_bin.exists():
                return str(local_bin.resolve())

        # 2. Check standard system PATH
        resolved = shutil.which(bin_name)
        if resolved:
            return resolved

        # 3. Windows Fallback for .cmd/.bat/.exe
        if os.name == 'nt':
            resolved = shutil.which(f"{bin_name}.cmd") or shutil.which(f"{bin_name}.exe")
            if resolved: return resolved

        return bin_name

    def _graft_path(self, base_env: Dict[str, str], venv_path: Optional[Path] = None) -> Dict[str, str]:
        """[ASCENSION 2]: CONTEXTUAL PATH GRAFTING."""
        env = os.environ.copy()
        env.update(base_env)

        new_paths = []

        # Local Node Binaries (Priority 1)
        node_bin = self.root / "node_modules" / ".bin"
        if node_bin.exists(): new_paths.append(str(node_bin))

        # Virtual Environment Binaries (Priority 2)
        if venv_path:
            bin_dir = venv_path / ("Scripts" if os.name == 'nt' else "bin")
            if bin_dir.exists(): new_paths.append(str(bin_dir))

        # Merge with existing system PATH
        env["PATH"] = os.pathsep.join(new_paths) + os.pathsep + env.get("PATH", "")
        return env


class NodeStrategy(IgnitionStrategy):
    """
    =============================================================================
    == THE NODE STRATEGY (V-Ω-JS-KINETICS)                                     ==
    =============================================================================
    Governs the manifestation of Vite, Next, Nuxt, and Astro realities.
    """

    def forge(self, port: int, custom_command: Optional[str] = None) -> ExecutionPlan:
        # 1. DIVINE PACKAGE MANAGER
        pm = ToolchainSentinel.find_best_node_artisan(self.root)
        binary = self._resolve_binary(pm)

        # 2. SCRY MANIFEST FOR AURA DETAILS
        aura = IgnitionAura.GENERIC
        scripts = {}
        try:
            with open(self.root / "package.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                scripts = data.get("scripts", {})
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
                if "next" in deps:
                    aura = IgnitionAura.NEXT
                elif "vite" in deps:
                    aura = IgnitionAura.VITE
                elif "astro" in deps:
                    aura = IgnitionAura.ASTRO
        except:
            pass

        # 3. SELECT COMMAND RITE
        # [ASCENSION 12]: Override Gate
        if custom_command:
            command = custom_command.replace("{{port}}", str(port)).split(" ")
        else:
            script_key = "dev" if "dev" in scripts else "start"
            command = [binary, "run", script_key]

            # [ASCENSION 5]: AURA-AWARE ARGUMENT SPLICING
            if aura in [IgnitionAura.VITE, IgnitionAura.ASTRO]:
                # Vite/Astro require '--' to pass flags to the underlying binary
                command.extend(["--", "--port", str(port), "--host", "0.0.0.0"])
            elif aura == IgnitionAura.NEXT:
                # Next.js uses -p directly
                command.extend(["--", "-p", str(port)])

        return ExecutionPlan(
            command=command,
            cwd=self.root,
            aura=aura,
            env=self._graft_path({"NODE_ENV": "development", "PORT": str(port)}),
            network=NetworkPhysics(port=port, protocol=Protocol.HTTP),
            confidence=0.98,
            reasoning_trace=[
                f"Binary Resolution: {pm} -> {binary}",
                f"Script Triage: Found '{command[2]}' in package.json",
                f"Port Injection: Assigned {port} via {aura.value} dialect"
            ]
        )


class PythonStrategy(IgnitionStrategy):
    """
    =============================================================================
    == THE PYTHON STRATEGY (V-Ω-SERPENT-KINETICS)                              ==
    =============================================================================
    Governs the manifestation of FastAPI, Flask, and Streamlit realities.
    """

    def forge(self, port: int, custom_command: Optional[str] = None) -> ExecutionPlan:
        # 1. LOCATE BIOLOGICAL ANCHOR (VENV)
        venv_path = next((self.root / d for d in [".venv", "venv", "env"] if (self.root / d).exists()), None)
        python_bin = self._resolve_binary("python")

        if venv_path:
            # [ASCENSION 1]: Isomorphic Venv Mapping
            if os.name == 'nt':
                python_bin = str((venv_path / "Scripts" / "python.exe").resolve())
            else:
                python_bin = str((venv_path / "bin" / "python").resolve())

        # 2. DIVINE FRAMEWORK & ENTRY POINT
        aura = IgnitionAura.PYTHON_SCRIPT
        entry = "main.py"

        # Check entries for known framework signatures
        for cand in ["main.py", "app.py", "api.py", "wsgi.py", "asgi.py"]:
            p = self.root / cand
            if p.exists():
                entry = cand
                content = p.read_text(encoding="utf-8", errors="ignore")
                if "FastAPI" in content or "from fastapi" in content:
                    aura = IgnitionAura.FASTAPI
                    break
                if "Flask" in content:
                    aura = IgnitionAura.FLASK
                    break

        # 3. FORGE COMMAND
        if custom_command:
            command = custom_command.replace("{{port}}", str(port)).split(" ")
        elif aura == IgnitionAura.FASTAPI:
            uvicorn = self._resolve_binary("uvicorn")
            command = [uvicorn, f"{Path(entry).stem}:app", "--reload", "--port", str(port), "--host", "0.0.0.0"]
        elif aura == IgnitionAura.FLASK:
            command = [python_bin, "-m", "flask", "run", "--port", str(port), "--host", "0.0.0.0"]
        elif (self.root / "manage.py").exists():
            aura = IgnitionAura.DJANGO
            command = [python_bin, "manage.py", "runserver", str(port)]
        else:
            command = [python_bin, entry]

        return ExecutionPlan(
            command=command,
            cwd=self.root,
            aura=aura,
            env=self._graft_path({"PYTHONUNBUFFERED": "1", "PORT": str(port)}, venv_path),
            network=NetworkPhysics(port=port),
            confidence=0.95,
            reasoning_trace=[
                f"Interpreter: {Path(python_bin).parent.name}/{Path(python_bin).name}",
                f"Framework Scry: {aura.value} detected via {entry}",
                f"Environment: UTF-8 & Unbuffered enabled"
            ]
        )


class StrategyArchitect:
    """
    =================================================================================
    == THE STRATEGY ARCHITECT (V-Ω-TOTALITY-FACTORY)                               ==
    =================================================================================
    The High Priest that chooses the Hand for the Mind.
    """

    @staticmethod
    def forge(aura: IgnitionAura, root: Path, port: int, custom_command: Optional[str] = None) -> ExecutionPlan:
        """The Master Factory for generating deterministic Execution Plans."""

        Logger.verbose(f"Constructing Strategic Command for Aura: [bold]{aura}[/bold]")

        # 1. NODE ECOSYSTEM
        if aura in [IgnitionAura.VITE, IgnitionAura.NEXT, IgnitionAura.ASTRO, IgnitionAura.NUXT, IgnitionAura.REMIX]:
            return NodeStrategy(root).forge(port, custom_command)

        # 2. PYTHON ECOSYSTEM
        if aura in [IgnitionAura.FASTAPI, IgnitionAura.FLASK, IgnitionAura.DJANGO, IgnitionAura.PYTHON_SCRIPT]:
            return PythonStrategy(root).forge(port, custom_command)

        # 3. RUST / CARGO
        if aura == IgnitionAura.CARGO:
            python_bin = sys.executable
            # We assume a standard 'cargo run' but allow for port injection if using Axum/Rocket
            return ExecutionPlan(
                command=["cargo", "run"],
                cwd=root,
                aura=aura,
                env={"PORT": str(port), "RUST_BACKTRACE": "1"},
                network=NetworkPhysics(port=port),
                confidence=0.9
            )

        # 4. ULTIMATE FALLBACK: STATIC ORACLE
        # [ASCENSION 7]: Harmonic Fallback
        python_bin = sys.executable
        return ExecutionPlan(
            command=[python_bin, "-m", "http.server", str(port)],
            cwd=root,
            aura=IgnitionAura.STATIC,
            env={"PORT": str(port)},
            network=NetworkPhysics(port=port),
            confidence=0.4,
            reasoning_trace=["Manifests silent. Defaulting to Ocular Reality (Static Server)."]
        )