# Path: scaffold/core/cli/cli_utils.py
# ------------------------------------
# LIF: 10,000,000,000 (THE ARSENAL OF ARGUMENTS)
# ROLE: Provides reusable argument groups for the CLI Grimoire.
#
# WHY SO MANY FLAGS?
# ------------------
# 1. EXPLICIT INTERFACE DEFINITION:
#    Each Artisan possesses unique faculties. We must explicitly define the
#    inputs (flags) required to summon these faculties. Relying on implicit
#    kwargs causes runtime paradoxes.
#
# 2. TYPE SAFETY AT THE EDGE:
#    By defining `type=int` or `choices=[...]` here, we validate input
#    before the heavy Engine executes, failing fast (sub-50ms)
#    with helpful messages if the user provides invalid input.
#
# 3. MODULAR COMPOSABILITY:
#    Rites are often composed of multiple skillsets. For example, the 'Distill'
#    rite uses 'Simulation' flags (dry-run), 'Variable' flags (--set), AND
#    'Analysis' flags (--depth). By defining these as mixin functions, we can
#    mix-and-match capabilities for any command without rewriting code.
#
# 4. CONFLICT RESOLUTION:
#    Since multiple mixins might try to add the same common flag (like --focus),
#    we implement a Universal Conflict Guard (`_safe_add`) to ignore duplicates
#    gracefully.
# =================================================================================

import argparse
import os


# =================================================================================
# == THE GNOSTIC HELPER (CONFLICT RESOLUTION)                                    ==
# =================================================================================

def _safe_add(group, *args, **kwargs):
    """
    [THE CONFLICT GUARD]
    Attempts to add an argument to a parser group.

    If the argument is already claimed by a sibling group or the parent parser,
    argparse raises an ArgumentError. We catch this silence it, allowing the
    first definition of the flag to serve as the Source of Truth.

    This enables additive mixins without crash risk.
    """
    try:
        group.add_argument(*args, **kwargs)
    except argparse.ArgumentError:
        # The flag already exists in this scope.
        # We bow to the existing definition and proceed.
        pass


# =================================================================================
# == I. THE UNIVERSAL VOWS (GLOBAL FLAGS)                                        ==
# =================================================================================

def add_common_flags(parser: argparse.ArgumentParser):
    """
    Bestows universal flags for simulation, force, and verbosity.
    These are the Laws of Physics for every CLI command.
    """
    group = parser.add_argument_group("Universal Vows (Global Flags)")

    _safe_add(group, '-v', '--verbose', action='store_true',
              help='Enable luminous logging for a hyper-diagnostic Gaze.')

    _safe_add(group, '--force', '-f', action='store_true',
              help='The Rite of Absolute Will. Bypasses interactive safeguards.')

    _safe_add(group, '--non-interactive', '-y', action='store_true',
              help='The Vow of Silence. Suppresses all interactive prompts.')

    _safe_add(group, '--root',
              help='Override the project root sanctum for this rite.')

    _safe_add(group, '--debug', action='store_true',
              help="Wait for debugger attachment.")

    _safe_add(group, '--silent', action='store_true',
              help="Suppress all standard output.")


def add_simulation_flags(parser: argparse.ArgumentParser):
    """Bestows the flags for quantum simulation and Gnostic inspection."""
    group = parser.add_argument_group("Quantum Simulation & Inspection")

    # Mutually exclusive groups are tricky with _safe_add, so we handle carefully
    try:
        exclusive_group = group.add_mutually_exclusive_group()
        _safe_add(exclusive_group, '--dry-run', '-d', action='store_true',
                  help='Engage Quantum Simulation Mode (no writes).')
        _safe_add(exclusive_group, '--preview', '-p', action='store_true',
                  help='Render a visual dry run of the intended reality.')
        _safe_add(exclusive_group, '--audit', '-a', action='store_true',
                  help='Proclaim a machine-readable JSON Dossier.')
    except argparse.ArgumentError:
        pass


def add_variable_flags(parser: argparse.ArgumentParser):
    """Bestows the sacred `--set` flag for alchemical injection."""
    group = parser.add_argument_group("Alchemical Injection")
    _safe_add(group, '--set', nargs='*', default=[],
              help="Inject Gnostic variables (e.g., --set name=nova-api author='The Guild').")


# =================================================================================
# == II. THE SPATIAL SURVEYOR (TREE FLAGS)                                       ==
# =================================================================================

