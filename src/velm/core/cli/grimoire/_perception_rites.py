# Path: core/cli/grimoire/_perception_rites.py
# --------------------------------------------

"""
=================================================================================
== THE SACRED CODEX OF PERCEPTION (V-Ω-ETERNAL. THE LAW OF THE GAZE)           ==
=================================================================================
@gnosis:title The Sacred Codex of Perception
@gnosis:summary The definitive registry of all CLI rites related to analysis,
                 introspection, and Gnostic perception.
@gnosis:LIF INFINITY

This scripture defines the rites of Gnostic perception and analysis. It teaches
the Grand Architect of Form the unique pleas (flags and arguments) for each
artisan that gazes upon the soul of a project.

It has been aligned with the `DistillRequest` schema to ensure no intent is lost.
=================================================================================
"""
import json
import argparse
from typing import Any

# [ASCENSION]: We import flag-adders from utils, but NOT the heavy shims.
from ..cli_utils import (
    add_common_flags,
    add_variable_flags,
    add_simulation_flags,
    add_tree_flags,
    add_graph_flags,
    add_holographic_flags,
    add_verify_flags,
    add_adopt_flags,
    add_analyze_flags,
    add_inspect_flags,
    add_distill_flags # Assuming this exists or we define it below if custom
)


# =================================================================================
# == THE LAZY HERALDS (PROXY ARTISANS)                                           ==
# =================================================================================

def _lazy_analyze_herald(result: Any, args: argparse.Namespace):
    """
    [THE PROXY]: Summons the heavy Herald only when the Rite is complete.
    This prevents the 'rich' library from loading during CLI startup.
    """
    from ..cli_shims import _handle_analyze_herald
    return _handle_analyze_herald(result, args)


# =================================================================================
# == THE PANTHEON OF FLAGS (THE VOICES OF THE ARTISANS)                          ==
# =================================================================================

