# Path: src/velm/parser_core/parser/parser_scribes/scaffold_scribes/directive_scribe/handlers/agent.py
# -------------------------------------------------------------------------------------------------------------
import re
import json
from typing import List, Dict, Any, Optional

from .base import BaseDirectiveHandler
from .......contracts.data_contracts import GnosticVessel, ScaffoldItem
from .......contracts.heresy_contracts import ArtisanHeresy, HeresySeverity


class AgentHandler(BaseDirectiveHandler):
    """
    =================================================================================
    == THE NEURAL SUPERVISOR (V-Ω-TOTALITY-V25-AGENT-MATRIX)                       ==
    =================================================================================
    LIF: 500x | ROLE: PERSONA_FORGE | RANK: OMEGA_SOVEREIGN

    The Conductor of Cognitive Entities. It parses the declarative definition of
    Autonomous Agents within the blueprint.

    [ASCENSIONS 21-25]:
    Enables Declarative Neural Autonomy.
    - @agent: Defines a cognitive persona and starts the definition block.
    - @system: Injects the constitutional law (System Prompt).
    - @tools: Grants kinetic limbs to the AI (Function Calling bindings).
    - @goal: Sets the convergence success criteria for the agent loop.
    =================================================================================
    """

    def conduct(self, lines: List[str], i: int, vessel: GnosticVessel) -> int:
        """
        The Rite of Neural Definition.
        """
        directive = vessel.directive_type
        raw_line = vessel.raw_scripture.strip()

        # --- MOVEMENT I: DECORATOR ACCUMULATION ---
        # Unlike tasks, agent metadata might be inside the block or decorators above.
        # We support decorators ABOVE for consistency with @task.
        if directive in ("system", "tools", "goal"):
            if not hasattr(self.parser, '_pending_agent_meta'):
                self.parser._pending_agent_meta = {}
            self.parser._pending_agent_meta[directive] = vessel.name
            return i + 1

        # --- MOVEMENT II: AGENT DEFINITION ---
        if directive == "agent":
            return self._conduct_agent_definition(lines, i, raw_line)

        # --- MOVEMENT III: ORPHAN GUARD ---
        if directive == "endagent":
            # Should be consumed by the block reader, so this is an orphan.
            return i + 1

        return i + 1

    def _conduct_agent_definition(self, lines: List[str], i: int, raw_line: str) -> int:
        """
        [THE RITE OF PERSONA FORGING]
        Parses @agent <name>, consumes the prompt body, and weaves in metadata.
        """
        # 1. PARSE IDENTITY
        match = re.match(r'^@agent\s+(?P<name>[\w\-]+)\s*:?', raw_line)
        if not match:
            raise ArtisanHeresy(
                "Malformed @agent syntax.",
                details=f"Line: {raw_line}",
                line_num=i + 1
            )

        agent_name = match.group('name')

        # 2. CONSUME COGNITIVE BODY (THE PROMPT)
        block_lines, next_i = self._consume_block(lines, i + 1, "@endagent")

        # 3. INHALE DECORATORS
        meta = getattr(self.parser, '_pending_agent_meta', {}).copy()
        if hasattr(self.parser, '_pending_agent_meta'):
            self.parser._pending_agent_meta.clear()

        # 4. INHALE INLINE DIRECTIVES (Optional support for defining tools inside the block)
        # We scan the block lines for @system, @goal lines to extract them from body if present
        cleaned_body = []
        for line in block_lines:
            stripped = line.strip()
            if stripped.startswith('@system '):
                meta['system'] = stripped.replace('@system ', '', 1).strip()
            elif stripped.startswith('@goal '):
                meta['goal'] = stripped.replace('@goal ', '', 1).strip()
            elif stripped.startswith('@tools '):
                meta['tools'] = stripped.replace('@tools ', '', 1).strip()
            else:
                cleaned_body.append(line)

        # 5. REGISTER PERSONA
        # In a full system, this would register with an AgentManager.
        # For now, we store it in the parser's memory for the Execution engine to find.
        if not hasattr(self.parser, 'agents'):
            self.parser.agents = {}

        # Parse tools string into list
        tools_raw = meta.get("tools", "")
        tools_list = [t.strip() for t in tools_raw.split(',')] if tools_raw else []

        # Validate Tool Existence (Prophecy Check)
        # We check if the requested tools exist in the system's registry
        # (This is a soft check, logging warnings if unknown)
        self._validate_tools(tools_list, i + 1)

        self.parser.agents[agent_name] = {
            "identity": agent_name,
            "constitution": meta.get("system", "You are a helpful Gnostic Architect."),
            "limbs": tools_list,
            "mission_success": meta.get("goal"),
            "initial_thought": "\n".join(cleaned_body),
            "trace_id": getattr(self.parser, 'trace_id', 'void'),
            "model_preference": meta.get("model", "smart")  # Future expansion
        }

        self.Logger.success(
            f"L{i + 1}: Neural Agent '{agent_name}' manifest. "
            f"Tools: {len(tools_list)} | Goal: {'Defined' if meta.get('goal') else 'Open'}"
        )
        return next_i

    def _validate_tools(self, tools: List[str], line_num: int):
        """[ASCENSION 25]: AGENTIC HANDSHAKE."""
        # This function would ideally consult a ToolRegistry.
        # For now, we just perform basic sanity checks on the tool names.
        for tool in tools:
            if not re.match(r'^[\w\-\.]+$', tool):
                self.Logger.warn(f"L{line_num}: Agent tool '{tool}' has invalid naming syntax.")