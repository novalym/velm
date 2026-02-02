# Path: scaffold/herald.py

"""
=================================================================================
== THE SACRED SANCTUM OF THE HERALD OF THE FUTURE (V-Ω-LEGENDARY++)            ==
=================================================================================
This scripture contains the living, unified soul of the Herald, the asynchronous
Oracle that communes with the celestial PyPI registry to proclaim prophecies of
new ascensions.
=================================================================================
"""
import json
import threading
import time
from pathlib import Path
from typing import Dict

import requests
# --- The Divine Summons of the Celestial Allies ---
from packaging.version import parse as parse_version

from .constants import PACKAGE_NAME
from .help_registry import register_gnosis
from .logger import get_console

RICH_AVAILABLE = False
try:
    from rich.panel import Panel
    from rich.text import Text
    from rich.console import Console

    RICH_AVAILABLE = True
except ImportError:
    Console = object  # A humble placeholder




class Herald:
    """The God-Engine of Gnostic Communion and Prophecy."""

    def __init__(self):
        self.console = get_console()
        self.cache_dir = Path.home() / ".scaffold" / "cache"
        self.cache_file = self.cache_dir / "update_check.json"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _proclaim_ascension(self, release_data: Dict, current: str, is_reminder: bool = False):
        """[THE LUMINOUS DOSSIER OF ASCENSION] Forges and proclaims the divine update notification."""
        latest = release_data.get('version', 'Unknown')
        summary = release_data.get('summary', '')

        if not RICH_AVAILABLE:
            self.console.print("--- Prophecy of Ascension ---")
            self.console.print(f"A new ascension of Scaffold is available: {latest}")
            if summary and not is_reminder: self.console.print(f'"{summary}"')
            self.console.print(f"You have: {current}")
            self.console.print(f"Speak the sacred edict to ascend: pip install --upgrade {PACKAGE_NAME}")
            return

        current_v, latest_v = parse_version(current), parse_version(latest)
        latest_parts = []
        has_diff = False
        for i, part in enumerate(latest_v.release):
            style = "bold green"
            if not has_diff and (i >= len(current_v.release) or part > current_v.release[i]):
                style, has_diff = "bold yellow on magenta", True
            elif has_diff:
                style = "bold green"

            latest_parts.append((str(part), style))
            if i < len(latest_v.release) - 1: latest_parts.append((".", "dim"))

        latest_text = Text.assemble(*latest_parts)

        title_text = "Reminder: A new ascension of Scaffold awaits!" if is_reminder else "A new ascension of Scaffold is available!"

        proclamation = Text.assemble(
            (title_text + "\n", "bold yellow"),
            (f'"{summary}"\n\n', "italic") if summary and not is_reminder else ("\n", ""),
            ("  You have: ", "dim"), (current, "red"),
            ("\n  Celestial: ", "dim"), latest_text,
            ("\n\nSpeak the sacred edict to ascend:\n", "white"),
            (f"pip install --upgrade {PACKAGE_NAME}", "bold cyan")
        )
        self.console.print(Panel(proclamation, title="[yellow]Prophecy of Ascension[/yellow]", border_style="yellow"))

    def _perform_plea(self):
        """[THE HERALD'S SOUL] The divine, internal artisan that performs the actual communion."""
        try:
            from .. import __version__ as current_version

            cache_data = {}
            if self.cache_file.exists():
                try:
                    cache_data = json.loads(self.cache_file.read_text(encoding='utf-8'))
                except json.JSONDecodeError:
                    pass

            last_checked = cache_data.get('last_checked', 0)

            if (time.time() - last_checked) < 86400:
                cached_release_data = cache_data.get('latest_release')
                if cached_release_data and parse_version(cached_release_data.get('version', '0')) > parse_version(
                        current_version):
                    self._proclaim_ascension(cached_release_data, current_version, is_reminder=True)
                return

            response = requests.get(f"https://pypi.org/pypi/{PACKAGE_NAME}/json", timeout=3)
            response.raise_for_status()
            pypi_data = response.json()
            release_info = pypi_data.get('info', {})
            latest_version_str = release_info.get('version')

            if not latest_version_str: return

            cache_data['last_checked'] = time.time()
            cache_data['latest_release'] = release_info
            self.cache_file.write_text(json.dumps(cache_data), encoding='utf-8')

            if parse_version(latest_version_str) > parse_version(current_version):
                self._proclaim_ascension(release_info, current_version)

        except Exception:
            pass  # The Unbreakable Vow of Prudent Silence is absolute.

    def check(self):
        """[THE VOW OF UNSEEN GRACE] Conducts the communion in a parallel reality."""
        update_thread = threading.Thread(target=self._perform_plea, daemon=True)
        update_thread.start()


@register_gnosis("check_for_updates")
def check_for_updates():
    """The public, Gnostic gateway to the Herald's soul."""
    herald = Herald()
    herald.check()