def add_custom_distill_flags(parser: argparse.ArgumentParser):
    """
    =================================================================================
    == THE GRIMOIRE OF PERCEPTION (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                ==
    =================================================================================
    @gnosis:title add_distill_flags
    @gnosis:summary The divine scripture that teaches the CLI the complete, sacred
                     tongue of the ascended `distill` artisan.
    @gnosis:LIF 10,000,000
    @gnosis:auth_code:YES!!!!!

    This is the final, eternal, and ultra-definitive form of the `distill`
    artisan's interface definition. It is a masterpiece of Gnostic clarity,
    organizing the vast power of the perception engine into a luminous,
    self-documenting hierarchy that guides the Architect's hand.
    =================================================================================
    """
    # === I. CORE INTENT: The High-Level Plea ===
    intent_group = parser.add_argument_group("I. Core Intent (The Architect's Will)")
    intent_group.add_argument(
        '--intent', '--plea',
        dest='intent',
        help='A natural language plea (e.g., "fix auth bug"). Summons the AI Oracle for a semantic search to find the most relevant scriptures.'
    )
    intent_group.add_argument(
        '--focus',
        nargs='*',
        help='Gnostic keywords or file paths to focus the Gaze upon (e.g., "auth.py", "User"). Summons the Causal Slicer to extract a hyper-focused context.'
    )

    # === II. FORENSIC INQUEST: The Investigation of Paradox ===
    forensic_group = parser.add_argument_group("II. Forensic Inquest (The Investigation)")
    forensic_group.add_argument(
        '--problem', '--error',
        dest='problem',
        help='An error log, stack trace, or crash report. Summons the Forensic Inquisitor to find the scriptures of heresy.'
    )
    forensic_group.add_argument(
        '--diagnose', action='store_true',
        help="The AI Inquisitor's Vow. Commands an AI Analyst to prophesy a root cause hypothesis in the final dossier."
    )
    forensic_group.add_argument(
        '--exec', dest='exec_command',
        help="The Active Witness. Execute a command (e.g., 'pytest') to capture the runtime context of a failure."
    )
    forensic_group.add_argument('--exec-timeout', type=int, default=60,
                                help="Timeout (in seconds) for the Active Witness's Gaze.")

    # === III. TEMPORAL GAZE: The Perception of Time ===
    temporal_group = parser.add_argument_group("III. Temporal Gaze (The Chronomancer's Art)")
    temporal_group.add_argument('--since',
                                help='Annotate scriptures with heat markers (🔥) for any changes made since this Git reference (e.g., a branch name or commit hash).')
    temporal_group.add_argument('--diff-context', action='store_true',
                                help="The Ghost of Versions Past. Inscribe inline diffs (`[WAS: ...]`) showing the scripture's soul at HEAD versus the current reality.")
    temporal_group.add_argument('--regression', action='store_true',
                                help="Summon the Temporal Inquisitor to conduct a `git bisect` rite, automatically finding the commit that introduced a heresy.")
    temporal_group.add_argument('--focus-change',
                                help="A stricter form of '--since'. EXCLUDES all files that have NOT changed since the reference.")

    # === IV. PERCEPTUAL FILTERS: The Gaze of Aversion & Focus ===
    filter_group = parser.add_argument_group("IV. Perceptual Filters (Refining the Gaze)")
    filter_group.add_argument('--ignore', nargs='*',
                              help='Glob patterns of scriptures or sanctums to avert the Gaze from.')
    filter_group.add_argument('--include', nargs='*',
                              help='Glob patterns to exclusively focus the Gaze upon. All else is shadow.')
    filter_group.add_argument('--stub-deps', nargs='*',
                              help='Paths/globs to be replaced by Semantic Stubs (signatures only), reducing token weight.')
    # [THE FIX] Budget is now a string to allow '800k', '1m', etc.
    filter_group.add_argument('--budget', '--token-budget', dest='token_budget', type=str,
                              help='The Gnostic Budget. A token limit for the final scripture (e.g., 100k, 8000).')
    filter_group.add_argument('--profile', choices=['frontend', 'backend', 'data'],
                              help='Apply a pre-defined filter profile (e.g., ignore .py for frontend).')
    filter_group.add_argument('--depth', type=int, default=2,
                              help='The maximum depth of the Causal Weaver\'s graph traversal.')
    filter_group.add_argument('--no-tests', action='store_false', dest='prioritize_tests',
                              help='Demote test files in the ranking algorithms.')

    # === V. STRATEGY & FIDELITY: The Nature of the Scripture ===
    strategy_group = parser.add_argument_group("V. Strategy & Fidelity (The Form of the Gnosis)")
    strategy_group.add_argument(
        '--fidelity', '--strategy',
        dest='strategy',
        # [THE FIX] Added 'skeleton' to choices
        choices=['full', 'balanced', 'aggressive', 'tree', 'surgical', 'skeleton'],
        default='balanced',
        help="The level of detail: 'full' (all content), 'balanced' (smart skeletons), 'aggressive' (minimal stubs), 'tree' (structure only), 'surgical' (causal slicing), 'skeleton' (AST-only)."
    )
    # Sacred Aliases for Fidelity
    strategy_group.add_argument('--full', action='store_const', const='full', dest='strategy',
                                help='Alias for --fidelity=full.')
    strategy_group.add_argument('--surgical', action='store_const', const='surgical', dest='strategy',
                                help='Alias for --fidelity=surgical.')
    strategy_group.add_argument('--skeleton', action='store_const', const='skeleton', dest='strategy',
                                help='Alias for --fidelity=skeleton.')

    # [THE FIX] Re-consecrated the --llm flag as a first-class alias for 'balanced'
    strategy_group.add_argument('--llm', '--llm-optimized', action='store_const', const='balanced', dest='strategy',
                                help='The Vow of the Machine. Optimizes output for LLM context windows (Alias for --fidelity=balanced).')
    strategy_group.add_argument('--form-only', action='store_const', const='tree', dest='strategy',
                                help=argparse.SUPPRESS)

    # === VI. ADVANCED AI & RUNTIME: The Neural & Kinetic Links ===
    ai_group = parser.add_argument_group("VI. Advanced AI & Runtime (The Deep Gaze)")
    ai_group.add_argument('--no-ai', action='store_true',
                          help='A sacred vow to forbid the Oracle from communing with the Neural Cortex.')
    ai_group.add_argument('--interactive', action='store_true',
                          help='Enable Socratic Mode. The Oracle may pause to ask clarifying questions.')
    ai_group.add_argument('--recursive-agent', action='store_true',
                          help='Activate the Socratic Reviewer. The AI will critique its own context selection and perform a second pass.')
    ai_group.add_argument('--trace-command',
                          help='Execute a command to capture live variable states (The Runtime Wraith).')
    ai_group.add_argument('--profile-perf', action='store_true',
                          help='Activate the Wraith of Celerity to profile execution time and weave a performance heatmap.')
    ai_group.add_argument('--snapshot-path',
                          help='Inject a JSON crash dump or state snapshot into the blueprint.')
    ai_group.add_argument('--audit-security', action='store_true',
                          help='Activate the Security Sentinel to scan for vulnerabilities.')

    # === VII. FINAL PROCLAMATION: The Output Form ===
    output_group = parser.add_argument_group("VII. Final Proclamation (The Output)")
    output_group.add_argument(
        '--format',
        choices=['blueprint', 'dossier', 'json', 'markdown', 'mermaid'],
        default='blueprint',
        help="The final Gnostic form: 'blueprint' (.scaffold), 'dossier' (.md), or machine-readable 'json'."
    )
    # Sacred Aliases for Format
    output_group.add_argument('--holocron', action='store_const', const='dossier', dest='format',
                              help='A sacred alias for --format=dossier.')
    output_group.add_argument('--json', action='store_const', const='json', dest='format',
                              help='A sacred alias for --format=json.')

    output_group.add_argument('--output', '-o',
                              help='Path to inscribe the final scripture. If omitted, proclaims to stdout.')
    output_group.add_argument('--clipboard', '-c', action='store_true',
                              help='Teleport the final scripture to the system clipboard.')
    output_group.add_argument('--summarize', action='store_true',
                              help='Summon an AI Scribe to generate a final README.md summary of the Gnosis.')
    output_group.add_argument('--pad', action='store_true',
                              help='Summon the interactive Gnostic Workbench (TUI) for this distillation.')
    output_group.add_argument('--diagram', choices=['mermaid', 'json'],
                              help="Generate a supplementary architectural diagram.")
    output_group.add_argument('--lfg', action='store_true',
                              help='Inject a Logic Flow Graph into the header.')
    output_group.add_argument('--summarize-arch', action='store_true',
                              help='Append a high-level architectural summary to the header.')


