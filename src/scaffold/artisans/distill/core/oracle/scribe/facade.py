# === [scaffold/artisans/distill/core/oracle/scribe/facade.py] - SECTION 1 of 1: The Conductor ===
import time
import hashlib
import json
from pathlib import Path
from typing import Iterator

from ......logger import Scribe
from ..contracts import OracleContext

# --- THE DIVINE SUMMONS OF THE HERALDS ---
from .header import HeaderHerald
from .topology import TopologyHerald
from .manifest import ManifestHerald
from .content import ContentHerald
from .critique import CritiqueHerald  # <--- THE NEW SUMMONS

Logger = Scribe("OracleScribe")


class OracleScribe:
    """
    =================================================================================
    == THE SCRIBE OF REVELATION (V-Ω-STREAMING-MODULAR-ULTIMA)                     ==
    =================================================================================
    LIF: ∞ (THE ENDLESS SCROLL)

    The High Conductor. It orchestrates the specialized Heralds to produce a
    valid, executable, and hyper-informative .scaffold scripture.
    """

    def __init__(self, root: Path, silent: bool = False):
        self.root = root
        self.silent = silent
        self.hasher = hashlib.sha256()

    def weave(self, context: OracleContext) -> str:
        """The Grand Rite of Inscription."""
        t0 = time.time()
        output_buffer = []

        for chunk in self.weave_stream(context):
            self.hasher.update(chunk.encode('utf-8'))
            output_buffer.append(chunk)

        # Append the Safety Seal
        digest = self.hasher.hexdigest()
        seal = f"\n# @gnostic_seal: {digest}\n"
        output_buffer.append(seal)

        duration = (time.time() - t0) * 1000
        context.record_stat('weaving_ms', duration)

        return "".join(output_buffer)

    def weave_stream(self, context: OracleContext) -> Iterator[str]:
        """The Generator of Truth."""

        # 1. The Intelligent Header (Tech Stack, Debt, Stats, User Context)
        yield from HeaderHerald(self.root).proclaim(context)

        # 2. The Topology Herald (Logic Flow Graph)
        if context.profile.lfg:
            yield from TopologyHerald(self.root).proclaim(context)

        # 3. The Manifest Herald (File Map & Regression)
        yield from ManifestHerald(self.root).proclaim(context)

        # 4. The Content Herald (The Sacred Scriptures)
        yield from ContentHerald(self.root).proclaim(context)

        # 5. The Critique Herald (Architectural Heresies)
        # We append this at the end so the AI reads the code first, then the critique.
        yield from CritiqueHerald(self.root).proclaim(context)

        # 6. The Machine Epilogue
        yield self._forge_epilogue(context)

    def _forge_epilogue(self, context: OracleContext) -> str:
        meta = {
            "files": context.stats.get('files_included', 0),
            "tokens": context.stats.get('token_count', 0),
            "duration_ms": context.stats.get('weaving_ms', 0),
            "strategy": context.profile.strategy
        }
        return f"\n# <!-- GNOSTIC_TELEMETRY: {json.dumps(meta)} -->\n"

