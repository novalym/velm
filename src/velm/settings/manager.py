# Path: scaffold/settings/manager.py
# ----------------------------------

"""
=================================================================================
== THE ORACLE OF CONFIGURATION (V-Ω-ETERNAL-HIERARCHY)                         ==
=================================================================================
LIF: 10,000,000,000,000

This is the sentient brain of the Settings ecosystem. It manages the "Cascade of
Truth" for configuration and performs the "All-Seeing Gaze" to discover available
runtimes across the System, Managed, and Celestial (Docker) realms.

It is the single source of truth for the will of the Architect.
"""
import os
import re
import shutil
import subprocess
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from ..logger import Scribe

# --- THE SHADOW SWAP: JSON ALCHEMY (FACULTY 2) ---
try:
    import orjson


    class GnosticJson:
        @staticmethod
        def loads(content: str) -> Any: return orjson.loads(content)

        @staticmethod
        def dumps(obj: Any, indent: int = None) -> str:
            options = 0
            if indent: options |= orjson.OPT_INDENT_2
            return orjson.dumps(obj, option=options).decode('utf-8')


    json_lib = GnosticJson
    Scribe("JSON_Alchemist").verbose("orjson found. Engaging high-performance JSON.")
except ImportError:
    import json as json_lib
# --- END SHADOW SWAP ---

from .schema import get_default_config, DEFAULT_SETTINGS_SCHEMA
from ..containerization import DockerEngine

Logger = Scribe("SettingsManager")


