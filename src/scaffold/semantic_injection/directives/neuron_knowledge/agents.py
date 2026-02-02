# scaffold/semantic_injection/directives/neuron_knowledge/agents.py

"""
=================================================================================
== THE AGENTIC FOUNDRY (V-Ω-SINGULARITY)                                       ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000

This artisan generates state-of-the-art Cognitive Architectures.
It supports:
1. Structured Extraction (Instructor / OpenAI Native)
2. LangGraph Workflows (State, Nodes, Edges, Persistence)
3. Swarm Agents (Handoff Patterns)
4. Tool Definitions (Pydantic Schemas)

Usage:
    @neuron/structure(...)
    @neuron/crew(...) -> Now routed to specific architectures
    @neuron/graph(...)
=================================================================================
"""
from contextlib import contextmanager
from typing import List, Dict, Set


# =============================================================================
# == THE GNOSTIC CODE BUILDER (STANDARD)                                     ==
# =============================================================================

class GnosticCodeBuilder:
    """Stateful engine for atomic indentation and import management."""
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
            self.add("")

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
# == THE TYPE ALCHEMIST 2.0                                                  ==
# =============================================================================

def _parse_complex_type(raw_type: str, cb: GnosticCodeBuilder) -> str:
    """
    Transmutes complex type strings into valid Python types and registers imports.
    Handles: Literal['a','b'], List[str], Optional[int], custom types.
    """
    t = raw_type.strip()

    # Handle Literal['a', 'b']
    if t.lower().startswith('literal['):
        cb.add_from_import("typing", "Literal")
        return t # Pass through as is (assuming valid python syntax inside)

    # Handle List[...]
    if t.lower().startswith('list['):
        cb.add_from_import("typing", "List")
        return t

    # Handle Optional[...]
    if t.lower().startswith('optional['):
        cb.add_from_import("typing", "Optional")
        return t

    # Basic Types
    mapping = {
        'string': 'str', 'text': 'str', 'str': 'str',
        'int': 'int', 'integer': 'int',
        'float': 'float', 'number': 'float',
        'bool': 'bool', 'boolean': 'bool',
        'dict': 'Dict[str, Any]', 'object': 'Dict[str, Any]',
        'any': 'Any'
    }

    if t.lower() in mapping:
        if 'Dict' in mapping[t.lower()]:
            cb.add_from_import("typing", "Dict")
            cb.add_from_import("typing", "Any")
        if 'Any' in mapping[t.lower()]:
            cb.add_from_import("typing", "Any")
        return mapping[t.lower()]

    return t # Return raw (e.g. custom class name)

# =============================================================================
# == 1. THE STRUCTURED EXTRACTOR (OpenAI Native & Instructor)                ==
# =============================================================================

def forge_structured_extractor(
    model_name: str = "Extraction",
    fields: str = "summary:str, sentiment:Literal['pos','neg']",
    backend: str = "openai_native", # or 'instructor'
    async_mode: bool = False
) -> str:
    """
    Forges a type-safe data extraction pipeline.
    """
    cb = GnosticCodeBuilder()
    cb.add_metadata("requirements", "openai, pydantic" if backend == "openai_native" else "openai, pydantic, instructor")

    cb.add_from_import("pydantic", "BaseModel")
    cb.add_from_import("pydantic", "Field")
    cb.add_import("os")

    # --- Define the Model ---
    with cb.block(f"class {model_name}(BaseModel):"):
        cb.add(f'"""Structured output schema for {model_name}."""')

        field_list = fields.split(',')
        for f in field_list:
            if ':' not in f: continue
            name, raw_type = f.split(':', 1)
            py_type = _parse_complex_type(raw_type, cb)

            # [ELEVATION 6] The Validation Citadel (Regex Hints)
            if "email" in name.lower():
                cb.add_from_import("pydantic", "EmailStr") # Assume pydantic[email] is installed or suggest it
                # Or simple regex
                cb.add(f"{name.strip()}: {py_type} = Field(..., description='The email address')")
            else:
                cb.add(f"{name.strip()}: {py_type} = Field(..., description='Extracted {name.strip()}')")

    # --- Define the Extraction Logic ---
    func_prefix = "async def" if async_mode else "def"
    await_kw = "await " if async_mode else ""

    cb.add("")
    with cb.block(f"{func_prefix} extract_{model_name.lower()}(content: str) -> {model_name}:"):

        # Client Setup (Lazy Loading for Safety)
        if backend == "openai_native":
            cls = "AsyncOpenAI" if async_mode else "OpenAI"
            cb.add_from_import("openai", cls)
            cb.add(f"client = {cls}(api_key=os.getenv('OPENAI_API_KEY'))")

            cb.add("")
            cb.add("# [ELEVATION 3] Native Structured Output (2024)")
            cb.add(f"completion = {await_kw}client.beta.chat.completions.parse(")
            cb.add("    model='gpt-4o-2024-08-06',")
            cb.add("    messages=[")
            cb.add("        {'role': 'system', 'content': 'Extract the requested data structure.'},")
            cb.add("        {'role': 'user', 'content': content}")
            cb.add("    ],")
            cb.add(f"    response_format={model_name}")
            cb.add(")")
            cb.add("return completion.choices[0].message.parsed")

        elif backend == "instructor":
            cb.add_import("instructor")
            cls = "AsyncOpenAI" if async_mode else "OpenAI"
            cb.add_from_import("openai", cls)

            cb.add(f"client = instructor.patch({cls}(api_key=os.getenv('OPENAI_API_KEY')))")

            cb.add("")
            cb.add("# [ELEVATION] Instructor Enhanced Extraction")
            cb.add(f"return {await_kw}client.chat.completions.create(")
            cb.add("    model='gpt-3.5-turbo',")
            cb.add(f"    response_model={model_name},")
            cb.add("    messages=[{'role': 'user', 'content': content}]")
            cb.add(")")

    # --- Main Guard ---
    cb.add("")
    with cb.block('if __name__ == "__main__":'):
        if async_mode:
            cb.add("import asyncio")
            cb.add(f"result = asyncio.run(extract_{model_name.lower()}('Test content for extraction'))")
        else:
            cb.add(f"result = extract_{model_name.lower()}('Test content for extraction')")
        cb.add("print(result.model_dump_json(indent=2))")

    return cb.render()


