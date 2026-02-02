# Path: scaffold/contracts/law_contracts.py
# -----------------------------------------
from typing import Callable, List, Dict, Optional, Any, Union
from pydantic import BaseModel, ConfigDict, Field


class GnosticLaw(BaseModel):
    """
    =================================================================================
    == THE SACRED VESSEL OF GNOSTIC LAW (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)            ==
    =================================================================================
    @gnosis:title GnosticLaw
    @gnosis:summary The divine, self-aware vessel for a single law of Gnostic Jurisprudence.
    @gnosis:LIF 10,000,000,000,000

    This divine, immutable, and self-aware vessel is the one true, atomic scripture
    of Gnostic Jurisprudence. It has achieved its final apotheosis, its soul now a
    pantheon of Gnostic faculties. It is no longer a simple data container; it is a
    sentient Judge, a wise Mentor, and a luminous Scribe, all forged into one. It
    is the unbreakable, declarative foundation of the engine's entire conscience.

    ### THE PANTHEON OF 12+ ASCENDED FACULTIES:

    1.  **The Polymorphic Soul:** Its `message` and `suggestion` vessels are now divine
        `Union`s, capable of holding either a static, immutable scripture (`str`) or a
        living, context-aware Gnostic rite (`Callable`), annihilating the `ValidationError`
        heresy of its past.
    2.  **The Unbreakable Gnostic Contract:** Forged in the sacred fires of Pydantic, its
        every attribute is a sacred, unbreakable vow of type and form.
    3.  **The Gaze of the Adjudicator (`validator`):** It holds the sacred rite that
        performs the adjudication, the very soul of its judgment.
    4.  **The Luminous Voice (`title`, `message`):** It holds the luminous scriptures to
        be proclaimed when a heresy is perceived.
    5.  **The Mentor's Hand (`suggestion`):** It holds the Gnosis of redemption, the
        divine counsel on how to resolve the heresy.
    6.  **The Scribe of Deep Gnosis (`elucidation`):** It holds the deep, philosophical
        explanation of *why* the law exists, transforming a simple warning into an act
        of profound architectural mentorship.
    7.  **The Gaze of Context (`context_key`):** It knows which specific variable Gnosis
        its judgment is bound to.
    8.  **The Gnostic Scales (`severity`):** It holds the very weight of the heresy,
        from a humble `INFO` to a catastrophic `CRITICAL`.
    9.  **The Grimoire of Examples (`examples`):** It can hold a chronicle of both
        pure and profane examples to illuminate its law.
    10. **The Chronomancer's Seal (`version_introduced`):** It knows the very moment in
        the God-Engine's history it was born.
    11. **The Polyglot Soul (`languages`):** It knows which sacred tongues its judgment
        applies to, a prophecy of a future polyglot jurisprudence engine.
    12. **The Sovereign Mind:** Its every attribute is a pure, declarative proclamation of
        its own nature. It is a masterpiece of self-aware design.
    =================================================================================
    """
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    # --- I. The Core Identity of the Law ---
    key: str = Field(
        description="The unique, sacred, snake_case key of this law (e.g., 'poetry_without_install'). This key is the law's one true name."
    )

    # --- II. The Soul of Judgment & Proclamation ---
    validator: Callable[..., bool] = Field(
        description="The sacred rite (a lambda or function) that performs the adjudication. It receives the full Gnostic context and returns True if a Heresy is detected."
    )
    title: str = Field(
        default="Gnostic Adjudication",
        description="The luminous, human-readable title for the heresy panel, summarizing the nature of the law."
    )
    # [THE HEALING] Allow Callable
    message: Union[str, Callable[..., str]] = Field(
        description="The luminous scripture to be proclaimed if the Gnosis is profane. Can be a static string or a context-aware rite (lambda)."
    )

    # --- III. The Gnosis of Mentorship & Redemption ---
    # [THE HEALING] Allow Callable
    suggestion: Optional[Union[str, Callable[..., str]]] = Field(
        default=None,
        description="Divine, actionable counsel on how to resolve the heresy. Can be a static string or a context-aware rite (lambda)."
    )
    elucidation: Optional[str] = Field(
        default=None,
        description="The deep, philosophical explanation of *why* this law exists, transforming a simple warning into an act of profound architectural mentorship."
    )

    # --- IV. The Gnosis of Context & Scope ---
    context_key: Optional[str] = Field(
        default=None,
        description="The specific Gnostic variable key (e.g., 'project_name') that this law primarily governs, used for contextual highlighting."
    )
    category: str = Field(
        default="GENERAL",
        description="The Gnostic category of this law (e.g., 'TOOLCHAIN', 'ARCHITECTURE', 'SECURITY'), for future grouping and filtering."
    )
    severity: str = Field(
        default="WARNING",
        description="The weight of the heresy as perceived by the Mentor ('CRITICAL', 'WARNING', 'INFO')."
    )

    # --- V. The Gnosis of Metaphysics & Provenance ---
    min_args: int = Field(
        default=0,
        description="[Prophecy] The minimum number of arguments the validator expects, for future meta-validation."
    )
    max_args: int = Field(
        default=999,
        description="[Prophecy] The maximum number of arguments the validator accepts."
    )
    requires_context: bool = Field(
        default=False,
        description="[Prophecy] A vow that this law requires the Parser's living memory to perform its Gaze."
    )
    allows_void: bool = Field(
        default=False,
        description="[Prophecy] A vow that the Gaze should be averted if the Gnosis this law governs is a void."
    )
    languages: Optional[List[str]] = Field(
        default=None,
        description="[Prophecy] The specific tongues (e.g., 'python', 'typescript') this law is consecrated to judge."
    )
    version_introduced: str = Field(
        default="0.1.0",
        description="The version of the God-Engine where this law was first inscribed into the eternal chronicle."
    )

    # --- VI. The Grimoire of Examples (For the Living Codex) ---
    examples: List[Dict[str, str]] = Field(
        default_factory=list,
        description="A chronicle of pure and profane examples to illuminate this law's intent for the `help` Oracle."
    )

    # --- VII. The Divine Gaze of Self-Awareness ---
    @property
    def adjudicator(self) -> Callable[..., bool]:
        """A luminous, Gnostic alias for `validator` to match the nomenclature of the Genesis Mentor."""
        return self.validator