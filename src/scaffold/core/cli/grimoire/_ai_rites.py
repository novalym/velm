# scaffold/core/cli/grimoire/_ai_rites.py
"""The sacred rites for communing with the higher realms of intelligence."""
from ..cli_utils import add_common_flags, add_variable_flags, add_simulation_flags
import argparse

RITES = {
    "daemon": {
        "module_path": "artisans.daemon_artisan",
        "artisan_class_name": "DaemonArtisan",
        "request_class_name": "DaemonRequest",
        "help": "The High Priest of the Daemon. Manages the background Gnostic Nexus.",
        "flags": [add_common_flags],
        "subparsers": {
            "start": {
                    "help": "Awaken the Daemon in the current project sanctum.",
                    "args": [
                        ("--parent-pid", {"type": int, "help": "The PID of the creator."}),
                        ("--pulse-file", {"help": "Path to the heartbeat file."}), # <--- ADD THIS
                        ("--allow-remote", {"action": "store_true", "help": "Bind to 0.0.0.0."})
                    ]
            },
            "stop": {"help": "Command the Daemon to enter a state of grace."},
            "status": {"help": "Perceive the Daemon's current state of being."},
            "logs": {"help": "Commune with the Daemon to hear its thoughts."},
            "vigil": {"help": "Awaken the Daemon in Vigil mode, watching for file changes."},
        }
    },
    "neural": {
        "module_path": "artisans.neural",
        "artisan_class_name": "NeuralArtisan",
        "request_class_name": "NeuralRequest",
        "help": "Open the Synaptic Console for AI configuration.",
        "flags": [add_common_flags],
    },
    "query": {
        "module_path": "artisans.query",
        "artisan_class_name": "QueryArtisan",
        "request_class_name": "QueryRequest",
        "help": "The Gnostic Emissary. A universal, JSON-based query interface for AIs.",
        "flags": [
            add_common_flags,
            lambda p: p.add_argument('--json', action='store_true', help='Ensure output is pure JSON for machine consumption.')
        ],
        "args": [("query", {"help": "The JSON-formatted plea from the AI."})]
    },
    "architect": {
        "module_path": "artisans.architect",
        "artisan_class_name": "ArchitectArtisan",
        "request_class_name": "ArchitectRequest",
        "help": "The AI Co-Architect. Evolves a project based on natural language intent.",
        "flags": [add_common_flags, add_variable_flags],
        "args": [("prompt", {"help": "The architect's intent for the project's evolution."})],
    },
    "manifest": {
        "module_path": "artisans.manifest",
        "artisan_class_name": "ManifestArtisan",
        "request_class_name": "ManifestRequest",
        "help": "The Neuromancer. Transmutes Natural Language into Structural Reality.",
        "flags": [add_common_flags, add_variable_flags, add_simulation_flags],
        "args": [("prompt", {"help": "The natural language plea for the new reality."})],
    },
    "introspect": {
        "module_path": "artisans.introspect",
        "artisan_class_name": "IntrospectionArtisan",
        "request_class_name": "IntrospectionRequest",
        "help": "The Oracle's Gaze. Proclaims the engine's internal capabilities.",
        # [THE FIX]: We bestow the JSON vow upon the Introspector.
        "flags": [
            add_common_flags,
            lambda p: p.add_argument('--json', action='store_true', help='Proclaim Gnosis as machine-readable JSON.')
        ],
        "args": [("topic", {"choices": ["all", "ui_components", "semantic_domains", "help_topics"], "help": "The Gnostic topic to introspect."})],
    },
    "vector": {
        "module_path": "artisans.vector.artisan",
        "artisan_class_name": "VectorArtisan",
        "request_class_name": "VectorRequest",
        "help": "Manage the project's semantic vector index (for RAG).",
        "flags": [add_common_flags],
        "subparsers": {
            "index": {"help": "Scan and index the entire project."},
            "query": {
                "help": "Perform a semantic search.",
                "args": [("query_text", {"help": "The natural language query."})]
            },
            "clear": {"help": "Annihilate the vector store."},
        }
    },
    "resonate": {
        "module_path": "artisans.resonate",
        "artisan_class_name": "ResonateArtisan",
        "request_class_name": "ResonateRequest",
        "help": "Stop searching for strings. Search for *intent*.",
        "flags": [add_common_flags],
        "args": [("query", {"help": "The concept to search for."})],
    },
    "translate": {
        "module_path": "artisans.translate",
        "artisan_class_name": "TranslateArtisan",
        "request_class_name": "TranslateRequest",
        "help": "The Rosetta Stone. Transmutes code between tongues.",
        "flags": [add_common_flags],
        "args": [
            ("source_path", {"help": "The source scripture to translate."}),
            ("target_lang", {"help": "The target language (e.g., 'python', 'rust')."}),
        ],
    },
    "dream": {
        "module_path": "artisans.dream",
        "artisan_class_name": "DreamArtisan",
        "request_class_name": "DreamRequest",
        "help": "The Oneiromancer. Transmutes natural language into a Gnostic Blueprint.",
        "flags": [add_common_flags],
        "args": [("prompt", {"help": "The natural language description of the desired architecture."})],
    },
    "muse": {
        "module_path": "artisans.muse",
        "artisan_class_name": "MuseArtisan",
        "request_class_name": "MuseRequest",
        "help": "The Prescient Muse. Predicts your next action and offers to perform it.",
        "flags": [add_common_flags],
        "args": [("context_file", {"nargs": "?", "help": "The file you are currently working on to provide context."})],
    },
    "agent": {
        "module_path": "artisans.agent",
        "artisan_class_name": "AgentArtisan",
        "request_class_name": "AgentRequest",
        "help": "The Conqueror. Unleashes an autonomous AI agent to fulfill a complex mission.",
        "flags": [add_common_flags],
        "args": [("mission", {"help": "The mission objective for the agent."})],
    },
    "scribe": {
        "module_path": "artisans.scribe.conductor",
        "artisan_class_name": "ScribeConductor",
        "request_class_name": "ScribeRequest",
        "help": "The Gnostic Scribe. Transmutes natural language into a Gnostic scripture.",
        "flags": [
            add_common_flags,
            lambda p: p.add_argument('-o', '--output-path', help='Optional path to save the generated scripture.'),
            lambda p: p.add_argument('--lang', dest='language', default='scaffold', choices=['scaffold', 'symphony', 'arch'], help='The sacred tongue of the prophecy.')
        ],
        "args": [("plea", {"help": "The natural language architectural plea."})],
    },
    "train": {
        "module_path": "artisans.train",
        "artisan_class_name": "TrainArtisan",
        "request_class_name": "TrainRequest",
        "help": "The Gnostic Forge. Trains a custom AI adapter on your codebase.",
        "flags": [
            add_common_flags,
            lambda p: p.add_argument('--base-model', help="HuggingFace model ID to fine-tune."),
            lambda p: p.add_argument('--epochs', type=int, help="Number of training epochs."),
            lambda p: p.add_argument('--batch-size', type=int, help="Training batch size."),
            lambda p: p.add_argument('--limit', type=int, dest='limit_samples', help="Limit number of training samples for testing."),
        ],
        "args": [("output_model_name", {"help": "Name of the resulting adapter."})],
    },
    "akasha": {
        "module_path": "artisans.akasha.artisan",
        "artisan_class_name": "AkashaArtisan",
        "request_class_name": "AkashaRequest",
        "help": "The Keeper of the Akasha. Manage the global Gnostic memory.",
        "flags": [add_common_flags],
        "subparsers": {
            "stats": {"help": "View the vitality of the global memory."},
            "query": {
                "help": "Gaze into the Akasha for wisdom.",
                "args": [("query", {"help": "The natural language query."})]
            },
            "purge": {"help": "Annihilate the global memory."},
        }
    },
    "debate": {
        "module_path": "artisans.hivemind.artisan",
        "artisan_class_name": "HivemindArtisan",
        "request_class_name": "DebateRequest",
        "help": "The Hivemind. Summon a council of AI personas to debate a topic.",
        "flags": [add_common_flags, add_variable_flags],
        "args": [
            ("topic", {"help": "The subject of the debate."}),
            ("--with", {"dest": "personas", "nargs": "+", "default": ["architect", "security", "pragmatist"], "help": "Personas to summon (e.g., 'architect security')."}),
            ("--rounds", {"type": int, "default": 1, "help": "Number of rebuttal rounds."}),
            ("--blind", {"action": "store_true", "help": "If set, personas do not see each other's initial arguments."}),
            ("--no-synthesis", {"dest": "synthesize", "action": "store_false", "help": "Skip the final summarization step."})
        ],
    },
    "holocron": {
        "module_path": "artisans.holocron.artisan",
        "artisan_class_name": "HolocronArtisan",
        "request_class_name": "HolocronRequest",
        "help": "The Causal Context Engine. Maps execution paths to define perfect context.",
        "flags": [add_common_flags],
        "subparsers": {
            "trace": {
                "help": "Trace the static call graph from an entry point.",
                "args": [
                    ("entry_point", {"help": "The symbol or file to start from."}),
                    ("--depth", {"type": int, "default": 5, "help": "How deep to traverse the graph."}),
                ]
            },
            "slice": {
                "help": "Surgically extract code related to a specific symbol.",
                "args": [
                    ("entry_point", {"help": "The symbol to focus on."}),
                    ("--output", {"dest": "output_data", "help": "Where to save the slice."})
                ]
            },
            "forge": {
                "help": "Forge a Virtual Context based on a natural language problem description.",
                "args": [
                    ("entry_point", {"help": "The problem description (Intent)."}),
                    ("--output", {"dest": "output_data", "help": "Where to save the virtual context."}),
                    ("--depth", {"type": int, "default": 2, "help": "Graph traversal depth."})
                ]
            }
        }
    },

    "ocular": {
        "module_path": "artisans.ocular.artisan",
        "artisan_class_name": "OcularArtisan",
        "request_class_name": "OcularRequest",
        "help": "The Ocular Cortex. Multimodal perception for UI engineering.",
        "flags": [add_common_flags],
        "subparsers": {
            "gaze": {
                "help": "Inspect a live URL and map pixels to code.",
                "args": [
                    ("--url", {"required": True, "help": "The URL to inspect."}),
                    ("--target", {"dest": "target_element", "help": "Selector or text to find."})
                ]
            }
        }
    },

    "aether": {
        "module_path": "artisans.aether.artisan",
        "artisan_class_name": "AetherArtisan",
        "request_class_name": "AetherRequest",
        "help": "The Neural Aether. Federated learning and pattern sharing.",
        "flags": [add_common_flags],
        "subparsers": {
            "sync": {"help": "Download the latest wisdom from the mesh."},
            "broadcast": {"help": "Share local patterns (anonymized) with the mesh."}
        }
    },
}