class SettingsManager:
    """
    The Oracle of Configuration.
    Resolves: Defaults -> Global Config -> Project Config -> Env Vars.
    """

    def __init__(self, project_root: Optional[Path] = None):
        self.global_config_path = Path.home() / ".scaffold" / "config.json"
        self.project_config_path = (project_root / ".scaffold" / "config.json") if project_root else None

        # The Cache of Truth
        self._effective_config: Dict[str, Any] = {}
        self._runtime_cache: Optional[Dict[str, List[Dict]]] = None
        self._last_scan_time = 0.0

        # [FACULTY 12] The Lazy Gaze
        self._docker_engine: Optional[DockerEngine] = None

        self.reload()

    @property
    def docker_engine(self) -> DockerEngine:
        """Lazy-loads the Docker engine to avoid startup cost if not needed."""
        if self._docker_engine is None:
            self._docker_engine = DockerEngine()
        return self._docker_engine

    def reload(self):
        """
        [THE RITE OF HIERARCHICAL MERGE]
        Re-calculates the effective configuration from all sources.
        Layers of Precedence (Lowest to Highest):
        1. Schema Defaults
        2. Global Config (~/.scaffold/config.json)
        3. Project Config (./.scaffold/config.json)
        4. Environment Variables (SCAFFOLD_CATEGORY_KEY)
        """
        # 1. Defaults
        base = get_default_config()

        # 2. Global
        if self.global_config_path.exists():
            try:
                global_conf = json_lib.loads(self.global_config_path.read_text(encoding='utf-8'))
                base.update(global_conf)
            except Exception as e:
                Logger.warn(f"Global config corrupted: {e}")

        # 3. Project (Highest File Precedence)
        if self.project_config_path and self.project_config_path.exists():
            try:
                proj_conf = json_lib.loads(self.project_config_path.read_text(encoding='utf-8'))
                base.update(proj_conf)
                Logger.verbose("Project-specific settings have been applied.")
            except Exception as e:
                Logger.warn(f"Project config corrupted: {e}")

        # 4. Environment Override (The Transient Supremacy) (FACULTY 5 & 6)
        for setting in DEFAULT_SETTINGS_SCHEMA:
            env_key = "SCAFFOLD_" + setting.key.replace(".", "_").upper()
            env_val = os.getenv(env_key)
            if env_val is not None:
                # Basic type casting based on schema expectation
                if setting.value_type == "bool":
                    base[setting.key] = env_val.lower() in ('true', '1', 'yes')
                elif setting.value_type == "int":
                    try:
                        base[setting.key] = int(env_val)
                    except (ValueError, TypeError):
                        pass
                elif setting.value_type == "float":
                    try:
                        base[setting.key] = float(env_val)
                    except (ValueError, TypeError):
                        pass
                else:
                    base[setting.key] = env_val
                Logger.verbose(f"Environment override applied: {setting.key} -> {base[setting.key]}")

        self._effective_config = base

    def get(self, key: str, default: Any = None) -> Any:
        """
        [FACULTY 1] THE UNBREAKABLE CONTRACT
        Retrieves a setting value, returning 'default' if not found.
        """
        val = self._effective_config.get(key, default)

        # [FACULTY 7] The Path Alchemist
        if isinstance(val, str) and val.startswith("~/"):
            return str(Path(val).expanduser())

        return val

    def set_global(self, key: str, value: Any):
        """Inscribes a setting into the User's Global Soul."""
        self._write_setting(self.global_config_path, key, value)

    def set_project(self, key: str, value: Any):
        """Inscribes a setting into the Project's Soul."""
        if not self.project_config_path:
            raise ValueError("No project active. Cannot set project-level settings.")
        self._write_setting(self.project_config_path, key, value)

    def _write_setting(self, path: Path, key: str, value: Any):
        """[FACULTY 8] The Atomic Inscription."""
        path.parent.mkdir(parents=True, exist_ok=True)
        current = {}
        if path.exists():
            try:
                current = json_lib.loads(path.read_text(encoding='utf-8'))
            except:
                pass

        current[key] = value

        temp_path = path.with_suffix(f".{os.getpid()}.tmp")
        temp_path.write_text(json_lib.dumps(current, indent=2), encoding='utf-8')
        shutil.move(str(temp_path), str(path))

        self.reload()

    def bootstrap_project_config(self):
        """
        [FACULTY 3] THE RITE OF EJECTION
        Materializes the current effective configuration into the Project Sanctum.
        This 'locks' the project to the current defaults, ensuring reproducibility.
        """
        if not self.project_config_path:
            # If no project config path exists (rootless), forge it in CWD
            cwd = Path.cwd()
            self.project_config_path = cwd / ".scaffold" / "config.json"

        self.project_config_path.parent.mkdir(parents=True, exist_ok=True)

        # We replicate the current effective config, but purely
        current_state = self._effective_config.copy()

        self.project_config_path.write_text(json_lib.dumps(current_state, indent=2), encoding='utf-8')
        Logger.success(f"Configuration ejected to [cyan]{self.project_config_path}[/cyan]")
        self.reload()

    def scan_available_runtimes(self, force_refresh: bool = False) -> Dict[str, List[Dict[str, str]]]:
        """
        Performs a Gnostic Gaze upon the machine to find all executable souls.
        Returns: { 'python': [{type: 'system', path: '...', version: '...'}], ... }
        """
        if self._runtime_cache and not force_refresh and (time.time() - self._last_scan_time < 60):
            return self._runtime_cache

        results = {
            "python": [], "node": [], "go": [], "rust": [], "ruby": [], "docker": []
        }

        # 1. System Scan (PATH)
        for lang in ["python", "node", "go", "rustc", "ruby"]:
            sys_path = shutil.which(lang)
            key_lang = "rust" if lang == "rustc" else lang
            if key_lang not in results: continue
            if sys_path:
                version = self._extract_version(sys_path, lang)
                results[key_lang].append({
                    "type": "system", "path": sys_path, "version": version, "label": f"System ({version})"
                })

        # 2. Managed Scan (~/.scaffold/runtimes)
        runtimes_dir = Path.home() / ".scaffold" / "runtimes"
        if runtimes_dir.exists():
            for lang_dir in runtimes_dir.iterdir():
                if lang_dir.name in results:
                    for ver_dir in lang_dir.iterdir():
                        if ver_dir.is_dir():
                            results[lang_dir.name].append({
                                "type": "managed", "path": str(ver_dir), "version": ver_dir.name,
                                "label": f"Scaffold v{ver_dir.name} ✨"
                            })

        # 3. Celestial Scan (Docker Images)
        if self.docker_engine.is_available:
            try:
                res = subprocess.run(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"], capture_output=True,
                                     text=True)
                images = res.stdout.splitlines()
                for img in images:
                    if "python" in img:
                        results["python"].append(self._forge_docker_entry(img))
                    elif "node" in img:
                        results["node"].append(self._forge_docker_entry(img))
                    elif "golang" in img or "/go" in img:
                        results["go"].append(self._forge_docker_entry(img))
                    elif "rust" in img:
                        results["rust"].append(self._forge_docker_entry(img))
                    elif "ruby" in img:
                        results["ruby"].append(self._forge_docker_entry(img))
                results["docker"].append(
                    {"type": "system", "path": self.docker_engine.executable, "version": "Available",
                     "label": "Docker Daemon Active"})
            except Exception as e:
                Logger.warn(f"Docker scan failed: {e}")

        self._runtime_cache = results
        self._last_scan_time = time.time()
        return results

    def _extract_version(self, binary_path: str, lang: str) -> str:
        """[FACULTY 3] The Version Alchemist."""
        try:
            flag = "--version"
            if lang == "go": flag = "version"
            res = subprocess.run([binary_path, flag], capture_output=True, text=True, timeout=1)
            output = res.stdout + res.stderr
            match = re.search(r'(\d+\.\d+(\.\d+)?)', output)
            if match:
                return match.group(1)
        except:
            pass
        return "Unknown"

    def _forge_docker_entry(self, image_tag: str) -> Dict[str, str]:
        return {
            "type": "docker", "path": image_tag,
            "version": image_tag.split(':')[-1] if ':' in image_tag else "latest",
            "label": f"🐳 {image_tag}"
        }