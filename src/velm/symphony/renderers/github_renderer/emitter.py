# Path: scaffold/symphony/renderers/github_renderer/emitter.py
# ------------------------------------------------------------

import sys
import os
from typing import Optional, Dict, Any
from .sanitizer import GnosticSanitizer


class GHAEmitter:
    """
    =================================================================================
    == THE WORKFLOW COMMANDER (V-Ω-GHA-PROTOCOL)                                   ==
    =================================================================================
    LIF: 10,000,000,000

    Speaks the divine tongue of `::workflow-command parameter=value::message`.

    Reference: https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
    """

    def _command(self, command: str, value: str = "", params: Optional[Dict[str, Any]] = None):
        """Low-level command issuer."""
        params_str = ""
        if params:
            # Join properties with commas, key=value
            parts = [f"{k}={GnosticSanitizer.escape_property(v)}" for k, v in params.items() if v is not None]
            if parts:
                params_str = " " + ",".join(parts)

        # We perform a direct write to stdout to ensure the runner catches it immediately.
        print(f"::{command}{params_str}::{value}", flush=True)

    def start_group(self, title: str):
        """Create a collapsible log group."""
        self._command("group", title)

    def end_group(self):
        """Close the current group."""
        self._command("endgroup")

    def debug(self, message: str):
        """Visible only if ACTIONS_STEP_DEBUG is true."""
        self._command("debug", message)

    def notice(self, message: str, title: str = "", file: str = None, line: int = None):
        """Creates a neutral annotation."""
        params = {}
        if title: params["title"] = title
        if file: params["file"] = file
        if line: params["line"] = line
        self._command("notice", message, params)

    def warning(self, message: str, title: str = "", file: str = None, line: int = None):
        """Creates a warning annotation."""
        params = {}
        if title: params["title"] = title
        if file: params["file"] = file
        if line: params["line"] = line
        self._command("warning", message, params)

    def error(self, message: str, title: str = "", file: str = None, line: int = None):
        """
        Creates an error annotation. This will highlight code in PRs and mark the step as failed.
        """
        params = {}
        if title: params["title"] = title
        if file: params["file"] = file
        if line: params["line"] = line
        self._command("error", message, params)

    def mask_secret(self, secret: str):
        """Instructs the runner to mask this string in all future logs."""
        if secret and len(secret) > 3:  # Avoid masking common short words like 'true'
            self._command("add-mask", secret)

    def set_env(self, key: str, value: str):
        """Writes to GITHUB_ENV file (the modern way)."""
        env_file = os.getenv("GITHUB_ENV")
        if env_file:
            try:
                with open(env_file, "a", encoding="utf-8") as f:
                    # Use heredoc syntax for safety with multiline values
                    delimiter = "EOF_SCAFFOLD_ENV"
                    f.write(f"{key}<<{delimiter}\n{value}\n{delimiter}\n")
            except Exception:
                # Fallback if file IO fails
                pass

    def raw_log(self, message: str):
        """Standard log output, flushed immediately."""
        print(message, flush=True)