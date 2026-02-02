# path: scaffold/artisans/repl_artisan.py

import json
import re
import shlex
import subprocess
from typing import Dict, Any, Optional

from rich.console import Console
from rich.pretty import Pretty
from rich.prompt import Prompt

from ..core.artisan import BaseArtisan
from ..interfaces.base import ScaffoldResult
from ..interfaces.requests import ReplRequest
from ..help_registry import register_artisan
from ..contracts.heresy_contracts import ArtisanHeresy


# =============================================================================
# == THE PANTHEON OF POLYGLOT CONDUCTORS                                     ==
# =============================================================================

class _BaseConductor:
    """The abstract soul of a language executor."""

    def __init__(self, artisan: 'ReplArtisan'):
        self.artisan = artisan

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        raise NotImplementedError


class _PythonConductor(_BaseConductor):
    """Conducts Python rites."""

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        try:
            # Try to eval as an expression first to capture return values
            return eval(code, context)
        except SyntaxError:
            # If it's not an expression, exec it as a statement
            exec(code, context)
            return None  # Statements have no return value
        except Exception as e:
            raise ArtisanHeresy("Python execution paradox.", child_heresy=e)


class _JavaScriptConductor(_BaseConductor):
    """Conducts Node.js rites."""

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        # Transmute Python context into JS const declarations
        prelude = []
        for key, value in context.items():
            if not key.startswith("_"):  # Ignore internals
                prelude.append(f"const {key} = {json.dumps(value)};")

        full_script = "\n".join(prelude) + "\n" + code

        try:
            result = subprocess.run(
                ["node", "-e", full_script],
                capture_output=True, text=True, check=True
            )
            # We return stdout for JS, as console.log is the primary output
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy(f"JavaScript execution heresy.", details=e.stderr, child_heresy=e)
        except FileNotFoundError:
            raise ArtisanHeresy("The `node` artisan is not manifest in this reality's PATH.")


class _ShellConductor(_BaseConductor):
    """Conducts shell rites."""

    def execute(self, code: str, context: Dict[str, Any]) -> Any:
        # Inject context as environment variables
        env = os.environ.copy()
        for key, value in context.items():
            if not key.startswith("_") and isinstance(value, (str, int, float)):
                env[f"SC_{key.upper()}"] = str(value)

        try:
            result = subprocess.run(
                code, shell=True, capture_output=True, text=True, check=True, cwd=self.artisan.project_root, env=env
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise ArtisanHeresy(f"Shell execution heresy.", details=e.stderr, child_heresy=e)


# =============================================================================
# == THE GNOSTIC CONDUCTOR (THE REPL ARTISAN)                                ==
# =============================================================================

@register_artisan("repl")
class ReplArtisan(BaseArtisan[ReplRequest]):
    """The Tower of Babel: A Gnostic Polyglot REPL."""

    # `var = lang(...)` or `lang(...)`
    COMMAND_REGEX = re.compile(r"^\s*(?:([a-zA-Z_]\w*)\s*=\s*)?([a-z]{2,4})\((.*)\)\s*$", re.DOTALL)

    def execute(self, request: ReplRequest) -> ScaffoldResult:
        self.logger.info("The Polyglot Conduit is open. Welcome to the Tower of Babel.")
        self.console.print(
            "[dim]Speak your will, Architect. (e.g., `x = py('1+1')`, `js('console.log(x)')`, `sh('ls')`, or `exit`)\n")

        session_state: Dict[str, Any] = {}
        console = Console()

        conductors = {
            "py": _PythonConductor(self),
            "js": _JavaScriptConductor(self),
            "sh": _ShellConductor(self),
        }

        while True:
            try:
                raw_input = Prompt.ask(">>>")
                if raw_input.lower() in ('exit', 'quit', 'exit()'):
                    break

                match = self.COMMAND_REGEX.match(raw_input)
                if not match:
                    console.print("[bold red]Heresy:[/bold red] Unrecognized plea. Syntax: `[var =] py|js|sh(...)`")
                    continue

                var_name, lang, code_raw = match.groups()

                # Un-escape string literal if present
                code = code_raw.strip().strip("'\"")

                conductor = conductors.get(lang)
                if not conductor:
                    console.print(f"[bold red]Heresy:[/bold red] The tongue '{lang}' is unknown to this Conduit.")
                    continue

                # Conduct the rite
                result = conductor.execute(code, session_state)

                # Proclaim the result
                if result is not None:
                    console.print(Pretty(result))

                # Update the Gnostic State Cell
                if var_name:
                    session_state[var_name] = result
                    console.print(f"[dim]Gnosis '{var_name}' is now enshrined.[/dim]")

            except ArtisanHeresy as e:
                console.print(f"[bold red]Heresy:[/bold red] {e.message}")
                if e.details:
                    console.print(f"[dim]{e.details}[/dim]")
            except KeyboardInterrupt:
                console.print("\n[dim]The Architect wills silence.[/dim]")
                break
            except Exception as e:
                console.print(f"[bold red]Catastrophic Paradox:[/bold red] {e}")

        return self.success("Communion with the Polyglot Conduit is complete.")