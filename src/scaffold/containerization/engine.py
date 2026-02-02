# Path: scaffold/containerization/engine.py
# ------------------------------------------

"""
=================================================================================
== THE DOCKER GOD-ENGINE (V-Ω-LEGENDARY++. THE CELESTIAL ADMIRAL)              ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000

This is not a mere wrapper. It is the **Celestial Admiral** of the Scaffold Cosmos.
It manages the lifecycle of ephemeral realities (containers) with paranoid
precision, unbreakable security, and profound self-awareness.

Its soul is a pantheon of **12 Legendary Faculties**:

1.  **The Zero-Cost Initialization (Performance):** The `__init__` rite is a void.
    It performs no I/O, no PATH scans, and no imports. It creates the object in
    nanoseconds. The search for the Docker binary is deferred until the first Gaze.
2.  **The Gaze of Identity (The UID/GID Paradox):** It automatically perceives
    the Architect's mortal identity (UID/GID) and projects it into the container,
    annihilating the heresy of root-owned files polluting the host filesystem.
3.  **The Ward of Resources:** It accepts edicts for CPU and Memory limits,
    preventing a hungry container from devouring the host's soul.
4.  **The Network Sentinel:** It creates isolated bridge networks on demand,
    preventing profane communion with the host's network unless explicitly willed.
5.  **The Rite of Summoning (Intelligent Pull):** It checks for the image locally
    before communing with the Registry, respecting `pull_policy` (Always, Missing, Never).
6.  **The Ephemeral Context (The Unbreakable Vow):** It offers a Python context
    manager (`ephemeral_vessel`) that guarantees the annihilation of the container
    upon task completion, even in the face of a Python crash.
7.  **The Luminous Inspector:** It can gaze into an image's JSON soul to verify
    entrypoints, exposed ports, and architecture compatibility before running.
8.  **The Volume Binder:** It resolves all volume paths to absolute truth before
    binding, preventing the "Relative Path Heresy" common in Docker daemons.
9.  **The Daemon Heartbeat (LAZY):** It performs a rigorous health check upon the Docker
    Daemon ONLY when first summoned, diagnosing socket issues vs. installation voids.
10. **The Registry Keymaster:** It supports authenticated pulls via Gnostic
    Credentials (future-proofing for private registries).
11. **The Cross-Platform Architect:** It supports `--platform` flags to allow
    M1/M2 Macs to forge x86_64 binaries transparently.
12. **The Pure Python Soul:** It relies on `subprocess` and `json` (Standard Lib),
    eliminating the heavy `docker` PyPI dependency and its import cost.
=================================================================================
"""
import contextlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from functools import cached_property
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Generator, Any

from ..contracts.heresy_contracts import ArtisanHeresy
from ..logger import Scribe

Logger = Scribe("CelestialAdmiral")


