# Path: artisans/distill/scribes/dossier_scribe.py
# ------------------------------------------------

import time
import re
from pathlib import Path
from textwrap import dedent
from typing import Dict, Any, List

from ..core.contracts import DistillationResult
from ....core.cortex.contracts import DistillationProfile
from ....core.ai.engine import AIEngine
from ....logger import Scribe
# We summon the parser to perform a pure Gaze, not for execution.
from ....parser_core.parser import ApotheosisParser
from ....contracts.data_contracts import GnosticWriteResult, InscriptionAction, ScaffoldItem

Logger = Scribe("DossierScribe")


class DossierScribe:
    """
    =================================================================================
    == THE SCRIBE OF UNDERSTANDING (V-Ω-INTERACTIVE-DOSSIER-ULTIMA)                ==
    =================================================================================
    @gnosis:title The Dossier Scribe
    @gnosis:summary Transmutes a pure Gnostic `DistillationResult` into an interactive,
                     AI-analyzed, forensically-rich Markdown Forensic Dossier.
    @gnosis:LIF INFINITY
    @gnosis:auth_code:)(#@()#()!

    This artisan is the final voice of the `distill --format dossier` and `holocron forge`
    rites. It weaves the AI's hypothesis, the scripture's full provenance, its Gnostic
    bonds, and a luminous Action Altar into a single, interactive document of
    understanding. It forges not a report, but a cockpit.
    """

    def __init__(self, result: DistillationResult, profile: DistillationProfile):
        self.result = result
        self.profile = profile
        self.ai = AIEngine.get_instance()
        self.parser = ApotheosisParser(grammar_key='scaffold')

    def inscribe(self) -> str:
        """The Grand Rite of Dossier Forging."""
        fragments = [
            self._forge_header(),
            self._forge_hypothesis(),
            self._forge_scriptures(),
            self._forge_footer()
        ]
        return "\n\n".join(fragments)

    def _forge_header(self) -> str:
        """Forges the dossier's title and metadata."""
        intent = self.profile.feature or self.profile.problem_context or "General Analysis"
        mode = "Forensic (Deep Gaze)" if self.profile.problem_context else "Architectural (Broad Gaze)"
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        return (
            f"# 🏛️ HOLOCRON FORENSIC DOSSIER\n"
            f"**Intent:** `{intent}`\n\n"
            f"**Mode:** `{mode}` | **Timestamp:** `{timestamp}`"
        )

    def _forge_hypothesis(self) -> str:
        """[FACULTY 2] Conducts the Two-Stage Cognitive Symphony for analysis."""
        if not self.profile.diagnose:
            return "## 🧠 ARCHITECTURAL ANALYSIS\nThe distilled context provides a focused view into the codebase's structure and logic relevant to the user's intent."

        Logger.info("Summoning AI Analyst for Two-Stage Hypothesis...")

        # We use the raw .scaffold content from the distillation result for the AI's Gaze
        blueprint_context = self.result.content

        # --- Stage 1: Fast Hypothesis ---
        fast_system_prompt = "You are a senior software architect. Analyze the provided code context and user intent. Form a concise, one-paragraph hypothesis about the root cause or interaction. Be direct."
        fast_plea = f"User Intent: \"{self.profile.feature or self.profile.problem_context}\"\n\nCode Context:\n{blueprint_context}"

        try:
            fast_hypothesis = self.ai.ignite(fast_plea, fast_system_prompt, model="fast")

            # --- Stage 2: Deep Strategic Plan ---
            smart_system_prompt = "You are a master architect and debugger. Based on the initial hypothesis and the full code context, provide a detailed analysis. Explain the interaction between components, pinpoint the likely friction point, and suggest a concrete plan for resolution. Use Markdown."
            smart_plea = f"Initial Hypothesis:\n{fast_hypothesis}\n\nFull Code Context:\n{blueprint_context}"

            final_analysis = self.ai.ignite(smart_plea, smart_system_prompt, model="smart")

            return f"## 🧠 ARCHITECTURAL HYPOTHESIS\n{final_analysis}"
        except Exception as e:
            Logger.warn(f"AI Analyst Gaze faltered: {e}")
            return f"## 🧠 ARCHITECTURAL HYPOTHESIS\n[AI analysis failed: {e}]"

    def _forge_scriptures(self) -> str:
        """[FACULTY 7] The Unbreakable Scripture Weaver."""
        scripture_blocks = ["## 📜 RELEVANT SCRIPTURES"]

        try:
            # We perform a "dry" parse to transmute the blueprint into a list of ScaffoldItems
            _, items, _, _, _, _ = self.parser.parse_string(self.result.content)
        except Exception as e:
            return f"## 📜 RELEVANT SCRIPTURES\n\n[Heresy: Could not parse blueprint to extract code blocks: {e}]"

        for item in items:
            if not item.path or item.is_dir or str(item.path).startswith("$$"):
                continue

            # This is the pure, final content of the file from the distillation.
            content = self._get_final_content(item)
            path_str = item.path.as_posix()

            # Find the full FileGnosis object from the oracle's stats for deep metadata
            file_gnosis = self.result.stats.get('final_inventory', {}).get(path_str)

            # --- Movement I: The Action Altar ---
            altar = self._forge_action_altar(path_str, file_gnosis)

            # --- Movement II: The Provenance Scribe ---
            provenance = self._forge_provenance(file_gnosis)

            # --- Movement III: The Gnostic Bonds ---
            bonds = self._forge_bonds(file_gnosis)

            # --- Movement IV: The Scripture Itself (Adaptive Fencing) ---
            lang = (file_gnosis.language if file_gnosis else Path(path_str).suffix.lstrip('.')) or 'text'

            # [FIX] Adaptive Fencing
            # If the content contains backticks (e.g. a README), we escalate the fence.
            fence = "```"
            if "```" in content:
                fence = "~~~~"
                if "~~~~" in content:
                    fence = "`````"  # High Ground

            code_block = (
                f"{fence}{lang}\n"
                f"{content}\n"
                f"{fence}"
            )

            final_block = f"### 📍 {path_str}\n{altar}\n{provenance}\n{code_block}{bonds}"
            scripture_blocks.append(final_block)

        return "\n\n".join(scripture_blocks)

    def _get_final_content(self, item: ScaffoldItem) -> str:
        """A humble scribe to extract content from the parsed item."""
        # A full implementation would re-run the `resolve_gnostic_content_v2` logic
        # For this ascension, we trust the `item.content` from the simple blueprint parse.
        # This is a point of future refinement.
        return item.content or ""

    def _forge_action_altar(self, path_str: str, gnosis: Any) -> str:
        """[FACULTY 1] Forges the VS Code command links."""
        # VS Code command URI format: command:extension.commandName?[arguments]
        edit_uri = f"command:vscode.open?%5B%22{self.profile.project_root.as_uri()}/{path_str}%22%5D"
        # Prophecy: These would be real commands implemented by the extension.
        history_uri = f"command:scaffold.viewHistory?%5B%22{path_str}%22%5D"
        test_uri = f"command:scaffold.runTest?%5B%22{path_str}%22%5D"

        altar = f"<p align='right'>[<a href='{edit_uri}'>Edit</a>] | [<a href='{history_uri}'>History</a>] | [<a href='{test_uri}'>Test</a>]</p>"
        return altar

    def _forge_provenance(self, gnosis: Any) -> str:
        """[FACULTY 3] Inscribes the temporal soul of the scripture."""
        if not gnosis: return ""

        author_count = getattr(gnosis, 'author_count', 0)
        age = getattr(gnosis, 'days_since_last_change', 9999)
        churn = getattr(gnosis, 'churn_score', 0)

        return f"> **Provenance:** {author_count} Author(s) | **Last Change:** {age}d ago | **Churn:** {churn}"

    def _forge_bonds(self, gnosis: Any) -> str:
        """[FACULTY 4] Proclaims the scripture's Gnostic dependencies."""
        if not gnosis: return ""

        deps = getattr(gnosis, 'dependencies', [])
        if not deps: return ""

        dep_links = [f"`{d}`" for d in deps]
        return f"\n> **Gnostic Bonds:** {', '.join(dep_links)}"

    def _forge_footer(self) -> str:
        """[FACULTY 11] Inscribes the rich telemetry of the rite."""
        stats = self.result.stats
        telemetry = (
            f"| Perception | Divination | Propagation | Adjudication | Scribing |\n"
            f"|:----------:|:----------:|:-----------:|:------------:|:--------:|\n"
            f"| {stats.get('perception_ms', 0):.0f}ms | {stats.get('divination_ms', 0):.0f}ms | {stats.get('propagation_ms', 0):.0f}ms | {stats.get('governance_ms', 0):.0f}ms | {stats.get('weaving_ms', 0):.0f}ms |"
        )

        return (
            f"---\n## 🔬 GNOSTIC TELEMETRY\n"
            f"**Symphony concluded in {self.result.duration_seconds:.2f}s.**\n\n"
            f"{telemetry}"
        )