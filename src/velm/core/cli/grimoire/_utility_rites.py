# scaffold/core/cli/grimoire/_utility_rites.py
"""Rites of the Instrumentarium: Tooling, settings, and alchemical utilities."""
from ..cli_utils import add_common_flags, add_variable_flags
import argparse

RITES = {
    "settings": {
        "module_path": "artisans.settings",
        "artisan_class_name": "SettingsArtisan",
        "request_class_name": "SettingsRequest",
        "help": "The Altar of Configuration. Tune the soul of the Scaffold engine.",
        "flags": [add_common_flags],
    },
    "runtimes": {
        "module_path": "artisans.runtimes",
        "artisan_class_name": "RuntimesArtisan",
        "request_class_name": "RuntimesRequest",
        "help": "The High Priest of Runtimes. Manage hermetic and system execution.",
        "flags": [add_common_flags],
        "args": [("command", {"help": "The runtime management rite (setup, list, summon)."})],
    },
    "templates": {
        "module_path": "artisans.templates",
        "artisan_class_name": "TemplateManagerCLI",
        "request_class_name": "TemplateRequest",
        "help": "The Artisan of the Forge. Manage your private boilerplate library.",
        "flags": [add_common_flags],
        "args": [("template_command", {"help": "The forge management rite (list, add, edit, pull)."})],
    },
    "alias": {
        "module_path": "artisans.alias.artisan",
        "artisan_class_name": "AliasArtisan",
        "request_class_name": "AliasRequest",
        "help": "The Shortcut Forge. Manage Gnostic Macros.",
        "flags": [add_common_flags],
        "args": [("alias_command", {"choices": ["add", "remove", "list"], "help": "The macro rite."})],
    },
    "beautify": {
        "module_path": "artisans.beautify",
        "artisan_class_name": "BeautifyArtisan",
        "request_class_name": "BeautifyRequest",
        "help": "The Grand Purifier. Reinscribes blueprints in canonical form.",
        "flags": [add_common_flags],
    },
    "lint-blueprint": {
        "module_path": "artisans.lint_blueprint.artisan",
        "artisan_class_name": "BlueprintLinterArtisan",
        "request_class_name": "LintBlueprintRequest",
        "help": "The Architect's Level. Adjudicates .scaffold validity.",
        "flags": [
            add_common_flags,
            lambda p: p.add_argument('--strict', action='store_true', help='Enforce strict Archetype metadata rules.')
        ],
        "args": [("target", {"help": "Path to the .scaffold file to judge."})]
    },
    "lint": {
        "module_path": "artisans.lint",
        "artisan_class_name": "LintArtisan",
        "request_class_name": "LintRequest",
        "help": "The Gnostic Mentor. Adjudicates architectural and code purity.",
        "flags": [add_common_flags],
    },
    "tool": {
        "module_path": "artisans.tool.tool_cli",
        "artisan_class_name": "ToolArtisan",
        "request_class_name": "ToolRequest",
        "help": "Access the Gnostic Instrumentarium of developer utilities.",
        "flags": [add_common_flags],
        "subparsers": {
            "ascii": {"help": "Transmutes an image into colored ASCII scripture."},
            "banner": {"help": "Forges a beautiful ASCII banner for your project."},
            "hash": {"help": "The Cryptographic Sealer. Forges integrity hashes."},
            "keyring": {"help": "Manages the Gnostic Keyring of trusted authors."},
            "pack": {"help": "Encapsulates archetypes for distribution."},
            "sbom": {"help": "Chronicles the project's lineage in SPDX format."},
            "secrets": {"help": "The Keymaster. Manages secret rotation."},
            # ★★★ THE NEW SCRIPTURE ★★★
            "read-soul": {
                "module_path": "artisans.read_soul",
                "artisan_class_name": "ReadSoulArtisan",
                "request_class_name": "ReadSoulRequest",
                "help": "A sacred rite for AIs. Reads the raw content of a scripture to stdout.",
                "flags": [add_common_flags],
                "args": [("path_to_scripture", {"help": "The path to the scripture whose soul is to be read."})]
            },
        }
    },
    "self-test": {
        "module_path": "artisans.self_test",
        "artisan_class_name": "SelfTestArtisan",
        "request_class_name": "SelfTestRequest",
        "help": "The Mirror of Introspection. Verifies the Engine's own physics.",
        "flags": [add_common_flags],
    },
    "qr": {
        "module_path": "artisans.qr",
        "artisan_class_name": "QRArtisan",
        "request_class_name": "QRRequest",
        "help": "The Visual Bridge. Generates a QR code for mobile LAN linking.",
        "flags": [add_common_flags],
    },
    "snippet": {
        "module_path": "artisans.snippet.artisan",
        "artisan_class_name": "SnippetArtisan",
        "request_class_name": "SnippetRequest",
        "help": "The Fragment Keeper. Manages a local library of code snippets.",
        "flags": [add_common_flags],
    },
    "fuse": {
        "module_path": "artisans.fusion.artisan",
        "artisan_class_name": "FusionArtisan",
        "request_class_name": "FusionRequest",
        "help": "The Fusion Core. Polyglot compilation and binding (Rust/Go -> Python/Node).",
        "flags": [add_common_flags],
        "subparsers": {
            "compile": {
                "help": "Compile a system language file into a native binary or library.",
                "args": [
                    ("source", {"help": "Source file (e.g. src/math.rs)."}),
                    ("--lang", {"dest": "target_lang", "choices": ["python", "node"], "default": "python", "help": "Target host language for bindings."}),
                    ("--out", {"dest": "output_dir", "help": "Directory to place the compiled artifact."})
                ]
            },
            "bind": {
                "help": "Generate bindings and compile (alias for compile).",
                "args": [
                    ("source", {"help": "Source file."}),
                    ("--lang", {"dest": "target_lang", "choices": ["python", "node"], "default": "python", "help": "Target host language."})
                ]
            },
            "list": {
                "help": "List cached fusion artifacts."
            },
            "clean": {
                "help": "Purge the fusion build cache."
            }
        }
    },
    "observe": {
        "module_path": "artisans.neural_link.artisan",
        "artisan_class_name": "NeuralLinkArtisan",
        "request_class_name": "ObserveRequest",
        "help": "The Neural Link. Live runtime introspection dashboard.",
        "flags": [add_common_flags],
        "args": [
            ("--pid", {"dest": "target_pid", "type": int, "help": "PID to attach to."}),
            ("--log", {"dest": "log_stream", "help": "Log file to tail."}),
            ("--demo", {"action": "store_true", "help": "Run in simulation mode."})
        ]
    },
    "archetypes": {
        "module_path": "artisans.archetypes.artisan",
        "artisan_class_name": "ArchetypeArtisan",
        "request_class_name": "ArchetypeRequest",
        "help": "The Librarian of the Forge. Discover and manage blueprints.",
        "flags": [
            add_common_flags,
            lambda p: p.add_argument('--json', action='store_true', help='Machine-readable output.')
        ],
        "subparsers": {
            "list": {"help": "List all manifest archetypes."},
            "pull": {
                "help": "Download an archetype from a Celestial URL.",
                "args": [("target", {"help": "The URL of the blueprint."})]
            },
            "inspect": {
                "help": "Gaze into a specific archetype's soul.",
                "args": [("target", {"help": "The ID of the archetype."})]
            }
        }
    },
    "plugins": {
        "module_path": "artisans.plugins.artisan",
        "artisan_class_name": "PluginsArtisan",
        "request_class_name": "PluginsRequest",
        "help": "The Capability Census. Lists all active Rites in the Grimoire.",
        "flags": [add_common_flags],
        "args": [
            ("--category", {"help": "Filter by Gnostic Category."})
        ]
    },

}