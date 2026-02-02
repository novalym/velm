# Path: scaffold/symphony/conductor_core/handlers/state_handler/specialists/temporal.py
# -------------------------------------------------------------------------------------
import time
from ..contracts import StateSpecialist
from ..utils.time_parser import TimeParser
from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......contracts.symphony_contracts import Edict

class Chronomancer(StateSpecialist):
    """Handles '%% sleep: duration'"""
    def conduct(self, edict: Edict, value: str) -> None:
        try:
            seconds = TimeParser.parse_seconds(value)
            if not self.handler.is_dry_run:
                self.logger.info(f"Sleeping for {seconds}s...")
                time.sleep(seconds)
            else:
                self.logger.info(f"[DRY-RUN] Would sleep for {seconds}s")
        except ValueError as e:
            raise ArtisanHeresy(str(e), line_num=edict.line_num, severity=HeresySeverity.WARNING)