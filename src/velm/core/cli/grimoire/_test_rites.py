# Path: src/velm/core/cli/grimoire/_test_rites.py
# -----------------------------------------------

from ..cli_utils import add_common_flags

RITES = {
    "test": {
        "module_path": "artisans.test.artisan",
        "artisan_class_name": "TestArtisan",
        "request_class_name": "TestRequest",
        "help": "The High Inquisitor. Verifies the integrity of the code.",
        "description": (
            "The `test` artisan is the Gnostic Adjudicator of the codebase. "
            "It automatically detects your testing framework (Pytest, Jest, Cargo), "
            "configures the environment, and executes the suite.\n\n"
            "Capabilities:\n"
            "- **Polyglot:** Works with Python, Node, Rust, and Go.\n"
            "- **Vigilance:** `--watch` mode for TDD cycles.\n"
            "- **Forensics:** `--coverage` generation.\n"
            "- **Swarm:** `--parallel` execution."
        ),
        "flags": [
            add_common_flags,
            lambda p: p.add_argument('--watch', '-w', action='store_true', help='Enter Watch Mode (The Eternal Vigil).'),
            lambda p: p.add_argument('--cov', '--coverage', dest='coverage', action='store_true', help='Generate forensic coverage reports.'),
            lambda p: p.add_argument('--fail-fast', '-x', action='store_true', help='Halt the inquisition on the first heresy.'),
            lambda p: p.add_argument('--parallel', '-n', action='store_true', help='Summon the Swarm (Parallel execution).'),
            lambda p: p.add_argument('--update', '-u', dest='update_snapshots', action='store_true', help='Bless current snapshots as Truth.'),
            lambda p: p.add_argument('--framework', choices=['auto', 'pytest', 'jest', 'vitest', 'cargo', 'go'], default='auto', help='Force a specific Inquisitor engine.'),
            lambda p: p.add_argument('--docker', dest='docker_service', help='Run the trial inside a specific Docker service.'),
            lambda p: p.add_argument('-m', '--marker', dest='markers', action='append', help='Filter tests by Gnostic Markers (e.g., "not slow").'),
        ],
        "args": [
            ("target", {"nargs": "?", "help": "Specific file, directory, or test node to adjudicate."})
        ]
    }
}