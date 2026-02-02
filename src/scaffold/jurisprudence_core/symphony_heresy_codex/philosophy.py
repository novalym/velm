# Path: jurisprudence_core/symphony_heresy_codex/philosophy.py
# -----------------------------------------------------------

"""
=================================================================================
== THE LAWS OF THE GRAND DESIGN (PHILOSOPHY, RESILIENCE, & PARALLELISM)        ==
=================================================================================
These laws govern the metaphysical structure of the Symphony. They judge the
wisdom of concurrency, the robustness of error handling, and the elegance of
the workflow.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

PHILOSOPHICAL_LAWS: Dict[str, GnosticLaw] = {

    # --- THE LAWS OF THE MULTIVERSE (PARALLELISM) ---

    "EMPTY_MULTIVERSE_HERESY": GnosticLaw(
        key="EMPTY_MULTIVERSE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Silent Multiverse",
        message="A parallel block was proclaimed, but it contains no threads of execution.",
        elucidation="The `parallel:` or `&&:` rite is intended to spark concurrent realities. A block with no edicts inside is a void of will that consumes cognitive overhead for no effect.",
        severity="WARNING",
        suggestion="Add at least one Action (>>) or Polyglot block inside the parallel section, or remove the block entirely."
    ),

    "NESTED_MULTIVERSE_HERESY": GnosticLaw(
        key="NESTED_MULTIVERSE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Ouroboros of Parallelism",
        message="A parallel block was perceived within another parallel block.",
        elucidation="Nesting concurrent realities creates an exponential complexity that risks deadlocking the Conductor and exhausting the host machine's thread pool.",
        severity="CRITICAL",
        suggestion="Flatten the parallel execution plan. Use a single parallel block for all concurrent actions."
    ),

    "VOW_IN_PARALLEL_HERESY": GnosticLaw(
        key="VOW_IN_PARALLEL_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of Ambiguous Adjudication",
        message="A Vow (??) was perceived within a non-linear, parallel block.",
        elucidation="Vows require a deterministic state to judge. In a parallel block, the order of completion is non-deterministic, making the Vow's judgment a gamble.",
        severity="CRITICAL",
        suggestion="Move the Vow outside the parallel block to judge the collective result, or place it within a serialized sub-task."
    ),

    "STATE_IN_PARALLEL_HERESY": GnosticLaw(
        key="STATE_IN_PARALLEL_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Shared Mind",
        message="A State change (%%) was attempted within a parallel block.",
        elucidation="Allowing concurrent threads to mutate the global state (like 'sanctum' or 'let') leads to race conditions where the 'Truth' becomes a matter of chance.",
        severity="CRITICAL",
        suggestion="Perform state transmutations before or after the parallel block, or use local thread-bound variables if supported."
    ),

    "HERESY_OF_THE_ASYNCHRONOUS_PARADOX": GnosticLaw(
        key="HERESY_OF_THE_ASYNCHRONOUS_PARADOX",
        validator=NULL_VALIDATOR,
        title="The Asynchronous Paradox",
        message="A Vow attempts to judge a background process that has not yet finalized.",
        elucidation="This 'Temporal Schism' occurs when the Conductor proceeds to the next line before a backgrounded parallel task has committed its reality to disk.",
        severity="WARNING",
        suggestion="Use the `?? wait_for` Vow to ensure the background reality is manifest before proceeding."
    ),

    "PARALLEL_OVERHEAD_HERESY": GnosticLaw(
        key="PARALLEL_OVERHEAD_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Hollow Multiverse",
        message="Parallelism was invoked for a sequence of trivial tasks.",
        elucidation="Spawning threads for micro-tasks (like simple 'echo' commands) creates more overhead in context-switching than it saves in execution time.",
        severity="INFO",
        suggestion="Serialize these trivial actions to improve overall symphony performance."
    ),

    # --- THE LAWS OF RESILIENCE ---

    "CRACKED_FOUNDATION_HERESY": GnosticLaw(
        key="CRACKED_FOUNDATION_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Cracked Foundation",
        message="A critical setup rite is marked as 'allow_fail'.",
        elucidation="The Conductor perceived that a fundamental action (like `npm install` or `git init`) is allowed to fail. If the foundation is not manifest, every subsequent edict is predestined for failure.",
        severity="CRITICAL",
        suggestion="Remove the 'allow_fail' flag from foundational setup rites to ensure the symphony halts at the moment of fracture."
    ),

    "HERESY_OF_THE_TREACHEROUS_SANCTUARY": GnosticLaw(
        key="HERESY_OF_THE_TREACHEROUS_SANCTUARY",
        validator=NULL_VALIDATOR,
        title="The Treacherous Sanctuary",
        message="A destructive action was perceived within a 'catch' block.",
        elucidation="Error handling blocks (@try/@catch) are intended for recovery and cleanup. Performing critical or destructive actions (like `rm -rf`) inside a catch block risks creating a cascade of unpredictable paradoxes.",
        severity="WARNING",
        suggestion="Limit 'catch' blocks to logging, state-reversal, or benign fallbacks."
    ),

    "HERESY_OF_BLIND_FAITH": GnosticLaw(
        key="HERESY_OF_BLIND_FAITH",
        validator=NULL_VALIDATOR,
        title="Heresy of Blind Faith",
        message="The symphony conducts numerous actions without any Vows.",
        elucidation="Conducting long sequences of commands without adjudicating the state (??) assumes the mortal realm is perfect. This 'Blind Faith' is the primary cause of flaky deployments and silent data corruption.",
        severity="WARNING",
        suggestion="Inscribe Vow Edicts (??) after significant Actions (>>) to verify reality before proceeding."
    ),

    "SILENT_FAILURE_HERESY": GnosticLaw(
        key="SILENT_FAILURE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Black Hole of Truth",
        message="A catch block is empty, swallowing all Gnosis of failure.",
        elucidation="Catching a heresy without logging it or proclaiming it to the Scribe creates a logical void. Future architects will have no record of why the timeline branched.",
        severity="WARNING",
        suggestion="Add a `%% proclaim` edict to the catch block to record the nature of the paradox."
    ),

    # --- THE LAWS OF ARCHITECTURAL ELEGANCE ---

    "UNREPEATABLE_RITE_HERESY": GnosticLaw(
        key="UNREPEATABLE_RITE_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Unrepeatable Rite",
        message="The action is non-idempotent and lacks a guard.",
        elucidation="An edict that modifies state (like creating a user or a folder) will fail if run a second time. Gnostic scripts must be 'Idempotent'—capable of being run 100 times with the same result.",
        severity="WARNING",
        suggestion="Wrap the action in an `@if` guard or use a command that handles existence (e.g., `mkdir -p`)."
    ),

    "SYMPHONY_OF_A_THOUSAND_CUTS_HERESY": GnosticLaw(
        key="SYMPHONY_OF_A_THOUSAND_CUTS_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of a Thousand Cuts",
        message="The scripture contains an excessive number of atomic actions.",
        elucidation="A symphony with 50+ individual shell commands is difficult to audit and maintain. It suggests the Architect should group edicts into `@task` blocks or move complex logic into a polyglot artisan.",
        severity="INFO",
        suggestion="Consolidate related actions into `@task` blocks or use a script file via `scaffold run`."
    ),

    "MUTE_CONDUCTOR_HERESY": GnosticLaw(
        key="MUTE_CONDUCTOR_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Mute Conductor",
        message="The symphony performs the work but never speaks to the Architect.",
        elucidation="A script that provides no feedback during execution is a 'Dark Workflow'. High-fidelity symphonies use `%% proclaim` to narrate their progress.",
        severity="INFO",
        suggestion="Add `%% proclaim` edicts to narrate the different movements of your symphony."
    ),

    "BEGGING_GOD_HERESY": GnosticLaw(
        key="BEGGING_GOD_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Begging God",
        message="An interactive plea (confirm:) was detected in a non-interactive rite.",
        elucidation="Symphonies willed for CI/CD or automation must not ask for human input. Attempting to do so in a headless environment will hang the Conductor indefinitely.",
        severity="CRITICAL",
        suggestion="Use the `?? confirm` vow only when `SCAFFOLD_INTERACTIVE` is true, or provide a default via `--force`."
    ),

    "ILLUSION_OF_CHOICE_HERESY": GnosticLaw(
        key="ILLUSION_OF_CHOICE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Illusion of Choice",
        message="A conditional path is statically deterministic.",
        elucidation="The `@if` condition relies on variables that are hardcoded or constant, meaning one branch of the reality will *never* be born. This is a redundant complexity.",
        severity="INFO",
        suggestion="Remove the conditional logic and preserve only the path that is willed to exist."
    ),

    "TEMPORAL_SCHISM_HERESY": GnosticLaw(
        key="TEMPORAL_SCHISM_HERESY",
        validator=NULL_VALIDATOR,
        title="Heresy of the Temporal Schism",
        message="An action depends on a state that has been returned to the void.",
        elucidation="A command references a directory or variable defined inside a block that has already been closed. The soul it seeks is no longer manifest in this timeline.",
        severity="CRITICAL",
        suggestion="Ensure the dependency exists in a scope accessible to the action."
    ),
}