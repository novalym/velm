# Gnostic Codex: scaffold/core/cli/grimoire/_core_rites.py
# --------------------------------------------------------
# LIF: 100,000,000,000 (THE APOTHEOSIS OF WILL)
#
# HERESY ANNIHILATED: The Mute Vow
#
# The `create` rite's scripture in the Grimoire has been ascended. It is now
# taught to perceive the sacred `--raw` vow. This forges the final, unbreakable
# Gnostic link between the Architect's spoken plea and the engine's soul,
# allowing for absolute, explicit control over the nature of creation.

"""The foundational rites of creation and execution."""
from ..cli_utils import add_common_flags, add_simulation_flags, add_variable_flags
import argparse

# --- A NEW, SPECIALIZED SCRIBE FOR THE `create` RITE ---
def add_create_flags(parser: argparse.ArgumentParser):
    """Bestows the unique vows for the `create` artisan."""
    group = parser.add_argument_group("Creation Modifiers")

    # [ASCENSION I] The Path of Pure Will
    group.add_argument(
        '--raw',
        action='store_true',
        help='The Vow of Raw Creation. Bypasses all templates and uses content from --set content directly.'
    )
    group.add_argument(
        '--dir',
        action='store_true',
        help='Explicitly forge a directory, even if the path does not end with a slash.'
    )

    # [ASCENSION II] The Sentient Hand
    # Allows the architect to guide the creation with natural language immediately.
    # nargs='?' allows: --ai-edit (True) OR --ai-edit "Make it fast" (String)
    group.add_argument(
        '--ai-edit',
        nargs='?',
        const=True,
        help='Summon the Neural Cortex to transmute the template. Provide a prompt or leave empty for interactive mode.'
    )

    # [ASCENSION III] Governance & Silence
    group.add_argument(
        '--no-open',
        action='store_true',
        help='Suppress the auto-opening of the file in the editor.'
    )
    group.add_argument(
        '--no-tests',
        action='store_true',
        help='Suppress the generation of shadow twin (test) files.'
    )
    group.add_argument(
        '--no-assemble',
        action='store_true',
        help='The Vow of Isolation. Prevents the Gnostic Assembler from wiring this file into the project graph.'
    )

    # [ASCENSION IV] The Sources of Matter
    group.add_argument(
        '--needs',
        nargs='*',
        help='A list of system dependencies (e.g., git, docker) required for this creation to be pure.'
    )
    group.add_argument(
        '--teach',
        help='Teach the created file as a new template for the specified extension (e.g., `py`).'
    )
    group.add_argument(
        '--edit',
        '-e',
        action='store_true',
        help='Open the newly forged scriptures in your default editor.'
    )
    group.add_argument(
        '--from-url',
        help='Summon the scripture\'s soul from a celestial URL.'
    )
    group.add_argument(
        '--paste',
        '-c',
        action='store_true',
        help='Summon the scripture\'s soul from the system clipboard.'
    )
    group.add_argument(
        '--from-stdin',
        action='store_true',
        help='Summon the scripture\'s soul from the stdin stream.'
    )
    group.add_argument(
        '--of',
        nargs='+',
        help="The Rite of Semantic Forging (e.g., `component:Button`)."
    )
    group.add_argument(
        '--kit',
        help="Weave an entire Gnostic Kit from the Forge."
    )

