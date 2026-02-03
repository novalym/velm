# Path: scaffold/artisans/symphony.py
# -----------------------------------

import argparse
import sys
import traceback
from pathlib import Path
from typing import Optional

from ..contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ..core.artisan import BaseArtisan
from ..help_registry import register_artisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import SymphonyRequest
from ..logger import Scribe

Logger = Scribe("SymphonyGateway")


@register_artisan("symphony")
class SymphonyArtisan(BaseArtisan[SymphonyRequest]):
    """
    =================================================================================
    == THE SOVEREIGN CONDUCTOR (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                     ==
    =================================================================================
    LIF: 10,000,000,000,000

    This is the High Priest of the Symphony. It receives the `SymphonyRequest` from
    the CLI or Daemon, adjudicates the validity of the scripture, and summons the
    `SymphonyConductor` to begin the Great Work.
    """

    def execute(self, request: SymphonyRequest) -> ScaffoldResult:
        """
        The Rite of Orchestration.
        Prepares the context and summons the SymphonyConductor.
        """
        self.logger.info(f"The Sovereign Conductor awakens for the '[cyan]{request.symphony_command}[/cyan]' rite.")

        # --- MOVEMENT I: THE CONDUCT RITE (EXECUTION) ---
        if request.symphony_command == 'conduct':
            return self._conduct_symphony(request)

        # --- MOVEMENT II: THE DEBUG RITE (FORENSICS) ---
        elif request.symphony_command == 'debug':
            return self._debug_symphony(request)

        # --- MOVEMENT III: THE UNKNOWN TONGUE ---
        return self.failure(f"Unknown symphony command: '{request.symphony_command}'")

    def _conduct_symphony(self, request: SymphonyRequest) -> ScaffoldResult:
        """
        Summons the Conductor to execute a Symphony.
        """
        # 1. Validate Scripture
        if not request.symphony_path:
            raise ArtisanHeresy(
                "The Rite of Conduct requires a scripture.",
                suggestion="Provide the path to a .symphony file.",
                severity=HeresySeverity.CRITICAL
            )

        symphony_path = (self.project_root / request.symphony_path).resolve()

        if not symphony_path.exists() or not symphony_path.is_file():
            raise ArtisanHeresy(
                f"The Symphony scripture is a void.",
                details=f"Path searched: {symphony_path}",
                suggestion="Ensure the file exists and is readable.",
                severity=HeresySeverity.CRITICAL
            )

        # 2. Determine Sanctum (Execution Root)
        execution_root = request.project_root or symphony_path.parent
        self.logger.verbose(f"   -> Scripture: {symphony_path.name}")
        self.logger.verbose(f"   -> Sanctum:   {execution_root}")

        # [FACULTY 7] The Guardian's Offer
        # If we are NOT rehearsing (i.e. we are touching reality), we offer a snapshot.
        # We target the execution root as the "file" being modified (abstractly).
        if not request.rehearse and not request.dry_run:
            self.guarded_execution([execution_root], request, context="symphony_conduct")

        # 3. Import and Instantiate (The Divine Summons)
        try:
            from ..symphony.conductor import SymphonyConductor

            # [THE PURE CONTRACT]
            conductor = SymphonyConductor(
                symphony_path=symphony_path,
                request_vessel=request,
                execution_root=execution_root
            )

            # 4. Conduct the Rite
            conductor.conduct()

            return self.success(
                f"Symphony '{symphony_path.name}' concluded.",
                data={"path": str(symphony_path)}
            )

        except ImportError as e:
            # [FACULTY 6] The Forensic Scream
            sys.stderr.write(f"\n[CRITICAL IMPORT ERROR]\n{traceback.format_exc()}\n")
            raise ArtisanHeresy(
                "The Symphony Conductor could not be summoned.",
                details=f"Missing dependencies or circular import: {e}",
                child_heresy=e
            )
        except Exception as e:
            # [FACULTY 6] The Forensic Scream
            sys.stderr.write(f"\n[CRITICAL CONDUCTOR FAILURE]\n{traceback.format_exc()}\n")

            if isinstance(e, ArtisanHeresy):
                raise e
            raise ArtisanHeresy(
                f"The Conductor faltered while initiating '{symphony_path.name}'.",
                child_heresy=e,
                details=str(e)
            ) from e

    def _debug_symphony(self, request: SymphonyRequest) -> ScaffoldResult:
        """
        Summons the Inquisitor to analyze a past Symphony.
        """
        if not request.chronicle_path:
            raise ArtisanHeresy(
                "The Rite of Debugging requires a chronicle.",
                suggestion="Provide the path to a .jsonl log file via --log or chronicle_path."
            )

        chronicle_path = (self.project_root / request.chronicle_path).resolve()

        if not chronicle_path.exists():
            raise ArtisanHeresy(f"Gnostic Chronicle not found: {chronicle_path}")

        try:
            from ..symphony.inquisitor import SymphonyInquisitor

            inquisitor = SymphonyInquisitor(chronicle_path)
            inquisitor.conduct_inquest()

            return self.success("Inquest complete.")

        except ImportError as e:
            raise ArtisanHeresy(
                "The Symphony Inquisitor is not manifest.",
                details=f"Import Error: {e}",
                suggestion="Ensure 'scaffold[studio]' dependencies are installed."
            )