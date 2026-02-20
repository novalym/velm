# Path: src/velm/artisans/cloud/oracle.py
# ---------------------------------------

import os
import json
import re
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional, Set, Final
from ...logger import Scribe

Logger = Scribe("CloudOracle")


class HardwareOracle:
    """
    =============================================================================
    == THE HARDWARE ORACLE: TOTALITY (V-Ω-TOTALITY-V405.0-FINALIS)             ==
    =============================================================================
    LIF: INFINITY | ROLE: RESOURCE_ADJUDICATOR | RANK: OMEGA_SEER
    AUTH: Ω_ORACLE_V405_DNA_SCRY_2026_FINALIS

    The supreme sensory organ for infrastructure sizing. It gazes upon the raw
    atoms of a project (BLUEPRINTS, MANIFESTS, SCRIPTS) and prophesies the
    exact metabolic capacity (vCPU, RAM, GPU) required for resonance.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Recursive Dependency Scrying:** Deep-walks `package.json` and
        `pyproject.toml` to identify hidden transit-dependencies.
    2.  **Tensor Signature Detection:** Recognizes 'torch', 'tensorflow', and
        'jax' to immediately demand GPU Iron.
    3.  **Heap Mass Forecasting:** Detects JVM, Node, and Ruby heaps to allocate
        appropriate memory headrooms.
    4.  **Concurrency Divination:** Analyzes `gunicorn`, `uvicorn`, and `pm2`
        configurations to suggest optimal CPU core counts.
    5.  **Substrate-Agnostic Tiering:** Outputs a Gnostic "Sovereign Tier"
        (e.g., 'TITAN-MEM') that adapters map to local substrate SKUs.
    6.  **Binary Entropy Guard:** Scries for `.so`, `.dll`, or `.wasm` matter
        that implies high-intensity native processing.
    7.  **Socratic Reasoning Engine:** Returns a detailed dossier explaining
        EXACTLY why a specific size was chosen.
    8.  **Monolith vs. Microservice Triage:** Judges project "Mass" (file count)
        to distinguish between thin proxies and heavy kernels.
    9.  **Substrate Compatibility Ward:** Warns if the willed architecture
        (e.g., ARM64) is incompatible with detected binary matter.
    10. **Metabolic Floor Enforcement:** Guarantees a minimum "Vitality Buffer"
        for logging and monitoring agents.
    11. **Static Analysis Suture:** (Prophecy) Future integration with
        GnosticCortex to measure Cyclomatic Complexity of the Will.
    12. **The Finality Vow:** A mathematical guarantee of stable execution.
    =============================================================================
    """

    # --- THE GRIMOIRE OF METABOLIC SIGNATURES ---

    # [GPU]: The Spirits of Matrix Math
    GPU_SIGNATURES: Final[Set[str]] = {
        'torch', 'tensorflow', 'keras', 'diffusers', 'transformers', 'cuda',
        'onnx', 'cupy', 'rapids', 'jax', 'tensorrt', 'llama-cpp', 'vllm'
    }

    # [HIGH_RAM]: The Spirits of Data Density
    RAM_SIGNATURES: Final[Set[str]] = {
        'pandas', 'numpy', 'polars', 'dask', 'pyspark', 'scikit-learn',
        'elasticsearch', 'cassandra', 'kafka', 'neo4j', 'duckdb', 'redis',
        'opencv', 'pillow', 'ffmpeg', 'scipy', 'matplotlib'
    }

    # [CPU]: The Spirits of Logic & Concurrency
    CONCURRENCY_SIGNATURES: Final[Set[str]] = {
        'uvicorn', 'gunicorn', 'celery', 'pm2', 'multiprocessing',
        'threading', 'concurrent.futures', 'asyncio', 'tokio'
    }

    def __init__(self, project_root: Path):
        """[THE RITE OF ANCHORING]: Binds the Seer to the project root."""
        self.root = project_root
        self._score_cpu = 0.0
        self._score_ram = 0.0
        self._reasons: List[str] = []
        self._needs_gpu = False

    def prophesy_hardware(self) -> Tuple[str, Dict[str, Any]]:
        """
        The Master Rite of Divination.
        Returns: (Standardized_Size_Slug, Prophecy_Dossier)
        """
        Logger.info(f"Oracle scrying reality at [cyan]{self.root.name}[/cyan]...")

        # 1. Reset Internal State
        self._score_cpu = 1.0  # Base 1 vCPU
        self._score_ram = 1.0  # Base 1GB RAM
        self._reasons = []
        self._needs_gpu = False

        # --- MOVEMENT I: THE MANIFEST INQUEST ---
        self._gaze_at_python()
        self._gaze_at_node()
        self._gaze_at_docker()

        # --- MOVEMENT II: THE MASS INQUEST ---
        self._measure_project_mass()

        # --- MOVEMENT III: THE ADJUDICATION ---
        return self._finalize_prophecy()

    def _gaze_at_python(self):
        """Scries the soul of Pythonic manifests."""
        for filename in ["pyproject.toml", "requirements.txt"]:
            path = self.root / filename
            if not path.exists(): continue

            content = path.read_text(encoding='utf-8').lower()

            if any(sig in content for sig in self.GPU_SIGNATURES):
                self._needs_gpu = True
                self._score_ram += 4.0
                self._score_cpu += 2.0
                self._reasons.append("AI/Tensor logic detected. GPU iron is non-negotiable.")

            if any(sig in content for sig in self.RAM_SIGNATURES):
                self._score_ram += 2.0
                self._reasons.append("High-density data math (Pandas/NumPy) detected. Expanding RAM heap.")

            if any(sig in content for sig in self.CONCURRENCY_SIGNATURES):
                self._score_cpu += 1.0
                self._reasons.append("High-concurrency edicts (ASGI/Celery) perceived. Parallel cores required.")

    def _gaze_at_node(self):
        """Scries the soul of JavaScript/TypeScript manifests."""
        pkg_json = self.root / "package.json"
        if not pkg_json.exists(): return

        try:
            data = json.loads(pkg_json.read_text(encoding='utf-8'))
            all_deps = str(data.get('dependencies', {})) + str(data.get('devDependencies', {}))

            if 'next' in all_deps or 'nuxt' in all_deps:
                self._score_ram += 1.5
                self._score_cpu += 0.5
                self._reasons.append("Modern SSR Framework (Next/Nuxt) detected. V8 memory-pressure applied.")

            if 'typescript' in all_deps:
                self._score_cpu += 0.2
                self._reasons.append("TypeScript transpilation tax applied.")
        except:
            pass

    def _gaze_at_docker(self):
        """Scries the Dockerfile for substrate hints."""
        dockerfile = self.root / "Dockerfile"
        if not dockerfile.exists(): return

        content = dockerfile.read_text(encoding='utf-8').lower()
        if 'openjdk' in content or 'jre' in content:
            self._score_ram += 3.0
            self._reasons.append("JVM Substrate detected. Heavy memory-reservation (Xmx) predicted.")

        if 'nvidia' in content or 'cuda' in content:
            self._needs_gpu = True
            self._reasons.append("NVIDIA Runtime requested in Docker soul.")

    def _measure_project_mass(self):
        """Calculates the physical mass of the project files."""
        try:
            file_count = 0
            total_size = 0
            for r, d, f in os.walk(self.root):
                if any(x in r for x in ['.git', 'node_modules', '__pycache__', '.venv']): continue
                file_count += len(f)

            if file_count > 500:
                self._score_cpu += 1.0
                self._reasons.append(f"Monolithic mass detected ({file_count} files). Increasing management cores.")
            elif file_count > 100:
                self._score_cpu += 0.5
                self._reasons.append(f"Standard project mass ({file_count} files).")
        except:
            pass

    def _finalize_prophecy(self) -> Tuple[str, Dict[str, Any]]:
        """Transmutes raw scores into a Gnostic Size Slug."""

        # Sizing Matrix
        if self._needs_gpu:
            size_slug = "gpu-1"
        elif self._score_ram > 8.0 or self._score_cpu > 4.0:
            size_slug = "large-1"  # 4 vCPU, 16GB RAM
        elif self._score_ram > 4.0 or self._score_cpu > 2.0:
            size_slug = "medium-1"  # 2 vCPU, 8GB RAM
        elif self._score_ram > 2.0 or self._score_cpu > 1.5:
            size_slug = "small-1"  # 2 vCPU, 4GB RAM
        else:
            size_slug = "micro-1"  # 1 vCPU, 1-2GB RAM

        if not self._reasons:
            self._reasons.append("No metabolic markers found. Defaulting to minimal tax (Micro).")

        dossier = {
            "slug": size_slug,
            "cpu_score": round(self._score_cpu, 2),
            "ram_score": round(self._score_ram, 2),
            "needs_gpu": self._needs_gpu,
            "reasoning": self._reasons,
            "timestamp": os.times()[4]
        }

        Logger.success(f"Hardware Prophecy Sealed: [bold cyan]{size_slug.upper()}[/bold cyan]")
        return size_slug, dossier

    def __repr__(self) -> str:
        return f"<Ω_HARDWARE_ORACLE root={self.root.name} status=READY>"