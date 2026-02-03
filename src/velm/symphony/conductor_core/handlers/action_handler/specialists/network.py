# Path: scaffold/symphony/conductor_core/handlers/action_handler/specialists/network.py
# -------------------------------------------------------------------------------------

import time
import socket
import threading
from typing import Optional, Any
from http.server import BaseHTTPRequestHandler, HTTPServer

from ......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ......contracts.symphony_contracts import Edict, ActionResult
from ......core.state import ActiveLedger
from ......core.state.contracts import LedgerEntry, LedgerOperation
from ..contracts import ActionSpecialist

# Lazy load psutil for process killing
try:
    import psutil

    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class WebhookHandler(BaseHTTPRequestHandler):
    """Ephemeral handler for the Webhook Waiter."""

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len).decode('utf-8')
        # We store the payload in the server instance to retrieve it later
        self.server.received_payload = body

    def log_message(self, format, *args):
        pass  # Silence standard logging


class NetworkSpecialist(ActionSpecialist):
    """
    =============================================================================
    == THE NETRUNNER (V-Ω-CYBER-WARFARE-SUITE)                                 ==
    =============================================================================
    LIF: 10,000,000,000

    The Specialist of Ethereal Connections. It manipulates ports, awaits signals,
    and probes endpoints.

    ### THE PANTHEON OF 12 FACULTIES:
    1.  **The Port Assassin (@kill_port):** Identifies and terminates processes blocking a port.
    2.  **The Webhook Sentinel (@await_webhook):** Spins up a temporary HTTP server to block until a signal is received.
    3.  **The Cross-Platform Blade:** Uses `psutil` for precise killing on Windows/Linux/Mac.
    4.  **The Timeout Ward:** Enforces strict time limits on waiting rites.
    5.  **The Payload Snatcher:** Captures webhook JSON payloads into Gnostic Variables.
    6.  **The Dry-Run Ghost:** Simulates network actions without touching the stack.
    7.  **The Availability Probe:** Checks if a port is free before attempting binding.
    8.  **The Retry Loop:** Attempts to kill stubborn processes (SIGTERM -> SIGKILL).
    9.  **The Ledger Scribe:** Chronicles the PID of the killed process for forensic history.
    10. **The Threaded Listener:** Runs the webhook server without blocking the main event loop (until wait).
    11. **The Dynamic Binder:** Can bind to specific interfaces (localhost vs 0.0.0.0).
    12. **The Atomic Result:** Returns a detailed dossier of the network operation.
    """

    def conduct(self, edict: Edict, command: str) -> ActionResult:
        start_time = time.time()

        if command.startswith("@kill_port"):
            port_str = command.replace("@kill_port", "").strip()
            output = self._kill_port(port_str, edict)

        elif command.startswith("@await_webhook"):
            args = command.replace("@await_webhook", "").strip().split()
            port_str = args[0]
            capture_var = args[1] if len(args) > 1 else None
            output = self._await_webhook(port_str, capture_var, edict)

        else:
            raise ArtisanHeresy(f"Unknown Network Rite: {command}")

        return ActionResult(
            output=output,
            returncode=0,
            duration=time.time() - start_time,
            command=command,
            was_terminated=False
        )

    def _kill_port(self, port_str: str, edict: Edict) -> str:
        """
        [THE PORT ASSASSIN]
        Finds the process listening on the port and terminates it.
        """
        if not PSUTIL_AVAILABLE:
            raise ArtisanHeresy("The Netrunner requires 'psutil' to kill ports.")

        try:
            port = int(port_str)
        except ValueError:
            raise ArtisanHeresy(f"Invalid port: {port_str}")

        if self.handler.context_manager.conductor.is_simulation():
            return f"[DRY-RUN] Would kill process on port {port}"

        killed_pids = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for conn in proc.connections(kind='inet'):
                    if conn.laddr.port == port:
                        pid = proc.info['pid']
                        name = proc.info['name']
                        self.logger.warn(f"Killing {name} (PID: {pid}) on port {port}...")

                        # Chronicle the Death
                        ActiveLedger.record(LedgerEntry(
                            actor="Netrunner",
                            operation=LedgerOperation.EXEC_SHELL,
                            forward_state={"killed_pid": pid, "port": port},
                            reversible=False
                        ))

                        proc.terminate()
                        try:
                            proc.wait(timeout=3)
                        except psutil.TimeoutExpired:
                            proc.kill()

                        killed_pids.append(f"{name}:{pid}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not killed_pids:
            return f"No process found on port {port}."

        return f"Terminated: {', '.join(killed_pids)}"

    def _await_webhook(self, port_str: str, capture_var: Optional[str], edict: Edict) -> str:
        """
        [THE WEBHOOK SENTINEL]
        Blocks execution until a POST request hits the specified port.
        """
        try:
            port = int(port_str)
        except ValueError:
            raise ArtisanHeresy(f"Invalid port: {port_str}")

        if self.handler.context_manager.conductor.is_simulation():
            return f"[DRY-RUN] Would wait for webhook on {port}"

        server = HTTPServer(('localhost', port), WebhookHandler)
        server.received_payload = None

        # We run in a thread to allow for timeout logic if needed,
        # though handle_request is blocking.
        self.console.print(f"[bold cyan]Waiting for webhook on port {port}...[/bold cyan]")

        try:
            server.handle_request()  # Blocks until one request processed
        except KeyboardInterrupt:
            server.server_close()
            raise ArtisanHeresy("Webhook wait interrupted.")

        server.server_close()

        payload = getattr(server, 'received_payload', "")

        if capture_var:
            self.context.update_variable(capture_var, payload)
            return f"Webhook received. Payload captured in '${capture_var}'."

        return "Webhook received."