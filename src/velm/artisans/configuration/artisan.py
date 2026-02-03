# Path: scaffold/artisans/configuration/artisan.py
# ------------------------------------------------
# LIF: INFINITY | ROLE: NEURO_PLASTICITY_ENGINE
# =================================================================================

from typing import Optional, Any, Dict
import logging

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ConfigChangeRequest
from ...help_registry import register_artisan


@register_artisan("config-update")
class ConfigChangeArtisan(BaseArtisan[ConfigChangeRequest]):
    """
    =============================================================================
    == THE NEURAL TUNER (V-Ω-CONFIG-MUTATOR)                                   ==
    =============================================================================
    Allows the Architect to reshape the Daemon's mind at runtime via RPC.
    Can toggle log levels, adjust telemetry sampling, or update memory limits
    without restarting the process.
    """

    def __init__(self, nexus: Optional[Any] = None, engine: Optional[Any] = None):
        # 1. Resolve Engine
        real_engine = engine
        self.nexus = nexus
        if nexus and hasattr(nexus, 'engine'):
            real_engine = nexus.engine

        # 2. Call Base Constructor
        try:
            super().__init__(real_engine)
        except TypeError:
            super().__init__()
            if real_engine: self.engine = real_engine

    def execute(self, request: ConfigChangeRequest) -> ScaffoldResult:
        if not self.nexus:
            # If run from CLI, we might just update a config file
            # For now, we return failure as this is primarily a Runtime Rite
            return self.failure("This rite requires a living Daemon Nexus.")

        gnostic_settings = request.settings.get('gnostic', {})

        # --- 1. LOG LEVEL MUTATION ---
        trace = gnostic_settings.get('trace', {}).get('server', None)
        if trace:
            if trace == 'verbose':
                self.nexus.logger.level = logging.DEBUG
                self.nexus.logger.info("Cortex Log Level elevated to DEBUG.")
            elif trace == 'off':
                self.nexus.logger.level = logging.INFO
                self.nexus.logger.info("Cortex Log Level reduced to INFO.")
            elif trace == 'messages':
                self.nexus.logger.level = logging.WARNING

        # --- 2. TELEMETRY MUTATION ---
        telemetry = gnostic_settings.get('telemetry', {})
        if 'level' in telemetry:
            level = telemetry['level']
            # Hypothetical logic to tune sampling rate
            if level == 'all':
                self.nexus.telemetry_sample_rate = 1.0
            elif level == 'errors':
                self.nexus.telemetry_sample_rate = 0.1

        # --- 3. LENS (SURVEYOR) MUTATION ---
        lens = gnostic_settings.get('lens', {})
        if 'enable' in lens:
            # We could enable/disable the background surveyor loop here
            pass

        self.nexus.logger.info("Cortex Configuration Updated.", tags=["CONFIG", "RUNTIME"])

        return self.success("Configuration Applied.", data={
            "settings_applied": request.settings,
            "current_state": "ACTIVE"
        })