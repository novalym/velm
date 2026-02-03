# Path: scaffold/artisans/services/twilio/simulation/reactor.py
# -------------------------------------------------------------

import threading
import time
import requests
import logging
from typing import Dict, Any

Logger = logging.getLogger("PhantomReactor")


class CallbackReactor:
    """
    [THE CALLBACK CANNON]
    Spawns background threads to fire HTTP webhooks back to the Kernel.
    Simulates the asynchronous nature of carrier delivery reports.
    """

    @staticmethod
    def dispatch_status(url: str, message_sid: str, status: str, delay: float = 1.0, data: Dict = None):
        """
        Schedules a status callback (e.g., 'sent', 'delivered').
        """
        if not url: return

        def _fire():
            time.sleep(delay)
            payload = {
                "MessageSid": message_sid,
                "MessageStatus": status,
                "ApiVersion": "2010-04-01",
                "SmsSid": message_sid,
                "SmsStatus": status,
                **(data or {})
            }
            try:
                # [SECURITY WARD]: Only fire to localhost in simulation
                if "localhost" in url or "127.0.0.1" in url:
                    Logger.debug(f"Firing Phantom Callback ({status}) -> {url}")
                    requests.post(url, data=payload, timeout=2)
            except Exception as e:
                Logger.warning(f"Phantom Callback Fractured: {e}")

        t = threading.Thread(target=_fire, daemon=True)
        t.start()

    @staticmethod
    def simulate_lifecycle(url: str, sid: str, final_status: str = "delivered"):
        """
        Simulates the full lifecycle: Queued -> Sending -> Sent -> Delivered.
        """
        # 1. Queued (Immediate)
        CallbackReactor.dispatch_status(url, sid, "queued", delay=0.1)

        # 2. Sending (Short delay)
        CallbackReactor.dispatch_status(url, sid, "sending", delay=0.5)

        # 3. Sent (Carrier Handover)
        CallbackReactor.dispatch_status(url, sid, "sent", delay=1.0)

        # 4. Final State (Delivered/Undelivered/Failed)
        CallbackReactor.dispatch_status(url, sid, final_status, delay=2.0)