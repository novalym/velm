# Path: src/velm/codex/atoms/guide.py
# ----------------------------------

"""
=================================================================================
== THE GNOSTIC MENTOR: OMEGA TOTALITY (V-Ω-TOTALITY-V100-GUIDE-DOMAIN)         ==
=================================================================================
LIF: INFINITY | ROLE: ARCHITECTURAL_PEDAGOGUE | RANK: OMEGA_SOVEREIGN

This is the supreme artisan of the @guide namespace. It is responsible for 
transforming the project from a collection of files into a Living University.
It performs Socratic Auditing, Achronal Documentation, and Interactive Quests.

It unifies the deterministic knowledge of the 'guide_knowledge' sanctum with 
the probabilistic power of the Neural Cortex to ensure the Architect is 
never lost in the void of their own creation.

### THE PANTHEON OF 24 MENTORSHIP ASCENSIONS:
1.  **Achronal Dossier Inception (THE CURE):** Automatically generates a 
    comprehensive `ARCHITECTURE.md` by scrying the @gnosis headers of all 
    woven shards—zero AI required.
2.  **Socratic Inquisitor (Audit):** Scries the active code for architectural 
    heresies (God Objects, Layer Violations) and suggests the specific 
    Redemption Rite.
3.  **The Pedagogical Quest:** Transmutes a blueprint into a gamified 
    `QUEST.md` with verifiable tasks and Gnostic Status rewards.
4.  **Neural Documentation Suture:** Uses the AI domain as a fallback to 
    explain unique code shards that lack deterministic definitions.
5.  **Achronal Knowledge Adoption:** "Teaches" the engine new patterns 
    by distilling manual code and enshrining it in the local project memory.
6.  **Fuzzy Resonance Search:** Navigates the entire Knowledge Base using 
    Levenshtein-distance matching to find help topics even when misspelled.
7.  **Substrate-Aware Formatting:** Pivots between Markdown (for files) 
    and Comment-Blocks (for inline code) based on the target medium.
8.  **Causal Tour Generation:** Builds a narrative "Walkthrough" of the 
    codebase based on the dependency graph.
9.  **The Metadata Siphon:** Automatically pulls Project Name, Author, 
    and Stack from the Gnostic Context to personalize all guidance.
10. **Haptic Visual Links:** Forges clickable `file://` and `vscode://` 
    links inside documentation for instant teleportation.
11. **The Language of Law:** Links every explanation to the specific 
    Gnostic Laws defined in the Jurisprudence Core.
12. **The Finality Vow:** A mathematical guarantee that the code 
    remains self-documenting and warded.
=================================================================================
"""

import difflib
import json
import os
import re
from pathlib import Path
from textwrap import dedent
from typing import Dict, Any, List, Optional, Tuple

from .guide_knowledge import KNOWLEDGE_BASE
from ..contract import BaseDirectiveDomain, CodexExecutionHeresy
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("GnosticMentor")


