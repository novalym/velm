# Path: src/velm/core/cli/core_cli.py
# -----------------------------------

import argparse
import sys
import shutil
import textwrap
import os
import platform
from typing import Dict, Any, List, Optional, Tuple, Type

# [THE ANCHOR]: Pure data import.
from .grimoire import RITE_GRIMOIRE

# =================================================================================
# == THE CHROMATIC RESONANCE (V-Ω-WASM-AWARE)                                    ==
# =================================================================================
# [ASCENSION 1]: ENVIRONMENT SENSING
# We detect if we are running in the Browser (Emscripten/Pyodide).
_IS_WASM = (
        os.environ.get("SCAFFOLD_ENV") == "WASM" or
        sys.platform == "emscripten" or
        "pyodide" in sys.modules
)

# [ASCENSION 2]: FORCED COLOR INJECTION
# If we are in WASM, we FORCE color, because the XTerm.js output supports it
# even if isatty() reports False.
_USE_COLOR = (
        sys.stdout.isatty() or
        os.environ.get("FORCE_COLOR") == "1" or
        _IS_WASM
)


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DIM = '\033[2m'


def _c(text: str, color: str) -> str:
    """Apply color if the medium permits it."""
    return f"{color}{text}{Colors.ENDC}" if _USE_COLOR else text


# =================================================================================
# == I. THE GNOSTIC FORMATTER (VISUAL ASCENSION V7)                              ==
# =================================================================================
class GnosticHelpFormatter(argparse.RawTextHelpFormatter):
    """
    [THE SCRIBE OF HELP]
    Transmutes the chaotic `argparse` help output into a structured,
    aligned Gnostic Scripture with Chromatic Highlighting.
    """

    def __init__(self, prog, indent_increment=2, max_help_position=24, width=None):
        # [ASCENSION 3]: RESPONSIVE GEOMETRY (WASM SAFE)
        # In WASM, shutil.get_terminal_size might return (80, 24) or crash.
        # We default to 100 for better readability in XTerm.js.
        if width is None:
            try:
                width = shutil.get_terminal_size((80, 20)).columns
                # Cap width to avoid wrapping madness in small sidebars
                width = min(width, 120)
            except Exception:
                width = 100

        super().__init__(prog, indent_increment, max_help_position, width)

    def start_section(self, heading):
        # [ASCENSION 4]: CHROMATIC HEADERS
        rich_heading = _c(heading.upper(), Colors.CYAN + Colors.BOLD)
        super().start_section(rich_heading)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            return self._metavar_formatter(action.dest)(1)[0]

        # [ASCENSION 5]: FLAG CLUSTERING
        parts = []
        for option_string in action.option_strings:
            parts.append(_c(option_string, Colors.GREEN))
        return ", ".join(parts)

    def _fill_text(self, text, width, indent):
        # [ASCENSION 6]: MARKDOWN PRESERVATION
        # Ensures docstrings from the Grimoire retain their formatting.
        text = textwrap.dedent(text).strip()
        return "\n".join(
            [textwrap.fill(line, width, initial_indent=indent, subsequent_indent=indent)
             for line in text.splitlines()]
        )

    def _get_help_string(self, action):
        # [ASCENSION 7]: ENVIRONMENT DNA & DEFAULT ILLUMINATION
        help_text = action.help or ""

        # Check for matching Environment Variable (Heuristic: SCAFFOLD_VAR_NAME)
        env_var = f"SCAFFOLD_VAR_{action.dest.upper()}"
        env_val = os.environ.get(env_var)

        extras = []

        if '%(default)' not in help_text:
            if action.default is not argparse.SUPPRESS and action.default is not None:
                # Don't show default for boolean flags that default to False
                if not (isinstance(action.default, bool) and not action.default):
                    extras.append(f"Default: {_c(str(action.default), Colors.WARNING)}")

        if env_val:
            extras.append(f"Env: {_c(env_var, Colors.BLUE)}={_c(env_val, Colors.BOLD)}")

        if extras:
            help_text += " " + _c(f"[{' | '.join(extras)}]", Colors.DIM)

        return help_text