# =============================================================================
# == 2. THE LANGGRAPH ARCHITECT (Flow Engineering)                           ==
# =============================================================================

def forge_langgraph_workflow(
    graph_name: str = "ResearchGraph",
    nodes: str = "Researcher, Writer, Reviewer",
    state_schema: str = "topic:str, feedback:str, final_report:str",
    use_memory: bool = True
) -> str:
    """
    [ELEVATION 1] The LangGraph Architect.
    Constructs a cyclic, stateful cognitive graph.
    """
    cb = GnosticCodeBuilder()
    cb.add_metadata("requirements", "langgraph, langchain_openai, langchain_core")

    cb.add_from_import("typing", "TypedDict")
    cb.add_from_import("typing", "Annotated")
    cb.add_from_import("typing", "List")
    cb.add_from_import("typing", "Dict")
    cb.add_from_import("typing", "Any")

    cb.add_from_import("langgraph.graph", "StateGraph")
    cb.add_from_import("langgraph.graph", "END")
    cb.add_from_import("langgraph.graph", "START")

    if use_memory:
        cb.add_from_import("langgraph.checkpoint.memory", "MemorySaver")

    cb.add_import("os")

    # --- 1. Define State ---
    cb.add("")
    with cb.block("class AgentState(TypedDict):"):
        for f in state_schema.split(','):
            if ':' in f:
                n, t = f.split(':')
                py_type = _parse_complex_type(t, cb)
                cb.add(f"{n.strip()}: {py_type}")
        # Always add messages
        cb.add_from_import("langchain_core.messages", "BaseMessage")
        cb.add("messages: List[BaseMessage]")

    # --- 2. Define Node Functions ---
    node_list = [n.strip() for n in nodes.split(',') if n.strip()]

    for node in node_list:
        func_name = f"{node.lower()}_node"
        cb.add("")
        with cb.block(f"def {func_name}(state: AgentState):"):
            cb.add(f'"""Role: {node}. Logic for this step."""')
            cb.add(f"print(f'--- {node.upper()} WORKING ---')")
            cb.add("# [TODO] Inject LLM logic here")

            # Simple state mutation mock
            if node == node_list[-1]:
                cb.add(f"return {{'final_report': 'Finished by {node}'}}")
            else:
                cb.add(f"return {{'messages': [f'Message from {node}']}}")

    # --- 3. Build Graph ---
    cb.add("")
    with cb.block(f"def build_{graph_name.lower()}():"):
        cb.add("builder = StateGraph(AgentState)")

        # Add Nodes
        for node in node_list:
            cb.add(f"builder.add_node('{node}', {node.lower()}_node)")

        # Add Edges (Sequential Default)
        cb.add("")
        cb.add("# Flow: START -> " + " -> ".join(node_list) + " -> END")
        cb.add(f"builder.add_edge(START, '{node_list[0]}')")

        for i in range(len(node_list) - 1):
            cb.add(f"builder.add_edge('{node_list[i]}', '{node_list[i+1]}')")

        cb.add(f"builder.add_edge('{node_list[-1]}', END)")

        # [ELEVATION 14] Memory Persistence
        if use_memory:
            cb.add("")
            cb.add("checkpointer = MemorySaver()")
            cb.add("return builder.compile(checkpointer=checkpointer)")
        else:
            cb.add("return builder.compile()")

    # --- 4. Visualization & Execution ---
    cb.add("")
    with cb.block('if __name__ == "__main__":'):
        cb.add("app = build_researchgraph()")

        # [ELEVATION 15] Visualization Hook
        cb.add("# Generate Mermaid Graph (Optional)")
        cb.add("# print(app.get_graph().draw_mermaid())")

        cb.add("")
        cb.add("print('⚡ Igniting Graph...')")
        cb.add("initial_state = {'messages': [], 'topic': 'Quantum Computing'}")
        cb.add("config = {'configurable': {'thread_id': '1'}}")

        cb.add("")
        with cb.block("for output in app.stream(initial_state, config):"):
            with cb.block("for key, value in output.items():"):
                cb.add("print(f'Node {key}: Done')")

    return cb.render()

