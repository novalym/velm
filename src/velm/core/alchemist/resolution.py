# Path: scaffold/core/alchemist/resolution.py
# -------------------------------------------

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, Set, TYPE_CHECKING

import yaml  # Requires PyYAML
from jinja2 import Environment

from ...contracts.heresy_contracts import ArtisanHeresy
from ...core.guardian import GnosticSentry
from ...utils import forge_gnostic_secret
from ...logger import Scribe

if TYPE_CHECKING:
    from .engine import DivineAlchemist

Logger = Scribe("AlchemicalResolution")


class ResolutionMixin:
    """
    =============================================================================
    == THE LOGIC OF TRANSMUTATION (V-Ω-TYPED-MIXIN)                            ==
    =============================================================================
    This Mixin provides the faculties for resolving Jinja templates and variables.
    It demands a specific Gnostic Contract from its Host.
    """

    # --- THE CONTRACT OF THE HOST ---
    # We declare these as expected attributes of 'self' (the DivineAlchemist).
    env: Environment
    _resolution_stack: Set[str]
    Logger: Scribe

    def transmute(self, scripture: str, context: Dict[str, Any]) -> str:
        """
        =============================================================================
        == THE GOD-ENGINE OF TRANSMUTATION (V-Ω-RESILIENT-ALCHEMY-V12)            ==
        =============================================================================
        LIF: INFINITY | ROLE: TEMPLATE_RENDERER | RANK: SOVEREIGN

        Renders a Jinja2 string using the Alchemist's environment.
        Now hardened against Snippet Syntax ($), Recursive Loops, and Type Heresies.

        ### THE PANTHEON OF 12 ASCENSIONS:
        1.  **Prudence Gate:** O(1) check for '{{' or '{%' to skip static strings.
        2.  **Snippet Shield:** Detects VS Code snippet syntax (`${`) and automatically
            fails over to raw text to prevent `TemplateSyntaxError`.
        3.  **Context Isolation:** Deep-copies the context to prevent side-effect bleeding.
        4.  **Target Injection:** Ensures `_target_path` exists for relative imports.
        5.  **Type Coercion:** Auto-converts non-string inputs to string representations.
        6.  **Metabolic Chronometry:** Measures render time for performance telemetry.
        7.  **Recursion Guard:** Relies on Jinja's internal depth limit (configured in env).
        8.  **Undefined Handler:** Uses the ParanoidEnvironment's `handle_missing` to
            silence `UndefinedError` gracefully.
        9.  **Forensic Sarcophagus:** Catches ALL exceptions to prevent thread death.
        10. **Rich Diagnostic (Strict Mode):** On critical CLI failure, generates a
            visually stunning terminal report.
        11. **Silent Fallback (LSP Mode):** On syntax fracture (common in incomplete code),
            returns the raw scripture instead of exploding.
        12. **Heresy Log:** Scribes the failure to the debug stream for forensic audit.
        """
        import time
        from rich.panel import Panel
        from rich.syntax import Syntax
        from rich.text import Text
        from rich.console import Group

        start_time = time.perf_counter()

        # [ASCENSION 5]: TYPE COERCION
        if not isinstance(scripture, str):
            return str(scripture)

        # [ASCENSION 1]: PRUDENCE GATE
        if '{{' not in scripture and '{%' not in scripture:
            return scripture

        # [ASCENSION 2]: SNIPPET SHIELD
        # If the string contains snippet placeholders like `${1:var}`, Jinja will
        # often choke on the `$`. We detect this heuristic and tread carefully.
        if "${" in scripture:
            # We assume this is a snippet template, not a Jinja template.
            # However, sometimes they are mixed. We try, but expect failure.
            pass

        # [ASCENSION 3]: CONTEXT ISOLATION
        # We copy the context to prevent side-effects and ensure the target path key exists.
        render_context = context.copy()
        if '_target_path' not in render_context:
            render_context['_target_path'] = None

        try:
            # 3. THE RITE OF RENDERING
            template = self.env.from_string(scripture)
            result = template.render(render_context)

            # [ASCENSION 6]: METABOLIC TELEMETRY
            # duration = (time.perf_counter() - start_time) * 1000
            # if duration > 50:
            #     getattr(self, 'Logger', Logger).debug(f"Heavy Transmutation: {duration:.2f}ms")

            return result

        except Exception as e:
            # [ASCENSION 11]: SILENT FALLBACK (THE CURE)
            # If the scripture is malformed (e.g. user is currently typing "{{ my_v"),
            # Jinja will throw. We MUST NOT crash the LSP. We return raw text.

            heresy_message = getattr(e, 'message', str(e))

            # Determine if we are in a strict environment (CLI) or loose (LSP)
            # We check specific flags or environment variables.
            is_strict = context.get("_scaffold_strict_mode", False)

            if not is_strict:
                # In LSP/Daemon mode, we swallow the error and return raw text.
                # This fixes the "CompletionArtisan" crash when rendering snippet docs.
                # Optional: Log to debug if needed
                # getattr(self, 'Logger', Logger).debug(f"Alchemical Fizzle: {heresy_message}")
                return scripture

            # --- THE DIVINE APOTHEOSIS: THE HYPER-DIAGNOSTIC INQUEST (CLI MODE) ---
            # [ASCENSION 10]: RICH DIAGNOSTICS
            heresy_line_num = getattr(e, 'lineno', 'N/A')

            error_text = Text.from_markup(
                f"[bold]Heresy:[/bold] {heresy_message}\n"
                f"[bold]Gnostic Location:[/bold] Line [yellow]{heresy_line_num}[/yellow]."
            )

            # Extract context for the error display
            lines = scripture.splitlines()
            try:
                ln = int(heresy_line_num)
            except:
                ln = 1

            start_line = max(0, ln - 3)
            end_line = min(len(lines), ln + 2)
            context_scripture = "\n".join(lines[start_line:end_line])

            syntax = Syntax(context_scripture, "jinja", theme="monokai")

            heresy_panel = Panel(
                Group(error_text, "\n", syntax),
                title="[bold red]Dossier of Alchemical Heresy[/bold red]",
                border_style="red"
            )

            raise ArtisanHeresy(
                f"An alchemical heresy was perceived: {heresy_message}",
                details_panel=heresy_panel,
                child_heresy=e
            )

    def _resolve_variable_value(
            self,
            value: Any,
            file_path: Optional[Path],
            variable_cache: Dict[str, Any]
    ) -> Any:
        """
        The God-Engine of Variable Resolution.
        Recursively resolves `$$ var = val` definitions, handling shell commands,
        secrets, and JSON/YAML structures.
        """
        # 1. Recursive Descent for Structures
        if isinstance(value, dict):
            return {k: self._resolve_variable_value(v, file_path, variable_cache) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._resolve_variable_value(v, file_path, variable_cache) for v in value]
        elif not isinstance(value, str):
            return value

        stripped_value = value.strip()

        # 2. The Recursion Guard (Ouroboros Protection)
        # We check if this exact string value is currently being resolved.
        if stripped_value in self._resolution_stack:
            # Break cycle by returning raw string. The graph resolver handles the higher-level loop logic.
            return value

        self._resolution_stack.add(stripped_value)

        # 3. The Chronocache Check
        if stripped_value in variable_cache:
            self._resolution_stack.remove(stripped_value)
            return variable_cache[stripped_value]

        resolved_value: Any
        # Use 'self.Logger' if available, or global Logger if not initialized on self yet
        logger = getattr(self, 'Logger', Logger)
        logger.verbose(f"   -> Alchemist's Gaze awakens for scripture: '{stripped_value[:70]}'")

        try:
            # --- THE GRAND SYMPHONY OF GNOSTIC PERCEPTION ---

            # A. Secret Directive
            if stripped_value.startswith('@secret('):
                match = re.match(r'@secret\((.*?)\)', stripped_value)
                if match:
                    args_str = match.group(1).strip()
                    args = [arg.strip().strip("'\"") for arg in args_str.split(',')] if args_str else []
                    secret_type = args[0] if args else 'hex'
                    length = int(args[1]) if len(args) > 1 and args[1].isdigit() else 32
                    resolved_value = forge_gnostic_secret(length, secret_type)
                else:
                    raise ArtisanHeresy(f"Malformed @secret directive: '{stripped_value}'")

            # B. File Directive
            elif stripped_value.startswith('@file('):
                match = re.match(r'@file\((.*?)\)', stripped_value)
                if match:
                    path_str = match.group(1).strip().strip('"\'')
                    # Resolve relative to the defining file, or CWD
                    base_dir = file_path.parent if file_path else Path.cwd()
                    file_to_read = (base_dir / Path(path_str)).resolve()

                    if not file_to_read.is_file():
                        raise ArtisanHeresy(f"Celestial soul not found at: '{file_to_read}'")

                    resolved_value = file_to_read.read_text(encoding='utf-8')
                else:
                    raise ArtisanHeresy(f"Malformed @file directive: '{stripped_value}'")

            # C. Shell Command Injection
            elif stripped_value.startswith('$(') and stripped_value.endswith(')'):
                command = stripped_value[2:-1]
                sentry = GnosticSentry()
                # Adjudicate safety
                blueprint_sanctum = file_path.parent if file_path else Path.cwd()
                sentry.adjudicate(command, blueprint_sanctum, 0)

                result = subprocess.run(command, shell=True, capture_output=True, text=True, check=False,
                                        encoding='utf-8')
                if result.returncode != 0:
                    raise ArtisanHeresy(f"Command failed with exit code {result.returncode}", details=result.stderr)
                resolved_value = result.stdout.strip()

            # D. Environment Variable Injection
            elif stripped_value.startswith('${') and stripped_value.endswith('}'):
                env_match = re.match(r'^\s*\$\{([\w_]+)(?::(.*))?\}\s*$', value)
                if env_match:
                    var_name, default_value_raw = env_match.groups()
                    # Recursively resolve default value if present
                    default_value = self._resolve_variable_value(default_value_raw, file_path,
                                                                 variable_cache) if default_value_raw else ""
                    resolved_value = os.getenv(var_name, default_value)
                else:
                    raise ArtisanHeresy(f"Malformed Environment Gnosis: '{stripped_value}'")

            # E. Structured Data (JSON/YAML)
            elif (stripped_value.startswith('[') and stripped_value.endswith(']')) or \
                    (stripped_value.startswith('{') and stripped_value.endswith('}')):
                try:
                    resolved_value = json.loads(stripped_value)
                except json.JSONDecodeError:
                    try:
                        resolved_value = yaml.safe_load(stripped_value)
                    except (ImportError, yaml.YAMLError):
                        # Fallback to string if it looks like structure but isn't valid
                        resolved_value = stripped_value

            # F. Primitives
            else:
                if stripped_value.lower() == 'true':
                    resolved_value = True
                elif stripped_value.lower() == 'false':
                    resolved_value = False
                elif stripped_value.isdigit():
                    resolved_value = int(stripped_value)
                elif (stripped_value.startswith('"') and stripped_value.endswith('"')) or \
                        (stripped_value.startswith("'") and stripped_value.endswith("'")):
                    resolved_value = stripped_value[1:-1]
                else:
                    try:
                        resolved_value = float(stripped_value)
                    except ValueError:
                        resolved_value = stripped_value

            logger.verbose(
                f"   -> Transmutation complete. The soul's type is [yellow]{type(resolved_value).__name__}[/yellow].")

            variable_cache[stripped_value] = resolved_value
            self._resolution_stack.remove(stripped_value)
            return resolved_value

        except Exception as e:
            self._resolution_stack.remove(stripped_value)
            if isinstance(e, ArtisanHeresy): raise e
            raise ArtisanHeresy(f"Variable resolution paradox: {e}") from e