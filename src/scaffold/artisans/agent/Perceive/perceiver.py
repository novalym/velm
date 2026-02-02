# artisans/agent/Perceive/perceiver.py
from pathlib import Path
from typing import Any
from ...distill.core.oracle import DistillationOracle
from ....core.cortex.contracts import DistillationProfile
from ..contracts import AgentState


class Perceiver:
    """
    The All-Seeing Eye of the Agent.
    Gathers context from the project to ground the Agent's hallucinations in reality.
    """

    def __init__(self, project_root: Path, engine: Any):
        self.root = project_root
        self.engine = engine

    def perceive(self, state: AgentState) -> str:
        """
        Distills the current state of the project into a blueprint string.
        """
        # We use a balanced profile to give the agent enough context without
        # overflowing its context window.
        profile = DistillationProfile(
            strategy='balanced',
            strip_comments=True,
            redact_secrets=True,
            # We focus on code and config, ignoring lockfiles and assets
            ignore=['*.lock', 'package-lock.json', 'yarn.lock', 'assets/', 'dist/', 'build/']
        )

        oracle = DistillationOracle(
            distill_path=self.root,
            profile=profile,
            project_root=self.root,
            silent=True
        )

        result = oracle.perceive_and_distill()
        return result.content