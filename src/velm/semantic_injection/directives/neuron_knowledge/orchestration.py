# scaffold/semantic_injection/directives/neuron_knowledge/orchestration.py

"""
=================================================================================
== THE ORCHESTRATOR OF MINDS (V-Ω-CREW-BUILDER)                                ==
=================================================================================
LIF: ∞ (ETERNAL & ABSOLUTE)

This artisan generates the social fabric for Multi-Agent Systems (MAS).
It constructs a complete, production-grade CrewAI architecture with
configurable agents, tasks, tools, and process management.

Usage:
    @neuron/crew(agents="Researcher:Analyze Data,Writer:Create Blog", process="sequential")
=================================================================================
"""
from contextlib import contextmanager
from typing import List, Dict, Set, Tuple


# =============================================================================
# == THE GNOSTIC CODE BUILDER (REUSED FOR CONSISTENCY)                       ==
# =============================================================================

class GnosticCodeBuilder:
    """
    A stateful engine for constructing indented code without string-mashing.
    """

    def __init__(self, indent_char: str = "    "):
        self.lines: List[str] = []
        self.level: int = 0
        self.indent_char: str = indent_char
        self.imports: Set[str] = set()
        self.from_imports: Dict[str, Set[str]] = {}
        self.metadata: List[str] = []

    def add_import(self, module: str):
        self.imports.add(module)

    def add_from_import(self, module: str, name: str):
        if module not in self.from_imports:
            self.from_imports[module] = set()
        self.from_imports[module].add(name)

    def add_metadata(self, key: str, value: str):
        self.metadata.append(f"# {key}: {value}")

    def add(self, line: str = ""):
        if not line:
            self.lines.append("")
        else:
            self.lines.append((self.indent_char * self.level) + line)

    @contextmanager
    def block(self, header: str):
        self.add(header)
        self.level += 1
        try:
            yield
        finally:
            self.level -= 1

    def render(self) -> str:
        output = []
        if self.metadata:
            output.extend(self.metadata)
            output.append("")

        if self.imports:
            output.extend([f"import {m}" for m in sorted(self.imports)])
        if self.from_imports:
            for mod in sorted(self.from_imports.keys()):
                names = ", ".join(sorted(self.from_imports[mod]))
                output.append(f"from {mod} import {names}")

        if self.imports or self.from_imports:
            output.append("")
            output.append("")

        output.extend(self.lines)
        return "\n".join(output).strip()


# =============================================================================
# == THE PARSING LOGIC                                                       ==
# =============================================================================

def _parse_agent_spec(agent_str: str) -> Tuple[str, str]:
    """
    Parses 'Role:Goal' or just 'Role'.
    Returns (RoleName, Goal).
    """
    if ':' in agent_str:
        role, goal = agent_str.split(':', 1)
        return role.strip(), goal.strip()
    return agent_str.strip(), f"Perform expert analysis and execution for {agent_str.strip()} tasks"


# =============================================================================
# == THE FORGE (GENERATION LOGIC)                                            ==
# =============================================================================