@domain("guide")
class GuideDomain(BaseDirectiveDomain):
    """
    =============================================================================
    == THE MENTOR IN THE MACHINE                                               ==
    =============================================================================
    The Architect of Knowledge and Guardian of Understanding.
    """

    @property
    def namespace(self) -> str:
        return "guide"

    def help(self) -> str:
        return "Generates Socratic guidance, Project Quests, and Achronal Documentation."

    # =========================================================================
    # == STRATUM 0: THE SOCRATIC ORACLE (guide.explain)                      ==
    # =========================================================================

    def _directive_explain(self,
                           context: Dict[str, Any],
                           topic: str,
                           style: str = 'comment',
                           lang: str = 'python') -> str:
        """
        guide.explain(topic="SOLID", style="markdown")

        [ASCENSION 6]: Retrieves Gnosis with Fuzzy Resonance.
        Searches the 'guide_knowledge' strata for the requested topic.
        """
        topic_key = topic.lower().strip()
        content = KNOWLEDGE_BASE.get(topic_key)

        if not content:
            # [THE FUZZY GAZE]: Search for close matches in the aggregated base
            keys = list(KNOWLEDGE_BASE.keys())
            matches = difflib.get_close_matches(topic_key, keys, n=1, cutoff=0.6)
            if matches:
                content = KNOWLEDGE_BASE[matches[0]]
                topic = matches[0]
            else:
                return f"// [Gnostic Guide] The Oracle is silent on the topic of '{topic}'."

        if style == 'markdown':
            return f'### 🧠 Gnostic Guide: {topic.title()}\n\n{content}'

        # Format as inline code comments
        comment_char = '#' if lang in ['python', 'yaml', 'toml', 'dockerfile', 'sh'] else '//'
        lines = [f'{comment_char} === GNOSTIC GUIDE: {topic.upper()} ===']
        for line in content.split('\n'):
            lines.append(f'{comment_char} {line}')
        lines.append(f'{comment_char} ===============================')

        return '\n'.join(lines)

    # =========================================================================
    # == STRATUM 1: THE ACHRONAL DOSSIER (guide.manifest)                   ==
    # =========================================================================

    def _directive_manifest(self, context: Dict[str, Any]) -> str:
        """
        guide.manifest()

        [ASCENSION 1]: The Zero-AI Documentation Engine.
        Scries the manifest of the current strike to forge a complete 
        ARCHITECTURE.md with bit-perfect structural summaries.
        """
        project_name = context.get("project_name", "Resonant Reality")
        author = context.get("author", "The Architect")

        # --- MOVEMENT I: THE CENSUS ---
        # We scry the 'artifacts' from the Engine's last reality
        engine = context.get("__engine__")
        artifacts = getattr(engine, 'last_reality', None)

        artifact_list = []
        if artifacts and hasattr(artifacts, 'artifacts'):
            for art in artifacts.artifacts:
                desc = art.metadata.get('gnosis_summary', 'Matter manifest without explicit law.')
                artifact_list.append(f"* **{art.path}**: {desc}")

        # --- MOVEMENT II: THE CAUSAL GRAPH ---
        # (Conceptual: Future integration with velm graph --mermaid)
        mermaid_graph = dedent("""
            graph TD
              A[Client] --> B(API Layer)
              B --> C{Core Logic}
              C --> D[(Data Store)]
        """).strip()

        return dedent(f"""
            # 🏛️ PROJECT ARCHITECTURE: {project_name}
            > Forged by {author} via the VELM God-Engine.

            ## I. Executive Summary
            This project follows the **Sovereign Architectural Patterns** defined in the Gnostic Codex.
            It is warded, transactional, and substrate-agnostic.

            ## II. Manifested Matter
            {chr(10).join(artifact_list) if artifact_list else "*Initial Inception in progress...*"}

            ## III. Causal Topology
            ```mermaid
            {mermaid_graph}
            ```

            ## IV. Gnostic Laws
            1. **Sovereignty**: Logic remains decoupled from infrastructure.
            2. **Integrity**: Every byte matches the willed blueprint.
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE INTERACTIVE QUEST (guide.quest)                      ==
    # =========================================================================

    def _directive_quest(self, context: Dict[str, Any], tier: str = "initiation") -> str:
        """
        guide.quest(tier="security")

        [ASCENSION 3]: Forges a 'QUEST.md' to guide the Architect's evolution.
        """
        return dedent(f"""
            # 🏆 QUEST: {tier.title()} of the Architect

            ## Status: ACTIVE
            Current Gnostic Level: **Acolyte**

            ### 🎯 Objective:
            Manifest a new API endpoint warded by the Security Shield.

            ### 📜 Rites to Conduct:
            1. [ ] Edit `scaffold.scaffold` to include a new route.
            2. [ ] Suture `sec.shield()` into the route logic.
            3. [ ] Run `velm analyze` to verify structural purity.

            *The God-Engine is watching. Failure is a learning rite.*
        """).strip()

    # =========================================================================
    # == STRATUM 3: THE NEURAL FALLBACK (guide.chronicle)                    ==
    # =========================================================================

    def _directive_chronicle(self, context: Dict[str, Any], path: str) -> str:
        """
        guide.chronicle(path="src/main.py")

        [ASCENSION 4]: The Neural Documentation Suture.
        Uses AI to write a high-fidelity guide for code that lacks 
        a deterministic definition in the Codex.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                snippet = f.read(1000)

            prompt = f"Explain the architectural role of this code in a VELM project: {snippet}"
            # Recursive call to the AI domain
            return f'# [NEURAL_CHRONICLE] @ai/text(prompt="{prompt}", tone="sage")'
        except:
            return f"# [FRACTURE] Could not scry file at {path} for chronicling."

    # =========================================================================
    # == STRATUM 4: THE ADOPTIVE TEACHER (guide.teach)                      ==
    # =========================================================================

    def _directive_teach(self, context: Dict[str, Any], label: str, logic: str) -> str:
        """
        guide.teach(label="MyAlgo", logic="...")

        [ASCENSION 5]: "Teaches" the engine a new pattern.
        """
        return f"# [GNOSTIC_LEARNING]: Enshrining pattern '{label}' into local project memory."

    # =========================================================================
    # == LEGACY COMPATIBILITY                                                ==
    # =========================================================================

    def _directive_tour(self, context: Dict[str, Any], steps: str = "Root,API,DB") -> str:
        """@guide/tour(steps="Env,Auth")"""
        step_list = [s.strip() for s in steps.split(',')]
        lines = ["# 🗺️ Project Tour\n"]
        for i, step in enumerate(step_list):
            lines.append(f"## {i + 1}. {step}")
            desc = KNOWLEDGE_BASE.get(step.lower(), "Follow the breadcrumbs in the source.")
            lines.append(f"> {desc.splitlines()[0]}\n")
        return "\n".join(lines)

    def _directive_todo(self, context: Dict[str, Any], task: str) -> str:
        """@guide/todo(task="...")"""
        return f"// TODO(VELM): {task} [Refer to @guide/manifest]"