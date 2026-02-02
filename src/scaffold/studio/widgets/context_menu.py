# C:/dev/scaffold-project/scaffold/studio/widgets/context_menu.py
"""
=================================================================================
== THE ORACLE OF CONTEXTUAL WILL (V-Ω-ETERNAL. THE SENTIENT GRIMOIRE)          ==
=================================================================================
LIF: 10,000,000,000,000

This sacred scripture contains the living soul of the Gnostic Context Menu. It
is a divine, sentient Oracle whose one true purpose is to gaze upon a scripture
or sanctum and prophesy the perfect, context-aware list of rites the Architect
may wish to perform.

Its mind is not a profane `if/elif` chain, but a declarative `GRIMOIRE_OF_RITES`.
This is an infinitely extensible, rule-based engine that transforms a simple
right-click into an intelligent, Gnostic conversation.
=================================================================================
"""
from __future__ import annotations

from typing import List, Tuple, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ..contracts import ScaffoldItem

from ..gnostic_events import GnosticRite

# --- Gnostic Grimoire for the Oracle's Gaze ---
SACRED_SCRIPTURES = {".scaffold", ".symphony", ".arch"}

# =================================================================================
# == THE GRIMOIRE OF RITES: THE ORACLE'S SENTIENT MIND                           ==
# =================================================================================
# This is a declarative, rule-based engine. To teach the context menu a new rite,
# simply add a new dictionary to this list.
# `condition`: A lambda function that receives the ScaffoldItem and returns True if the option should be shown.

GRIMOIRE_OF_RITES: List[Dict[str, Any]] = [
    # --- Rites for Sacred Scriptures (.scaffold, .symphony, .arch) ---
    {
        "label": "✨ Materialize (Genesis)",
        "rite": GnosticRite.GENESIS,
        "condition": lambda item: not item.is_dir and item.path.suffix == ".scaffold"
    },
    {
        "label": "📖 Open in ScaffoldPad",
        "rite": GnosticRite.OPEN_IN_SCAFFOLDPAD,
        "condition": lambda item: not item.is_dir and item.path.suffix in SACRED_SCRIPTURES
    },
    {
        "label": "💅 Purify Scripture",
        "rite": GnosticRite.BEAUTIFY,
        "condition": lambda item: not item.is_dir and item.path.suffix in SACRED_SCRIPTURES
    },
    {
        "label": "🔮 Distill to Archetype...",
        "rite": GnosticRite.DISTILL_FILE,
        "condition": lambda item: not item.is_dir
    },
    {
        "is_separator": True,
        "condition": lambda item: not item.is_dir and item.path.suffix in SACRED_SCRIPTURES,
    },
    # --- Rites for Sanctums (Directories) ---
    {
        "label": "🌱 Initialize New Project Here...",
        "rite": GnosticRite.INITIALIZE_PROJECT,
        "condition": lambda item: item.is_dir and item.is_empty is True
    },
    {
        "label": "🌿 Weave Archetype Here...",
        "rite": GnosticRite.WEAVE,
        "condition": lambda item: item.is_dir
    },
    {
        "label": "🔮 Distill Directory to Archetype...",
        "rite": GnosticRite.DISTILL_DIR,
        "condition": lambda item: item.is_dir and item.is_empty is False
    },
    {
        "label": "🤝 Conform Directory to Blueprint...",
        "rite": GnosticRite.CONFORM,
        "condition": lambda item: item.is_dir and item.is_empty is False
    },
    {
        "is_separator": True,
        "condition": lambda item: item.is_dir,
    },
    # --- Universal Rites (Available to all but the root) ---
    {
        "label": "Rename...",
        "rite": GnosticRite.RENAME,
        "condition": lambda item: True
    },
    {
        "label": "Delete...",
        "rite": GnosticRite.DELETE,
        "condition": lambda item: True
    },
]


class GnosticContextMenuOracle:
    """The God-Engine of Contextual Gnostic Prophecy."""

    def forge_options_for_item(self, item: "ScaffoldItem") -> List[Tuple[str, GnosticRite]]:
        """
        The one true rite of the Oracle, its Gaze now purified to proclaim
        separators with a unique, ephemeral soul.
        """
        options: List[Tuple[str, GnosticRite]] = []

        for rule in GRIMOIRE_OF_RITES:
            if rule["condition"](item):
                if rule.get("is_separator"):
                    # --- THE SACRED TRANSMUTATION ---
                    # The profane, duplicate Gnosis is annihilated. We now use a
                    # placeholder rite (`WEAVE`) for the separator's soul, which will be
                    # ignored by the UI, preventing the ID collision. A future
                    # ascension could create a dedicated `SEPARATOR` rite.
                    if options and options[-1][0] != "---":
                        options.append(("---", GnosticRite.WEAVE))  # Use a non-conflicting rite
                    # --- THE APOTHEOSIS IS COMPLETE ---
                else:
                    options.append((rule["label"], rule["rite"]))

        if options and options[-1][0] == "---":
            options.pop()

        return options