def add_tree_flags(parser: argparse.ArgumentParser):
    """
    [FACULTY: THE OMNISCIENT MAPPER]
    Configures the `tree` rite with high-fidelity visualization controls.
    """
    group = parser.add_argument_group("The Spatial Gaze (Tree Visualization)")

    _safe_add(group, '--depth', '-d', type=int, default=-1,
              help="Limit the depth of the Gnostic gaze. (-1 for infinite)")

    _safe_add(group, '--dirs-only', action='store_true',
              help="Perceive only the structure of Sanctums (directories).")

    _safe_add(group, '--all', '-a', action='store_true',
              help="The All-Seeing Eye. Reveals hidden sanctums (.git, .env).")

    _safe_add(group, '--full-path', action='store_true',
              help="Display the absolute coordinate of every node.")

    _safe_add(group, '--size', '-s', action='store_true',
              help="Measure the mass (bytes) of every node.")

    _safe_add(group, '--permissions', action='store_true',
              help="Reveal the access rites (chmod) of every node.")

    _safe_add(group, '--sort', choices=['name', 'size', 'modified', 'extension'], default='name',
              help="The Law of Order.")

    _safe_add(group, '--reverse', '-r', action='store_true',
              help="Invert the Law of Order.")

    _safe_add(group, '--format', choices=['text', 'json', 'svg', 'html', 'mermaid', 'csv'], default='text',
              help="The medium of the revelation.")

    _safe_add(group, '--output', '-o',
              help="Inscribe the visualization into a physical scroll (file).")

    _safe_add(group, '--serve', action='store_true',
              help="Spin up an ephemeral Holo-Server.")

    _safe_add(group, '--no-color', action='store_true',
              help="Disable chromatic aberration.")

    _safe_add(group, '--editor-links', action='store_true',
              help="Forge clickable hyperlinks (vscode://).")


# =================================================================================
# == III. THE GNOSTIC SPECIALISTS (CONFLICT HEALED)                              ==
# =================================================================================

def add_graph_flags(parser: argparse.ArgumentParser):
    """
    Flags for the GraphArtisan (Topology).
    [HEALED]: We removed flags (--format, --focus, --orphans) that are already
    explicitly defined in the 'args' list of the Graph rite definition to prevent
    'ArgumentError: conflicting option string'.
    """
    group = parser.add_argument_group("Topological Analysis")

    # We only add flags that are NOT covered by the main rite args.
    _safe_add(group, '--direction', choices=['TD', 'LR'], default='LR',
              help="Flow of gravity.")


def add_holographic_flags(parser: argparse.ArgumentParser):
    """Flags for the HolographicBlueprintArtisan."""
    group = parser.add_argument_group("Holographic Projection")
    _safe_add(group, '--full-fidelity', action='store_true',
              help='Capture full file content instead of just structure.')
    _safe_add(group, '--checksums', action='store_true',
              help='Include SHA256 fingerprints.')


def add_verify_flags(parser: argparse.ArgumentParser):
    """Flags for the VerifyArtisan."""
    group = parser.add_argument_group("Reality Verification")
    _safe_add(group, '--fast', action='store_true',
              help='Verify using size/mtime (faster).')
    _safe_add(group, '--strict', action='store_true',
              help='Report untracked files as anomalies.')
    _safe_add(group, '--fix', action='store_true',
              help='Attempt to heal reality to match the chronicle.')


def add_adopt_flags(parser: argparse.ArgumentParser):
    """Flags for the AdoptArtisan."""
    group = parser.add_argument_group("Adoption Rites")
    _safe_add(group, '--output-file', default='scaffold.scaffold',
              help='The blueprint file to create/merge.')
    _safe_add(group, '--full', action='store_true',
              help='Perform full content hashing (slower).')

    _safe_add(group, '--ignore', nargs='*', help='Glob patterns to ignore.')
    _safe_add(group, '--include', nargs='*', help='Glob patterns to include.')

    # [THE FIX]: Safe add ensures --focus doesn't crash if shared with Graph flags
    _safe_add(group, '--focus', nargs='*', help='Keywords to guide logic induction.')


def add_analyze_flags(parser: argparse.ArgumentParser):
    """Flags for the AnalyzeArtisan."""
    group = parser.add_argument_group("Forensic Analysis")
    _safe_add(group, '--batch', action='store_true',
              help='Analyze all files in directory.')
    _safe_add(group, '--auto-redeem', action='store_true',
              help='Automatically attempt to heal heresies.')
    _safe_add(group, '--depth', type=int, default=1,
              help='Depth of the scan.')
    _safe_add(group, '--json', action='store_true',
              help='Output structured JSON.')


def add_inspect_flags(parser: argparse.ArgumentParser):
    """Flags for the InspectArtisan."""
    group = parser.add_argument_group("Blueprint Inspection")
    _safe_add(group, '--format', choices=['json', 'mermaid', 'text'], default='text',
              help='Output format.')
    _safe_add(group, '--json-output', action='store_true', help='Alias for --format=json.')
    _safe_add(group, '--lfg', action='store_true', help="Render Logic Flow Graph.")


def add_distill_flags(parser: argparse.ArgumentParser):
    """
    Legacy/Placeholder for Distill flags.
    The true logic is in `add_custom_distill_flags` within `_perception_rites.py`.
    We keep this for compatibility but it adds nothing, safe from conflicts.
    """
    pass

