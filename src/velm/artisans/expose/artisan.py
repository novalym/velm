# Path: scaffold/artisans/expose/artisan.py
# -----------------------------------------

import time
from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import ExposeRequest
from ...help_registry import register_artisan
from ...core.net.tunnel import TunnelWeaver


@register_artisan("expose")
class ExposeArtisan(BaseArtisan[ExposeRequest]):
    """
    =============================================================================
    == THE PORT KEY (V-Ω-PUBLIC-GATEWAY)                                       ==
    =============================================================================
    LIF: 10,000,000,000

    Exposes a local port to the public internet via a secure SSH tunnel.
    """

    def execute(self, request: ExposeRequest) -> ScaffoldResult:
        port = request.port
        provider = request.provider

        # Forge the SSH Spec
        # localhost.run syntax: ssh -R 80:localhost:PORT nokey@localhost.run
        if provider == "localhost.run":
            user_host = "nokey@localhost.run"
            # Note: localhost.run ignores the bound port (80), it assigns a random domain
            spec = f"{user_host} -R 80:localhost:{port}"
        elif provider == "serveo":
            user_host = "serveo.net"
            spec = f"{user_host} -R 80:localhost:{port}"
        else:
            return self.failure(f"Unknown provider: {provider}")

        self.logger.info(f"Forging Port Key for localhost:{port} via {provider}...")

        try:
            weaver = TunnelWeaver()
            # The Weaver runs in background.
            # For 'expose', we usually want to block and show the URL until Ctrl+C.
            # But TunnelWeaver is designed for background.
            # We will use the Weaver's logic but keep the main thread alive.

            pid = weaver.weave(spec)

            self.console.print(f"[bold green]✓ Tunnel Active (PID {pid})[/bold green]")
            self.console.print(f"Check your terminal output or {provider} logs for the public URL.")
            self.console.print("[dim]Press Ctrl+C to close the portal.[/dim]")

            # Keep alive
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            # Weaver handles cleanup on exit via SystemManager hooks usually,
            # but we can explicitly close here.
            weaver.close_all()
            return self.success("Portal closed.")
        except Exception as e:
            return self.failure(f"The Port Key shattered: {e}")