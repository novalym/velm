# === [scaffold/artisans/distill/core/oracle/engine.py] - SECTION 1 of 1: The Recursive Oracle ===
import time
from pathlib import Path
from typing import Optional, Dict, List, Any
from .....core.cortex.contracts import DistillationProfile
from ..contracts import DistillationResult
from .....logger import Scribe

# --- THE FACULTIES ---
from .contracts import OracleContext
from .perceiver import OraclePerceiver
from .diviner import OracleDiviner
from .propagator import OraclePropagator
from .adjudicator import OracleAdjudicator
from .scribe import OracleScribe
from .reviewer import SocraticReviewer  # <--- THE NEW FACULTY

# --- SURGICAL SLICER ---
try:
    from ..slicer.engine import CausalSlicer

    SLICER_AVAILABLE = True
except ImportError:
    SLICER_AVAILABLE = False

Logger = Scribe("DistillationOracle")


class DistillationOracle:
    """
    =================================================================================
    == THE DISTILLATION ORACLE (V-Ω-RECURSIVE-AGENT)                               ==
    =================================================================================
    """

    def __init__(
            self,
            distill_path: Path,
            profile: DistillationProfile,
            project_root: Path,
            verbose: bool = False,
            silent: bool = False,
            focus: Optional[List[str]] = None,
            intent: Optional[str] = None,  # New arg mapping
            problem: Optional[str] = None,
            interactive: bool = False,
            runtime_context: Optional[Dict] = None,
            regression_dossier: Any = None,
            perf_stats: Optional[Dict] = None
    ):
        self.root = project_root
        self.target_path = distill_path
        self.profile = profile
        self.verbose = verbose
        self.silent = silent
        self.initial_stats = perf_stats or {}

        # --- Gnostic Overrides ---
        if focus: self.profile.focus_keywords = focus
        if intent: self.profile.feature = intent  # Map intent to feature field in profile
        if problem: self.profile.problem_context = problem
        if interactive: self.profile.interactive_mode = interactive

        # --- The Faculty Forge ---
        self.perceiver = OraclePerceiver(self.root, silent)
        self.diviner = OracleDiviner(self.root, silent)
        self.propagator = OraclePropagator(self.root, silent)
        self.adjudicator = OracleAdjudicator(silent)
        self.scribe = OracleScribe(self.root, silent)

        # [FACULTY 6] The Socratic Reviewer
        self.reviewer = SocraticReviewer(self.root)

        # --- Surgical Slicer ---
        self.slicer: Optional[CausalSlicer] = None
        if SLICER_AVAILABLE and self.profile.strategy == 'surgical' and self.profile.focus_keywords:
            self.slicer = CausalSlicer(self.root, self.profile.focus_keywords)
            object.__setattr__(self.profile, 'slicer', self.slicer)

    def distill(self) -> str:
        return self.perceive_and_distill().content

    def perceive_and_distill(self) -> DistillationResult:
        """
        [THE RECURSIVE SYMPHONY]
        1. Perceive -> Divine -> Propagate -> Adjudicate (Pass 1).
        2. Socratic Review (Check for missing Gnosis).
        3. If Missing Found -> Propagate -> Adjudicate (Pass 2).
        4. Inscribe.
        """
        start_time = time.time()

        # 1. Forge the Gnostic Vessel
        context = OracleContext(
            root=self.root,
            profile=self.profile,
            stats=self.initial_stats
        )

        if not self.silent:
            Logger.info(f"The Oracle awakens. Strategy: [cyan]{self.profile.strategy}[/cyan]")

        # 2. Base Pipeline (Pass 1)
        self.perceiver.perceive(context)
        self.diviner.divine(context)
        self.propagator.propagate(context)
        self.adjudicator.adjudicate(context)

        # 3. The Socratic Loop (Pass 2)
        if self.profile.recursive_agent:
            # The Reviewer gazes upon the plan from Pass 1
            missing_scriptures = self.reviewer.review(context)

            if missing_scriptures:
                # Add new findings to the seeds
                context.seed_files.update(missing_scriptures)
                for f in missing_scriptures:
                    context.add_reason(f, "Socratic Refinement")

                if not self.silent:
                    Logger.info("Re-running Propagation and Adjudication with refined Gnosis...")

                # Re-run the expansion logic with the new seeds
                self.propagator.propagate(context)
                self.adjudicator.adjudicate(context)

        # 4. Inscription
        final_content = self.scribe.weave(context)

        total_duration = time.time() - start_time

        return DistillationResult(
            content=final_content,
            file_count=context.stats.get('files_included', 0),
            token_count=context.stats.get('token_count', 0),
            duration_seconds=total_duration,
            stats=context.stats
        )