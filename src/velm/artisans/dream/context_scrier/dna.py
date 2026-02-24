# Path: artisans/dream/context_scrier/dna.py
# ------------------------------------------

import json
import toml
import re
from pathlib import Path
from typing import List, Dict, Any, Set

from .contracts import ProjectDNA
from ....logger import Scribe

Logger = Scribe("Scrier:Biologist")


class DNAAnalyzer:
    """
    =============================================================================
    == THE GENETIC SEQUENCER (V-Ω-DEPENDENCY-SCRYER)                           ==
    =============================================================================
    Reads the 'Soul Files' (configs) to determine the exact tech stack.
    """

    def analyze(self, root: Path) -> ProjectDNA:
        dna = ProjectDNA()

        # 1. NODE / JS SEQUENCE
        if (root / "package.json").exists():
            self._sequence_node(root, dna)
            return dna

        # 2. PYTHON SEQUENCE
        if (root / "pyproject.toml").exists() or (root / "requirements.txt").exists():
            self._sequence_python(root, dna)
            return dna

        # 3. RUST SEQUENCE
        if (root / "Cargo.toml").exists():
            self._sequence_rust(root, dna)
            return dna

        # 4. GO SEQUENCE
        if (root / "go.mod").exists():
            dna.language = "go"
            dna.build_system = "go mod"
            return dna

        return dna

    def _sequence_node(self, root: Path, dna: ProjectDNA):
        dna.language = "node"
        try:
            pkg = json.loads((root / "package.json").read_text())
            all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

            dna.dependencies = list(all_deps.keys())

            # Framework Detection
            if "next" in all_deps: dna.frameworks.append("nextjs")
            if "react" in all_deps: dna.frameworks.append("react")
            if "vue" in all_deps: dna.frameworks.append("vue")
            if "express" in all_deps: dna.frameworks.append("express")
            if "nest.js" in all_deps: dna.frameworks.append("nest")

            dna.build_system = "npm"
            if (root / "pnpm-lock.yaml").exists():
                dna.build_system = "pnpm"
            elif (root / "yarn.lock").exists():
                dna.build_system = "yarn"

        except Exception as e:
            Logger.warn(f"DNA sequencing fractured on package.json: {e}")

    def _sequence_python(self, root: Path, dna: ProjectDNA):
        dna.language = "python"
        deps = set()

        # Poetry
        if (root / "pyproject.toml").exists():
            try:
                data = toml.load(root / "pyproject.toml")
                tool = data.get("tool", {})
                if "poetry" in tool:
                    dna.build_system = "poetry"
                    deps.update(tool["poetry"].get("dependencies", {}).keys())
            except Exception:
                pass

        # Pip
        if (root / "requirements.txt").exists():
            if not dna.build_system: dna.build_system = "pip"
            try:
                content = (root / "requirements.txt").read_text()
                # Basic parsing
                found = re.findall(r'^([a-zA-Z0-9\-_]+)', content, re.MULTILINE)
                deps.update(found)
            except Exception:
                pass

        dna.dependencies = list(deps)

        if "fastapi" in deps: dna.frameworks.append("fastapi")
        if "django" in deps: dna.frameworks.append("django")
        if "flask" in deps: dna.frameworks.append("flask")
        if "sqlalchemy" in deps: dna.frameworks.append("sqlalchemy")

    def _sequence_rust(self, root: Path, dna: ProjectDNA):
        dna.language = "rust"
        dna.build_system = "cargo"
        try:
            content = (root / "Cargo.toml").read_text()
            # Simple heuristic regex for deps
            deps = re.findall(r'^([a-zA-Z0-9\-_]+)\s*=', content, re.MULTILINE)
            dna.dependencies = deps

            if "tokio" in deps: dna.frameworks.append("tokio")
            if "actix-web" in deps: dna.frameworks.append("actix")
            if "axum" in deps: dna.frameworks.append("axum")
        except:
            pass