# =================================================================================
# == THE GRIMOIRE (RITE DEFINITIONS)                                             ==
# =================================================================================

RITES = {
    "audit": {
            "module_path": "artisans.audit",
            "artisan_class_name": "AuditArtisan",
            "request_class_name": "AuditRequest",
            "help": "The High Inquisitor. Audits reality for compliance and purity.",
            "flags": [add_common_flags],
            "args": [
                ("audit_target", {"choices": ["licenses", "arch"], "help": "The domain of reality to audit."})
            ],
        },
    "distill": {
        "module_path": "artisans.distill",
        "artisan_class_name": "DistillArtisan",
        "request_class_name": "DistillRequest",
        "help": "The Rite of Reverse Genesis. Transmutes reality into a blueprint.",
        "flags": [add_common_flags, add_variable_flags, add_custom_distill_flags],
        "args": [("source_path", {"nargs": "?", "default": ".", "help": "The directory or remote URL to distill."})],
    },
    "adopt": {
        "module_path": "artisans.adopt",
        "artisan_class_name": "AdoptArtisan",
        "request_class_name": "AdoptRequest",
        "help": "Transmutes the current reality into Gnostic Law (Blueprint) and Memory (Lockfile).",
        "flags": [add_common_flags, add_adopt_flags],
        "args": [("target_path", {"nargs": "?", "default": ".", "help": "The path to adopt."})],
    },
    "verify": {
        "module_path": "artisans.verify",
        "artisan_class_name": "VerifyArtisan",
        "request_class_name": "VerifyRequest",
        "help": "The Gnostic Auditor. Verifies reality against the `scaffold.lock` chronicle.",
        "flags": [add_common_flags, add_verify_flags],
        "args": [("target_path", {"nargs": "?", "default": ".", "help": "The project path to verify."})],
    },
    "analyze": {
        "module_path": "artisans.analyze",
        "artisan_class_name": "AnalyzeArtisan",
        "request_class_name": "AnalyzeRequest",
        "help": "The Inquisitor's Gaze. Performs deep static analysis on a scripture.",
        "flags": [add_common_flags, add_analyze_flags],
        "args": [("path_to_scripture", {"help": "The file to analyze."})],
        "herald": _lazy_analyze_herald,  # [FIXED]: Lazy Proxy for the Herald
    },
    "inspect": {
        "module_path": "artisans.inspect",
        "artisan_class_name": "InspectArtisan",
        "request_class_name": "InspectRequest",
        "help": "The Gnostic Lens. Previews a blueprint's reality without materialization.",
        "flags": [add_common_flags, add_variable_flags, add_inspect_flags],
        "args": [("blueprint_path", {"help": "The blueprint to inspect."})],
    },
    "tree": {
        "module_path": "artisans.tree",
        "artisan_class_name": "TreeArtisan",
        "request_class_name": "TreeRequest",
        "help": "The Gnostic Surveyor. Visualizes a directory with deep metadata.",
        "flags": [add_common_flags, add_tree_flags],
        "args": [("target_path", {"nargs": "?", "default": ".", "help": "Directory to survey."})],
    },
    "graph": {
        "module_path": "artisans.graph.artisan",
        "artisan_class_name": "GraphArtisan",
        "request_class_name": "GraphRequest",
        "help": "The High Conductor of Topology. Perceives and manifests the architectural cosmos.",
        "description": "The `graph` rite is the one true bridge between visual intent and physical matter. "
                       "Without arguments, it scans reality to forge a Gnostic Graph. "
                       "When provided with --data, it transmutes that graph back into scriptures and sanctums.",
        "flags": [
            add_common_flags,
            add_variable_flags,
            add_simulation_flags,
            add_graph_flags,
            # [ASCENSION]: The JSON Visibility Flag
            lambda p: p.add_argument('--json', action='store_true', help='Ensure output is pure JSON for machine consumption.')
        ],
        "args": [
            ("--focus", {
                "help": "Anchor the Gaze to a specific symbol, file, or architectural domain."
            }),
            ("--format", {
                "choices": ["json", "mermaid", "svg", "text"],
                "default": "json",
                "help": "The sacred tongue of the proclamation."
            }),
            ("--data", {
                "dest": "graph_data",
                "type": json.loads,
                "help": "The JSON Graph payload (nodes/edges) to manifest on disk. Primarily used by the Cockpit."
            }),
            ("--orphans", {
                "dest": "include_orphans",
                "action": "store_true",
                "default": True,
                "help": "Include atoms in reality that are not yet bound to the Gnostic Law."
            }),
            ("--depth", {
                "type": int,
                "default": -1,
                "help": "The maximum depth of the Causal Weaver's traversal."
            })
        ],
    },

    "matrix": {
        "module_path": "artisans.matrix",
        "artisan_class_name": "MatrixArtisan",
        "request_class_name": "MatrixRequest",
        "help": "Analyses lockfiles to reveal the true state of the supply chain.",
        "flags": [add_common_flags],
    },
    "mri": {
        "module_path": "artisans.mri",
        "artisan_class_name": "MRIArtisan",
        "request_class_name": "MRIRequest",
        "help": "Scans the dependency graph for Layer Violations.",
        "flags": [add_common_flags],
    },
    "risk": {
        "module_path": "artisans.risk",
        "artisan_class_name": "BusFactorArtisan",
        "request_class_name": "BusFactorRequest",
        "help": "Calculates the 'Bus Factor' of the codebase.",
        "flags": [add_common_flags],
    },
    "hunt": {
        "module_path": "artisans.ghost_hunter",
        "artisan_class_name": "GhostHunterArtisan",
        "request_class_name": "GhostRequest",
        "help": "Identifies code that exists but has no purpose (dead code).",
        "flags": [add_common_flags],
    },
    "summarize": {
        "module_path": "artisans.summarize",
        "artisan_class_name": "SummarizeArtisan",
        "request_class_name": "SummarizeRequest",
        "help": "Generates a human-readable summary of a codebase using the Gnostic Cortex.",
        "flags": [add_common_flags],
    },
    "sgrep": {
        "module_path": "artisans.sgrep",
        "artisan_class_name": "SgrepArtisan",
        "request_class_name": "SgrepRequest",
        "help": "Searches the Gnostic Memory (AST) for symbols, not strings.",
        "flags": [add_common_flags],
        "args": [
            ("type", {"choices": ["function", "class", "any"], "help": "The type of symbol to search for."}),
            ("pattern", {"help": "The regex pattern to match against the symbol name."}),
        ],
    },
    "semdiff": {
        "module_path": "artisans.semdiff",
        "artisan_class_name": "SemDiffArtisan",
        "request_class_name": "SemDiffRequest",
        "help": "Compares the current reality against a Git reference by symbols, not lines.",
        "flags": [add_common_flags],
        "args": [
            ("target", {"help": "The file or directory to compare."}),
            ("reference", {"nargs": "?", "default": "HEAD",
                           "help": "The Git reference to compare against (e.g., HEAD~1, a branch name, a tag)."}),
        ],
    },
    "holographic": {
        "module_path": "artisans.holographic",
        "artisan_class_name": "HolographicBlueprintArtisan",
        "request_class_name": "HolographicBlueprintRequest",
        "help": "The Reality Scanner. Transmutes a physical directory into a single .scaffold scripture.",
        "flags": [add_common_flags, add_holographic_flags],
        "args": [
            ("target_dir", {"help": "The source directory to digitize into a blueprint."}),
            ("output_file", {"help": "The name of the final .scaffold scripture."}),
        ],
    },
    "preview": {
        "module_path": "artisans.preview",
        "artisan_class_name": "PreviewArtisan",
        "request_class_name": "PreviewRequest",
        "help": "Projects a structural hologram of a UI component.",
        "flags": [add_common_flags],
        "args": [("path", {"help": "The path to the UI scripture."})],
    },
    "index": {
        "module_path": "artisans.indexer",
        "artisan_class_name": "IndexerArtisan",
        "request_class_name": "IndexRequest",
        "help": "The Silent Scholar. Indexes symbols for O(1) intelligence.",
        "flags": [add_common_flags],
        "args": [("--force", {"action": "store_true", "help": "Force re-indexing."})]
    },
}