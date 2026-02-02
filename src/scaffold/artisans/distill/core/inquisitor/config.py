# Path: artisans/distill/core/inquisitor/config.py
# ------------------------------------------------

import re
import subprocess
import shutil
from typing import List, Dict, Set
from pathlib import Path

from .....core.cortex.contracts import FileGnosis
from .....logger import Scribe

Logger = Scribe("ConfigCartographer")


class ConfigurationCartographer:
    """
    =================================================================================
    == THE CONFIGURATION CARTOGRAPHER (THE SCRIBE OF GNOSIS FLOWS)                 ==
    =================================================================================
    This artisan is a master of perceiving the flow of Gnostic configuration.
    When it encounters a configuration scripture (.env, settings.toml, etc.), it
    extracts every variable defined within. It then performs a hyper-performant
    `ripgrep` across the entire project for each variable name, building a complete
    map of where each piece of Gnosis is consumed.

    This map is then attached to the `FileGnosis` vessel of the configuration file,
    ready to be inscribed into the final blueprint by the `ContentWeaver`.
    =================================================================================
    """

    # Heuristic regex for finding variable definitions in .env or .toml files
    CONFIG_VAR_REGEX = re.compile(r"^([A-Z0-9_]+)\s*=", re.MULTILINE)

    def __init__(self, project_root: Path):
        self.root = project_root
        self.rg_path = shutil.which("rg")  # Ripgrep for hyper-performance

    def map_gnosis_flows(self, config_file: FileGnosis):
        """
        Performs the Gaze upon a single configuration file and maps its influence.
        Updates the `FileGnosis` object in-place.
        """
        if not self.rg_path:
            Logger.warn("The `rg` (ripgrep) artisan is not manifest. Configuration tracing will be skipped.")
            return

        try:
            content = (self.root / config_file.path).read_text(encoding='utf-8')
        except Exception:
            return  # Cannot read the file

        variables = self.CONFIG_VAR_REGEX.findall(content)
        if not variables:
            return

        usage_map: Dict[str, List[str]] = {}
        for var in variables:
            try:
                # Use ripgrep to find all occurrences of the variable name
                # rg -l VAR_NAME .
                result = subprocess.run(
                    [self.rg_path, "-l", "--", var, "."],
                    cwd=self.root,
                    capture_output=True,
                    text=True,
                    check=True,
                    encoding='utf-8'
                )

                # Collect and normalize paths, excluding the config file itself
                usage_files = [
                    f.strip() for f in result.stdout.splitlines()
                    if f.strip() != str(config_file.path)
                ]
                if usage_files:
                    usage_map[var] = usage_files

            except (subprocess.CalledProcessError, FileNotFoundError):
                continue  # Ripgrep might fail if no matches are found or if it's not installed

        if usage_map:
            # We attach this rich Gnosis to the ast_metrics vessel for later rendering.
            if config_file.ast_metrics is None:
                config_file.ast_metrics = {}
            config_file.ast_metrics["config_usage_map"] = usage_map