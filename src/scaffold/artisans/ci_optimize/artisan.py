# Path: scaffold/artisans/ci_optimize/artisan.py
# ----------------------------------------------

import json
from pathlib import Path
from rich.panel import Panel

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import OptimizeCIRequest
from ...help_registry import register_artisan
from .engine import GnosticCIEngine


@register_artisan("ci-optimize")
class OptimizeCIArtisan(BaseArtisan[OptimizeCIRequest]):
    """
    =============================================================================
    == THE SELF-MUTATING CI (V-Ω-EVOLUTIONARY-ARCHITECT)                       ==
    =============================================================================
    Analyzes execution telemetry and rewrites workflow YAML to optimize speed.
    """

    def execute(self, request: OptimizeCIRequest) -> ScaffoldResult:
        workflow_path = (self.project_root / request.workflow_path).resolve()

        if not workflow_path.exists():
            return self.failure(f"Workflow scripture not found at {workflow_path}")

        self.logger.info(f"The Evolutionary Architect examines [cyan]{workflow_path.name}[/cyan]...")

        # 1. Ingest Telemetry (The Gnostic Feat)
        stats = {}
        if request.stats_file:
            try:
                stats = json.loads(Path(request.stats_file).read_text())
                self.logger.info(f"Ingested telemetry from {request.stats_file}.")
            except Exception as e:
                self.logger.warn(f"Could not read stats: {e}. Proceeding with Heuristics.")

        # 2. Heuristic Analysis (If no stats)
        # We look for heavy keywords in the workflow file itself if we have no stats.
        raw_content = workflow_path.read_text()

        engine = GnosticCIEngine(workflow_path)
        modifications = []

        # 3. Mutation: Parallelism (Aggressive Strategy)
        if request.strategy == "aggressive":
            # Heuristic: If we see 'pytest' or 'npm test', we assume it's the bottleneck
            # and verify if it's currently slow (mock logic for V1) or just apply it.

            # Find the job name. Usually 'build' or 'test'.
            # We scan keys.
            job_names = engine.content.get("jobs", {}).keys()

            for job in job_names:
                # We try to split 'test' steps
                if engine.inject_matrix_sharding(job, "pytest", shards=4):
                    modifications.append(f"Injected Matrix Strategy (4 shards) into '{job}' for pytest.")
                if engine.inject_matrix_sharding(job, "npm test", shards=4):
                    modifications.append(f"Injected Matrix Strategy (4 shards) into '{job}' for Jest.")

        # 4. Mutation: Caching (Conservative Strategy)
        # Always good to add caching if missing.
        for job in engine.content.get("jobs", {}).keys():
            # Check for python
            if "pip" in str(engine.content["jobs"][job]):
                if engine.inject_caching(job, "pip", "~/.cache/pip"):
                    modifications.append(f"Injected Pip Caching into '{job}'.")
            # Check for node
            if "npm" in str(engine.content["jobs"][job]):
                if engine.inject_caching(job, "npm", "~/.npm"):
                    modifications.append(f"Injected Npm Caching into '{job}'.")

        if not modifications:
            return self.success("The pipeline is already optimal (or no patterns matched).")

        # 5. The Rite of Evolution (Write to Disk)
        self.console.print(Panel(
            "\n".join(f"- {m}" for m in modifications),
            title="[bold green]Prophecy of Evolution[/bold green]",
            border_style="green"
        ))

        # We backup first
        backup_path = workflow_path.with_suffix(".yml.bak")
        import shutil
        shutil.copy2(workflow_path, backup_path)
        self.logger.verbose(f"Ancient DNA preserved at {backup_path.name}")

        engine.save()

        return self.success(
            f"The CI Pipeline has mutated. {len(modifications)} adaptations applied.",
            artifacts=[Artifact(path=workflow_path, type="file", action="modified")]
        )