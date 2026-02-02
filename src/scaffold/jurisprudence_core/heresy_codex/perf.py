# Path: jurisprudence_core/heresy_codex/perf.py
# ---------------------------------------------

"""
=================================================================================
== THE WRAITH OF LATENCY (PERFORMANCE & RESOURCE HERESIES)                     ==
=================================================================================
These laws govern the efficiency of the code. They detect algorithmic
inefficiencies, blocking I/O, and resource exhaustion risks.
=================================================================================
"""
from typing import Dict
from ...contracts.law_contracts import GnosticLaw

# A humble, default validator fulfilling the sacred contract.
NULL_VALIDATOR = lambda x: True

PERFORMANCE_LAWS: Dict[str, GnosticLaw] = {

    "N_PLUS_ONE_QUERY_HERESY": GnosticLaw(
        key="N_PLUS_ONE_QUERY_HERESY",
        validator=NULL_VALIDATOR,
        title="The Avalanche of Queries",
        message="Potential N+1 database query pattern perceived.",
        elucidation="Executing a database query inside a loop causes an avalanche of network requests, leading to the Heresy of the Frozen River (high latency).",
        severity="CRITICAL",
        suggestion="Use 'eager loading' (JOINs) or batch the data retrieval into a single, atomic query."
    ),

    "BLOCKING_ASYNC_HERESY": GnosticLaw(
        key="BLOCKING_ASYNC_HERESY",
        validator=NULL_VALIDATOR,
        title="The Frozen River: Blocking I/O in Async",
        message="Synchronous I/O detected inside an asynchronous rite.",
        elucidation="Blocking the event loop with synchronous calls (like `time.sleep` or `requests.get`) halts all other concurrent tasks, shattering the illusion of parallelism.",
        severity="CRITICAL",
        suggestion="Use asynchronous alternatives (like `asyncio.sleep` or `httpx.get`)."
    ),

    "INEFFICIENT_STRING_CONCAT_HERESY": GnosticLaw(
        key="INEFFICIENT_STRING_CONCAT_HERESY",
        validator=NULL_VALIDATOR,
        title="The O(N^2) String",
        message="Inefficient string concatenation in a loop.",
        elucidation="Repeatedly adding to a string in a loop creates a new object in memory every time. For large datasets, this devours the machine's spirit.",
        severity="WARNING",
        suggestion="Collect the parts in a list and use `''.join(list)` at the conclusion."
    ),

    "LARGE_CONFIG_FILE_HERESY": GnosticLaw(
        key="LARGE_CONFIG_FILE_HERESY",
        validator=NULL_VALIDATOR,
        title="The Monolithic Config",
        message="A configuration scripture exceeds the bounds of prudence (>200 lines).",
        elucidation="Massive configuration files slow down the parsing rites and make the cognitive load unbearable for the Architect.",
        severity="WARNING",
        suggestion="Split the configuration into domain-specific files (e.g., `logging.json`, `database.yaml`)."
    ),
}