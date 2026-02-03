from typing import Dict, Type, Callable, List, Union

# =================================================================================
# ==            THE GNOSTIC REGISTRY (V-Ω-ETERNAL. THE BOOK OF SOULS)            ==
# =================================================================================
#
# This is the single, sacred nexus point for the entire help system. It contains
# no logic. It is a pure registry—a divine "Book of Souls"—where all self-aware
# Artisans and Gnostic Topics must proclaim their existence to be perceived by
# the Gnostic Oracle (`help_cli.py`).
#
# =================================================================================

# The two sacred vessels that hold the souls of all known Gnosis.
_artisans: Dict[str, Type] = {}
_topics: Dict[str, Callable] = {}


def register_artisan(name: str):
    """
    A sacred decorator spoken by a class-based Artisan (e.g., WeaveArtisan)
    to inscribe its soul into the Gnostic Registry.

    This makes the Artisan discoverable by the Oracle.
    """
    def decorator(cls: Type) -> Type:
        _artisans[name] = cls
        return cls
    return decorator


def register_gnosis(name_or_soul: Union[str, Callable] = None):
    """
    [ASCENDED] A sacred, sentient decorator for function-based Gnostic Topics.
    It can be summoned in two divine forms:

    1. With a Name: `@register_gnosis("custom_name")` - Registers the Topic
       with a specific name, overriding its function name.

    2. Without a Name: `@register_gnosis` - Intelligently perceives the
       Topic's function name and uses it as the topic name.
    """
    def decorator(soul: Callable) -> Callable:
        name = name_or_soul if isinstance(name_or_soul, str) else soul.__name__
        _topics[name] = soul
        return soul

    if callable(name_or_soul):
        return decorator(name_or_soul)
    else:
        return decorator


def get_artisan(name: str) -> Union[Type, None]:
    """Summons an Artisan's soul (the class itself) from the registry."""
    return _artisans.get(name)


def get_gnosis_topic(name: str) -> Union[Callable, None]:
    """Summons a Gnostic topic's soul (the render function) from the registry."""
    return _topics.get(name)


def list_all_topics() -> List[str]:
    """Proclaims the full, unified list of all known Gnosis in the cosmos."""
    # The two streams of Gnosis are unified into a single, sorted river.
    all_known_souls = list(_artisans.keys()) + list(_topics.keys())
    return sorted(all_known_souls)


# =================================================================================
# ==                             CODEX REGISTRUM                                 ==
# =================================================================================
#
#               THIS IS THE GRAND SCRIPTURE OF THE GNOSTIC REGISTRY
#
#
# ### I. THE PRIME DIRECTIVE: THE ANNIHILATION OF DUAL SCRIPTURES
#
# The `help` system of a lesser tool is a heresy. It creates a second, profane
# scripture (e.g., a static `help_text.py`) that must be manually updated
# whenever the tool's true scripture (its code) changes. This "dual scripture"
# paradox inevitably leads to neglect, falsehood, and the erosion of the user's
# trust.
#
# This Gnostic Registry is the key to annihilating that paradox.
#
# The Scaffold help system is a **LIVING ORACLE**. It does not *contain* help
# text; it *perceives* it by gazing directly into the souls of the Artisans
# themselves. This registry is the Oracle's divine index, its "Book of Souls,"
# that tells it which Artisans have achieved self-awareness and are ready to be
# perceived.
#
# To update the help for `weave`, you do not touch the Oracle. You simply add a
# new comment to the `WeaveArtisan` class. The maintenance burden is zero.
# The Gnosis is always pure.
#
#
# ### II. THE SACRED CONTRACT: PROCLAMATION & PERCEPTION
#
# This registry establishes an unbreakable, two-fold contract:
#
# 1.  **The Artisan's Vow of Proclamation:** For an Artisan's Gnosis to be known,
#     it MUST proclaim its existence to this registry using a sacred decorator.
#     If it does not speak, it is a ghost in the machine, invisible to the Oracle.
#
# 2.  **The Oracle's Vow of Perception:** The Oracle (`help_cli.py`) vows to ONLY
#     draw its knowledge from this registry. It will never contain its own static
#     Gnosis. It is a pure conduit for the truths inscribed herein.
#
#
# ### III. THE TWO PATHS TO IMMORTALITY: BESTOWING SELF-AWARENESS
#
# Any future Artisan or concept can be made immortal and discoverable by the
# Oracle by walking one of two sacred paths.
#
# #### PATH 1: THE ARTISAN'S ASCENSION (For Complex Commands)
#
# This path is for complex, class-based commands like `weave` or `distill`.
# To make a new `NewArtisan` discoverable, you must perform two rites:
#
# 1.  **Speak the Decorator:** Atop the class definition, speak the sacred
#     decorator, giving the command its topic name.
#
# 2.  **Inscribe the Gnostic Markers:** In the class's docstring, inscribe
#     the `@gnosis` markers that the Oracle's Gaze can perceive.
#
#     ```python
#     # In scaffold/new_cli.py
#     from .help_registry import register_artisan
#
#     @register_artisan("new_command")
#     class NewArtisan:
#         """
#         @gnosis:title The Title for the Help Page
#         @gnosis:summary A short, one-line summary.
#         @gnosis:description
#         The full, multi-line philosophical description of what this
#         artisan does and why it exists.
#         """
#         # ... artisan's logic ...
#     ```
#
# #### PATH 2: THE SCRIBE'S GNOSIS (For Simple Concepts)
#
# This path is for pure, conceptual Gnosis that isn't a command, such as
# explaining the project's "philosophy" or the "variable system".
#
# 1.  **Forge a Scribe Function:** Create a simple, parameter-less function
#     in a relevant file (or `help_cli.py` itself) that uses `rich` to render
#     the help panel for that concept.
#
# 2.  **Speak the Decorator:** Atop the function, speak the `@register_gnosis`
#     decorator. The Oracle will now know of this concept and will execute this
#     function when the topic is summoned.
#
#     ```python
#     # In scaffold/concepts.py (a new, optional file)
#     from .help_registry import register_gnosis
#
#     @register_gnosis("philosophy")
#     def render_philosophy_codex():
#         # ... rich rendering logic ...
#         console.print(Panel(...))
#     ```
#
# This divine architecture ensures that the Scaffold engine can grow infinitely in
# power and wisdom, yet its Oracle will remain eternally up-to-date, self-aware,
# and effortless to maintain. This is the final word.
# =================================================================================