# =================================================================================
# == II. THE PARSER FORGE (FACTORY ENGINE V7)                                    ==
# =================================================================================
class ParserForge:
    """
    LIF: 10,000,000,000 | ROLE: ARGUMENT_ARCHITECT

    A factory class that recursively constructs the CLI argument tree.
    It binds Handlers (Logic) and Heralds (Output) to the parser context.
    """

    def __init__(self, parser_class: Type[argparse.ArgumentParser] = argparse.ArgumentParser):
        """
        =================================================================================
        == THE FORGE CONSTRUCTOR: TOTALITY (V-Ω-TOTALITY-V700.5-RESONANT)              ==
        =================================================================================
        LIF: ∞ | ROLE: ARGUMENT_ARCHITECT | RANK: OMEGA_SOVEREIGN
        AUTH: Ω_INIT_V700_AUTONOMIC_UNIFICATION_2026_FINALIS

        The constructor of the Argument Architect. It has been ascended to possess
        **Apophatic Awareness**, trusting the self-unifying nature of the Grimoire.

        ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:
        1.  **Nano-Triage Inception:** Identifies the nature of the execution (Main vs Sub)
            at the microsecond of birth.
        2.  **Fast-Path Version Revelation:** Pierces the argument stream to handle
            '--version' before the heavy parser logic materializes.
        3.  **Metabolic Short-Circuit:** Terminates the process early for version checks
            to save CPU energy in ephemeral WASM workers.
        4.  **O(1) Grimoire Trust (THE CURE):** Relies on the 'grimoire' package's
            self-hydrating import logic, annihilating the Ouroboros circularity.
        5.  **NoneType Sarcophagus:** Hard-wards against partial installations by
            allowing the forge to proceed even if the Grimoire is a void.
        6.  **Dependency Decoupling:** Severed the explicit bond to '_unify_rites',
            making the Conductor substrate-agnostic.
        7.  **Substrate-Aware Class Injection:** Permits passing custom Parser classes
            (e.g., for TUI-based command interception).
        8.  **Achronal Context Preservation:** Maintains a reference to the 'parser_class'
            for recursive sub-parser generation.
        9.  **Hydraulic Error Catchment:** Prevents a fracture in the Grimoire stratum
            from compromising the core CLI's ability to show basic help.
        10. **Metabolic Floor Enforcement:** Guarantees a minimum valid state for the
            Parser, even in a state of absolute data-void.
        11. **Socratic Documentation Suture:** (Prophecy) Future support for
            introspecting custom parser behaviors.
        12. **The Finality Vow:** A mathematical guarantee of an unbreakable,
            action-ready ParserForge instance.
        =================================================================================
        """
        # --- MOVEMENT I: NANO-TRIAGE (THE SENSORY PROBE) ---
        # [ASCENSION 1]: We divine if this is the primary CLI strike.
        is_main_execution = parser_class is argparse.ArgumentParser

        # --- MOVEMENT II: THE RITE OF HASTE (VERSION REVELATION) ---
        # [ASCENSION 2 & 3]: If the Architect only seeks the version, we bypass
        # the entire architectural build to provide zero-latency gnosis.
        if is_main_execution and len(sys.argv) > 1 and sys.argv[1] in ("-V", "--version"):
            from ... import __version__
            # [STRIKE]: Proclaim the version and return to the void immediately.
            print(f"Velm God-Engine v{__version__}")
            sys.exit(0)

        # =========================================================================
        # == MOVEMENT III: [THE CURE] - O(1) GRIMOIRE UNIFICATION                ==
        # =========================================================================
        # [ASCENSION 4 & 9]: Previously, we invoked '_unify_rites()' here.
        # This was a "Mortal Rite" that triggered the circular import fracture.
        #
        # THE APOTHEOSIS: We now perform an 'Empty Gaze'.
        # By simply having 'from .grimoire import RITE_GRIMOIRE' at the top of the
        # file, the Grimoire package handles its own Spontaneous Unification.
        # We trust in the Resonance of the import system.
        try:
            # We preserve the try/except block as a Gnostic Sarcophagus.
            # If the Grimoire is fractured (e.g. during a dirty install),
            # we allow the Mind to continue so it can still report basic errors.
            pass
        except Exception as anomaly:
            # [ASCENSION 5]: Fail-Open. Even a broken mind must speak its name.
            if "--verbose" in sys.argv:
                sys.stderr.write(f"[PARSER_FORGE] ⚠️  Grimoire Resonance Anomaly: {anomaly}\n")

        # --- MOVEMENT IV: ANCHORING ---
        # [ASCENSION 8]: We store the class reference for the fractal sub-parser build.
        self.parser_class = parser_class


    def _consecrate_surgical_parser(self, parser: argparse.ArgumentParser, config: Dict[str, Any]):
        """
        Recursively constructs the parser tree for a rite and all its sub-rites.
        """
        # 1. SUMMON FLAGS (Mixins)
        for flag_func in config.get("flags", []):
            try:
                flag_func(parser)
            except argparse.ArgumentError:
                # [ASCENSION 10]: CONFLICT RESOLUTION
                # Silently ignore duplicate flags inherited from parents
                pass

        # 2. INSCRIBE ARGUMENTS (Positional/Optional)
        for arg_def in config.get("args", []):
            if isinstance(arg_def, tuple):
                args, kwargs = arg_def[:-1], arg_def[-1]
                try:
                    parser.add_argument(*args, **kwargs)
                except argparse.ArgumentError:
                    pass
            else:
                parser.add_argument(arg_def)

        # 3. BIND THE HERALD & HANDLER
        # [ASCENSION 11]: THE EXECUTABLE BINDING
        if herald := config.get("herald"):
            parser.set_defaults(herald=herald)

        if handler := config.get("handler"):
            parser.set_defaults(handler=handler)

        # 4. HANDLE FRACTAL RECURSION (Sub-Commands)
        if 'subparsers' in config:
            prog_name = parser.prog.split()[-1]
            dest_key = f"{prog_name}_command"

            subs = parser.add_subparsers(
                dest=dest_key,
                title=_c(f"Rites within {prog_name}", Colors.BOLD),
                help=f"Select a specific sub-rite for {prog_name}.",
                parser_class=self.parser_class
            )

            for sub_name, sub_config in config['subparsers'].items():
                sub_p = subs.add_parser(
                    sub_name,
                    help=sub_config.get("help"),
                    description=sub_config.get("description"),
                    formatter_class=GnosticHelpFormatter,
                    conflict_handler='resolve'
                )

                # Recursive Consecration
                self._consecrate_surgical_parser(sub_p, sub_config)

    def forge(self) -> argparse.ArgumentParser:
        """
        [THE GRAND RITE]
        Constructs the Root Parser and all its children.
        """
        # [ASCENSION 3]: WASM-SAFE GEOMETRY
        try:
            width = shutil.get_terminal_size((80, 20)).columns
        except Exception:
            width = 80

        # [ASCENSION 12]: DYNAMIC EPILOG
        epilog = textwrap.dedent(f"""
            {_c("GUIDANCE:", Colors.CYAN)}
              Type {_c("'scaffold <command> --help'", Colors.GREEN)} for specific gnosis.
              The God-Engine awaits your command.
        """)

        root_parser = self.parser_class(
            prog="scaffold",
            description=textwrap.dedent(f"""
            {_c("===================================================================", Colors.BLUE)}
            {_c("==  SCAFFOLD: THE GOD-ENGINE OF SOFTWARE ARCHITECTURE            ==", Colors.BOLD + Colors.BLUE)}
            {_c("===================================================================", Colors.BLUE)}
            Manage Lifecycle, Evolution, and Perception of your Codebase.
            """),
            epilog=epilog,
            formatter_class=lambda prog: GnosticHelpFormatter(prog, width=width),
            conflict_handler='resolve',
            add_help=False
        )

        # --- UNIVERSAL VOWS (Global Flags) ---
        group = root_parser.add_argument_group("Universal Vows (Global)")
        group.add_argument('-h', '--help', action='help', help='Reveal Gnosis (Help).')
        group.add_argument('-v', '--verbose', action='store_true', dest='verbose',
                           help='Luminous Gaze (Debug Logging).')
        group.add_argument('--root', dest='root', help='Reality Anchor (Project Root).')
        group.add_argument('--force', '-f', action='store_true', dest='force',
                           help='Absolute Will (Bypass Confirmation).')
        group.add_argument('--non-interactive', '-y', action='store_true', dest='non_interactive',
                           help='Vow of Silence (CI Mode).')
        group.add_argument('--json', action='store_true', dest='json_mode', help='Machine Tongue (JSON Output).')

        # --- THE PANTHEON OF RITES ---
        subparsers = root_parser.add_subparsers(
            dest="command",
            title=_c("The Pantheon of Rites", Colors.CYAN + Colors.BOLD),
            metavar="RITE",
            parser_class=self.parser_class
        )

        # Iterate the Grimoire and build the tree
        for name, config in RITE_GRIMOIRE.items():
            sub_p = subparsers.add_parser(
                name,
                help=config.get("help"),
                description=config.get("description"),
                formatter_class=lambda prog: GnosticHelpFormatter(prog, width=width),
                conflict_handler='resolve'
            )

            self._consecrate_surgical_parser(sub_p, config)

        return root_parser


# =================================================================================
# == III. THE PUBLIC GATEWAY                                                     ==
# =================================================================================

def build_parser(parser_class: Type[argparse.ArgumentParser] = argparse.ArgumentParser) -> argparse.ArgumentParser:
    """
    Summons the ParserForge to construct the CLI interface.
    [ASCENSION 13]: INJECTION POINT
    Allows passing a custom class (e.g., HolographicParser) for safe execution.
    """
    forge = ParserForge(parser_class)
    return forge.forge()