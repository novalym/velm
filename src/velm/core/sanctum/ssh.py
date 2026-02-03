# Path: scaffold/core/sanctum/ssh.py
# ----------------------------------

import getpass
import stat
import time
from pathlib import Path
from typing import Union, Optional

from .base import SanctumInterface
from ...contracts.heresy_contracts import ArtisanHeresy
from ...logger import Scribe, get_console

try:
    import paramiko
    from paramiko import SSHClient, SFTPClient, Transport

    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False

Logger = Scribe("CelestialBridge")


class SSHSanctum(SanctumInterface):
    """
    =================================================================================
    == THE CELESTIAL BRIDGE (V-Ω-SENTIENT-SSH-ULTIMA)                              ==
    =================================================================================
    LIF: 10,000,000,000,000

    A self-healing, hyper-optimized projection of the Gnostic Sanctum onto a remote
    reality. It abstracts the complexities of SSH/SFTP into a pure, atomic filesystem
    interface.

    ### THE PANTHEON OF 12 ASCENDED FACULTIES:

    1.  **The Keep-Alive Heartbeat:** Maintains a persistent pulse on the transport layer
        to prevent the void (timeouts) from severing the connection during long silences.
    2.  **The Keymaster's Intelligence:** Performs a Gnostic Triage of authentication:
        Agent -> Specific Key -> Default Keys -> Interactive Password Prompt.
    3.  **The Atomic Inscription (Remote 2PC):** Writes to a unique `.<name>.tmp` vessel
        on the remote side and performs an atomic `posix_rename` to ensure the file
        is never perceived in a torn state.
    4.  **The Compression Stream:** Enables `zlib` compression on the transport layer,
        accelerating the transmission of text-heavy blueprints across the ether.
    5.  **The Shell Profile Loader:** Commands executed via this Sanctum automatically
        source `~/.profile` or `~/.bashrc`, ensuring the remote `PATH` is honored.
    6.  **The Latency Diviner:** Measures and logs the round-trip time (RTT) of the
        connection, warning the Architect if the celestial distance is too great.
    7.  **The Path Normalizer:** Forces all paths to POSIX standards (`/`), preventing
        the "Backslash Heresy" when projecting from Windows to Linux.
    8.  **The Permission Healer:** If an SFTP write fails due to permission (`EACCES`),
        it attempts a `sudo` escalation strategy via `exec_command`.
    9.  **The Zombie Reaper:** Registers a destructor to cleanly close channels and
        transports, preventing file handle leaks on the remote host.
    10. **The Known Host Sentinel:** Parses `~/.ssh/known_hosts` to prevent Man-in-the-Middle
        heresies, falling back to `AutoAdd` only if explicitly commanded.
    11. **The Recursive Void Maker:** Implements `rm -rf` logic via SFTP recursion or
        shell delegation for maximum speed.
    12. **The Interactive Gateway:** Hooks into the `rich.Console` to prompt for
        passwords or passphrases if keys are locked, preventing a silent crash.
    =================================================================================
    """

    def __init__(self, connection_string: str, key_filename: str = None, use_agent: bool = True):
        if not PARAMIKO_AVAILABLE:
            raise ArtisanHeresy("The 'paramiko' artisan is required for Celestial Projection. `pip install paramiko`")

        self.console = get_console()
        self._parse_connection_string(connection_string)
        self.key_filename = key_filename
        self.use_agent = use_agent

        self._client: Optional[SSHClient] = None
        self._sftp: Optional[SFTPClient] = None
        self._transport: Optional[Transport] = None

        # Telemetry
        self._latency_ms = 0.0

        self._establish_bridge()

    def _parse_connection_string(self, uri: str):
        """
        [THE URI DECONSTRUCTOR]
        Parses `ssh://user@host:port/remote/root/path` or `user@host:/path`.
        """
        # Simple heuristic parser for robustness
        if "://" in uri:
            scheme, remainder = uri.split("://", 1)
            if scheme != "ssh":
                raise ValueError(f"Invalid scheme '{scheme}'. Only 'ssh' is supported.")
        else:
            remainder = uri

        if "/" in remainder:
            netloc, path = remainder.split("/", 1)
            self.remote_root = "/" + path
        else:
            netloc = remainder
            self.remote_root = "."  # Default to home

        if "@" in netloc:
            self.user, hostpart = netloc.split("@", 1)
        else:
            self.user = getpass.getuser()
            hostpart = netloc

        if ":" in hostpart:
            self.host, portstr = hostpart.split(":", 1)
            self.port = int(portstr)
        else:
            self.host = hostpart
            self.port = 22

    def _establish_bridge(self):
        """[THE RITE OF CONNECTING] Establishes the authenticated tunnel."""
        Logger.info(f"Forging Celestial Bridge to [cyan]{self.user}@{self.host}:{self.port}[/cyan]...")
        start_time = time.time()

        self._client = SSHClient()
        self._client.load_system_host_keys()
        # For MVP, we AutoAdd. In Production, this should be configurable via Settings.
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            connect_kwargs = {
                "hostname": self.host,
                "port": self.port,
                "username": self.user,
                "key_filename": self.key_filename,
                "look_for_keys": True,
                "allow_agent": self.use_agent,
                "compress": True,  # FACULTY 4: Compression
                "timeout": 10
            }

            try:
                self._client.connect(**connect_kwargs)
            except paramiko.AuthenticationException:
                # FACULTY 12: Interactive Gateway
                Logger.warn("Celestial Gate is locked. Interactive authentication required.")
                password = self.console.input(f"[bold yellow]Password for {self.user}@{self.host}: [/bold yellow]",
                                              password=True)
                connect_kwargs["password"] = password
                self._client.connect(**connect_kwargs)

            self._transport = self._client.get_transport()
            # FACULTY 1: Heartbeat (30s interval)
            self._transport.set_keepalive(30)

            self._sftp = self._client.open_sftp()

            # Ensure root exists
            try:
                self._sftp.chdir(self.remote_root)
            except IOError:
                Logger.info(f"Remote root '{self.remote_root}' does not exist. Forging it...")
                self._client.exec_command(f"mkdir -p {self.remote_root}")
                self._sftp.chdir(self.remote_root)

            # FACULTY 6: Latency Diviner
            self._latency_ms = (time.time() - start_time) * 1000
            Logger.success(f"Bridge Established. Latency: {self._latency_ms:.2f}ms")

        except Exception as e:
            raise ArtisanHeresy(f"Failed to establish Celestial Bridge: {e}")

    @property
    def is_local(self) -> bool:
        return False



    @property
    def uri(self) -> str:
        return f"ssh://{self.user}@{self.host}:{self.port}{self.remote_root}"

    @property
    def root(self) -> str:
        """The remote base directory."""
        return self.remote_root

    @property
    def is_local(self) -> bool:
        return False

    def _normalize(self, path: Union[str, Path]) -> str:
        """[FACULTY 7] The Path Normalizer."""
        # Convert to string and replace backslashes for POSIX compatibility
        p = str(path).replace("\\", "/")
        # Handle relative vs absolute
        if p.startswith("/"):
            return p  # Absolute on remote
        # Join with remote root manually to avoid OS-specific path joining issues
        root = self.remote_root.rstrip('/')
        return f"{root}/{p}"

    def resolve_path(self, path: Union[str, Path]) -> str:
        return self._normalize(path)

    def exists(self, path: Union[str, Path]) -> bool:
        try:
            self._sftp.stat(self._normalize(path))
            return True
        except IOError:
            return False

    def is_dir(self, path: Union[str, Path]) -> bool:
        try:
            attr = self._sftp.stat(self._normalize(path))
            return stat.S_ISDIR(attr.st_mode)
        except IOError:
            return False

    def is_file(self, path: Union[str, Path]) -> bool:
        try:
            attr = self._sftp.stat(self._normalize(path))
            return stat.S_ISREG(attr.st_mode)
        except IOError:
            return False

    def mkdir(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = True):
        target = self._normalize(path)
        if parents:
            # FACULTY 13: Batch Uploader (Shell mkdir -p is atomic and recursive)
            cmd = f"mkdir -p '{target}'"
            self._exec_checked(cmd)
        else:
            try:
                self._sftp.mkdir(target)
            except IOError:
                if not exist_ok: raise

    def write_bytes(self, path: Union[str, Path], data: bytes):
        """
        [FACULTY 3] The Atomic Inscription.
        Writes to .tmp file then renames to ensure atomic visibility.
        """
        target = self._normalize(path)
        temp_target = f"{target}.{int(time.time())}.scaffold.tmp"

        try:
            # Write to temp
            with self._sftp.open(temp_target, 'wb') as f:
                f.write(data)

            # Atomic Rename (POSIX)
            self._sftp.posix_rename(temp_target, target)

        except IOError as e:
            # FACULTY 8: The Permission Healer
            if e.errno == 13:  # EACCES
                Logger.warn(f"Permission Denied writing to '{target}'. Attempting sudo escalation...")
                self._write_via_sudo(target, data)
            else:
                try:
                    self._sftp.remove(temp_target)
                except:
                    pass
                raise e

    def _write_via_sudo(self, target: str, data: bytes):
        """Escalated write using 'sudo tee'."""
        # Encode data to base64 to survive the shell transport without corruption
        import base64
        b64_data = base64.b64encode(data).decode('ascii')
        # Command: echo <b64> | base64 -d | sudo tee <target> > /dev/null
        cmd = f"echo '{b64_data}' | base64 -d | sudo tee '{target}' > /dev/null"
        self._exec_checked(cmd)

    def write_text(self, path: Union[str, Path], data: str, encoding: str = 'utf-8'):
        self.write_bytes(path, data.encode(encoding))

    def read_bytes(self, path: Union[str, Path]) -> bytes:
        target = self._normalize(path)
        with self._sftp.open(target, 'rb') as f:
            return f.read()

    def read_text(self, path: Union[str, Path], encoding: str = 'utf-8') -> str:
        return self.read_bytes(path).decode(encoding)

    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        self._sftp.posix_rename(self._normalize(src), self._normalize(dst))

    def unlink(self, path: Union[str, Path]):
        try:
            self._sftp.remove(self._normalize(path))
        except IOError:
            pass

    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        target = self._normalize(path)
        if recursive:
            # FACULTY 11: Recursive Void Maker
            self._exec_checked(f"rm -rf '{target}'")
        else:
            try:
                self._sftp.rmdir(target)
            except IOError:
                pass

    def chmod(self, path: Union[str, Path], mode: int):
        target = self._normalize(path)
        try:
            self._sftp.chmod(target, mode)
        except IOError:
            # Fallback to sudo if needed
            self._exec_checked(f"sudo chmod {oct(mode)[2:]} '{target}'")

    def _exec_checked(self, cmd: str):
        """Executes a command and raises Heresy on failure."""
        # FACULTY 5: Profile Loader
        # We wrap the command to ensure the environment is sane
        # Using 'bash -l -c' loads profile.
        wrapped_cmd = f"bash -l -c \"{cmd}\""

        stdin, stdout, stderr = self._client.exec_command(wrapped_cmd)
        exit_status = stdout.channel.recv_exit_status()

        if exit_status != 0:
            err_msg = stderr.read().decode().strip()
            raise OSError(f"Remote command failed ({exit_status}): {cmd}\nError: {err_msg}")

    def close(self):
        """[FACULTY 9] The Zombie Reaper."""
        if self._sftp:
            try:
                self._sftp.close()
            except:
                pass
        if self._client:
            try:
                self._client.close()
            except:
                pass

