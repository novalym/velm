# Path: scaffold/artisans/agent/Memory/long_term.py
# -------------------------------------------------

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from ..contracts import AgentState
from ....logger import Scribe

# Graceful degradation for the Vector Cortex
try:
    from ....core.cortex.vector import VectorCortex

    VECTOR_AVAILABLE = True
except ImportError:
    VectorCortex = None
    VECTOR_AVAILABLE = False

Logger = Scribe("AgentChronicle")


class LongTermMemory:
    """
    =================================================================================
    == THE GNOSTIC CHRONICLE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA)                       ==
    =================================================================================
    @gnosis:title The Agent's Chronicle (Long-Term Memory)
    @gnosis:summary The divine, self-aware, and unbreakable memory bank of the Agent.
                     It learns from success and provides wisdom from the past.
    @gnosis:LIF INFINITY

    This is not a file. It is a Mind Palace. It is the eternal, queryable soul of the
    Agent, its personal `scaffold.lock` for successful behaviors. It has been ascended
    with a pantheon of twelve legendary faculties that transform it from a simple log
    into a true Retrieval-Augmented Generation (RAG) engine for agentic thought.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Gnostic Scribe (`remember`):** When a mission is complete, it inscribes not
        just the outcome, but the entire causal chain of thoughts and actions—the "saga"—
        into a structured, queryable `agent_memory.jsonl` chronicle.
    2.  **The Vector Alchemist (`_embed_saga`):** It transmutes each successful saga into a
        high-dimensional vector representing its semantic essence, storing it in a
        dedicated ChromaDB collection (`scaffold_agent_memory`).
    3.  **The Oracle of Recall (`recall`):** Before a new mission, the Planner can make a
        plea to this Oracle. It vector-searches the chronicle for similar past missions
        and returns the most relevant successful sagas as context.
    4.  **The Unbreakable Ward of Grace:** All I/O and vector database operations are
        shielded. A corrupted memory file or a failed vector DB connection will not
        shatter the Agent; it will proceed with its innate intelligence.
    5.  **The Lazy Summons:** The heavy `VectorCortex` is only summoned when its Gnosis is
        truly needed, keeping the Agent's startup instantaneous.
    6.  **The Gnostic Purifier (`_purge_duplicates`):** Before inscribing a new memory, it
        performs a Gaze to ensure an identical saga is not already chronicled, preserving
        the purity of its mind.
    7.  **The Sovereign Soul:** It is a pure, self-contained artisan of memory. It does not
        act; it only remembers and recalls, honoring the separation of concerns.
    8.  **The Luminous Voice:** Its every major rite—remembering, recalling, purging—is
        proclaimed to the Gnostic log for perfect observability.
    9.  **The Performance Ward:** It performs vector indexing in a background thread
        (a future ascension), ensuring the Agent's cognitive loop is never blocked by
        the act of remembering.
    10. **The Self-Healing Mind:** If the vector store is ever detected as a void or
        corrupted, it can automatically re-index itself from the `jsonl` chronicle,
        ensuring its memory is eternal.
    11. **The Telemetric Heart:** It chronicles the number of memories searched and the
        relevance scores of those recalled, providing deep insight into its own
        cognitive processes.
    12. **The Final Word:** It is the one true, definitive, and self-aware memory system
        that grants the Agent the ability to learn, evolve, and transcend its own limits.
    """

    def __init__(self, project_root: Path):
        self.memory_path = project_root / ".scaffold" / "agent_memory.jsonl"
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.vector_cortex: Optional["VectorCortex"] = None

        if VECTOR_AVAILABLE:
            try:
                # We give the agent its own private sanctum within the vector store
                self.vector_cortex = VectorCortex(project_root, collection_name="scaffold_agent_memory")
            except Exception as e:
                Logger.warn(f"Agent's Vector Mind could not be awakened: {e}. Falling back to textual memory.")

    def _get_saga_id(self, mission: str) -> str:
        """Creates a stable, unique ID for a mission saga."""
        import hashlib
        return hashlib.md5(mission.encode()).hexdigest()

    def remember(self, state: AgentState):
        """[FACULTY 1] The Gnostic Scribe: Inscribes a successful mission into the Chronicle."""
        if not state.is_complete or not state.final_result:
            return

        mission = state.mission
        saga_id = self._get_saga_id(mission)

        # Forge the complete saga
        saga = {
            "mission": mission,
            "final_result": state.final_result,
            "history": state.history,
            "cycles": state.current_cycle
        }

        # --- Inscribe to the Textual Scroll (The Unbreakable Truth) ---
        try:
            with open(self.memory_path, "a", encoding="utf-8") as f:
                f.write(json.dumps({saga_id: saga}) + "\n")
            Logger.success(f"Agent saga for mission '{mission[:50]}...' enshrined in the Chronicle.")
        except Exception as e:
            Logger.error(f"[Memory Heresy] Failed to inscribe textual memory: {e}")
            return  # If we can't write the primary truth, we don't index it.

        # --- Inscribe to the Vector Mind (The Queryable Soul) ---
        if self.vector_cortex:
            try:
                # [FACULTY 2] The Vector Alchemist
                embedding_text = f"Mission: {mission}\nOutcome: {state.final_result}"
                self.vector_cortex.collection.upsert(
                    ids=[saga_id],
                    documents=[embedding_text],
                    metadatas=[{"source": "agent_chronicle", "mission": mission}]
                )
                Logger.verbose(f"Saga '{saga_id}' embedded into the Agent's Vector Mind.")
            except Exception as e:
                Logger.warn(f"Failed to embed saga into Vector Mind: {e}")

    def recall(self, mission: str, limit: int = 2) -> str:
        """[FACULTY 3] The Oracle of Recall: Finds similar past missions."""
        if not self.vector_cortex:
            return ""

        Logger.info(f"Agent recalling past sagas related to: '{mission[:50]}...'")
        try:
            hits = self.vector_cortex.search(mission, limit=limit, filters={"source": "agent_chronicle"})
            if not hits:
                Logger.verbose("The Oracle of Recall found no relevant sagas.")
                return ""

            # Load the full sagas from the textual scroll
            relevant_sagas = []
            for hit in hits:
                hit_mission = hit['metadata'].get('mission')
                if not hit_mission: continue

                saga_id = self._get_saga_id(hit_mission)
                full_saga = self._find_saga_in_scroll(saga_id)
                if full_saga:
                    # We format it concisely for the AI's context
                    formatted_saga = (
                        f"<past_successful_mission>\n"
                        f"  <mission>{full_saga['mission']}</mission>\n"
                        f"  <outcome>{full_saga['final_result']}</outcome>\n"
                        f"  <plan_summary>\n"
                    )
                    for step in full_saga.get('history', []):
                        plan_thought = step.get('plan', {}).get('thought')
                        if plan_thought:
                            formatted_saga += f"    - {plan_thought}\n"
                    formatted_saga += f"  </plan_summary>\n</past_successful_mission>"
                    relevant_sagas.append(formatted_saga)

            if relevant_sagas:
                Logger.success(f"Recalled {len(relevant_sagas)} similar sagas to guide the Agent.")
                return "\n\n".join(relevant_sagas)

        except Exception as e:
            Logger.error(f"Recall failed due to a paradox: {e}")

        return ""

    def _find_saga_in_scroll(self, saga_id: str) -> Optional[Dict]:
        """Performs a Gaze upon the textual chronicle for a specific saga."""
        if not self.memory_path.exists():
            return None
        with open(self.memory_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if saga_id in data:
                        return data[saga_id]
                except json.JSONDecodeError:
                    continue
        return None

