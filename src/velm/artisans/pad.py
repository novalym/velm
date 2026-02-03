# scaffold/artisans/pad.py

import importlib.util
import inspect
import sys
import traceback
from pathlib import Path
from typing import Type

from textual.app import App

from ..contracts.heresy_contracts import ArtisanHeresy
from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import PadRequest
from ..studio.pads.pad_launcher import PAD_GRIMOIRE, _adjudicate_dependencies, _proclaim_pad_dossier


class PadArtisan(BaseArtisan[PadRequest]):
    """
    @gnosis:title The Gnostic Pad (`pad`)
    @gnosis:summary Launches a specific, lightweight TUI 'Pad' for focused tasks (e.g., beautify, help).
    """

    def execute(self, request: PadRequest) -> ScaffoldResult:
        pad_to_summon = request.pad_name.lower()

        # 1. The Gnostic Inquisitor (Help)
        if pad_to_summon == 'help':
            _proclaim_pad_dossier()
            return self.success("Pad Dossier proclaimed.")

        # 2. The Gnostic Triage
        pad_gnosis = PAD_GRIMOIRE.get(pad_to_summon)
        if not pad_gnosis:
            raise ArtisanHeresy(
                f"The cosmos knows no Gnostic Pad named '{pad_to_summon}'.",
                suggestion=f"Speak `scaffold pad help` to see all known rites."
            )

        self.logger.info(f"The Nexus prepares to summon the '{pad_to_summon}' Pad...")

        try:
            # 3. The Sentinel of Dependencies
            _adjudicate_dependencies(pad_gnosis.get("dependencies", []))

            # 4. The Just-In-Time Alchemist (Dynamic Import)
            # We must resolve the package relative to the pad_launcher's location
            package_base = "scaffold.studio.pads"
            module_path = pad_gnosis["module_path"]  # e.g. ".distill_pad.distill_pad_app"

            # [DIAGNOSTIC] Proclaim intent to import
            # self.logger.verbose(f"Importing module: {module_path} from {package_base}")

            pad_module = importlib.import_module(module_path, package=package_base)
            PadClass: Type[App] = getattr(pad_module, pad_gnosis["class_name"])

            # 5. The Rite of Introspection (Dynamic Argument Injection)
            sig = inspect.signature(PadClass.__init__)
            pad_kwargs = {}

            # Gnosis: Project Root
            if 'project_root' in sig.parameters:
                pad_kwargs['project_root'] = self.project_root

            # Gnosis: Initial File Path
            if 'initial_file_path' in sig.parameters and request.initial_path:
                initial_path = Path(request.initial_path).resolve()
                if initial_path.exists():
                    pad_kwargs['initial_file_path'] = initial_path
                else:
                    self.logger.warn(
                        f"Initial path '{request.initial_path}' is a void. The Pad will be born without it.")

            # 6. The Divine Delegation
            self.logger.verbose(f"Summoning '{PadClass.__name__}' with Gnosis: {list(pad_kwargs.keys())}...")
            pad_instance = PadClass(**pad_kwargs)

            # [CRITICAL] We run the app. If this returns immediately without UI, it crashed during startup.
            pad_instance.run()

            return self.success(f"Communion with '{pad_to_summon}' complete.")

        except ImportError as e:
            # [DIAGNOSTIC] Raw scream to stderr
            sys.__stderr__.write(f"\n[CRITICAL IMPORT ERROR] {e}\n")
            traceback.print_exc(file=sys.__stderr__)

            raise ArtisanHeresy(
                "The Gnostic Pad requires divine allies.",
                suggestion=f"Install missing dependencies: {e.name}",
                child_heresy=e
            )
        except Exception as e:
            # [DIAGNOSTIC] Raw scream to stderr to bypass any Textual/Rich capturing
            sys.__stderr__.write(f"\n[CRITICAL PAD CRASH] {e}\n")
            traceback.print_exc(file=sys.__stderr__)

            raise ArtisanHeresy(
                f"A catastrophic paradox shattered the '{pad_to_summon}' Pad.",
                details=f"Initialization or Runtime failure in '{pad_gnosis.get('class_name', 'Unknown')}'.\nSee stderr for traceback.",
                child_heresy=e
            ) from e