import socket
import subprocess
import shutil

try:
    import urllib.request

    URLLIB_AVAILABLE = True
except ImportError:
    URLLIB_AVAILABLE = False

from typing import Tuple
from .base import BaseVowHandler


class NetworkVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE ORACLE OF THE VOID (NETWORK & DOCKER)                               ==
    =============================================================================
    Judges connectivity and celestial vessels (Docker).
    """

    def _vow_port_open(self, port: str) -> Tuple[bool, str]:
        try:
            with socket.create_connection(("127.0.0.1", int(port)), timeout=1):
                return True, f"Port {port} is open."
        except:
            return False, f"Port {port} is closed."

    def _vow_url_reachable(self, url: str) -> Tuple[bool, str]:
        if not URLLIB_AVAILABLE: return False, "urllib missing."
        try:
            code = urllib.request.urlopen(url, timeout=2).getcode()
            return 200 <= code < 300, f"URL {url} responded {code}."
        except Exception as e:
            return False, f"URL {url} unreachable: {e}"

    def _vow_docker_running(self) -> Tuple[bool, str]:
        if not shutil.which("docker"): return False, "Docker binary missing."
        try:
            subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            return True, "Docker Daemon is awake."
        except:
            return False, "Docker Daemon is dormant."

    def _vow_image_exists(self, image: str) -> Tuple[bool, str]:
        try:
            subprocess.run(["docker", "image", "inspect", image], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           check=True)
            return True, f"Image '{image}' found."
        except:
            return False, f"Image '{image}' missing."

    def _vow_port_available(self, port: str) -> Tuple[bool, str]:
        """
        [THE SENTINEL OF THE VOID]
        Asserts that a TCP port is free (not listening).
        """
        try:
            # We attempt to bind to the port. If we succeed, it is available.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # set REUSEADDR to avoid false negatives from lingering timewaits
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind(("127.0.0.1", int(port)))
                return True, f"Port {port} is available."
        except OSError:
            return False, f"Port {port} is occupied."
        except Exception as e:
            return False, f"Port check paradox: {e}"