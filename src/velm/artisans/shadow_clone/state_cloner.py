# Path: scaffold/artisans/shadow_clone/state_cloner.py
# =================================================================================
# == THE STATE ALCHEMIST (V-Ω-DB-CLONING)                                       ==
# =================================================================================
import subprocess
import time
import uuid
from typing import Optional
from ...logger import Scribe
from .contracts import StateCloningResult
from .network import NetworkBinder

Logger = Scribe("StateAlchemist")


class StateCloner:
    """
    Performs the Rite of State Fission.
    1. Detects active DB container.
    2. Spins up ephemeral sibling.
    3. (Future) Pipes data.
    """

    def clone_postgres(self, shadow_id: str) -> StateCloningResult:
        """
        Spins up a fresh, empty Postgres container for the shadow.
        """
        container_name = f"scaffold-shadow-db-{shadow_id}"
        host_port = NetworkBinder.find_free_port()

        Logger.info(f"Spinning up Ephemeral DB Node: {container_name} on port {host_port}")

        try:
            # 1. Ignite Container
            # Using alpine for speed
            subprocess.run([
                "docker", "run", "-d", "--name", container_name,
                "-e", "POSTGRES_PASSWORD=shadow",
                "-e", "POSTGRES_DB=shadow_db",
                "-p", f"{host_port}:5432",
                "postgres:15-alpine"
            ], check=True, stdout=subprocess.DEVNULL)

            # Wait for life (Vitality Check)
            self._wait_for_container(container_name)

            # 2. Forge Connection String
            new_url = f"postgresql://postgres:shadow@localhost:{host_port}/shadow_db"

            Logger.success(f"State Vessel Created: {new_url}")
            return StateCloningResult(True, new_url, container_name, host_port)

        except Exception as e:
            Logger.error(f"State Fission Failed: {e}")
            self.kill_container(container_name)
            return StateCloningResult(False, None, None, None, str(e))

    def kill_container(self, container_id: str):
        if not container_id: return
        subprocess.run(["docker", "rm", "-f", container_id], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        Logger.verbose(f"Container {container_id} annihilated.")

    def _wait_for_container(self, container_name: str, timeout: int = 10):
        start = time.time()
        while time.time() - start < timeout:
            try:
                res = subprocess.run(
                    ["docker", "exec", container_name, "pg_isready"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                if res.returncode == 0:
                    return
            except:
                pass
            time.sleep(0.5)
        Logger.warn(f"Container {container_name} did not respond to ping, but proceeding.")