def forge_crew_structure(
        agents_csv: str = "Researcher,Writer",
        process: str = "sequential",
        verbose: bool = True,
        llm_provider: str = "openai"
) -> str:
    """
    Forges a complete CrewAI Swarm Architecture.
    """
    cb = GnosticCodeBuilder()

    # --- 1. Configuration & Metadata ---
    cb.add_metadata("requirements", "crewai, langchain_openai, python-dotenv")
    cb.add_metadata("description", f"Multi-Agent Swarm: {agents_csv} ({process})")

    cb.add_import("os")
    cb.add_from_import("crewai", "Agent")
    cb.add_from_import("crewai", "Task")
    cb.add_from_import("crewai", "Crew")
    cb.add_from_import("crewai", "Process")
    cb.add_from_import("langchain_openai", "ChatOpenAI")
    cb.add_from_import("textwrap", "dedent")

    # Parse Agents
    # Input: "Researcher:Analyze trends, Writer"
    raw_agents = [a.strip() for a in agents_csv.split(',') if a.strip()]
    parsed_agents = [_parse_agent_spec(a) for a in raw_agents]

    agent_vars = []
    task_vars = []

    # --- 2. The LLM Factory ---
    cb.add("")
    with cb.block("def _get_llm():"):
        cb.add('"""Constructs the Neural Brain for the agents."""')
        # Default to OpenAI, but structure allows expansion
        cb.add("return ChatOpenAI(")
        cb.add("    model='gpt-4-turbo-preview',")
        cb.add("    temperature=0.7,")
        cb.add("    api_key=os.getenv('OPENAI_API_KEY')")
        cb.add(")")

    # --- 3. The Swarm Constructor ---
    cb.add("")
    with cb.block("def create_swarm() -> Crew:"):
        cb.add('"""Forges the Agents, Tasks, and the Crew."""')
        cb.add("llm = _get_llm()")
        cb.add("")

        # Define Agents
        cb.add("# --- AGENTS ---")
        for role, goal in parsed_agents:
            var_name = role.lower().replace(" ", "_") + "_agent"
            agent_vars.append(var_name)

            # [ELEVATION 7] Delegation Logic
            # Hierarchical processes rely on delegation. Sequential usually implies chains.
            allow_delegation = "True" if process == "hierarchical" else "False"

            with cb.block(f"{var_name} = Agent("):
                cb.add(f"role='{role}',")
                cb.add(f"goal='{goal}',")
                cb.add(f"backstory=dedent('''You are an expert {role}. Your mission is to {goal.lower()}.")
                cb.add(f"You are known for your precision and insight.'''),")
                cb.add(f"verbose={str(verbose)},")
                cb.add(f"allow_delegation={allow_delegation},")
                cb.add("llm=llm,")
                cb.add("# tools=[...], # Inject tools here")
            cb.add(")")
            cb.add("")

        # Define Tasks
        cb.add("# --- TASKS ---")
        for i, (role, _) in enumerate(parsed_agents):
            agent_var = agent_vars[i]
            task_var = role.lower().replace(" ", "_") + "_task"
            task_vars.append(task_var)

            # [ELEVATION 8] Input Interpolation
            description = f"Conduct a comprehensive analysis on {{topic}} from the perspective of a {role}."

            with cb.block(f"{task_var} = Task("):
                cb.add(f"description=dedent('''{description}'''),")
                cb.add("expected_output='A detailed report formatted in markdown.',")
                cb.add(f"agent={agent_var},")

                # [ELEVATION 5] Context Linking (Sequential Logic)
                if i > 0 and process == "sequential":
                    prev_task = task_vars[i - 1]
                    cb.add(f"context=[{prev_task}], # Takes input from previous task")

            cb.add(")")
            cb.add("")

        # Define Crew
        cb.add("# --- CREW ---")
        proc_enum = "Process.hierarchical" if process == "hierarchical" else "Process.sequential"

        with cb.block("crew = Crew("):
            cb.add(f"agents=[{', '.join(agent_vars)}],")
            cb.add(f"tasks=[{', '.join(task_vars)}],")
            cb.add(f"process={proc_enum},")
            cb.add(f"verbose=2 if {verbose} else 0,")
            if process == "hierarchical":
                cb.add("manager_llm=llm,")
            # [ELEVATION 6] Memory Cortex
            cb.add("memory=True, # Enable long-term memory")
        cb.add(")")

        cb.add("return crew")

    # --- 4. Execution Wrapper ---
    cb.add("")
    with cb.block("def run_mission(topic: str):"):
        cb.add('"""Ignites the Swarm."""')
        cb.add("crew = create_swarm()")
        cb.add("print(f'\\n[Swarm] Engaging protocols for topic: {topic}\\n')")
        cb.add("result = crew.kickoff(inputs={'topic': topic})")
        cb.add("return result")

    # --- 5. The Self-Healing Main ---
    cb.add("")
    with cb.block('if __name__ == "__main__":'):
        # [ELEVATION 10] Environment Sentinel
        with cb.block("if not os.getenv('OPENAI_API_KEY'):"):
            cb.add("print('[Error] OPENAI_API_KEY missing. The minds cannot awaken.')")
            cb.add("# os.environ['OPENAI_API_KEY'] = 'sk-...'")
            cb.add("exit(1)")

        cb.add("# Sample Execution")
        cb.add('topic = "The Future of Generative Architecture"')

        with cb.block("try:"):
            cb.add("final_output = run_mission(topic)")
            cb.add("print('\\n[Swarm] Mission Complete. Final Output:\\n')")
            cb.add("print(final_output)")
        with cb.block("except Exception as e:"):
            cb.add("print(f'[Error] The Swarm encountered a paradox: {e}')")

    return cb.render()