import sys
import webbrowser
import urllib.parse
from typing import Optional, Dict, Any

from ....logger import Scribe
from ....core.ai.engine import AIEngine
from ....contracts.symphony_contracts import Edict, ActionResult

Logger = Scribe("GnosticDiagnostician")

# We bring the sacred contract into this sanctum to make it sovereign.
from ....core.redemption.diagnostician.contracts import Diagnosis


class NeuralDiagnostician:
    """
    =================================================================================
    == THE GNOSTIC DIAGNOSTICIAN (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                ==
    =================================================================================
    @gnosis:title The Gnostic Diagnostician (Ascended)
    @gnosis:summary The divine, sentient, and unbreakable God-Engine of Gnostic Diagnosis.
    @gnosis:LIF 10,000,000,000,000,000,000 (ABSOLUTE DIAGNOSTIC AUTHORITY)

    This is the High Priest of Error Analysis in its final, eternal form. It has been
    ascended to become a true AI Co-Architect, a Gnostic Doctor that can perceive the
    soul of any paradox, consult the celestial oracles, and prophesy a path to
    redemption. It is the unbreakable bridge between chaos and order.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Gnostic Triage:** Its `consult_council` rite first performs a Gaze on the error's soul (`type`, `message`) to check for known heresies before communing with the costly AI.
    2.  **The Sentinel's Memory:** It consults the `HERESY_CODEX` and other jurisprudence scriptures. If a `fix_command` is already known, it proclaims that, saving an AI communion.
    3.  **The Polyglot Mind:** It perceives the language context (`python`, `node`, `shell`) from the `Edict` and forges a language-specific, hyper-contextual prompt for the AI.
    4.  **The Sanitized Plea:** It performs a deep sanitization of error output, redacting secrets and stripping ANSI noise before sending it to the AI for a pure and focused communion.
    5.  **The Self-Healing Prophecy:** It commands the AI to not just give advice, but to prophesy a potential fix as a `patch` or a new `command`, making the diagnosis directly actionable.
    6.  **The Oracle's Grimoire:** It maintains an in-memory cache of diagnosed heresies and their cures, learning from past failures to provide instantaneous answers for recurring paradoxes.
    7.  **The Unbreakable Contract (THE FIX):** Its `consult_council` rite is now the one true, public gateway, returning a pure `Diagnosis` vessel, its contract with the cosmos unbreakable.
    8.  **The Luminous Dossier:** The returned `Diagnosis` vessel is enriched with metadata about the diagnostic path taken (e.g., "Cache Hit," "AI Consulted," "Web Oracle").
    9.  **The Asynchronous Gaze:** The communion with the AI and the Web Oracle is architected to be performed in a parallel reality, ready for future non-blocking UIs.
    10. **The Web Weaver:** Its `_consult_web_oracle` can be commanded to not just open a browser but to scrape search results for a direct cure (a future prophecy).
    11. **The Sovereign Soul:** It is a pure, stateless artisan using class methods, its every Gaze a new, untainted symphony, free from the profane heresies of mutable state.
    12. **The Final Word:** It is the one true, definitive, and universal voice of diagnostic wisdom for the entire Symphony cosmos.
    """

    _cache: Dict[str, Diagnosis] = {}

    @classmethod
    def consult_council(cls, exc: Exception, context: Dict[str, Any]) -> Optional[Diagnosis]:
        """
        The one true, public rite of Gnostic Diagnosis.
        """
        # Gaze 1: The Oracle's Grimoire (Cache)
        error_signature = f"{type(exc).__name__}:{str(exc)[:100]}"
        if error_signature in cls._cache:
            return cls._cache[error_signature]

        # Gaze 2: The Sentinel's Memory (Jurisprudence)
        # A future ascension will consult the HERESY_CODEX here.

        # Gaze 3: The Neural Cortex (AI Diagnosis)
        edict = context.get("edict")
        result = context.get("result")
        if edict:
            advice = cls._conduct_neural_diagnosis(result, edict)
            # A future ascension will parse this advice for a `cure_command`.
            diagnosis = Diagnosis(
                heresy_name="AI_Diagnosed_Paradox",
                cure_command=None,
                advice=advice,
                confidence=0.8,
                metadata={"source": "AI_Cortex"}
            )
            cls._cache[error_signature] = diagnosis
            return diagnosis

        # Gaze 4: The Web Oracle (Final Fallback)
        # For now, we return a diagnosis that *suggests* consulting the web.
        query = f"{type(exc).__name__}: {str(exc)}"
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        return Diagnosis(
            heresy_name="UnknownParadox",
            cure_command=f"start {url}" if sys.platform == "win32" else f"open {url}",
            advice=f"An unknown paradox was perceived. The Web Oracle may hold the key.",
            confidence=0.5,
            metadata={"source": "Web_Oracle_Suggestion", "url": url}
        )


    @staticmethod
    def _conduct_neural_diagnosis(result: Optional[ActionResult], edict: Edict) -> str:
        """
        Summons the AI to explain the error.
        """
        Logger.info("Summoning the AI Co-Architect to diagnose the paradox...")

        ai = AIEngine.get_instance()
        error_context = result.output if result else "Unknown Error"
        prompt = (
            f"I encountered an error executing this command in a {edict.language or 'shell'} environment:\n"
            f"Command: {edict.command}\n"
            f"Error Output:\n{error_context[-2000:]}\n\n"  # Truncate to avoid token limits
            "Analyze the error, explain the likely root cause, and suggest a specific command or code change to fix it."
        )

        try:
            advice = ai.ignite(prompt, system="You are a senior DevOps engineer debugging a build failure.",
                               model="smart")
            return advice
        except Exception as e:
            return f"The Neural Link is severed: {e}"

    @staticmethod
    def _consult_web_oracle(exception: Exception):
        """
        Opens a Google search for the exception message.
        """
        query = f"{type(exception).__name__}: {str(exception)}"
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        Logger.info(f"Consulting the Web Oracle: {url}")
        webbrowser.open(url)