RITES = {
    "genesis": {
        "module_path": "artisans.genesis",
        "artisan_class_name": "GenesisArtisan",
        "request_class_name": "GenesisRequest",
        "help": "The Rite of Genesis. Forges a new reality from a blueprint.",
        "description": "The `genesis` command is the Alpha. It takes a `.scaffold` blueprint and materializes it, running the full interactive dialogue if needed.",
        "flags": [
            add_common_flags,
            add_simulation_flags,
            add_variable_flags,
            # [ASCENSION]: The Vow of Silence for Maestro
            lambda p: p.add_argument('--no-edicts', action='store_true', help='Suppress execution of %% post-run edicts (Maestro Silence).')
        ],
        "args": [("blueprint_path", {"nargs": "?", "default": ".", "help": "Path to the .scaffold blueprint or an archetype name."})],
    },
    "init": {
            "module_path": "artisans.init",
            "artisan_class_name": "InitArtisan",
            "request_class_name": "InitRequest",
            "help": "The Rite of Inception. Begins the Sacred Dialogue to forge a new project.",
            "description": (
                "The `init` command is the luminous portal of the God-Engine. It initiates a "
                "Sacred Dialogue between the Architect and the Oracle, materializing a "
                "production-grade reality from the Gnostic Grimoire of Archetypes.\n\n"
                "LIF: INFINITY | ROLE: GENESIS_CONDUCTOR | RANK: OMEGA_SUPREME"
            ),
            # =========================================================================
            # == THE VOWS OF INCEPTION (FLAGS & DIRECTIVES)                         ==
            # =========================================================================
            "flags": [
                add_common_flags,    # Verbositiy, Force, Root, and Trace DNA
                add_variable_flags,  # The --set alchemical injections

                # [ASCENSION 1]: IDENTITY VOWS
                # Allows the Architect to proclaim the Name and Purpose upfront.
                lambda p: p.add_argument('--name', help="The sacred name of the new reality (project_name)."),
                lambda p: p.add_argument('--desc', dest='description', help="The semantic purpose of the project."),

                # [ASCENSION 2]: SUBSTRATE VOW (THE NEW POWER)
                # Allows defining the physical cloud target immediately.
                lambda p: p.add_argument('--provider', help="The infrastructure substrate (ovh, aws, azure, docker)."),

                # [ASCENSION 3]: THE PROFILE ORACLE
                lambda p: p.add_argument(
                    '--profile',
                    dest='profile_flag',
                    help="Summon a specific Archetype Profile (e.g., 'fastapi-service')."
                ),

                # [ASCENSION 4]: THE CENSUS RADIATOR
                lambda p: p.add_argument(
                    '--list',
                    action='store_true',
                    dest='list_profiles',
                    help="Proclaim the census of all manifest and user-forged profiles."
                ),

                # [ASCENSION 5]: THE SPEED VOWS
                lambda p: p.add_argument(
                    '--quick',
                    action='store_true',
                    help="The Vow of Haste. Skips the Sacred Dialogue and materializes using intelligent defaults."
                ),
                lambda p: p.add_argument(
                    '--manual',
                    action='store_true',
                    help="The Scribe's Altar. Forges a minimal, blank blueprint for manual inscription."
                ),

                # [ASCENSION 6]: THE ADOPTION RITE
                lambda p: p.add_argument(
                    '--distill',
                    action='store_true',
                    help="Gaze upon the current reality and adopt it into a Gnostic Blueprint before initializing."
                ),

                # [ASCENSION 7]: THE SEMANTIC ALIAS
                lambda p: p.add_argument(
                    '--type',
                    dest='type_alias',
                    help="A semantic alias for quick-selection (e.g., 'node', 'python')."
                )
            ],

            # =========================================================================
            # == THE POSITIONAL LOCUS (ARGUMENTS)                                    ==
            # =========================================================================
            "args": [
                # The Profile Name (Optional positional)
                ("profile", {
                    "nargs": "?",
                    "help": "The sacred name of the Archetype to materialize."
                })
            ],
    },
    "run": {
        "module_path": "artisans.run.conductor",
        "artisan_class_name": "RunArtisan",
        "request_class_name": "RunRequest",
        "help": "The Universal Conductor. Executes any scripture (.py, .js, .symphony, .scaffold).",
        "flags": [add_common_flags, add_variable_flags],
        "args": [
            ("target", {"help": "The scripture to run (e.g., 'main.py', 'deploy.symphony')."}),
            ("extra_args", {"nargs": argparse.REMAINDER, "help": "Arguments to pass to the script."}),
        ],
    },
     "create": {
        "module_path": "artisans.create",
        "artisan_class_name": "CreateArtisan",
        "request_class_name": "CreateRequest",
        "help": "The Rite of Ad-Hoc Creation. Forges a file from a template or the void.",
        "description": "Materializes new files. Can summon templates, use clipboard content, or download from URLs. Supports AI transmutation via --ai-edit.",
        "flags": [
            add_common_flags,
            add_simulation_flags,  # [ASCENSION]: Enables --preview / --dry-run
            add_variable_flags,
            # [ASCENSION]: Inline content injection
            lambda p: p.add_argument('--content', help='Bestow a soul (content) upon the new scripture directly from the command line.'),
            add_create_flags
        ],
        "args": [("paths", {"nargs": "+", "help": "Path(s) to the file(s) or directory to create."})],
    },
    "teach": {
        "module_path": "artisans.tutorial.artisan",
        "artisan_class_name": "TutorialArtisan",
        "request_class_name": "TeachRequest",
        "help": "The Tutorial Forge. Gamified onboarding and interactive learning.",
        "flags": [add_common_flags],
        "subparsers": {
            "generate": {
                "help": "Analyze codebase and forge a new curriculum.",
                "args": [("--topic", {"help": "Focus area."}), ("--difficulty", {"choices": ["novice", "adept"], "default": "novice"})]
            },
            "start": {"help": "Begin the next quest in the active curriculum."},
            "verify": {"help": "Check if the current quest objective is met."}
        }
    },
    "resurrect": {
        "module_path": "artisans.lazarus.artisan",
        "artisan_class_name": "LazarusArtisan",
        "request_class_name": "LazarusRequest",
        "help": "The Lazarus Protocol. Automatically diagnose and fix crashes.",
        "flags": [add_common_flags],
        "args": [
            ("command", {"help": "The command that triggers the crash (e.g. 'pytest')."}),
            ("--auto-apply", {"action": "store_true", "help": "Apply the fix without asking."})
        ]
    },
    "fortify": {
        "module_path": "artisans.fortress.artisan",
        "artisan_class_name": "FortressArtisan",
        "request_class_name": "FortressRequest",
        "help": "The Fortress. Scan for vulnerabilities and harden code.",
        "flags": [add_common_flags],
        "args": [("--fix", {"action": "store_true", "help": "Attempt auto-patching."})]
    },
    "port": {
        "module_path": "artisans.babel.artisan",
        "artisan_class_name": "BabelArtisan",
        "request_class_name": "BabelRequest",
        "help": "The Babel Engine. Port code to a new language.",
        "flags": [add_common_flags],
        "args": [
            ("source", {"help": "File to port."}),
            ("--to", {"dest": "target_lang", "choices": ["rust", "go", "python", "typescript"], "required": True, "help": "Target language."}),
            ("--fuse", {"dest": "fusion_bind", "action": "store_true", "help": "Auto-compile and bind using Fusion."})
        ]
    },
    "observatory": {
        "module_path": "artisans.observatory",
        "artisan_class_name": "ObservatoryArtisan",
        "request_class_name": "ObservatoryRequest",
        "help": "The Gnostic Observatory. Manage the multi-project cosmos.",
        "flags": [
            add_common_flags,
            lambda p: p.add_argument('--json', dest='json_mode', action='store_true', help='Output in JSON format.')
        ],
        "subparsers": {
            "list": {"help": "List all registered projects."},
            "add": {
                "help": "Register a project.",
                "args": [("target", {"help": "Path to the project root.", "nargs": "?"})]
            },
            "switch": {
                "help": "Switch active context.",
                "args": [("target", {"help": "Project Name or ID."})]
            },
            "discover": {
                "help": "Scan for unmanaged projects.",
                "args": [("target", {"help": "Root directory to scan.", "nargs": "?"})]
            },
            "prune": {"help": "Remove missing projects from registry."},
            "active": {"help": "Show current active project."},
            "open": {"help": "Open active project in editor."}
        }
    },

    "simulate": {
        "module_path": "artisans.simulacrum.artisan",
        "artisan_class_name": "SimulacrumArtisan",
        "request_class_name": "SimulateRequest",
        "help": "Executes code in a disposable, project-aware Void Sanctum.",
        "description": "The Simulacrum allows for ephemeral execution of code snippets within the context of the project. It bridges dependencies (node_modules, venv) but isolates side-effects to a temporary directory.",
        "flags": [add_common_flags],
        "args": [
            ("target_file", {"nargs": "?", "help": "Path to a local file to read content from."}),
            ("--content", {"help": "Inline code content to simulate (overrides target_file)."}),
            ("--lang", {"dest": "language", "help": "Force specific language runtime (e.g. 'python', 'ts')."}),
            ("--timeout", {"type": int, "default": 60, "help": "Maximum duration (seconds) before the void collapses."}),
            ("--env", {"action": "append", "help": "Inject env vars (KEY=VALUE)."})
        ]
    },
    "lsp": {
            "module_path": "core.lsp.scaffold_server",
            "artisan_class_name": "GnosticLSPRequest", # Direct class usage
            "request_class_name": "BaseRequest", # Dummy request, we don't use Dispatcher
            "help": "Starts the Gnostic Language Server (Stdio Mode).",
            "flags": [],
            "handler": lambda engine, args: _run_lsp_mode()
    },
}