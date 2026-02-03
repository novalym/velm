# Path: scaffold/symphony/__init__.py

import argparse
from pathlib import Path

from ..contracts.heresy_contracts import ArtisanHeresy
from ..logger import Scribe

Logger = Scribe("SymphonyGateway")


def handle_symphony(args: argparse.Namespace):
    """
    =================================================================================
    == THE SOVEREIGN CONDUCTOR (V-Ω-FINALIS. THE PURE GATEWAY)                     ==
    =================================================================================
    This gateway is now pure. It no longer forges its own parser. It receives the
    complete, final Gnosis from the Grand Conductor and performs its one true rite:
    the Triage of Souls and the Divine Delegation.
    =================================================================================
    """
    try:
        # === THE DEFERRED SUMMONS (BREAKING THE OUROBOROS) ===
        # We import these artisans ONLY when the rite is actually conducted.
        # This prevents 'scaffold.parser' -> 'scaffold.symphony' -> 'scaffold.parser' loops.
        from .conductor import SymphonyConductor
        from .inquisitor import SymphonyInquisitor
        # ===============================================
        if args.symphony_command == 'conduct':
            symphony_path = Path(args.symphony_path).resolve()
            if not symphony_path.is_file():
                raise ArtisanHeresy(f"Symphony scripture not found: {symphony_path}")

            conductor = SymphonyConductor(symphony_path, args)
            conductor.conduct()

        elif args.symphony_command == 'debug':
            chronicle_path = Path(args.chronicle_path).resolve()
            if not chronicle_path.is_file():
                raise ArtisanHeresy(f"Gnostic Chronicle not found: {chronicle_path}")

            inquisitor = SymphonyInquisitor(chronicle_path)
            inquisitor.conduct_inquest()


    except Exception as e:

        # We now re-raise with the full Gnostic soul of the paradox.

        raise ArtisanHeresy(

            f"A catastrophic, unhandled paradox occurred within the Symphony.",

            details=str(e)

        ) from e


__all__ = ["handle_symphony"]