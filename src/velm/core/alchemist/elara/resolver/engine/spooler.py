# Path: core/alchemist/elara/resolver/engine/spooler.py
# ------------------------------------------------------

import os
import gc
import pickle
from pathlib import Path
from typing import List, Final

from ...contracts.atoms import GnosticToken
from ......logger import Scribe

Logger = Scribe("LaminarSpooler")


class LaminarStreamSpooler:
    """
    =============================================================================
    == THE LAMINAR STREAM SPOOLER (V-Ω-TOTALITY-VMAX)                          ==
    =============================================================================
    [ASCENSION 122 & 154]: Protects the God-Engine from Metabolic Fever by writing
    excess AST nodes to the physical disk when parsing monoliths. Adaptively scales
    thresholds based on Substrate DNA.
    """

    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self._is_wasm = os.environ.get("SCAFFOLD_ENV") == "WASM"
        self._spool_dir = Path(os.environ.get("SCAFFOLD_PROJECT_ROOT", ".")) / ".scaffold" / "ast_spool"
        self._spool_index = 0
        self._active = False

        # [ASCENSION 154]: Substrate-Aware Spooling Limits
        try:
            import psutil
            ram_gb = psutil.virtual_memory().total / (1024 ** 3)
            if ram_gb > 32:
                self.SPOOL_THRESHOLD = 150_000
            elif ram_gb > 8:
                self.SPOOL_THRESHOLD = 50_000
            else:
                self.SPOOL_THRESHOLD = 20_000
        except Exception:
            self.SPOOL_THRESHOLD = 50_000

    def check_and_spool(self, node_count: int, buffer: List[GnosticToken]) -> List[GnosticToken]:
        """Surgically spools the current token buffer to disk if threshold is breached."""
        if node_count < self.SPOOL_THRESHOLD or self._is_wasm:
            return buffer

        self._active = True
        self._spool_dir.mkdir(parents=True, exist_ok=True)
        spool_file = self._spool_dir / f"spool_{self.trace_id}_{self._spool_index}.pkl"

        try:
            with open(spool_file, 'wb') as f:
                pickle.dump(buffer, f)
            Logger.warn(
                f"🌊 [SPOOLER] Metabolic limit reached ({node_count} nodes). Spooled {len(buffer)} atoms to {spool_file.name}.")
            self._spool_index += 1

            # [ASCENSION 149]: Checkpointing memory flush
            del buffer
            gc.collect(2)
            return []
        except Exception as e:
            Logger.error(f"Spooling fracture: {e}. Attempting to hold matter in RAM.")
            return buffer

    def unspool(self, final_buffer: List[GnosticToken]) -> List[GnosticToken]:
        """Resurrects spooled matter and fuses it with the final buffer."""
        if not self._active:
            return final_buffer

        Logger.info(f"🌊 [SPOOLER] Resurrecting {self._spool_index} spooled fragments...")
        resurrected_matter = []

        for i in range(self._spool_index):
            spool_file = self._spool_dir / f"spool_{self.trace_id}_{i}.pkl"
            if spool_file.exists():
                try:
                    with open(spool_file, 'rb') as f:
                        resurrected_matter.extend(pickle.load(f))
                    spool_file.unlink()  # Cleanup Iron
                except Exception as e:
                    Logger.error(f"Failed to resurrect spool {i}: {e}")

        resurrected_matter.extend(final_buffer)
        return resurrected_matter