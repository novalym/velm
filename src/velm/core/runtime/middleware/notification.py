# Path: scaffold/core/runtime/middleware/notification.py
# ------------------------------------------------------

import os
import time
import threading
import platform
from .contract import Middleware, NextHandler
from ....interfaces.requests import BaseRequest
from ....interfaces.base import ScaffoldResult
from ....settings.manager import SettingsManager  # <-- New Import

# Try to import plyer for cross-platform toasts
try:
    from plyer import notification

    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False


class NotificationMiddleware(Middleware):
    """
    =============================================================================
    == THE TOWN CRIER (V-Ω-MULTIMODAL-HERALD)                                  ==
    =============================================================================
    Proclaims the conclusion of long rites via OS Toasts and Audible Cues.
    """

    THRESHOLD_SECONDS = 5.0
    SUCCESS_SOUND = "\a"  # Standard terminal bell
    FAILURE_SOUND = "\a\a"  # Two bells for failure

    def handle(self, request: BaseRequest, next_handler: NextHandler) -> ScaffoldResult:
        start_time = time.time()

        settings = SettingsManager(request.project_root)
        use_toasts = PLYER_AVAILABLE
        use_audio = settings.get("ui.audible_cues", False)

        result = next_handler(request)
        duration = time.time() - start_time

        is_long_rite = duration > self.THRESHOLD_SECONDS

        # --- [ASCENSION] The Rite of Proclamation ---
        if not request.non_interactive:
            if is_long_rite and use_toasts:
                self._dispatch_notification(request, result, duration)

            if use_audio:
                sound = self.SUCCESS_SOUND if result.success else self.FAILURE_SOUND
                self.engine.console.print(sound, end="")

        return result

    def _dispatch_notification(self, request: BaseRequest, result: ScaffoldResult, duration: float):
        """Fire and forget notification thread."""

        def _notify():
            try:
                status = "Success" if result.success else "Failed"
                rite = type(request).__name__.replace("Request", "")
                title = f"Scaffold: {rite} {status}"
                message = f"Completed in {duration:.1f}s.\n{result.message}"

                notification.notify(
                    title=title,
                    message=message,
                    app_name="Velm God-Engine",
                    timeout=10  # Show for 10 seconds
                )
            except Exception:
                # The Herald must never crash the Engine.
                pass

        t = threading.Thread(target=_notify, daemon=True)
        t.start()