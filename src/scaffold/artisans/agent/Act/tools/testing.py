# === [scaffold/artisans/agent/Act/tools/testing.py] - SECTION 1 of 1: A Sample Tool ===
from .base import BaseTool
from .....interfaces.requests import RunRequest


class RunTestsTool(BaseTool):
    name: str = "run_tests"
    description: str = "Executes the project's test suite to verify changes. Returns the stdout and stderr."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Optional: Path to a specific test file to run."
            }
        },
        "required": []
    }

    def execute(self, **kwargs) -> str:
        # We dispatch a `RunRequest` back to the ScaffoldEngine
        # This is dogfooding at its purest.

        target = "pytest"  # Heuristic: find the test command
        # A better implementation would have a tool to "discover_test_command"

        test_path = kwargs.get("path")
        if test_path:
            target = f"{target} {test_path}"

        result = self.engine.dispatch(RunRequest(
            target=target,
            project_root=self.project_root,
            silent=True  # We capture output, not print it
        ))

        if result.success:
            return f"Tests Passed:\n{result.data.get('output', '')}"
        else:
            # We must return the error output so the agent can learn from it
            heresy_details = result.heresies[0].details if result.heresies else "Unknown error."
            return f"Tests Failed:\n{heresy_details}"