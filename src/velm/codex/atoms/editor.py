from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("editor")
class EditorDomain(BaseDirectiveDomain):
    """
    The Master of the Environment. Configures VS Code for immediate productivity.
    """

    @property
    def namespace(self) -> str:
        return "editor"

    def help(self) -> str:
        return "Generates VS Code configuration (launch, tasks, extensions) for the generated stack."

    def _directive_launch(self, context: Dict[str, Any], stack: str = "python", port: int = 8000, *args,
                          **kwargs) -> str:
        """
        @editor/launch(stack="python-fastapi", port=8000)
        Generates a .vscode/launch.json for debugging.
        """
        configurations = []

        if "python" in stack:
            configurations.append(f"""
            {{
                "name": "Debug FastAPI",
                "type": "python",
                "request": "launch",
                "module": "uvicorn",
                "args": ["src.main:app", "--reload", "--port", "{port}"],
                "jinja": true,
                "justMyCode": true
            }}""")

        if "node" in stack or "react" in stack:
            configurations.append(f"""
            {{
                "name": "Debug Chrome",
                "type": "chrome",
                "request": "launch",
                "url": "http://localhost:{port}",
                "webRoot": "${{workspaceFolder}}/src"
            }}""")
            configurations.append(f"""
            {{
                "name": "Debug Server",
                "type": "node",
                "request": "launch",
                "program": "${{workspaceFolder}}/server.js",
                "skipFiles": ["<node_internals>/**"]
            }}""")

        config_body = ",\n".join(configurations)
        return dedent(f"""
            {{
                "version": "0.2.0",
                "configurations": [
                    {config_body}
                ]
            }}
        """).strip()

    def _directive_extensions(self, context: Dict[str, Any], stack: str = "python", *args, **kwargs) -> str:
        """
        @editor/extensions(stack="python,react")
        Generates .vscode/extensions.json recommendations.
        """
        recs = []
        if "python" in stack:
            recs.extend(["ms-python.python", "charliermarsh.ruff"])
        if "react" in stack or "node" in stack:
            recs.extend(["dbaeumer.vscode-eslint", "esbenp.prettier-vscode"])
        if "docker" in stack:
            recs.append("ms-azuretools.vscode-docker")

        # Always recommend Scaffold!
        recs.append("scaffold.scaffold-vscode")

        # Format as JSON string list
        json_list = '",\n        "'.join(recs)

        return dedent(f"""
            {{
                "recommendations": [
                    "{json_list}"
                ]
            }}
        """).strip()

    def _directive_tasks(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        @editor/tasks
        Generates .vscode/tasks.json for common rites.
        """
        return dedent("""
            {
                "version": "2.0.0",
                "tasks": [
                    {
                        "label": "Run Dev Server",
                        "type": "shell",
                        "command": "make dev",
                        "group": {
                            "kind": "build",
                            "isDefault": true
                        },
                        "presentation": {
                            "reveal": "always",
                            "panel": "new"
                        }
                    },
                    {
                        "label": "Lint Project",
                        "type": "shell",
                        "command": "make lint",
                        "problemMatcher": []
                    }
                ]
            }
        """).strip()