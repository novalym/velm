# Path: scaffold/artisans/qr/artisan.py
# -------------------------------------

import socket
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import QRRequest
from ...help_registry import register_artisan

# Graceful degradation
try:
    import qrcode
    from rich.align import Align
    from rich.text import Text

    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


@register_artisan("qr")
class QRArtisan(BaseArtisan[QRRequest]):
    """
    =============================================================================
    == THE VISUAL BRIDGE (V-Ω-MOBILE-LINK)                                     ==
    =============================================================================
    LIF: 10,000,000,000

    Generates a QR code in the terminal pointing to the local machine's LAN IP.
    """

    def execute(self, request: QRRequest) -> ScaffoldResult:
        if not QR_AVAILABLE:
            return self.failure("The 'qrcode' artisan is missing. `pip install qrcode`")

        local_ip = self._get_local_ip()
        if not local_ip:
            return self.failure("Could not divine the Local IP address.")

        url = f"http://{local_ip}:{request.port}"

        self.console.rule("[bold green]The Visual Bridge[/bold green]")
        self.console.print(f"Sanctum URL: [bold link={url}]{url}[/bold link]")

        # Generate QR
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(url)
        qr.make(fit=True)

        # Render to string using ASCII characters
        f = io.StringIO()
        qr.print_ascii(out=f)
        f.seek(0)
        qr_str = f.read()

        # Display centered
        self.console.print(Align.center(Text(qr_str, style="black on white")))
        self.console.print(Align.center("[dim]Scan to access locally[/dim]"))

        return self.success(f"Bridge opened at {url}")

    def _get_local_ip(self) -> str:
        """Divines the LAN IP by connecting to a public DNS (without sending data)."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Doesn't actually connect, just determines routing
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"


import io