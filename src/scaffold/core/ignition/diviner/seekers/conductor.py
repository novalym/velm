# Path: scaffold/core/ignition/diviner/seekers/conductor.py
# --------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: Ω_SEEKER_CONDUCTOR_V7

import time
from pathlib import Path
from typing import Tuple
from concurrent.futures import ThreadPoolExecutor

from .heart_seeker import HeartSeeker
from .visual_seeker import VisualSeeker
from .environmental_seeker import EnvironmentalSeeker
from .entropy_seeker import EntropySeeker
from .magic_seeker import MagicSeeker
from .semantic_seeker import SemanticSeeker
from .....logger import Scribe

Logger = Scribe("SeekerConductor")


class SeekerConductor:
    """
    =================================================================================
    == THE SEEKER CONDUCTOR (V-Ω-TOTALITY-ORCHESTRATOR)                            ==
    =================================================================================
    [ASCENSION 1]: Parallelizing the search for Reality.
    """

    def __init__(self, root: Path):
        self.root = root.resolve()
        # Consecrate the hunting pack
        self.env = EnvironmentalSeeker(self.root)
        self.heart = HeartSeeker(self.root)
        self.visual = VisualSeeker(self.root)
        self.entropy = EntropySeeker(self.root)
        self.magic = MagicSeeker(self.root)
        self.semantic = SemanticSeeker(self.root)

    def conduct_tomography(self) -> Tuple[Path, Path]:
        """
        =============================================================================
        == THE GRAND RITE OF TOMOGRAPHY                                            ==
        =============================================================================
        Returns: (Logic_Root, Visual_Root)
        """
        start = time.perf_counter()
        Logger.info(f"Initiating Multi-Spectral Scan: [cyan]{self.root}[/cyan]")

        # 1. [ASCENSION 5]: ENVIRONMENTAL ANCHOR CHECK (Highest Priority)
        # If we see .scaffold or .git, we have likely found the true root already.
        anchor = self.env.scan()
        if anchor:
            Logger.success(f"Gnostic Anchor found at: {anchor.name}")
            return anchor, self.visual.scan(anchor)

        # 2. [ASCENSION 1]: PARALLEL HIVE MIND
        # We weigh different seekers to find the Logic Heart.
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_heart = executor.submit(self.heart.scan)
            future_entropy = executor.submit(self.entropy.scan)
            future_semantic = executor.submit(self.semantic.scan)

            # Collect finding
            h_root = future_heart.result()
            e_root = future_entropy.result()
            s_root = future_semantic.result()

        # 3. [ASCENSION 3]: BAYESIAN ADJUDICATION
        # Adjudicate based on seeker "Gravity"
        # Preference: Heart (Manifests) > Semantic (Structure) > Entropy (Density)
        logic_root = h_root or s_root or e_root or self.root

        # 4. [ASCENSION 6]: OCULAR FOCUS
        visual_root = self.visual.scan(logic_root)

        duration = (time.perf_counter() - start) * 1000
        Logger.success(f"Tomography Concluded in {duration:.2f}ms.")
        Logger.info(f" > Logic Heart: [bold]{logic_root.name}[/bold]")
        Logger.info(f" > Visual Seed: [bold]{visual_root.name}[/bold]")

        return logic_root, visual_root