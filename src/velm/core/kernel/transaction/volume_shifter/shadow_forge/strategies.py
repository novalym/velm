# Path: src/velm/core/kernel/transaction/volume_shifter/shadow_forge/strategies.py
# --------------------------------------------------------------------------------

import os
import time
import shutil
import concurrent.futures
from pathlib import Path
from typing import List, Tuple

from ......logger import Scribe
from .contracts import ForgeMetrics
from .sieve import EntropySieve
from .replicator import AtomicReplicator


class KineticStrategies:
    """
    =============================================================================
    == THE KINETIC STRATEGIST (V-Ω-SUBSTRATE-AWARE-PATHFINDER)                 ==
    =============================================================================
    Houses the algorithms that orchestrate the traversal of the physical disk.
    """

    @staticmethod
    def iron_hurricane(src_root: Path, dst_root: Path, replicator: AtomicReplicator, metrics: ForgeMetrics,
                       logger: Scribe):
        """
        [PATH A: THE IRON CORE (NATIVE)]
        The Parallel Hurricane. Floods the I/O bus using a ThreadPool to achieve
        maximum thermodynamic throughput on multi-core native machines.
        """
        tasks: List[Tuple[Path, Path]] = []

        # Phase 1: Topological Walk (Main Thread avoids race conditions on Dir Creation)
        for dirpath, dirnames, filenames in os.walk(str(src_root)):
            # Ouroboros Guard: Do not descend into our own shadow destination
            if str(dst_root) in dirpath:
                dirnames[:] = []
                continue

            # Abyssal Sieve
            dirnames[:] = [d for d in dirnames if not EntropySieve.is_profane(d)]

            rel_path = Path(dirpath).relative_to(src_root)
            dst_dir = dst_root / rel_path

            try:
                dst_dir.mkdir(exist_ok=True)
                shutil.copystat(dirpath, dst_dir)
                metrics.record_dir()
            except OSError:
                pass

            for file in filenames:
                if EntropySieve.is_profane(file): continue
                tasks.append((Path(dirpath) / file, dst_dir / file))

        # Phase 2: The Swarm Strike
        max_workers = min(64, (os.cpu_count() or 1) * 4)
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="HoloForge") as executor:
            futures = [executor.submit(replicator.replicate, s, d) for s, d in tasks]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    logger.debug(f"File replication atom fractured: {e}")

    @staticmethod
    def ether_flow(src_root: Path, dst_root: Path, replicator: AtomicReplicator, metrics: ForgeMetrics, logger: Scribe):
        """
        [PATH B: THE ETHER PLANE (WASM)]
        The Sequential Flow. Specifically designed for single-threaded browser
        environments (Emscripten). Injects micro-yields to prevent UI starvation.
        """
        iteration_count = 0

        for dirpath, dirnames, filenames in os.walk(str(src_root)):
            if str(dst_root) in dirpath:
                dirnames[:] = []
                continue

            dirnames[:] = [d for d in dirnames if not EntropySieve.is_profane(d)]

            rel_path = Path(dirpath).relative_to(src_root)
            dst_dir = dst_root / rel_path

            try:
                dst_dir.mkdir(exist_ok=True)
                try:
                    shutil.copystat(dirpath, dst_dir)
                except Exception:
                    pass
                metrics.record_dir()
            except OSError:
                pass

            for file in filenames:
                if EntropySieve.is_profane(file): continue

                try:
                    replicator.replicate(Path(dirpath) / file, dst_dir / file)
                except Exception as e:
                    logger.debug(f"File replication atom fractured: {e}")

                # [ASCENSION: HYDRAULIC YIELDING]
                iteration_count += 1
                if iteration_count % 15 == 0:
                    time.sleep(0)  # Allow Browser Event Loop to breathe

