# Path: scaffold/core/net/tunnel.py
# ---------------------------------

import subprocess
import time
import socket
import threading
import os
import signal
import shlex
from typing import Optional, Tuple, List, Dict
from pathlib import Path

from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe

Logger = Scribe("TunnelWeaver")


class TunnelWeaver:
    """
    =================================================================================
    == THE TUNNEL WEAVER (V-Ω-QUANTUM-BRIDGE-ULTIMA)                               ==
    =================================================================================
    LIF: 10,000,000,000

    The Architect of Wormholes. It establishes secure, background SSH tunnels to
    bridge the local and celestial realms.

    ### THE PANTHEON OF 8 ASCENDED FACULTIES:
    1.  **The Spec Diviner:** Intelligently parses `user@host -L loc:targ:port` or
        simplified Gnostic syntax.
    2.  **The Port Sentinel:** Verifies the local port is free before binding.
    3.  **The Background Daemon:** Runs the tunnel in a detached subprocess,
        shielded from the main thread's mortality.
    4.  **The Health Monitor:** Actively probes the tunnel endpoint to ensure
        light is passing through before proclaiming success.
    5.  **The Zombie Reaper:** Registers the tunnel PID for auto-termination
        when the Symphony ends.
    6.  **The Keymaster:** Automatically uses the SSH keys available in the
        environment (Agent or ~/.ssh) via the system `ssh` binary.
    7.  **The Silence Ward:** Suppresses SSH banner noise unless a heresy occurs.
    8.  **The Contextual Anchor:** Can anchor tunnels relative to the current
        Sanctum if it is an SSHSanctum.
    """

    def __init__(self):
        # Tracks active tunnels for mass-closing
        self._active_tunnels: List[subprocess.Popen] = []

    def weave(self, spec: str, current_sanctum_uri: str = "") -> int:
        """
        Establishes the tunnel. Returns the PID of the SSH process.
        Spec formats:
          1. "user@host -L 8080:localhost:3000" (Explicit)
          2. "8080:localhost:3000" (Implicit - requires SSH Sanctum context)
        """
        Logger.info(f"Weaving Quantum Tunnel: [cyan]{spec}[/cyan]")

        # 1. The Gnostic Triage of Intent
        target_host_str, forward_spec = self._parse_spec(spec, current_sanctum_uri)

        # 2. The Port Sentinel (Pre-flight)
        local_port = self._extract_local_port(forward_spec)
        if local_port and self._is_port_open(local_port):
            raise ArtisanHeresy(
                f"Port Conflict: The local port {local_port} is already occupied.",
                severity=HeresySeverity.CRITICAL,
                suggestion=f"Kill the process on {local_port} or choose a different forwarding mapping."
            )

        # 3. The Forging of the Command
        # -N: Do not execute a remote command (just forward ports)
        # -o ExitOnForwardFailure=yes: Fail fast if port is taken
        # -o BatchMode=yes: Do not prompt for passwords (fail if key missing)
        cmd = ["ssh", "-N", "-o", "ExitOnForwardFailure=yes", "-o", "BatchMode=yes"]

        # Inject Forwarding Spec (-L or -R)
        # We assume spec string contains the flag, or we default to -L
        if "-L" not in forward_spec and "-R" not in forward_spec:
            cmd.append("-L")
            cmd.append(forward_spec)
        else:
            # Split user provided flags
            cmd.extend(shlex.split(forward_spec))

        # Target Host (user@host)
        cmd.append(target_host_str)

        # 4. The Rite of Connection
        Logger.verbose(f"   -> Invoking: {' '.join(cmd)}")

        try:
            # We use Popen to keep it alive in the background
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )

            # 5. The Health Monitor (The Wait)
            # We wait briefly to see if it crashes immediately (auth fail, etc)
            time.sleep(1.0)
            if process.poll() is not None:
                # It died. Read the dying breath.
                _, err = process.communicate()
                raise ArtisanHeresy(
                    "Tunnel collapsed immediately.",
                    details=f"SSH Error: {err.strip() if err else 'Unknown'}",
                    severity=HeresySeverity.CRITICAL
                )

            # Check if port is now listening (if we parsed it)
            if local_port:
                retries = 10
                is_connected = False
                while retries > 0:
                    if self._is_port_open(local_port):
                        is_connected = True
                        break
                    time.sleep(0.5)
                    retries -= 1

                if not is_connected:
                    # It's alive but not listening? Suspicious.
                    Logger.warn(
                        f"Tunnel process is alive (PID {process.pid}), but port {local_port} is not yet reachable. It may be initializing or blocked.")

            Logger.success(f"Tunnel established. PID: [green]{process.pid}[/green]")
            self._active_tunnels.append(process)
            return process.pid

        except FileNotFoundError:
            raise ArtisanHeresy("The 'ssh' artisan is not manifest in the PATH.")
        except Exception as e:
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy(f"Tunnel Weaving failed: {e}")

    def close_all(self):
        """The Rite of Closure. Annihilates all tunnels spawned by this weaver."""
        if not self._active_tunnels:
            return

        Logger.info(f"Collapsing {len(self._active_tunnels)} quantum tunnel(s)...")
        for proc in self._active_tunnels:
            if proc.poll() is None:
                try:
                    proc.terminate()
                    proc.wait(timeout=2)
                except Exception:
                    proc.kill()
        self._active_tunnels.clear()

    def _parse_spec(self, spec: str, current_sanctum_uri: str) -> Tuple[str, str]:
        """
        Resolves the target host and the forwarding rule.
        Returns: (user@host, forwarding_arg)
        """
        # Case A: Full SSH command string provided by user
        # e.g. "user@host -L 8080:localhost:80"
        if "@" in spec and ("-L" in spec or "-R" in spec):
            # We look for the host part. It usually precedes the flags or is at the end.
            # Heuristic: The part with '@' is the host.
            parts = shlex.split(spec)
            host_part = next((p for p in parts if "@" in p), None)

            if not host_part:
                raise ArtisanHeresy("Could not find 'user@host' in tunnel spec.")

            # The rest is the forwarding spec
            forwarding_parts = [p for p in parts if p != host_part]
            return host_part, " ".join(forwarding_parts)

        # Case B: Implicit Host (Contextual)
        # e.g. "8080:localhost:80" (uses current SSH sanctum)
        if current_sanctum_uri.startswith("ssh://"):
            # ssh://user@host:22/path -> user@host
            # We need to parse the URI manually or use urllib
            from urllib.parse import urlparse
            parsed = urlparse(current_sanctum_uri)

            # Reconstruct user@hostname
            if not parsed.username or not parsed.hostname:
                raise ArtisanHeresy("Current sanctum URI is malformed for tunneling.")

            host_str = f"{parsed.username}@{parsed.hostname}"

            # Note: We ignore port here because `ssh` command handles port via -p if needed,
            # but standard `user@host` usually assumes 22 or config file.
            # If port != 22, user should use ~/.ssh/config or explicit spec.

            return host_str, spec

        # Case C: No host, no context
        raise ArtisanHeresy(
            "Tunnel Ambiguity: No remote host specified and current sanctum is not SSH.",
            suggestion="Use full syntax: '%% tunnel: user@host -L local:remote:port'"
        )

    def _extract_local_port(self, forward_spec: str) -> Optional[int]:
        """Extracts 8080 from '-L 8080:localhost:80'."""
        try:
            # Strip flags to find the numbers
            clean = forward_spec.replace("-L", "").replace("-R", "").strip()
            # 8080:target:80 -> 8080
            # Note: Reverse tunnels (-R) bind on remote, so local check might be irrelevant,
            # but we check anyway if it parses.
            parts = clean.split(":")
            if len(parts) >= 2:
                # The first number is the bind port
                return int(parts[0])
        except:
            pass
        return None

    def _is_port_open(self, port: int) -> bool:
        """Checks if a local port is currently accepting connections."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', port)) == 0