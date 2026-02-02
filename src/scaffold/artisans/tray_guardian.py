# Path: scaffold/artisans/tray_guardian.py
# ----------------------------------------
import time
from pathlib import Path
from PIL import Image  # pystray requires Pillow
import pystray
from pystray import MenuItem as item

from ..logger import Scribe

Logger = Scribe("TrayGuardian")


class TrayGuardian:
    """
    =============================================================================
    == THE SYSTEM TRAY GUARDIAN                                                ==
    =============================================================================
    Provides a persistent, visible presence for the Gnostic Daemon.
    """

    def __init__(self, daemon_status_func, stop_func):
        self.get_status = daemon_status_func
        self.stop_daemon = stop_func
        self.icon = None

    def _create_icon_image(self):
        # Placeholder for a real icon file
        # For now, we create a simple 64x64 image
        width = 64
        height = 64
        # A simple blue 'S'
        image = Image.new('RGB', (width, height), 'black')
        # In a real implementation, we would use ImageDraw to draw the letter
        return image

    def run(self):
        try:
            image = self._create_icon_image()

            menu = (
                item('Status: Unknown', self._update_status, enabled=False),
                item('Stop Daemon', self._on_stop),
                item('Quit Guardian', self._on_quit)
            )

            self.icon = pystray.Icon("scaffold_daemon", image, "Scaffold Daemon", menu)
            self.icon.run()
        except ImportError:
            Logger.error("The Tray Guardian requires 'pystray' and 'pillow'. `pip install pystray pillow`")
        except Exception as e:
            Logger.error(f"Tray Guardian shattered: {e}")

    def _update_status(self):
        # This would be called periodically to update the menu item
        pass

    def _on_stop(self):
        self.stop_daemon()
        self.icon.stop()

    def _on_quit(self, icon, item):
        icon.stop()


# Example usage (would be called from a new CLI command `scaffold daemon --with-tray`)
if __name__ == "__main__":
    def get_mock_status(): return "Running"


    def stop_mock(): print("Stopping daemon...")


    guardian = TrayGuardian(get_mock_status, stop_mock)
    guardian.run()