# =============================================================================
# == 3. THE TOOL FABRICATOR (Pydantic Schemas)                               ==
# =============================================================================

def forge_tool_definition(
    tool_name: str,
    desc: str,
    args_schema: str = "query:str",
    async_mode: bool = False
) -> str:
    """
    [ELEVATION 8] The Tool Schema Fabricator.
    Generates a LangChain tool with a strictly typed Pydantic schema.
    """
    cb = GnosticCodeBuilder()
    cb.add_metadata("requirements", "langchain, pydantic")

    cb.add_from_import("langchain.tools", "tool")
    cb.add_from_import("pydantic", "BaseModel")
    cb.add_from_import("pydantic", "Field")

    # Schema Class
    schema_name = f"{tool_name}Input"
    with cb.block(f"class {schema_name}(BaseModel):"):
        for f in args_schema.split(','):
            if ':' in f:
                n, t = f.split(':')
                py_type = _parse_complex_type(t, cb)
                cb.add(f"{n.strip()}: {py_type} = Field(..., description='Argument for {n.strip()}')")

    # Tool Function
    func_def = "async def" if async_mode else "def"

    cb.add("")
    cb.add(f"@tool(args_schema={schema_name})")

    args_list = [f.split(':')[0].strip() for f in args_schema.split(',')]
    signature_args = ", ".join(args_list)

    with cb.block(f"{func_def} {tool_name.lower()}_tool({signature_args}) -> str:"):
        cb.add(f'"""{desc}"""')

        # [ELEVATION 12] The Resilient Invoker (Concept)
        cb.add("# [GNOSTIC TODO]: Implement tool logic here")
        cb.add(f"print(f'Tool invoked with: {{ {args_list[0]} }}')")
        cb.add('return "Tool execution successful"')

    return cb.render()

# =============================================================================
# == 4. THE SWARM GENESIS (OpenAI Patterns)                                  ==
# =============================================================================

def forge_swarm_agent(
    agent_name: str = "TriageAgent",
    handoffs: str = "SalesAgent, SupportAgent"
) -> str:
    """
    [ELEVATION 2] The Swarm Protocol.
    Generates an agent structure compatible with the OpenAI Swarm pattern (routine + handoffs).
    """
    cb = GnosticCodeBuilder()
    cb.add_metadata("requirements", "openai, pydantic")

    cb.add_from_import("typing", "Dict")
    cb.add_from_import("typing", "Any")

    # Handoff Functions
    targets = [t.strip() for t in handoffs.split(',') if t.strip()]

    for target in targets:
        func_name = f"transfer_to_{target.lower()}"
        cb.add("")
        with cb.block(f"def {func_name}():"):
            cb.add(f'"""Transfers the conversation to the {target}."""')
            cb.add(f"return {target}")

    # Agent Definition (Pseudo-code for Swarm framework)
    cb.add("")
    cb.add("# Define the Swarm Agent")
    with cb.block(f"{agent_name} = {{"):
        cb.add(f'"name": "{agent_name}",')
        cb.add(f'"model": "gpt-4o",')
        cb.add('"instructions": "You are a triage agent. Route the user based on their intent.",')

        # Bind Tools (Handoffs)
        handoff_funcs = [f"transfer_to_{t.lower()}" for t in targets]
        cb.add(f'"functions": [{", ".join(handoff_funcs)}]')
    cb.add("}")

    return cb.render()