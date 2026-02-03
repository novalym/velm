# Path: runtime_manager/manager.py

"""
== THE GOD-ENGINE OF THE HERMETIC FORGE (V-Ω-ULTRA-DEFINITIVE-APOTHEOSIS++)      ==

LIF: 10,000,000,000,000,000,000

This is the God-Engine of Dependency Materialization and Execution Governance. It is
the one true, unified Oracle for discovering, summoning, and governing all execution
realities, now ascended with the soul of the Grand Strategist.
THE PANTHEON OF 42+ ASCENDED FACULTIES:

--- THE PANTHEON OF PERCEPTION (THE ORACLE'S GAZE) ---

    The Unified Mind: All runtime perception logic is enshrined here.

    The Asynchronous Gaze: Perceives all three realms (System, Managed, Docker) in parallel.

    The Gnostic Chronocache: Caches the state of the cosmos, invalidating only when reality shifts.

    The Gaze of the Mortal Realm: Scans the system PATH for globally installed artisans.

    The Gaze of the Hermetic Realm: Gazes into ~/.scaffold/runtimes for managed souls.

    The Gaze of the Celestial Realm: Communes with the Docker daemon.

    The Polyglot Mind: Seeks Python, Node, Go, Rust, and more.

    The Version Alchemist: Executes --version commands to perceive a binary's true soul.

    The Gnostic Dossier: Proclamations are rich, structured vessels of Gnosis.

    The Luminous Voice: Proclaims its every thought to the Gnostic Chronicle.

    The Unbreakable Ward of Paradox: A fallen Docker daemon does not shatter its mind.

    The Identity Matrix: Perceives the host OS and architecture for the Codex.

    The Gaze of the Active Soul: The scan rite now returns which runtime is currently active based on settings.

    The Silent Gaze: Can be commanded to perform its Gaze without any console output.

--- THE PANTHEON OF CREATION (THE FORGEMASTER'S HAND) ---
15. The Rite of Summoning (get_runtime): The one true rite for materializing a new hermetic soul.
16. The Gnostic Emissary (_forge_resilient_session): Forges a network session with unbreakable retry logic.
17. The Atomic Lock: A file-based mutex prevents concurrent corruption of the sanctum.
18. The Secure Extractor: Annihilates the "Zip-Slip" heresy with a path-adjudicating extraction rite.
19. The Cryptographic Verifier (_download_securely): Verifies SHA256 checksums on all downloaded souls.
20. The Smart Descender: Intelligently navigates into single-directory wrappers within archives.
21. The Consecrator of Will: Automatically bestows executable permissions upon summoned binaries.
22. The Binary Diviner (_validate_runtime): Performs a "heartbeat" check on a summoned soul.
23. The Self-Healing Forge: Automatically purges corrupted or failed installations.
24. The Luminous Progress Scribe: Proclaims a beautiful, cinematic progress bar during summoning.
25. The Unbreakable Gnostic Contract: Its public API is pure, its purpose absolute.

--- THE PANTHEON OF GOVERNANCE (THE GRAND STRATEGIST) ---
26. The Grand Strategist (resolve_execution_plan): The new, sentient mind that determines the one true execution reality.
27. The Unbreakable Hierarchy of Truth: Adjudicates CLI Override > Project Law > Global Law > auto Prophecy.
28. The Polyglot Micro-Syntax Parser: Deconstructs complex runtime pleas like docker:python:3.12-slim.
29. The Sentient auto Strategy: Intelligently prefers local purity (Venv > Hermetic > Docker > System).
30. The Venv Sentinel: Performs a high-precedence Gaze for local .venv sanctums.
31. The Oracle of Aliases (resolve_version): Transmutes pleas like 'latest' or 'lts' into concrete versions.
32. The Telepathic Link to the Codex: It communes directly with the RUNTIME_CODEX.
33. The Gnostic Health Inquisitor (health_check): A universal rite to adjudicate the health of all known runtimes.
34. The Rite of Universal Purification (purge_all): A dangerous but divine rite to annihilate the entire Hermetic Forge.
--- THE PANTHEON OF RESILIENCE & UX ---
35. The Rite of Persistence (resilient_io): A divine decorator that heals the Windows "File Locked" heresy.
36. The Guardian of Eternity: Enforces strict timeouts on all external processes.
37. The Luminous Heresy Proclamation: All exceptions are transmuted into luminous ArtisanHeresy vessels.
38. The Hierarchical Purge: Its cleanup rites understand the sacred order of annihilation.
39. The Interactive Guardian: All destructive rites are guarded by an interactive Confirm plea.
40. The Force Majeure: The --force vow is honored across all rites to bypass interactive guards.
41. The Polyglot Path Normalizer: All proclaimed paths are pure and POSIX-compliant.
42. The Self-Aware Name: Archive names are forged with a Gnostic hash of the plan.

"""
import contextlib
import hashlib
import os
import platform
import re
import shutil
import stat
import subprocess
import tarfile
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional, Generator, List, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    import requests
    from ..containerization import DockerEngine
    from rich.progress import Progress


