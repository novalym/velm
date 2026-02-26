# scaffold/core/cli/grimoire/_evolution_rites.py
"""Rites of architectural transmutation and refactoring."""
import argparse
from ..cli_utils import add_common_flags, add_simulation_flags, add_variable_flags

def add_patch_flags(parser: argparse.ArgumentParser):
    """Bestows the vows for kinetic mutation."""
    parser.add_argument('--prepend', help='Content to inject at the start of the file (Ad-Hoc Mode).')
    parser.add_argument('--append', help='Content to inject at the end of the file (Ad-Hoc Mode).')
    parser.add_argument('--anchor', help='Optional SHA256 hash anchor for safety.')

RITES = {
    "transmute": {
        "module_path": "artisans.transmute",
        "artisan_class_name": "TransmuteArtisan",
        "request_class_name": "TransmuteRequest",
        "help": "Transmutes reality to match a blueprint's will.",
        "flags": [add_common_flags, add_simulation_flags, add_variable_flags],
        "args": [("path_to_scripture", {"nargs": "?", "default": "scaffold.scaffold", "help": "Path to the blueprint."})],
    },
    "patch": {
        "module_path": "artisans.patch",
        "artisan_class_name": "PatchArtisan",
        "request_class_name": "PatchRequest",
        "help": "The Gnostic Surgeon. Surgically applies a `.patch.scaffold` file or direct mutation.",
        "flags": [add_common_flags, add_simulation_flags, add_variable_flags, add_patch_flags],
        "args": [("patch_path", {"help": "Path to the .patch.scaffold file OR the target file for ad-hoc mutation."})],
    },
    "translocate": {
        "module_path": "artisans.translocate",
        "artisan_class_name": "TranslocateArtisan",
        "request_class_name": "TranslocateRequest",
        "help": "The God-Engine of Refactoring. Moves files and heals their Gnostic bonds.",
        "flags": [add_common_flags, add_simulation_flags],
        "args": [("paths", {"nargs": "*", "help": "Source and destination paths (e.g., `src dest`, `src1 src2 dest/`)."})],
    },
    "conform": {
        "module_path": "artisans.conform",
        "artisan_class_name": "ConformArtisan",
        "request_class_name": "ConformRequest",
        "help": "Forces a directory structure to align with a Gnostic Blueprint.",
        "flags": [add_common_flags, add_simulation_flags, add_variable_flags],
        "args": [("blueprint_path", {"help": "The blueprint scripture to conform to."})],
    },
    "refactor": {
        "module_path": "artisans.refactor",
        "artisan_class_name": "RefactorArtisan",
        "request_class_name": "RefactorRequest",
        "help": "Summons the Quantum Forge for visual, interactive refactoring.",
        "flags": [add_common_flags],
        "args": [("blueprint_path", {"nargs": "?", "default": "scaffold.scaffold", "help": "The blueprint to refactor."})],
    },
    "excise": {
        "module_path": "artisans.excise",
        "artisan_class_name": "ExciseArtisan",
        "request_class_name": "ExciseRequest",
        "help": "Surgically removes all artifacts born from a specific blueprint.",
        "flags": [add_common_flags, add_simulation_flags],
        "args": [("blueprint_origin", {"help": "The name of the blueprint whose artifacts should be removed."})],
    },
    "weave": {
        "module_path": "artisans.weave",
        "artisan_class_name": "WeaveArtisan",
        "request_class_name": "WeaveRequest",
        "help": "Weaves an architectural pattern (Archetype) into the current reality.",
        "flags": [add_common_flags, add_simulation_flags, add_variable_flags],
        "args": [
            ("fragment_name", {"nargs": "?", "help": "The name of the archetype to weave."}),
            ("target_directory", {"nargs": "?", "default": ".", "help": "The directory to weave into."})
        ],
    },
    "compose": {
        "module_path": "artisans.compose",
        "artisan_class_name": "ComposeArtisan",
        "request_class_name": "ComposeRequest",
        "help": "Weaves multiple realities into a single cosmos using a `.manifest`.",
        "flags": [add_common_flags, add_simulation_flags, add_variable_flags],
        "args": [("manifest_path", {"help": "Path to the .manifest scripture."})],
    },
    "arch": {
        "module_path": "artisans.arch",
        "artisan_class_name": "ArchArtisan",
        "request_class_name": "ArchRequest",
        "help": "Executes a `.arch` Monad, a scripture of both Form and Will.",
        "flags": [add_common_flags, add_simulation_flags, add_variable_flags],
        "args": [("arch_path", {"help": "Path to the .arch scripture."})],
    },
    "upgrade": {
        "module_path": "artisans.upgrade",
        "artisan_class_name": "UpgradeArtisan",
        "request_class_name": "UpgradeRequest",
        "help": "The Phoenix. Upgrades a project from a newer template version.",
        "flags": [add_common_flags, add_simulation_flags],
        "args": [("from_template", {"help": "The name of the newer template/archetype to upgrade from."})],
    },
    "shadow": {
        "module_path": "artisans.shadow_clone",
        "artisan_class_name": "ShadowCloneArtisan",
        "request_class_name": "ShadowCloneRequest",
        "help": "The Shadow Engine. Conduct Reality Fission (Spawn) and Fusion (Merge).",
        "description": (
            "===============================================================================\n"
            "== THE SHADOW ENGINE: BICAMERAL REALITY GOVERNOR (V-Ω-TOTALITY)              ==\n"
            "===============================================================================\n"
            "The `shadow` artisan is the gateway to parallel development. It allows you to\n"
            "spawn isolated copies of your project to test risky changes or AI experiments.\n\n"
            "Use '--mode lab' for silent refactoring environments, and 'merge' to bring\n"
            "luminous shards of code back to the Prime Timeline with absolute safety."
        ),
        "flags": [add_common_flags],
        "subparsers": {
            # =========================================================================
            # == RITE I: SPAWN (REALITY FISSION)                                     ==
            # =========================================================================
            "spawn": {
                "help": "Materialize a new parallel dimension (Reality Fission).",
                "args": [
                    ("--mode", {
                        "choices": ["run", "lab"],
                        "default": "run",
                        "help": "Dimension purpose: 'run' (Preview + HMR) or 'lab' (Silent Experiment)."
                    }),
                    ("--label", {
                        "default": "experiment",
                        "help": "Human-readable identity for this dimension."
                    }),
                    ("--ref", {
                        "dest": "target_ref",
                        "default": "HEAD",
                        "help": "Git reference or Rite ID to clone from."
                    }),
                    ("--strategy", {
                        "dest": "strategy",
                        "choices": ["git_worktree", "physical_copy", "hybrid"],
                        "default": "hybrid",
                        "help": "Materialization method. 'hybrid' is the path of least resistance."
                    }),
                    ("--port", {
                        "type": int,
                        "default": 0,
                        "help": "Resonance port. 0 = Automated Network Scry."
                    }),
                    ("--no-provision", {
                        "action": "store_false",
                        "dest": "auto_provision",
                        "help": "Disable dependency lung-transplantation (node_modules/venv)."
                    }),
                    ("--owner", {
                        "default": "architect",
                        "help": "The identity responsible for this reality."
                    })
                ]
            },
            # =========================================================================
            # == RITE II: MERGE (REALITY FUSION)                                     ==
            # =========================================================================
            "merge": {
                "help": "Fuse luminous shards from a shadow back into the Prime Timeline.",
                "args": [
                    ("--label", {
                        "help": "The identity of the shadow to fuse from."
                    }),
                    ("--id", {
                        "dest": "target_id",
                        "help": "Specific UUID of the shadow to target."
                    }),
                    ("--no-cleanup", {
                        "action": "store_true",
                        "help": "The Vow of Persistence. Keep the shadow alive after fusion."
                    })
                ]
            },
            # =========================================================================
            # == RITE III: VANISH (REALITY DISSOLUTION)                              ==
            # =========================================================================
            "vanish": {
                "help": "Annihilate a shadow dimension and return its matter to the void.",
                "args": [
                    ("--label", {"help": "Vanish all shadows matching this label."}),
                    ("--id", {"dest": "target_id", "help": "Surgically vanish a specific UUID."})
                ]
            },
            # =========================================================================
            # == RITE IV: STATUS (VITALITY SCRY)                                     ==
            # =========================================================================
            "status": {
                "help": "Scry the metabolic health and coordinates of a dimension.",
                "args": [
                    ("--label", {"help": "Target label."}),
                    ("--id", {"dest": "target_id", "help": "Target UUID."})
                ]
            },
            # =========================================================================
            # == RITE V: LOGS (CHRONICLE RECALL)                                     ==
            # =========================================================================
            "logs": {
                "help": "Commune with a shadow to hear its thoughts (stdout/stderr).",
                "args": [
                    ("--label", {"help": "Target label."}),
                    ("--id", {"dest": "target_id", "help": "Target UUID."})
                ]
            },
            # =========================================================================
            # == RITE VI: LIST (PANOPTIC CENSUS)                                     ==
            # =========================================================================
            "list": {
                "help": "Proclaim the census of all active parallel dimensions."
            },
            # =========================================================================
            # == RITE VII: HIBERNATE (STATE FREEZE)                                  ==
            # =========================================================================
            "hibernate": {
                "help": "Suspend a shadow dimension (Freeze state and kill process).",
                "args": [
                    ("--id", {"dest": "target_id", "help": "UUID to freeze."})
                ]
            }
        }
    },


    "garden": {
        "module_path": "artisans.garden.artisan",
        "artisan_class_name": "GardenArtisan",
        "request_class_name": "GardenRequest",
        "help": "The Entropy Garden. Autonomous pruning of dead code and debt.",
        "flags": [add_common_flags],
        "subparsers": {
            "scan": {
                "help": "Identify dead code candidates without action.",
                "args": [
                    ("--aggressive", {"dest": "aggressiveness", "type": int, "default": 1, "help": "Pruning intensity (1=Safe, 5=Ruthless)."}),
                    ("--path", {"dest": "focus_path", "help": "Limit scan to a specific path."})
                ]
            },
            "report": {
                "help": "Generate a detailed breakdown of technical debt.",
                "args": [("--json", {"action": "store_true", "help": "Output as JSON."})]
            },
            "prune": {
                "help": "Generate a .patch.scaffold to remove dead code.",
                 "args": [
                    ("--aggressive", {"dest": "aggressiveness", "type": int, "default": 1, "help": "Pruning intensity."}),
                    ("--path", {"dest": "focus_path", "help": "Limit pruning to a specific path."})
                ]
            }
        }
    },
    "evolve": {
        "module_path": "artisans.schema.artisan",
        "artisan_class_name": "SchemaArtisan",
        "request_class_name": "EvolveRequest",
        "help": "The Schema Engine. Synchronize Code (Models) with Data (DB).",
        "flags": [add_common_flags],
        "subparsers": {
            "check": {
                "help": "Check for drift between models and database."
            },
            "plan": {
                "help": "Generate a new migration script based on changes.",
                "args": [("--message", "-m", {"help": "Name of the migration."})]
            },
            "apply": {
                "help": "Execute pending migrations.",
                "args": [("--target-env", {"default": "dev", "help": "Target environment."})]
            }
        }
    },
}
