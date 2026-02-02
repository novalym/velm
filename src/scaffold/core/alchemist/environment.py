# Path: scaffold/core/alchemist/environment.py
# --------------------------------------------

import inspect
from typing import Any

from jinja2 import Environment
from jinja2.exceptions import FilterArgumentError

from ...logger import Scribe
from ...logger import get_console
from ...jurisprudence_core.gnostic_type_system import adjudicate_gnostic_purity

# We create a localized scribe for this module to avoid circular dependencies on the main Alchemist logger
Logger = Scribe("ParanoidEnvironment")


class ParanoidEnvironment(Environment):
    """A divine, hyper-aware Jinja environment."""

    def handle_missing(self, name):
        Logger.warn(f"Gnostic Paradox: The variable '{name}' was summoned but is a void. Resolving as empty.")
        return ''


def gnostic_validation_rite(value: Any, *rules: str) -> Any:
    """
    The divine rite that adjudicates a value's purity against the Gnostic Grimoire.
    This is the soul of the `| validate(...)` filter.
    """
    if not rules:
        return value

    rule_string = '|'.join(rules)
    is_pure, heresy = adjudicate_gnostic_purity(str(value), rule_string)

    if not is_pure:
        raise FilterArgumentError(f"Gnostic Adjudication Failed for value '{value}'. Reason: {heresy}")

    return value


def gnostic_native_rite(value: Any, context: Any) -> str:
    """
    The God-Engine of Gnostic Polyglotism.
    Transmutes Gnosis into the native tongue of the target file.
    """
    import json
    from pathlib import Path

    # Context is a jinja2.runtime.Context object, we access vars via parent or direct get
    target_path = context.get('_target_path')
    target_ext = Path(target_path).suffix if target_path else ".txt"

    # Gaze for languages where booleans are lowercase
    if target_ext in ['.go', '.js', '.ts', '.rs', '.java', '.json', '.yml', '.yaml']:
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, (int, float)):
            return str(value)
        return json.dumps(str(value))

    # Gaze for Python
    elif target_ext == '.py':
        return repr(value)

    return str(value)


def paranoid_finalizer(value: Any, env_globals: dict, env_filters: dict, env_tests: dict) -> Any:
    """
    The Omniscient Guardian.
    Adjudicates the purity of function calls within templates.
    """
    if value is None:
        Logger.warn("Gnostic Paradox: An expression resolved to a void (None). Proclaiming as empty string.")
        return ""

    if not callable(value):
        return value

    # The Guardian first gazes upon its own, consecrated souls.
    if (value in env_globals.values() or
            value in env_filters.values() or
            value in env_tests.values()):
        return value

    try:
        module_name = inspect.getmodule(value).__name__ if inspect.getmodule(value) else ""
        if module_name.startswith('jinja2.'):
            return value

        # If we are here, a Heresy of the Unsummoned Artisan has occurred.
        from rich.panel import Panel
        from rich.text import Text
        from rich.table import Table
        from rich.console import Group

        console = get_console()

        func_name = getattr(value, '__name__', 'unknown')
        func_lineno = "unknown line"
        try:
            func_lineno = inspect.getsourcelines(value)[1]
        except (TypeError, AttributeError, OSError):
            pass

        dossier_table = Table(box=None, show_header=False, padding=(0, 1))
        dossier_table.add_column(style="dim", justify="right", width=18)
        dossier_table.add_column(style="white")
        dossier_table.add_row("Profane Artisan:", f"[bold red]{func_name}[/bold red]")
        dossier_table.add_row("Origin:", f"[cyan]{module_name}[/cyan] (line ~{func_lineno})")

        heresy_text = Text.assemble(
            ("A callable artisan was proclaimed without being summoned (did you forget the parentheses?).\n", "white"))

        console.print(Panel(
            Group(heresy_text, dossier_table),
            title="[bold red]Gnostic Inquest: The Unsummoned Artisan[/bold red]",
            border_style="red"
        ))

    except Exception as e:
        Logger.error(f"META-HERESY: A paradox occurred within the Grand Inquisitor's Gaze: {e}")

    return f"!!HERESY:UNCALLED_FUNCTION:{getattr(value, '__name__', 'unknown')}!!"