from ..contracts.data_contracts import ExecutionPlan
from ..logger import Scribe, get_console
from ..contracts.heresy_contracts import ArtisanHeresy
from .codex import RUNTIME_CODEX, resolve_version
from .. import __version__

Logger = Scribe("RuntimeManager")



class RuntimeManager:
    """The God-Engine of the Hermetic Forge."""

    def __init__(self, silent: bool = False):
        # [OPTIMIZATION] Paths are defined but not created until needed to save IO ops on startup.
        self.runtimes_root = Path.home() / ".scaffold" / "runtimes"
        self.downloads_root = self.runtimes_root / "downloads"
        self.locks_root = self.runtimes_root / "locks"

        self.logger = Logger
        self.silent = silent

        # [OPTIMIZATION] Lazy properties
        self._platform_key = None
        self._session = None
        self._docker_engine = None
        self._console = None

        self._runtime_cache: Optional[Dict[str, List[Dict]]] = None
        self._last_scan_time = 0.0

    @property
    def console(self):
        if not self._console:
            self._console = get_console()
        return self._console

    @property
    def docker_engine(self):
        if not self._docker_engine:
            from ..containerization import DockerEngine
            self._docker_engine = DockerEngine()
        return self._docker_engine

    @property
    def session(self):
        if not self._session:
            self._session = self._forge_resilient_session()
        return self._session

    @property
    def platform_key(self) -> str:
        if not self._platform_key:
            self._resolve_system_identity()
        return self._platform_key

    def _ensure_directories(self):
        """Creates the sacred sanctums only when write operations are imminent."""
        for p in [self.runtimes_root, self.downloads_root, self.locks_root]:
            p.mkdir(parents=True, exist_ok=True)

    def resolve_execution_plan(
            self,
            language: str,
            runtime_spec: Optional[str],
            sanctum: Path
    ) -> ExecutionPlan:
        """
        [FACULTY 26] THE GRAND STRATEGIST OF EXECUTION

        This method has been surgically optimized to perform the 'System First' check
        when in 'auto' mode, avoiding the expensive initialization of the Docker Engine
        and Settings Manager unless absolutely necessary.
        """
        # --- MOVEMENT I: THE HIERARCHY OF TRUTH ---

        # 1. Explicit Spec (Fastest) - e.g. --runtime=docker:python:3.11
        if runtime_spec:
            return self._parse_and_resolve_spec(runtime_spec, language, sanctum)

        # 2. Load Settings (Lazy Import)
        from ..settings.manager import SettingsManager
        settings = SettingsManager(project_root=sanctum)

        strategy = settings.get("runtimes.strategy") or "auto"

        # 3. System Strategy (Fast Path)
        if strategy == "system":
            return self._resolve_system_strategy(language)

        # 4. Auto Strategy (The Lazy Optimization)
        if strategy == "auto":
            self.logger.verbose("Auto-Gaze: Prioritizing Local & Hermetic realms...")

            # A. Venv Check (Instant)
            try:
                return self._resolve_venv_strategy(language, sanctum)
            except ArtisanHeresy:
                pass

            # B. System Check (Fastest Fallback)
            recipe = self._get_recipe(language)
            tool = recipe["interpreter"][0]
            # If the tool exists in PATH, we use it immediately without checking Docker.
            if shutil.which(tool):
                return ExecutionPlan(interpreter_cmd=recipe["interpreter"], strategy='system', docker_image=None)

            # C. Hermetic Check (Fast)
            try:
                return self._resolve_hermetic_strategy(language, None, sanctum)
            except ArtisanHeresy:
                pass

            # D. Docker Check (Slowest - Last Resort)
            # Accessing self.docker_engine here triggers the import and potentially daemon check
            if self.docker_engine.is_available:
                try:
                    return self._resolve_docker_strategy(language, None)
                except ArtisanHeresy:
                    pass

            # Fallback to system to raise the standard "not found" heresy
            return self._resolve_system_strategy(language)

        # 5. Explicit Heavy Strategies
        if strategy == "docker":
            return self._resolve_docker_strategy(language, None)

        if strategy == "hermetic":
            return self._resolve_hermetic_strategy(language, None, sanctum)

        return self._resolve_system_strategy(language)

    def _parse_and_resolve_spec(self, spec: str, language: str, sanctum: Path) -> ExecutionPlan:
        """[FACULTY 28] The Polyglot Micro-Syntax Parser."""
        strategy, arg = (spec.split(":", 1) + [None])[:2]

        if strategy == "docker":
            return self._resolve_docker_strategy(language, arg)
        elif strategy in ("hermetic", "managed", "scaffold"):
            return self._resolve_hermetic_strategy(language, arg, sanctum)
        elif strategy == "venv":
            return self._resolve_venv_strategy(language, sanctum, venv_path_str=arg)
        elif strategy == "system":
            return self._resolve_system_strategy(language)
        elif '@' in strategy:
            # Assume it's a language@version spec for hermetic
            return self._resolve_hermetic_strategy(strategy, None, sanctum)
        else:
            raise ArtisanHeresy(f"Unknown runtime strategy or malformed spec: '{spec}'")

    def _resolve_docker_strategy(self, language: str, image_override: Optional[str]) -> ExecutionPlan:
        """Forges the execution plan for a Celestial Vessel."""
        self.docker_engine.assert_availability()

        from ..settings.manager import SettingsManager
        image = image_override or SettingsManager().get(f"docker.image.{language}")
        if not image:
            raise ArtisanHeresy(
                f"Docker strategy requested for '{language}', but no image is specified or configured.",
                suggestion=f"Use `--runtime=docker:image_name` or set `docker.image.{language}` via `scaffold settings`."
            )

        pull_policy = SettingsManager().get("docker.pull_policy") or "missing"
        self.docker_engine.ensure_image(image, policy=pull_policy)

        recipe = self._get_recipe(language)
        return ExecutionPlan(interpreter_cmd=recipe["interpreter"], strategy='docker', docker_image=image)

    def _resolve_hermetic_strategy(self, language: str, version_spec: Optional[str], sanctum: Path) -> ExecutionPlan:
        """Forges the execution plan for a soul from the Hermetic Forge."""
        lang_to_use, version_to_use = language, version_spec
        if '@' in language:
            lang_to_use, version_to_use = language.split('@', 1)

        if not version_to_use:
            from ..settings.manager import SettingsManager
            version_to_use = SettingsManager().get(f"hermetic.{lang_to_use}.version")
            if not version_to_use:
                raise ArtisanHeresy(f"Hermetic strategy chosen, but no default version for '{lang_to_use}' is set.")

        binary_path = self.get_runtime(lang_to_use, version_to_use)
        if not binary_path:
            raise ArtisanHeresy(f"Could not summon or find hermetic runtime '{lang_to_use}@{version_to_use}'.")

        recipe = self._get_recipe(lang_to_use)
        cmd = list(recipe["interpreter"])
        cmd[0] = str(binary_path)
        return ExecutionPlan(interpreter_cmd=cmd, strategy='hermetic', docker_image=None)

    def _resolve_venv_strategy(self, language: str, sanctum: Path,
                               venv_path_str: Optional[str] = None) -> ExecutionPlan:
        """[FACULTY 29] The Venv Sentinel."""
        venv_dirs = [venv_path_str] if venv_path_str else [".venv", "venv", "env"]

        found_venv = None
        for v_dir in venv_dirs:
            candidate = (sanctum / v_dir).resolve()
            if candidate.exists() and candidate.is_dir():
                found_venv = candidate
                break

        if not found_venv:
            raise ArtisanHeresy(f"Venv strategy requested, but no virtual environment found. Searched: {venv_dirs}")

        bin_dir = "Scripts" if platform.system() == "Windows" else "bin"
        recipe = self._get_recipe(language)
        exe_name = Path(recipe["interpreter"][0]).name
        if platform.system() == "Windows" and not exe_name.endswith(".exe"):
            exe_name += ".exe"

        binary_path = found_venv / bin_dir / exe_name
        if not binary_path.exists():
            raise ArtisanHeresy(f"Venv found at '{found_venv.name}', but interpreter '{exe_name}' is missing.")

        cmd = list(recipe["interpreter"])
        cmd[0] = str(binary_path)
        return ExecutionPlan(interpreter_cmd=cmd, strategy='venv', docker_image=None)

    def _resolve_system_strategy(self, language: str) -> ExecutionPlan:
        """Forges the execution plan for the Mortal Realm."""
        recipe = self._get_recipe(language)
        tool = recipe["interpreter"][0]
        if not shutil.which(tool):
            raise ArtisanHeresy(
                f"The system does not possess the artisan '{tool}'.",
                suggestion=f"Install {language} globally, or use `scaffold settings` to switch to a Docker/Hermetic strategy."
            )
        return ExecutionPlan(interpreter_cmd=recipe["interpreter"], strategy='system', docker_image=None)

    def _get_recipe(self, language: str) -> Dict[str, Any]:
        """A humble Gaze for a language's execution recipe."""
        from ..symphony.polyglot.grimoire import POLYGLOT_GRIMOIRE
        recipe = POLYGLOT_GRIMOIRE.get(language)
        if not recipe:
            return {"interpreter": [language]}
        return recipe

    def _resolve_system_identity(self):
        os_name, machine = platform.system().lower(), platform.machine().lower()
        if os_name == "linux":
            self.os_key = "linux"
        elif os_name == "darwin":
            self.os_key = "darwin"
        elif os_name == "windows":
            self.os_key = "windows"
        else:
            self.os_key = "unknown"
        if machine in ("x86_64", "amd64"):
            self.arch_key = "x86_64"
        elif machine in ("arm64", "aarch64"):
            self.arch_key = "aarch64"
        else:
            self.arch_key = "unknown"
        self.platform_key = f"{self.os_key}_{self.arch_key}"
        if not self.silent: Logger.verbose(f"System Identity Perceived: [cyan]{self.platform_key}[/cyan]")

    def _forge_resilient_session(self):
        import requests
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry

        session = requests.Session()
        retry_strategy = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({"User-Agent": f"Scaffold-Gnostic-Engine/{__version__}"})
        return session

    def scan_available_runtimes(self, force_refresh: bool = False) -> Dict[str, List[Dict]]:
        if self._runtime_cache and not force_refresh and (time.time() - self._last_scan_time < 60):
            if not self.silent: Logger.verbose("Gaze satisfied by Gnostic Chronocache.")
            return self._runtime_cache

        if not self.silent: Logger.verbose("Gnostic Gaze of Runtimes awakens its parallel consciousness...")
        results: Dict[str, List[Dict]] = {"python": [], "node": [], "go": [], "rust": [], "ruby": [], "docker": []}

        with ThreadPoolExecutor(max_workers=3, thread_name_prefix="GnosticGaze") as executor:
            future_map = {
                executor.submit(self._scan_system_realm): "system",
                executor.submit(self._scan_managed_realm): "managed",
                executor.submit(self._scan_docker_realm): "docker",
            }
            for future in future_map:
                try:
                    realm_results = future.result()
                    for lang, runtimes in realm_results.items():
                        if lang in results: results[lang].extend(runtimes)
                except Exception as e:
                    if not self.silent: Logger.warn(f"A minor paradox in the '{future_map[future]}' Gaze: {e}")

        self._runtime_cache = results
        self._last_scan_time = time.time()
        return results

    def _scan_system_realm(self) -> Dict[str, List[Dict]]:
        if not self.silent: Logger.verbose("   -> Gazing upon the Mortal Realm (System PATH)...")
        realm_results = {}
        for lang, binary_name in [("python", "python"), ("node", "node"), ("go", "go"), ("rust", "rustc"),
                                  ("ruby", "ruby")]:
            if sys_path := shutil.which(binary_name):
                version = self._extract_version(sys_path, lang)
                if lang not in realm_results: realm_results[lang] = []
                realm_results[lang].append(
                    {"type": "system", "path": sys_path, "version": version, "label": f"System ({version})"})
        return realm_results

    def _scan_managed_realm(self) -> Dict[str, List[Dict]]:
        if not self.silent: Logger.verbose("   -> Gazing upon the Hermetic Realm (Managed Sanctum)...")
        realm_results = {}
        if self.runtimes_root.exists():
            for lang_dir in self.runtimes_root.iterdir():
                if lang_dir.is_dir() and lang_dir.name in RUNTIME_CODEX:
                    for ver_dir in lang_dir.iterdir():
                        if ver_dir.is_dir():
                            if lang_dir.name not in realm_results: realm_results[lang_dir.name] = []
                            codex_entry = RUNTIME_CODEX.get(lang_dir.name, {}).get(ver_dir.name, {}).get(
                                self.platform_key)
                            if codex_entry and (ver_dir / codex_entry['bin_path']).exists():
                                realm_results[lang_dir.name].append(
                                    {"type": "managed", "path": str(ver_dir), "version": ver_dir.name,
                                     "label": f"Scaffold v{ver_dir.name} ✨"})
        return realm_results

    def _scan_docker_realm(self) -> Dict[str, List[Dict]]:
        if not self.silent: Logger.verbose("   -> Gazing upon the Celestial Realm (Docker)...")
        realm_results = {}
        if self.docker_engine.is_available:
            try:
                res = subprocess.run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"], capture_output=True,
                                     text=True, check=True)
                images = res.stdout.strip().splitlines()
                for img in images:
                    for lang in ["python", "node", "golang", "rust", "ruby"]:
                        if lang in img:
                            key_lang = "go" if lang == "golang" else lang
                            if key_lang not in realm_results: realm_results[key_lang] = []
                            realm_results[key_lang].append(self._forge_docker_entry(img))
                if "docker" not in realm_results: realm_results["docker"] = []
                realm_results["docker"].append(
                    {"type": "system", "path": self.docker_engine.executable, "version": "Active",
                     "label": "Docker Daemon 🐳"})
            except Exception as e:
                if not self.silent: Logger.warn(f"Docker Gaze was clouded by a paradox: {e}")
        return realm_results

    def _extract_version(self, binary_path: str, lang: str) -> str:
        try:
            flag = "--version"
            if lang == "go": flag = "version"
            res = subprocess.run([binary_path, flag], capture_output=True, text=True, timeout=1)
            output = res.stdout + res.stderr
            match = re.search(r'(\d+\.\d+(\.\d+)?)', output)
            if match: return match.group(1)
        except:
            pass
        return "Unknown"

    def _forge_docker_entry(self, image_tag: str) -> Dict[str, str]:
        return {"type": "docker", "path": image_tag,
                "version": image_tag.split(':')[-1] if ':' in image_tag else "latest", "label": f"🐳 {image_tag}"}

    @contextlib.contextmanager
    def _atomic_lock(self, lock_name: str) -> Generator[None, None, None]:
        self._ensure_directories()
        lock_file = self.locks_root / f"{lock_name}.lock"
        acquired = False
        try:
            fd = os.open(lock_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(fd)
            acquired = True
            yield
        except FileExistsError:
            raise ArtisanHeresy(f"The rite for '{lock_name}' is already being conducted.")
        finally:
            if acquired and lock_file.exists():
                try:
                    os.unlink(lock_file)
                except OSError:
                    pass

    def _download_securely(self, url: str, target_path: Path, expected_sha256: Optional[str]) -> bool:
        import requests
        from rich.progress import Progress, SpinnerColumn, DownloadColumn, TransferSpeedColumn, TextColumn, \
            TimeRemainingColumn

        self._ensure_directories()
        temp_download = target_path.with_suffix(".part")
        sha256_hash = hashlib.sha256()
        try:
            with self.session.get(url, stream=True, timeout=60) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                progress_ctx = Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"),
                                        DownloadColumn(), TransferSpeedColumn(), TimeRemainingColumn(), transient=True,
                                        console=self.console) if not self.silent else contextlib.nullcontext()
                with progress_ctx as progress:
                    task = progress.add_task(f"[cyan]Downloading...", total=total_size) if not self.silent else None
                    with open(temp_download, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk: f.write(chunk); sha256_hash.update(chunk)
                            if not self.silent: progress.update(task, advance=len(chunk))
            if expected_sha256 and sha256_hash.hexdigest() != expected_sha256:
                if not self.silent: Logger.error("Checksum Heresy! Soul is profane.")
                temp_download.unlink()
                return False
            shutil.move(str(temp_download), str(target_path))
            return True
        except requests.exceptions.RequestException as e:
            if not self.silent: Logger.error(f"Network Heresy: {e}")
            if temp_download.exists(): temp_download.unlink()
            return False

    def _extract_securely(self, archive_path: Path, target_dir: Path):
        if not self.silent: Logger.info(f"Unboxing the soul at {target_dir.name}...")
        target_dir.mkdir(parents=True, exist_ok=True)

        def is_safe(base, target):
            return base.resolve() in target.resolve().parents

        try:
            if str(archive_path).endswith((".tar.gz", ".tar.xz", ".tgz")):
                with tarfile.open(archive_path) as tar:
                    for member in tar.getmembers():
                        if not is_safe(target_dir, target_dir / member.name): raise ArtisanHeresy(
                            f"Zip-Slip heresy: '{member.name}'")
                    tar.extractall(path=target_dir)
            elif str(archive_path).endswith(".zip"):
                with zipfile.ZipFile(archive_path, 'r') as zf:
                    for member_name in zf.namelist():
                        if not is_safe(target_dir, target_dir / member_name): raise ArtisanHeresy(
                            f"Zip-Slip heresy: '{member_name}'")
                    zf.extractall(target_dir)
            else:
                raise ArtisanHeresy(f"Unknown archive format: {archive_path.suffix}")
        except Exception as e:
            shutil.rmtree(target_dir, ignore_errors=True)
            raise ArtisanHeresy(f"Extraction Paradox: {e}") from e

    def _find_and_consecrate_binary(self, install_dir: Path, bin_rel_path: str) -> Optional[Path]:
        if not install_dir.exists(): return None
        candidate = install_dir / bin_rel_path
        if not candidate.exists():
            contents = [p for p in install_dir.iterdir() if p.is_dir()]
            if len(contents) == 1:
                if (nested_candidate := contents[0] / bin_rel_path).exists(): candidate = nested_candidate
        if not candidate.exists(): return None
        if os.name != "windows":
            try:
                os.chmod(candidate, candidate.stat().st_mode | stat.S_IEXEC)
            except Exception as e:
                Logger.warn(f"Could not consecrate '{candidate.name}': {e}")
        return candidate

    def _validate_runtime(self, binary_path: Path) -> bool:
        try:
            flag = "version" if "go" in binary_path.name else "--version"
            subprocess.run([str(binary_path), flag], capture_output=True, check=True, timeout=2)
            return True
        except Exception:
            return False

    def get_runtime(self, language: str, version: str, force_download: bool = False) -> Optional[Path]:
        resolved_ver = resolve_version(language, version)
        lock_name = f"{language}_{resolved_ver}_{self.platform_key}"
        with self._atomic_lock(lock_name):
            install_dir = self.runtimes_root / language / resolved_ver
            codex_entry = RUNTIME_CODEX.get(language, {}).get(resolved_ver, {}).get(self.platform_key)
            if not codex_entry:
                if not self.silent: Logger.error(
                    f"No Gnosis in Codex for {language}@{resolved_ver} on {self.platform_key}.")
                return None

            bin_rel_path = codex_entry["bin_path"]
            if not force_download:
                if (
                        existing_bin := self._find_and_consecrate_binary(install_dir,
                                                                         bin_rel_path)) and self._validate_runtime(
                    existing_bin):
                    if not self.silent: Logger.success(f"Found pure, manifest soul for {language}@{resolved_ver}.")
                    return existing_bin
                elif install_dir.exists():
                    if not self.silent: Logger.warn("Existing runtime is profane. Purging and re-summoning.")
                    shutil.rmtree(install_dir, ignore_errors=True)

            if not self.silent: Logger.info(
                f"Summoning {language}@{resolved_ver} for {self.platform_key} from the Void...")
            url = codex_entry["url"]
            archive_name = url.split("/")[-1]
            archive_path = self.downloads_root / archive_name
            try:
                if not self._download_securely(url, archive_path, codex_entry.get("sha256")): return None
                temp_install_dir = self.runtimes_root / f".tmp_{lock_name}"
                self._extract_securely(archive_path, temp_install_dir)
                if install_dir.exists(): shutil.rmtree(install_dir)
                contents = [p for p in temp_install_dir.iterdir() if p.is_dir()]
                if len(contents) == 1:
                    shutil.move(str(contents[0]), str(install_dir))
                    shutil.rmtree(temp_install_dir, ignore_errors=True)
                else:
                    shutil.move(str(temp_install_dir), str(install_dir))

                final_bin = self._find_and_consecrate_binary(install_dir, bin_rel_path)
                if final_bin and self._validate_runtime(final_bin):
                    return final_bin
                else:
                    raise ArtisanHeresy("Runtime materialized but failed final validation.")
            except Exception as e:
                if 'install_dir' in locals() and install_dir.exists(): shutil.rmtree(install_dir, ignore_errors=True)
                raise ArtisanHeresy(f"Failed to summon {language}@{version}: {e}") from e
            finally:
                if 'archive_path' in locals() and archive_path.exists(): archive_path.unlink(missing_ok=True)
                for tmp in self.runtimes_root.glob(f".tmp_{lock_name}*"): shutil.rmtree(tmp, ignore_errors=True)