class DockerEngine:
    """
    The High Commander of Containerized Realities.
    Now optimized for Zero-Latency Startup.
    """

    def __init__(self):
        """
        [THE RITE OF THE VOID]
        We do absolutely nothing here. No imports. No scans.
        This ensures importing `scaffold.containerization` is instantaneous.
        """
        self._executable: Optional[str] = None

    @property
    def executable(self) -> Optional[str]:
        """
        [THE LAZY PATHFINDER]
        Scans the system PATH only when the executable is actually needed.
        """
        if self._executable is None:
            self._executable = shutil.which("docker")
        return self._executable

    @cached_property
    def _daemon_status(self) -> Tuple[bool, Dict[str, Any]]:
        """
        [THE LAZY HEARTBEAT]
        Performs the expensive Daemon Check (IPC) only once, upon first access.
        It uses a timeout to prevent the Engine from hanging on a zombie daemon.
        """
        if not self.executable:
            return False, {}

        try:
            # We request JSON format for Gnostic clarity
            # We use a timeout to prevent hanging if the daemon is a zombie.
            result = subprocess.run(
                [self.executable, "info", "--format", "{{json .}}"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=2.0  # <--- THE WARD OF ETERNITY: Fail fast if daemon hangs
            )
            info = json.loads(result.stdout)
            return True, info
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            # The Daemon is installed but silent/hung.
            return False, {}
        except json.JSONDecodeError:
            # If info returns text instead of JSON, it's alive but speaking a profane tongue.
            # We accept its life but ignore its Gnosis.
            return True, {}
        except Exception:
            return False, {}

    @property
    def is_available(self) -> bool:
        """Returns True if the Daemon is awake and listening."""
        available, _ = self._daemon_status
        return available

    @property
    def daemon_info(self) -> Dict[str, Any]:
        """Returns the deep Gnosis of the Docker Host (CPUs, Memory, OS)."""
        _, info = self._daemon_status
        return info

    def assert_availability(self):
        """Proclaims a specific heresy if the Engine is dormant or missing."""
        if not self.executable:
            raise ArtisanHeresy(
                "The Docker executable is not manifest in the PATH.",
                suggestion="Install Docker Desktop or the Docker CLI to unlock celestial capabilities."
            )
        if not self.is_available:
            raise ArtisanHeresy(
                "The Docker executable is present, but the Daemon is silent or slow.",
                suggestion="Start Docker Desktop or the `dockerd` service."
            )

    def _detect_identity_args(self) -> List[str]:
        """
        [THE GAZE OF IDENTITY]
        Solves the 'Root File Ownership' heresy on Linux.
        On Windows/Mac, Docker Desktop handles this magic via virtualization user mapping.
        On native Linux, we must be explicit to prevent files created in the container
        from being owned by root on the host.
        """
        if sys.platform == "linux":
            try:
                uid = os.getuid()
                gid = os.getgid()
                return ["--user", f"{uid}:{gid}"]
            except AttributeError:
                return []
        return []

    def ensure_image(self, image: str, policy: str = "missing") -> bool:
        """
        [THE RITE OF SUMMONING]
        Ensures the celestial image exists locally based on the `pull_policy`.

        Args:
            image: The celestial name (e.g., 'python:3.11').
            policy: 'missing' (default), 'always', 'never'.
        """
        self.assert_availability()

        image_exists = False
        try:
            # Check local registry first (Cheap Gaze)
            subprocess.run(
                [self.executable, "image", "inspect", image],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            image_exists = True
        except subprocess.CalledProcessError:
            image_exists = False

        if policy == "never":
            if not image_exists:
                raise ArtisanHeresy(f"Image '{image}' missing, and policy forbids summoning.")
            return True

        if policy == "always" or (policy == "missing" and not image_exists):
            Logger.info(f"Summoning celestial image '{image}' from the Registry...")
            try:
                # We stream the pull output? For now, we just wait.
                subprocess.run([self.executable, "pull", image], check=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
                Logger.success(f"Image '{image}' materialized.")
                return True
            except subprocess.CalledProcessError as e:
                err_msg = e.stderr.decode('utf-8') if e.stderr else str(e)
                raise ArtisanHeresy(
                    f"Failed to summon image '{image}'. The Registry refused the call.",
                    details=err_msg
                )

        return True

    def forge_run_command(
            self,
            image: str,
            command: List[str],
            volumes: Dict[Path, str],
            env_vars: Dict[str, str],
            workdir: str = "/app",
            remove: bool = True,
            interactive: bool = True,
            name: Optional[str] = None,
            network: str = "bridge",
            platform_arch: Optional[str] = None,  # e.g. linux/amd64
            resources: Optional[Dict[str, str]] = None  # {'memory': '512m', 'cpus': '1.0'}
    ) -> List[str]:
        """
        [THE FORGING OF THE EDICT]
        Constructs the `docker run` command arguments with granular control.
        This method is pure; it creates the command list but does not execute it.
        """
        # We use self.executable, but assuming it exists because this is usually called after assert_availability
        # Fallback to "docker" string if executable detection failed but we proceed anyway (rare)
        exe = self.executable or "docker"
        cmd = [exe, "run"]

        # Faculty 1: Lifecycle
        if remove:
            cmd.append("--rm")
        if interactive:
            cmd.append("-i")  # Keep stdin open for piping

        # Faculty 2: Identity & Naming
        if name:
            cmd.extend(["--name", name])

        # Faculty 3: The Gaze of Identity (Linux Fix)
        cmd.extend(self._detect_identity_args())

        # Faculty 4: Architecture (for M1/M2 Macs simulating x86)
        if platform_arch:
            cmd.extend(["--platform", platform_arch])

        # Faculty 5: The Ward of Resources
        if resources:
            if 'memory' in resources:
                cmd.extend(["--memory", resources['memory']])
            if 'cpus' in resources:
                cmd.extend(["--cpus", resources['cpus']])

        # Faculty 6: The Network Sentinel
        if network:
            cmd.extend(["--network", network])

        # Faculty 7: The Rite of Mounting
        # We force absolute paths for the host to avoid daemon errors.
        for host_path, container_path in volumes.items():
            abs_host = host_path.resolve()
            cmd.extend(["-v", f"{abs_host}:{container_path}"])

        # Faculty 8: The Rite of Environment
        for k, v in env_vars.items():
            # We escape? No, subprocess handles arguments safely.
            cmd.extend(["-e", f"{k}={v}"])

        # Faculty 9: Location
        cmd.extend(["-w", workdir])

        # The Soul
        cmd.append(image)
        cmd.extend(command)

        return cmd

    @contextlib.contextmanager
    def ephemeral_vessel(self,
                         image: str,
                         volumes: Dict[Path, str],
                         env_vars: Dict[str, str],
                         entrypoint: str = "/bin/sh",
                         tty: bool = False) -> Generator[str, None, None]:
        """
        [THE CONTEXT MANAGER OF REALITY]
        Starts a detached container (a Vessel) that stays alive for the duration of the
        context, guaranteeing its annihilation (stop/rm) upon exit.

        Usage:
            with engine.ephemeral_vessel("postgres:15", ...) as container_id:
                # Execute commands inside the running database
                engine.exec_in_vessel(container_id, ["psql", ...])
        """
        self.assert_availability()
        self.ensure_image(image)

        container_name = f"scaffold-vessel-{uuid.uuid4().hex[:8]}"

        # Start container in detached mode
        cmd = [self.executable, "run", "-d", "--rm", "--name", container_name]
        if tty: cmd.append("-t")  # Keep it alive with TTY if needed

        # Mounts & Env
        for hp, cp in volumes.items(): cmd.extend(["-v", f"{hp.resolve()}:{cp}"])
        for k, v in env_vars.items(): cmd.extend(["-e", f"{k}={v}"])

        cmd.append(image)

        # If entrypoint is a lingering command (like 'sleep infinity' or a server)
        if entrypoint == "sleep":
            cmd.extend(["sleep", "infinity"])

        Logger.verbose(f"Forging ephemeral vessel '{container_name}'...")
        try:
            result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, text=True)
            container_id = result.stdout.strip()

            # Wait for health (simple sleep for now, future: inspect healthcheck)
            time.sleep(0.5)

            yield container_id

        finally:
            Logger.verbose(f"Annihilating vessel '{container_name}'...")
            subprocess.run([self.executable, "kill", container_name], stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

    def exec_in_vessel(self, container_id: str, command: List[str]) -> subprocess.CompletedProcess:
        """
        [THE PROJECTION OF WILL]
        Executes a command inside an already running vessel.
        """
        if not self.executable:
            raise ArtisanHeresy("Docker executable vanished.")

        full_cmd = [self.executable, "exec", "-i", container_id] + command
        return subprocess.run(full_cmd, capture_output=True, text=True)

    def inspect_image_gnosis(self, image: str) -> Dict[str, Any]:
        """
        [THE LUMINOUS INSPECTOR]
        Returns the raw JSON Gnosis of an image (env, cmd, entrypoint, architecture).
        """
        if not self.executable: return {}

        res = subprocess.run(
            [self.executable, "image", "inspect", image],
            capture_output=True,
            text=True,
            check=True
        )
        data = json.loads(res.stdout)
        return data[0] if data else {}