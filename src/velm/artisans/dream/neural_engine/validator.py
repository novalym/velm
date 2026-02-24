# Path: artisans/dream/neural_engine/validator.py
# -----------------------------------------------

import re
from pathlib import Path
from typing import Tuple, Optional, Any, List

# --- CORE UPLINKS ---
from ....contracts.heresy_contracts import HeresySeverity
from ....parser_core.parser import ApotheosisParser
from ....logger import Scribe

Logger = Scribe("Dream:Inquisitor")


class NeuralInquisitor:
    """
    =============================================================================
    == THE NEURAL INQUISITOR (V-Ω-SHADOW-SIMULATOR)                            ==
    =============================================================================
    LIF: ∞ | ROLE: HALLUCINATION_FIREWALL

    Audits the prophecy returned by the LLM by running it through the actual
    `ApotheosisParser` in a sandboxed, ephemeral context.

    If the blueprint is structurally unsound (invalid syntax, bad nesting,
    missing variables), the Inquisitor rejects it with a forensic traceback,
    forcing the AI to self-correct.
    """

    def __init__(self, engine: Optional[Any] = None):
        self.engine = engine

    def adjudicate(self, content: str) -> Tuple[bool, Optional[str]]:
        """
        [THE RITE OF SHADOW PARSING]
        Returns (is_valid, error_message).
        """
        if not content.strip():
            return False, "The Oracle returned a Void (Empty Response)."

        # 1. Structural Regex Check (Fast Fail)
        # Must have at least one file definition (::) or directory (/) or mutation (+=)
        has_file = "::" in content or "<< " in content
        has_dir = re.search(r"[\w_\-\./]+/$", content, re.MULTILINE)
        has_mutation = re.search(r"[\w_\-\./]+\s*(\+=|\^=|~=)", content)

        if not (has_file or has_dir or has_mutation):
            return False, "No physical matter (files, directories, or mutations) detected in the blueprint."

        # 2. Markdown Pollution Check
        if content.strip().startswith("```"):
            return False, "Markdown code fences detected. Output must be raw."

        # 3. [ASCENSION]: THE SHADOW PARSE
        # We attempt to actually parse the string using the God-Engine's own mind.
        try:
            # Summon a localized parser instance
            parser = ApotheosisParser(grammar_key="scaffold", engine=self.engine)

            # We use a dummy path for context
            shadow_path = Path("shadow_prophecy.scaffold")

            # Conduct the Parse (Silent Mode)
            # We catch exceptions internally, but we also check the heresy log
            parser.parse_string(content, file_path_context=shadow_path)

            # 4. Forensic Heresy Scan
            # We look for CRITICAL heresies in the parser's log
            critical_heresies = [
                h for h in parser.heresies
                if h.severity == HeresySeverity.CRITICAL
            ]

            if critical_heresies:
                # We return the first critical failure as the rejection reason
                primary_heresy = critical_heresies[0]
                error_msg = (
                    f"Structural Heresy at Line {primary_heresy.line_num}: {primary_heresy.message}. "
                    f"Details: {primary_heresy.details}"
                )
                return False, error_msg

            # If we reach here, the blueprint is syntactically perfect.
            return True, None

        except Exception as e:
            # If the parser itself crashes, the blueprint is radioactively bad.
            return False, f"Catastrophic Parsing Fracture: {str(e)}"

    def purify(self, content: str) -> str:
        """
        Attempts to heal minor heresies in the output.
        """
        clean = content.strip()

        # Heal Markdown
        if clean.startswith("```scaffold"):
            clean = clean[11:]
        elif clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]

        return clean.strip()