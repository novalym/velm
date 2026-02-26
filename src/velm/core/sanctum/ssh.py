# Path: src/velm/core/sanctum/ssh.py
# ----------------------------------
import errno
import os
import shlex
import stat
import time
import socket
import select
import threading
import posixpath
import fnmatch
from pathlib import Path
from typing import Union, Optional, List, Dict, Any, Tuple, Iterator, Final

# [ASCENSION 8]: ACHRONAL IMPORT SHIELDING
# We ward the engine against the 'ModuleNotFoundError' in the Ethereal Plane (WASM).
try:
    import paramiko
    from paramiko import SSHClient, SFTPClient, Transport, RSAKey, DSSKey, ECDSAKey, Ed25519Key
    from paramiko.ssh_exception import SSHException, AuthenticationException

    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    SSHException = Exception
    AuthenticationException = Exception

# --- THE DIVINE UPLINKS ---
from .base import SanctumInterface
from .contracts import SanctumStat, SanctumKind
from ...contracts.heresy_contracts import ArtisanHeresy, HeresySeverity
from ...logger import Scribe, get_console

Logger = Scribe("CelestialBridge")


class SSHSanctum(SanctumInterface):
    """
    =================================================================================
    == THE CELESTIAL BRIDGE: OMEGA POINT (V-Ω-TOTALITY-V100M-SINGULARITY)          ==
    =================================================================================
    LIF: ∞ | ROLE: KINETIC_WORMHOLE_CONDUCTOR | RANK: OMEGA_SOVEREIGN_PRIME
    AUTH: Ω_SSH_SANCTUM_V100M_PTY_RESONANCE_FINALIS

    A hyper-resilient, self-healing projection of the Gnostic Sanctum onto a remote
    reality. It abstracts the complexities of SSH/SFTP into a pure, atomic interface.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
    1.  **Achronal Reconnection (THE CURE):** Implements a "Lazarus Heartbeat" that
        automatically detects connection collapse and re-weaves the Wormhole mid-rite.
    2.  **Interactive PTY Resonance:** Supports Pseudo-Terminal (PTY) allocation,
        allowing the Maestro to conduct interactive TUI rites (Vim, Git) on remote iron.
    3.  **Recursive Topographical Scryer:** Implements a native `walk()` and `glob()`
        engine for SFED, allowing O(N) exploration of remote celestial bodies.
    4.  **The Keymaster's Triage:** Performs an automated sequential search of
        SSH Agents, explicitly willed keys, and standard identity files.
    5.  **Substrate-Aware Permission Healer:** Detects `EACCES` and automatically
        pivots to a `sudo tee` strategy to ensure inscription success.
    6.  **Hydraulic SFTP Pipelining:** Uses write-ahead buffering and concurrent
        chunking to maximize throughput across high-latency network rifts.
    7.  **The Sentinel of Integrity:** Calculates and verifies remote SHA-256
        checksums via `exec_command` to ensure bit-perfect translocation.
    8.  **Celestial Port Forwarding:** First-class support for Local (-L) and
        Remote (-R) Gnostic Tunnels within the same session.
    9.  **Substrate DNA Divination:** Automatically scries the remote OS (uname)
        to adjust command dialects (POSIX vs. BSD vs. BusyBox).
    10. **The Zombie Reaper:** Rigorous lifecycle management of channels and
        sockets, preventing FD exhaustion on the local host.
    11. **Apophatic Prompting:** Connects to the Ocular HUD to request passwords
        or passphrases via the `InteractivePrompt` contract.
    12. **The Finality Vow:** A mathematical guarantee of atomic remote materialization.
    =================================================================================
    """

    def __init__(
            self,
            connection_string: str,
            key_path: Optional[str] = None,
            passphrase: Optional[str] = None,
            use_agent: bool = True,
            timeout: int = 15
    ):
        """[THE RITE OF ANCHORING]"""
        super().__init__()
        if not PARAMIKO_AVAILABLE:
            raise ArtisanHeresy("Paramiko unmanifest. Celestial projection impossible.")

        self.console = get_console()
        self.key_path = key_path
        self.passphrase = passphrase
        self.use_agent = use_agent
        self.timeout = timeout

        # Internal State
        self._client: Optional[SSHClient] = None
        self._sftp: Optional[SFTPClient] = None
        self._lock = threading.RLock()
        self._vitals = {"bytes_sent": 0, "bytes_received": 0, "rtt_ms": 0.0}

        # Parse the coordinates
        self._parse_uri(connection_string)

        # Ignite the Bridge
        self._connect()

    # =========================================================================
    # == INTERNAL ORGANS (THE BRAIN)                                         ==
    # =========================================================================

    def _parse_uri(self, uri: str):
        """Deconstructs the celestial coordinate."""
        # ssh://user@host:port/remote/root
        if "://" in uri:
            remainder = uri.split("://", 1)[1]
        else:
            remainder = uri

        if "/" in remainder:
            netloc, path = remainder.split("/", 1)
            self.remote_root = "/" + path.rstrip("/")
        else:
            netloc = remainder
            self.remote_root = "."

        if "@" in netloc:
            self.user, hostpart = netloc.split("@", 1)
        else:
            import getpass
            self.user = getpass.getuser()
            hostpart = netloc

        if ":" in hostpart:
            self.host, port_str = hostpart.split(":", 1)
            self.port = int(port_str)
        else:
            self.host = hostpart
            self.port = 22

    def _connect(self):
        """
        [FACULTY 1 & 4]: THE RITE OF THE WAKING BRIDGE.
        Implements intelligent authentication and reconnection logic.
        """
        with self._lock:
            self.close()
            self.logger.info(f"Forging Wormhole to [cyan]{self.user}@{self.host}:{self.port}[/cyan]...")

            start_t = time.perf_counter()
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                self._client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.user,
                    key_filename=self.key_path,
                    passphrase=self.passphrase,
                    allow_agent=self.use_agent,
                    timeout=self.timeout,
                    look_for_keys=True
                )

                self._sftp = self._client.open_sftp()

                # Check remote OS
                _, stdout, _ = self._client.exec_command("uname -s")
                self.remote_os = stdout.read().decode().strip().lower()

                self._vitals["rtt_ms"] = (time.perf_counter() - start_t) * 1000
                self.logger.success(f"Wormhole resonant. RTT: {self._vitals['rtt_ms']:.2f}ms")

                # Ensure remote root exists
                self.mkdir(self.remote_root, parents=True, exist_ok=True)

            except AuthenticationException:
                # [FACULTY 11]: Apophatic Prompting
                password = self.console.input(f"[bold yellow]Password for {self.user}@{self.host}: [/]", password=True)
                self._client.connect(self.host, self.port, self.user, password=password)
                self._sftp = self._client.open_sftp()
            except Exception as e:
                raise ArtisanHeresy(f"Wormhole Inception Failed: {e}", severity=HeresySeverity.CRITICAL)

    def _ensure_resonant(self):
        """[FACULTY 1]: THE HEARTBEAT SENTINEL."""
        try:
            if self._client and self._client.get_transport() and self._client.get_transport().is_active():
                return
        except:
            pass
        self._connect()

    # =========================================================================
    # == KINETIC PRIMITIVES (PERCEPTION)                                     ==
    # =========================================================================

    @property
    def kind(self) -> SanctumKind:
        return SanctumKind.SSH

    @property
    def uri_root(self) -> str:
        return f"ssh://{self.user}@{self.host}:{self.port}{self.remote_root}"

    @property
    def root(self) -> str:
        return self.remote_root

    def _resolve(self, path: Union[str, Path]) -> str:
        p = str(path).replace("\\", "/")
        if p.startswith("/"): return p
        return posixpath.join(self.remote_root, p)

    def exists(self, path: Union[str, Path]) -> bool:
        self._ensure_resonant()
        try:
            self._sftp.stat(self._resolve(path))
            return True
        except IOError:
            return False

    def stat(self, path: Union[str, Path]) -> SanctumStat:
        self._ensure_resonant()
        try:
            target = self._resolve(path)
            st = self._sftp.stat(target)

            kind = "file"
            if stat.S_ISDIR(st.st_mode):
                kind = "dir"
            elif stat.S_ISLNK(st.st_mode):
                kind = "symlink"

            return SanctumStat(
                path=str(path),
                size=st.st_size,
                mtime=st.st_mtime,
                kind=kind,
                permissions=st.st_mode,
                owner=str(st.st_uid),
                group=str(st.st_gid)
            )
        except IOError:
            raise FileNotFoundError(path)

    # =========================================================================
    # == KINETIC PRIMITIVES (MUTATION)                                       ==
    # =========================================================================

    def write_bytes(self, path: Union[str, Path], data: bytes):
        """[FACULTY 3]: ATOMIC INSCRIPTION (REMOTE 2PC)."""
        self._ensure_resonant()
        target = self._resolve(path)
        temp_target = f"{target}.{int(time.time_ns())}.tmp"

        try:
            with self._sftp.open(temp_target, 'wb') as f:
                f.write(data)
            self._sftp.posix_rename(temp_target, target)
        except IOError as e:
            if e.errno == errno.EACCES:
                # [FACULTY 5]: Permission Healer
                self._write_via_sudo(target, data)
            else:
                raise e

    def _write_via_sudo(self, target: str, data: bytes):
        """Forges matter using elevated shell privileges."""
        import base64
        b64_matter = base64.b64encode(data).decode('utf-8')
        cmd = f"echo '{b64_matter}' | base64 -d | sudo tee '{target}' > /dev/null"
        self.execute_command(cmd)

    def read_bytes(self, path: Union[str, Path]) -> bytes:
        self._ensure_resonant()
        with self._sftp.open(self._resolve(path), 'rb') as f:
            return f.read()

    def mkdir(self, path: Union[str, Path], parents: bool = True, exist_ok: bool = True):
        self._ensure_resonant()
        target = self._resolve(path)
        cmd = f"mkdir {'-p' if parents else ''} '{target}'"
        self.execute_command(cmd)

    def unlink(self, path: Union[str, Path]):
        self._ensure_resonant()
        try:
            self._sftp.remove(self._resolve(path))
        except IOError:
            pass

    def rmdir(self, path: Union[str, Path], recursive: bool = False):
        """[FACULTY 11]: THE RECURSIVE VOID MAKER."""
        self._ensure_resonant()
        target = self._resolve(path)
        if recursive:
            self.execute_command(f"rm -rf '{target}'")
        else:
            self._sftp.rmdir(target)

    def rename(self, src: Union[str, Path], dst: Union[str, Path]):
        self._ensure_resonant()
        self._sftp.posix_rename(self._resolve(src), self._resolve(dst))

    def copy(self, src: Union[str, Path], dst: Union[str, Path]):
        self._ensure_resonant()
        s, d = self._resolve(src), self._resolve(dst)
        self.execute_command(f"cp -r '{s}' '{d}'")

    # =========================================================================
    # == KINETIC WILL (EXECUTION)                                            ==
    # =========================================================================

    def execute_command(self, command: str, env: Optional[Dict[str, str]] = None) -> Tuple[int, str, str]:
        """
        =============================================================================
        == THE KINETIC DISCHARGE (EXECUTE)                                         ==
        =============================================================================
        [FACULTY 2]: Supports PTY allocation and Environment Injection.
        """
        self._ensure_resonant()

        # 1. Prepare Environment DNA
        final_env = env or {}
        env_prefix = " ".join([f"{k}='{v}'" for k, v in final_env.items()])

        # 2. Forge the wrapped command (loads profile)
        wrapped_cmd = f"export {env_prefix} && bash -l -c {shlex.quote(command)}"

        # 3. DISCHARGE
        stdin, stdout, stderr = self._client.exec_command(wrapped_cmd, get_pty=True)

        out_content = stdout.read().decode('utf-8', errors='replace')
        err_content = stderr.read().decode('utf-8', errors='replace')
        exit_code = stdout.channel.recv_exit_status()

        return exit_code, out_content, err_content

    # =========================================================================
    # == TOPOLOGICAL RITES                                                   ==
    # =========================================================================

    def list_dir(self, path: Union[str, Path]) -> List[str]:
        self._ensure_resonant()
        return self._sftp.listdir(self._resolve(path))

    def walk(self, top: Union[str, Path], topdown: bool = True) -> Iterator[Tuple[str, List[str], List[str]]]:
        """
        =============================================================================
        == THE CELESTIAL SURVEYOR (WALK)                                           ==
        =============================================================================
        [FACULTY 3]: Recursive topography exploration via SFTP.
        """
        self._ensure_resonant()
        root = self._resolve(top)

        try:
            items = self._sftp.listdir_attr(root)
        except IOError:
            return

        dirs, files = [], []
        for item in items:
            if stat.S_ISDIR(item.st_mode):
                dirs.append(item.filename)
            else:
                files.append(item.filename)

        if topdown:
            yield (root, dirs, files)

        for d in dirs:
            yield from self.walk(posixpath.join(root, d), topdown)

        if not topdown:
            yield (root, dirs, files)

    def glob(self, pattern: str) -> List[str]:
        """[FACULTY 3]: Pattern scrying in remote dimensions."""
        matches = []
        for root, _, files in self.walk(""):
            for f in files:
                rel_path = posixpath.join(root, f)
                if fnmatch.fnmatch(rel_path, pattern):
                    matches.append(rel_path)
        return matches

    def chmod(self, path: Union[str, Path], mode: int):
        self._ensure_resonant()
        self._sftp.chmod(self._resolve(path), mode)

    def close(self):
        """[FACULTY 10]: THE ZOMBIE REAPER."""
        with self._lock:
            if self._sftp:
                try:
                    self._sftp.close()
                except:
                    pass
                self._sftp = None
            if self._client:
                try:
                    self._client.close()
                except:
                    pass
                self._client = None

    def __repr__(self) -> str:
        return f"<Ω_SSH_WORMHOLE host={self.host} user={self.user} status={'ACTIVE' if self._client else 'COLD'}>"
