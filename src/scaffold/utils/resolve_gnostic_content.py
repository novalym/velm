# Path: scaffold/utils/resolve_gnostic_content.py
"""
=================================================================================
== THE SACRED SANCTUM OF THE ORACLE OF GNOSTIC ORIGINS (V-Ω-ETERNAL)           ==
=================================================================================
This scripture contains the living soul of the God-Engine that perceives the
true origin and soul of any scripture's content. It is a universal, pure, and
unbreakable artisan, available to all in the Scaffold cosmos.
=================================================================================
"""
from pathlib import Path
from typing import Dict, Tuple, TYPE_CHECKING

from ..contracts.data_contracts import ScaffoldItem, GnosticSoulVessel
from ..logger import Scribe

# === THE UNBREAKABLE WARD OF TYPE CHECKING ===
# We hide the heavy imports behind this ward to break the Ouroboros.
if TYPE_CHECKING:
    from ..core.alchemist import DivineAlchemist
    from ..artisans.template_engine import TemplateEngine

Logger = Scribe("GnosticOriginOracle")


def resolve_gnostic_content(
        item: ScaffoldItem,
        alchemist: 'DivineAlchemist', # Forward reference string not needed in 3.10+, but safe
        template_engine: 'TemplateEngine',
        variables: Dict,
        sanctum: Path,
        source_override_map: Dict[Path, str]
) -> Tuple[str, str]:
    """
    =================================================================================
    == THE DIVINE CONDUIT (V-Ω-ETERNAL. THE BRIDGE TO THE NEW REALITY)             ==
    =================================================================================
    This is the sacred conduit, the bridge between the old reality and the new. It
    honors the ancient, two-fold contract while conducting its symphony through the
    new, ascended God-Engine. It summons `resolve_gnostic_content_v2`, receives its
    pure `GnosticSoulVessel`, and translates its Gnosis back into the humble tongue
    of the old world. It is the unbreakable promise of backward compatibility.
    =================================================================================
    """
    soul_vessel = resolve_gnostic_content_v2(
        item=item,
        alchemist=alchemist,
        template_engine=template_engine,
        variables=variables,
        sanctum=sanctum,
        source_override_map=source_override_map
    )

    # The translation back to the ancient tongue.
    if soul_vessel.is_binary_copy:
        return f"__SCAFFOLD_BINARY_COPY_INSTRUCTION__:{soul_vessel.binary_source_path}", soul_vessel.origin_scripture
    else:
        return soul_vessel.untransmuted_content, soul_vessel.origin_scripture


def resolve_gnostic_content_v2(
        item: ScaffoldItem,
        alchemist: 'DivineAlchemist',
        template_engine: 'TemplateEngine',
        variables: Dict,
        sanctum: Path,
        source_override_map: Dict[Path, str]
) -> GnosticSoulVessel:
    """
    =================================================================================
    == THE GOD-ENGINE OF GNOSTIC ORIGINS (V-Ω-ASCENDED-INTENT)                       ==
    =================================================================================
    LIF: 100,000,000,000

    This divine artisan has been ascended with the **Law of Gnostic Intent**. It now
    understands that a `seed_path` (`<<`) is a sacred vow of content preservation,
    not a hint of binary profanity. It will now righteously treat seeded souls as
    text unless the scripture's very form (its extension) proclaims it to be binary.

    The Heresy of the False Prophet is annihilated. The `transmute` rite is healed.
    """
    from ..utils import is_binary_extension # We summon a new, purer Gaze

    # FACULTY #3: The Law of the Explicit Void
    if item.content is not None:
        origin = f"[yellow]from Inline Gnosis[/yellow] [dim]({len(item.content)} chars)[/dim]"
        dependencies = alchemist.discover_variables(item.content)
        return GnosticSoulVessel(untransmuted_content=item.content, origin_scripture=origin, dependencies=dependencies)

    # FACULTY #11: The Gaze of the Source Override
    if item.path in source_override_map:
        content = source_override_map[item.path]
        origin = "[magenta]from Memory Override[/magenta]"
        dependencies = alchemist.discover_variables(content)
        return GnosticSoulVessel(untransmuted_content=content, origin_scripture=origin, dependencies=dependencies)

    # FACULTY #4, #5: The Guardian's Gaze & Alchemical Seed
    if item.seed_path is not None:
        try:
            resolved_seed_path_str = alchemist.transmute(str(item.seed_path), variables)
            seed_full_path = (sanctum / resolved_seed_path_str).resolve()

            if not str(seed_full_path).startswith(str(sanctum.resolve())):
                raise PermissionError("Seed path attempts to escape the sacred sanctum.")
            if not seed_full_path.is_file():
                raise FileNotFoundError(f"Promised seed scripture not found at: '{seed_full_path}'")

            # [THE ASCENSION] The Law of Gnostic Intent
            # The profane, content-sniffing `is_binary` is annihilated. We now
            # perform a pure Gaze upon the file's extension. We trust the
            # Architect's will that a `.scaffold` file is text.
            if is_binary_extension(seed_full_path):
                Logger.verbose(f"Binary soul perceived for '{item.path}' via seed extension.")
                return GnosticSoulVessel(
                    untransmuted_content="", origin_scripture="[red]from Binary Seed[/red]",
                    is_binary_copy=True, binary_source_path=seed_full_path
                )

            # If not a known binary extension, we proceed with the sacred rite of reading text.
            content = seed_full_path.read_text(encoding='utf-8', errors='replace')
            origin = f"[cyan]from External Seed[/cyan] [dim]({resolved_seed_path_str})[/dim]"

            dependencies = alchemist.discover_variables(content)
            return GnosticSoulVessel(untransmuted_content=content, origin_scripture=origin, dependencies=dependencies)

        except (FileNotFoundError, PermissionError) as e:
            raise IOError(f"External seed heresy for '{item.path}': {e}") from e
        except Exception as e:
            raise IOError(f"A paradox occurred while reading seed for '{item.path}': {e}") from e

    # FACULTY #6: The Polyglot Oracle
    template_gnosis = template_engine.perform_gaze(item.path, variables)
    if template_gnosis:
        origin = f"[blue]from {template_gnosis.gaze_tier}[/blue] [dim]({template_gnosis.display_path})[/dim]"
        dependencies = alchemist.discover_variables(template_gnosis.content)
        return GnosticSoulVessel(untransmuted_content=template_gnosis.content, origin_scripture=origin,
                                 dependencies=dependencies)

    # The Final Proclamation of the Void
    return GnosticSoulVessel(untransmuted_content="", origin_scripture="[dim](as Empty Scripture)[/dim]")