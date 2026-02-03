import subprocess
import json
from typing import Tuple
from .base import BaseVowHandler


class DockerOpsVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE CELESTIAL INSPECTOR (V-Ω-INTRA-CONTAINER-GAZE)                      ==
    =============================================================================
    Judges the internal reality of running containers.
    """

    def _vow_container_running(self, container_name: str) -> Tuple[bool, str]:
        """Asserts a specific container is UP."""
        try:
            res = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Running}}", container_name],
                capture_output=True, text=True
            )
            is_running = res.stdout.strip() == "true"
            return is_running, f"Container '{container_name}' is {'running' if is_running else 'stopped'}."
        except:
            return False, f"Container '{container_name}' not found."

    def _vow_container_healthy(self, container_name: str) -> Tuple[bool, str]:
        """Asserts a container passes its HEALTHCHECK."""
        try:
            res = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Health.Status}}", container_name],
                capture_output=True, text=True
            )
            status = res.stdout.strip()
            return status == "healthy", f"Container health is '{status}'."
        except:
            return False, f"Container '{container_name}' check failed."

    def _vow_container_log_contains(self, container_name: str, text: str) -> Tuple[bool, str]:
        """Gaze into the logs of a container."""
        try:
            res = subprocess.run(
                ["docker", "logs", "--tail", "1000", container_name],
                capture_output=True, text=True
            )
            logs = res.stdout + res.stderr
            return text in logs, f"Log {'contains' if text in logs else 'lacks'} '{text}'."
        except:
            return False, f"Could not read logs for '{container_name}'."

    def _vow_container_file_exists(self, container_name: str, file_path: str) -> Tuple[bool, str]:
        """
        The Teleporting Gaze. Checks if a file exists INSIDE the container.
        Uses `docker exec` to run a lightweight check.
        """
        try:
            # Use 'test -e' which works in sh, bash, ash (Alpine)
            res = subprocess.run(
                ["docker", "exec", container_name, "test", "-e", file_path],
                capture_output=True
            )
            exists = res.returncode == 0
            return exists, f"'{file_path}' {'exists' if exists else 'missing'} inside '{container_name}'."
        except:
            return False, "Exec failed."