# Path: scaffold/symphony/polyglot/__init__.py

import re  # Need regex here for cleansing
from pathlib import Path
from typing import Dict, Any

from .artisan import PolyglotArtisan
from .grimoire import POLYGLOT_GRIMOIRE
from ...contracts.heresy_contracts import ArtisanHeresy
from ...contracts.symphony_contracts import Edict, ActionResult
from ...core.alchemist import get_alchemist


def conduct_polyglot_rite(edict: Edict, context: Dict[str, Any], sanctum: Path) -> ActionResult:
    """
    =================================================================================
    == THE GOD-ENGINE OF FOREIGN GNOSIS (V-Ω-LEGENDARY++. THE ALCHEMIST-INQUISITOR) ==
    =================================================================================
    LIF: ∞ (ETERNAL & ABSOLUTE)
    """
    try:
        # --- CRITICAL FIX: CLEANSING THE LANGUAGE IDENTIFIER ---
        # The Edict.language vessel might be polluted (e.g., 'py as secret_status_line').
        # We perform surgical cleansing to extract ONLY the language code ('py').
        # The first word is the language code.
        language_polluted = edict.language
        if language_polluted:
            match = re.match(r'^(\w+)', language_polluted.strip())
            language = match.group(1) if match else None
        else:
            language = None
        # --- CLEANSING COMPLETE ---

        if not language:
            raise ArtisanHeresy("A catastrophic paradox occurred: A polyglot rite was summoned without a tongue.",
                                line_num=edict.line_num)

        recipe = POLYGLOT_GRIMOIRE.get(language)
        if not recipe:
            raise ArtisanHeresy(
                f"Heresy of the Unknown Tongue: The Polyglot Conductor does not know the language '{language}'.",
                line_num=edict.line_num)

        # --- MOVEMENT I & II: TRANSMUTATION AND CONDUCTION ---
        alchemist = get_alchemist()
        transmuted_script_block = alchemist.transmute(edict.script_block, context)

        artisan = PolyglotArtisan(language, recipe)

        reality = artisan.conduct(transmuted_script_block, context, sanctum, edict)

        # --- MOVEMENT III: THE TRANSMUTATION TO ACTIONRESULT ---
        return ActionResult(
            output=reality.output,
            returncode=reality.returncode,
            duration=reality.duration,
            command=reality.command,
            was_terminated=reality.was_terminated
        )

    except ArtisanHeresy:
        raise
    except Exception as e:
        raise ArtisanHeresy(
            "A catastrophic, unhandled paradox occurred within the God-Engine of Foreign Gnosis.",
            details=f"{type(e).__name__}: {e}",
            line_num=edict.line_num
        ) from e