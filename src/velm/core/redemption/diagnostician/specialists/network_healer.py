# Path: scaffold/core/redemption/diagnostician/specialists/network_healer.py
# --------------------------------------------------------------------------

import platform
from typing import Optional, Dict, Any
from ..contracts import Diagnosis


class NetworkHealer:
    """The Specialist of the Ethereal Connection."""

    @staticmethod
    def heal(exc: BaseException, context: Dict[str, Any]) -> Optional[Diagnosis]:
        msg = str(exc).lower()

        # 1. The Port Conflict
        if "address already in use" in msg or "10048" in msg or "eaddrinuse" in msg:
            port = context.get('port', 5555)
            system = platform.system()

            if system == "Windows":
                # Windows requires PowerShell or netstat magic
                cmd = f"netstat -ano | findstr :{port}"
                advice = f"Port {port} is occupied. Use Task Manager to kill the PID found by '{cmd}'."
            else:
                # Linux/Mac
                cmd = f"lsof -ti:{port} | xargs kill -9"
                advice = f"Port {port} is occupied. Execute the Rite of Liberation."

            return Diagnosis(
                heresy_name="PortConflict",
                cure_command=cmd if system != "Windows" else None,
                advice=advice,
                confidence=0.95,
                metadata={"port": port}
            )

        # 2. The Celestial Vessel (Docker)
        if "docker" in msg and ("connect" in msg or "socket" in msg or "daemon" in msg):
            system = platform.system()
            cmd = None
            if system == "Darwin":
                cmd = "open -a Docker"
            elif system == "Linux":
                cmd = "sudo systemctl start docker"
            elif system == "Windows":
                cmd = 'start "" "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"'

            return Diagnosis(
                heresy_name="DormantVessel",
                cure_command=cmd,
                advice="The Docker Daemon sleeps. Awaken it.",
                confidence=1.0,
                metadata={}
            )

        # 3. The Severed Link (Daemon Connection)
        import socket
        if isinstance(exc,
                      (ConnectionRefusedError, ConnectionResetError, socket.timeout)) or "connection refused" in msg:
            return Diagnosis(
                heresy_name="SeveredLink",
                cure_command="scaffold daemon start",
                advice="The Gnostic Nexus is unreachable. Start the Daemon.",
                confidence=0.9,
                metadata={}
            )

        return None