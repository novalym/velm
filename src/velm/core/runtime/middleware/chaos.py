# Path: scaffold/core/runtime/middleware/chaos.py

import os
import random
from typing import List, Dict, Any

from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....contracts.heresy_contracts import ArtisanHeresy
from ....logger import Scribe

# The Gnostic Link: We summon the ChaosEngine, but with a graceful fallback.
try:
    from ....core.chaos_engine import ChaosEngine

    CHAOS_ENGINE_AVAILABLE = True
except ImportError:
    ChaosEngine = None
    CHAOS_ENGINE_AVAILABLE = False

Logger = Scribe("ChaosConductor")


class ChaosMiddleware(Middleware):
    """
    =============================================================================
    == THE GRAND INQUISITOR OF ENTROPY (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)         ==
    =============================================================================
    The divine Conductor that perceives the will for chaos, summons the ChaosEngine
    to inject entropy, and guarantees the restoration of a pure reality.
    =============================================================================
    """

    # [FACULTY 1] The Gnostic Triage of Rites
    # We now define which types of chaos are relevant for each rite.
    RESILIENCE_RITE_PROFILES: Dict[str, List[str]] = {
        'RunRequest': ["io", "resource", "time"],
        'SymphonyRequest': ["network", "io", "resource", "time"],
        'GenesisRequest': ["io", "resource", "time"],
        'TransmuteRequest': ["io"],
        'FreezeRequest': ["network"],
    }

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        # 1. The Gaze of Intent (Environment > CLI)
        chaos_mode_str = os.getenv("SCAFFOLD_CHAOS_MODE") or getattr(request, 'chaos', None)
        request_type = request.__class__.__name__

        # [FACULTY 9] The Seed of Determinism
        chaos_seed = getattr(request, 'chaos_seed', None)
        if chaos_seed:
            random.seed(chaos_seed)
            Logger.warn(f"[CHAOS] Randomness has been seeded with '{chaos_seed}'. The storm will be identical.")

        # 2. Adjudicate Applicability
        applicable_chaos_domains = self.RESILIENCE_RITE_PROFILES.get(request_type)
        if not chaos_mode_str or not applicable_chaos_domains:
            return next_handler(request)

        # 3. Graceful Degradation
        if not CHAOS_ENGINE_AVAILABLE:
            self.logger.error("The ChaosEngine artisan is not manifest. The rite will proceed in a pure state.")
            return next_handler(request)

        # 4. The Gnostic Parser Ascended
        chaos_settings = self._parse_chaos_string(chaos_mode_str, applicable_chaos_domains)
        if not chaos_settings:
            self.logger.warn(
                f"Chaos vow '{chaos_mode_str}' was not understood or not applicable. Proceeding without chaos.")
            return next_handler(request)

        # 5. [FACULTY 10] The Dry-Run Prophet
        if request.dry_run:
            self.logger.info("[DRY-RUN] The Chaos Syringe is armed but its hand is stayed.")
            result = next_handler(request)
            if result.data is None: result.data = {}
            result.data['chaos_prophecy'] = {"injected": False, "settings": chaos_settings}
            return result

        # 6. Summon the Artisan of Entropy
        syringe = ChaosEngine(settings=chaos_settings)

        try:
            # 7. The Rite of Injection
            syringe.inject()

            # 8. Conduct the (Now Chaotic) Rite
            result = next_handler(request)
            return result

        finally:
            # 9. [FACULTY 4] The Unbreakable Vow of Restoration
            syringe.retract()

            # 10. [FACULTY 5] The Forensic Dossier Ascended
            # Ensure 'result' exists before modifying it (handles crashes in `next_handler`)
            if 'result' in locals() and result:
                if result.data is None: result.data = {}
                result.data['chaos_report'] = {
                    "injected": True,
                    "scripture": chaos_mode_str,
                    "parsed_settings": chaos_settings,
                    "events_triggered": syringe.events_triggered
                }

    def _parse_chaos_string(self, chaos_str: str, applicable_domains: List[str]) -> List[Dict[str, Any]]:
        """
        [FACULTY 2] The Polyglot Parser Ascended.
        Parses: "network:latency:0.5,io:failure:0.1:path=*/db.py"
        """
        settings = []
        parts = chaos_str.split(',')
        valid_types = {
            "network": ["latency", "failure", "http_error"],
            "io": ["latency", "failure", "corruption"],
            "resource": ["memory_spike", "cpu_spike"],
            "time": ["warp"]
        }

        for part in parts:
            try:
                segments = part.split(':')
                # Handle simple modes like --chaos=latency
                if len(segments) == 1:
                    # Find which domain this chaos type belongs to
                    found = False
                    for domain, types in valid_types.items():
                        if segments[0] in types:
                            if domain in applicable_domains:
                                settings.append({"type": f"{domain}_{segments[0]}", "probability": 0.3})
                                found = True
                                break
                    if not found and segments[0] == "full":
                        # Unleash the full, applicable storm
                        for domain in applicable_domains:
                            if domain == "network":
                                settings.append({"type": "network_latency", "probability": 0.3})
                                settings.append({"type": "network_failure", "probability": 0.1})
                            if domain == "io":
                                settings.append({"type": "io_failure", "probability": 0.05})
                    continue

                domain, chaos_type = segments[0], segments[1]

                # Check if this chaos is relevant for the current rite
                if domain not in applicable_domains:
                    self.logger.verbose(f"Skipping chaos '{part}': Domain '{domain}' is not applicable to this rite.")
                    continue

                probability = float(segments[2]) if len(segments) > 2 and segments[2] else 0.3

                # Surgical Targeting
                target_info = {}
                if len(segments) > 3:
                    target_str = segments[3]
                    if '=' in target_str:
                        key, value = target_str.split('=', 1)
                        target_info["target_key"] = key
                        target_info["target"] = value

                if domain in valid_types and chaos_type in valid_types[domain]:
                    settings.append({
                        "type": f"{domain}_{chaos_type}",
                        "probability": probability,
                        **target_info
                    })
                else:
                    self.logger.warn(f"Unknown chaos directive: '{part}'")
            except (ValueError, IndexError):
                self.logger.warn(f"Malformed chaos directive: '{part}'")

        return settings