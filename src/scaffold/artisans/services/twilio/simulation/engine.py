# Path: scaffold/artisans/services/twilio/simulation/engine.py
# ------------------------------------------------------------

import logging
from typing import Dict, Any

from .....interfaces.requests import TwilioRequest
from .....interfaces.base import ScaffoldResult
from ..constants import COST_SMS_LOCAL, COST_NUMBER_LOCAL
from .generators import PhantomGenerator
from .physics import CarrierPhysics
from .state import SimState
from .reactor import CallbackReactor

Logger = logging.getLogger("PhantomEngine")


class PhantomEngine:
    """
    =============================================================================
    == THE PHANTOM LATTICE (V-Ω-DIGITAL-TWIN)                                  ==
    =============================================================================
    A high-fidelity simulation of the Global Carrier Network.

    Capabilities:
    1. Stateful Memory (Remembers bought numbers).
    2. Physics-Based Latency (Calculates drag based on message size).
    3. Chaos Injection (Simulates specific error codes via trigger words).
    4. Webhook Reactor (Fires real HTTP callbacks to localhost).
    """

    def execute(self, request: TwilioRequest) -> ScaffoldResult:
        action = request.action.lower()
        Logger.info(f"⚡ [PHANTOM] Intercepting Rite: {action}")

        if action in ["send", "send_sms", "send_mms"]:
            return self._mock_send(request)

        elif action == "search":
            return self._mock_search(request)

        elif action == "buy":
            return self._mock_buy(request)

        elif action == "configure":
            return self._mock_configure(request)

        elif action == "link_number":
            return ScaffoldResult(success=True, message=f"[SIM] Number linked to Service.")

        elif action == "lookup":
            return self._mock_lookup(request)

        return ScaffoldResult(success=False, message=f"[SIM] Unknown Rite: {action}")

    def _mock_send(self, req: TwilioRequest):
        # 1. Physics Calculation
        body_len = len(req.body or "")
        media_count = len(req.media_url) if req.media_url else 0
        latency = CarrierPhysics.calculate_latency(body_len, media_count)

        # 2. Chaos Adjudication
        chaos = CarrierPhysics.adjudicate_chaos(req.body, req.to_number)

        # 3. Simulate Physics (Sleep)
        time.sleep(latency)

        # 4. Handle Failure (Chaos)
        if chaos:
            code, msg = chaos
            Logger.warning(f"[PHANTOM] Chaos Triggered: {code} - {msg}")
            return ScaffoldResult(
                success=False,
                message=f"Carrier Rejection: {msg}",
                error=msg,
                data={"code": code, "status": "failed"}
            )

        # 5. Handle Blacklist (State)
        if SimState.check_blacklist(req.to_number):
            return ScaffoldResult(
                success=False,
                message="Carrier Rejection: The Blacklist. User has opted out.",
                data={"code": 21610, "status": "failed"}
            )

        # 6. Success Manifestation
        sid = PhantomGenerator.sid("SM")

        # 7. Reactor Ignition (Webhooks)
        if req.status_callback:
            CallbackReactor.simulate_lifecycle(req.status_callback, sid, "delivered")

        # 8. State Persistence
        SimState.log_message({
            "sid": sid, "to": req.to_number, "body": req.body,
            "status": "queued", "ts": time.time()
        })

        return ScaffoldResult(
            success=True,
            message=f"[PHANTOM] Signal Manifest: {sid}",
            data={
                "sid": sid,
                "status": "queued",
                "price": PhantomGenerator.price(COST_SMS_LOCAL),
                "direction": "outbound-api",
                "latency_ms": latency * 1000
            }
        )

    def _mock_search(self, req: TwilioRequest):
        area = req.area_code or "555"
        count = req.limit or 5

        results = []
        for _ in range(count):
            num = PhantomGenerator.phone_number(area)
            meta = PhantomGenerator.node_metadata(num)
            results.append(meta)

        return ScaffoldResult(
            success=True,
            message=f"[PHANTOM] Scrying complete. {len(results)} nodes found.",
            data=results
        )

    def _mock_buy(self, req: TwilioRequest):
        sid = PhantomGenerator.sid("PN")
        num = req.phone_number or PhantomGenerator.phone_number("555")

        # Persist the Asset
        SimState.acquire_node(num, sid, {"friendly": req.friendly_name})

        return ScaffoldResult(
            success=True,
            message=f"[PHANTOM] Node {num} acquired.",
            data={
                "sid": sid,
                "phone_number": num,
                "status": "in-use",
                "price": COST_NUMBER_LOCAL
            }
        )

    def _mock_configure(self, req: TwilioRequest):
        # Update State?
        return ScaffoldResult(success=True, message=f"[PHANTOM] Node {req.phone_number or req.sid} re-tuned.")

    def _mock_lookup(self, req: TwilioRequest):
        return ScaffoldResult(
            success=True,
            message=f"[PHANTOM] Revelation: {req.phone_number} is mobile.",
            data={
                "caller_name": {"caller_name": "Phantom User", "caller_type": "CONSUMER"},
                "carrier": {"name": "Phantom Wireless", "type": "mobile"}
            }
        )