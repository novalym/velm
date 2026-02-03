# Path: scaffold/artisans/ci_optimize/engine.py
# ---------------------------------------------

import yaml
from pathlib import Path
from typing import Dict, Any, List

from ...logger import Scribe

Logger = Scribe("CIOptimizer")


class GnosticCIEngine:
    """
    =============================================================================
    == THE GENETIC ENGINEER (V-Ω-YAML-MUTATOR)                                 ==
    =============================================================================
    Parses CI workflows and mutates them to optimize for time and resources.
    """

    def __init__(self, workflow_path: Path):
        self.path = workflow_path
        self.content = {}
        if self.path.exists():
            try:
                self.content = yaml.safe_load(self.path.read_text(encoding='utf-8'))
            except Exception as e:
                Logger.warn(f"Could not parse workflow: {e}")

    def inject_matrix_sharding(self, job_name: str, step_name_keyword: str, shards: int = 4) -> bool:
        """
        [MUTATION: MITOSIS]
        Splits a monolithic job into parallel shards using a matrix strategy.
        """
        if not self.content: return False

        jobs = self.content.get("jobs", {})
        target_job = jobs.get(job_name)

        if not target_job:
            Logger.warn(f"Job '{job_name}' not found in workflow.")
            return False

        # 1. Check if already optimized
        if "strategy" in target_job and "matrix" in target_job["strategy"]:
            Logger.info(f"Job '{job_name}' is already evolving (Matrix detected).")
            return False

        Logger.info(f"Mutating job '{job_name}' to reproduce via Mitosis ({shards} shards)...")

        # 2. Inject Strategy
        target_job["strategy"] = {
            "matrix": {
                "shard": list(range(1, shards + 1)),
                "total_shards": [shards]
            },
            "fail-fast": False
        }

        # 3. Mutate Steps
        mutated = False
        if "steps" in target_job:
            for step in target_job["steps"]:
                # Look for the test runner step (e.g., "pytest", "npm test")
                run_cmd = step.get("run", "")
                if step_name_keyword in run_cmd or step_name_keyword in step.get("name", ""):
                    # Inject sharding logic into the command
                    # This assumes the tool supports sharding (like pytest-shard)
                    # For a generic V1, we append a placeholder or specific flags.

                    if "pytest" in run_cmd:
                        step[
                            "run"] = f"{run_cmd} --shard_id=${{{{ matrix.shard }}}} --num_shards=${{{{ matrix.total_shards }}}}"
                        mutated = True
                        Logger.success(f"Injected sharding logic into step: {step.get('name', 'run')}")
                    elif "npm" in run_cmd:
                        # Jest sharding
                        step["run"] = f"{run_cmd} --shard=${{{{ matrix.shard }}}}/${{{{ matrix.total_shards }}}}"
                        mutated = True
                        Logger.success(f"Injected sharding logic into step: {step.get('name', 'run')}")

        return mutated

    def inject_caching(self, job_name: str, cache_key: str, path_to_cache: str) -> bool:
        """
        [MUTATION: MNEMOSYNE]
        Injects a cache action to preserve state between incarnations.
        """
        jobs = self.content.get("jobs", {})
        target_job = jobs.get(job_name)
        if not target_job: return False

        steps = target_job.get("steps", [])

        # Check if cache already exists
        if any("actions/cache" in s.get("uses", "") for s in steps):
            return False

        Logger.info(f"Injecting Mnemosyne (Caching) into '{job_name}'...")

        # Create cache step
        cache_step = {
            "name": "Cache Dependencies",
            "uses": "actions/cache@v3",
            "with": {
                "path": path_to_cache,
                "key": f"${{{{ runner.os }}}}-{cache_key}-${{{{ hashFiles('**/lockfiles') }}}}",
                "restore-keys": f"${{{{ runner.os }}}}-{cache_key}-"
            }
        }

        # Insert after Checkout (usually index 1)
        steps.insert(1, cache_step)
        target_job["steps"] = steps
        return True

    def save(self):
        """Inscribes the mutated DNA back to disk."""
        # Note: PyYAML loses comments. For V1 this is acceptable,
        # but a warning is issued.
        with open(self.path, 'w', encoding='utf-8') as f:
            yaml.dump(self.content, f, sort_keys=False)