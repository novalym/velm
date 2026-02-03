# artisans/agent/Act/executor.py
from pathlib import Path
from typing import Any, List, Dict
from ..contracts import Plan, Observation
from .tools.base import BaseTool
from .tools.file_system import WriteFileTool, ReadFileTool, ListDirTool
from .tools.testing import RunTestsTool
from .tools.git import GitStatusTool
from ....logger import Scribe

Logger = Scribe("AgentExecutor")


class Executor:
    """
    The Kinetic Arm.
    Executes the tool calls in the Plan.
    """

    def __init__(self, project_root: Path, engine: Any):
        self.registry: Dict[str, BaseTool] = {}

        # Filesystem Tools
        from .tools.file_system import WriteFileTool, ReadFileTool, ListDirTool, MoveFileTool, DeleteFileTool, \
            CreateDirTool
        self._register(WriteFileTool(project_root, engine))
        self._register(ReadFileTool(project_root, engine))
        self._register(ListDirTool(project_root, engine))
        self._register(MoveFileTool(project_root, engine))
        self._register(DeleteFileTool(project_root, engine))
        self._register(CreateDirTool(project_root, engine))

        # Testing Tool
        from .tools.testing import RunTestsTool
        self._register(RunTestsTool(project_root, engine))

        # Git Tools
        from .tools.git import GitStatusTool, GitDiffTool, GitCommitTool
        self._register(GitStatusTool(project_root, engine))
        self._register(GitDiffTool(project_root, engine))
        self._register(GitCommitTool(project_root, engine))

        # Gnostic (Scaffold) Tools
        from .tools.gnostic_tools import ScaffoldDistillTool, ScaffoldGraphTool
        self._register(ScaffoldDistillTool(project_root, engine))
        self._register(ScaffoldGraphTool(project_root, engine))

    def _register(self, tool: BaseTool):
        self.registry[tool.name] = tool

    def execute_plan(self, plan: Plan) -> List[Observation]:
        observations = []
        Logger.info(f"Agent Thought: {plan.thought}")

        for call in plan.tool_calls:
            tool = self.registry.get(call.tool_name)
            if not tool:
                obs = Observation(
                    tool_name=call.tool_name,
                    tool_input=call.arguments,
                    output=f"Error: Tool '{call.tool_name}' not found.",
                    status="FAILURE"
                )
            else:
                try:
                    Logger.info(f"  >> Invoking {tool.name}...")
                    output = tool.execute(**call.arguments)
                    obs = Observation(
                        tool_name=call.tool_name,
                        tool_input=call.arguments,
                        output=str(output),
                        status="SUCCESS"
                    )
                except Exception as e:
                    obs = Observation(
                        tool_name=call.tool_name,
                        tool_input=call.arguments,
                        output=f"Tool Execution Error: {e}",
                        status="FAILURE"
                    )
            observations.append(obs)

        return observations