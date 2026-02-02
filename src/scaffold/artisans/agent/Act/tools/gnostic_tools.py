# Path: artisans/agent/Act/tools/gnostic_tools.py
# -----------------------------------------------

import json
from typing import Optional, Dict

from .base import BaseTool
from .....interfaces.requests import DistillRequest, GraphRequest, RunRequest, WeaveRequest, BlameRequest, \
    InspectRequest
from .....contracts.heresy_contracts import ArtisanHeresy


class ScaffoldDistillTool(BaseTool):
    """
    =============================================================================
    == THE ORACLE OF CONTEXT                                                   ==
    =============================================================================
    The Agent's primary sense organ. It summons the DistillArtisan to transmute a
    chaotic reality into a pure, token-efficient Gnostic blueprint. This is how
    the Agent asks, "What is the nature of this place?" or "Show me everything
    related to the database."
    """
    name: str = "scaffold_distill"
    description: str = "Performs a 'distill' operation to get a high-level summary or deep context of the codebase. This is your primary tool for understanding the project."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "description": "Optional: A natural language plea to guide the distillation (e.g., 'refactor the authentication logic'). This activates a semantic search to find the most relevant files."
            },
            "strategy": {
                "type": "string",
                "description": "The distillation strategy: 'structure' (files only), 'balanced' (default), 'surgical' (highly focused on intent), or 'full' (all content)."
            }
        },
        "required": []
    }

    def execute(self, intent: Optional[str] = None, strategy: str = 'balanced') -> str:
        """Summons the DistillArtisan and returns its scripture."""
        try:
            req = DistillRequest(
                source_path=".",
                strategy=strategy,
                intent=intent,
                silent=True,
                non_interactive=True,
                # Force a small budget to protect the agent's own context window
                token_budget=16000
            )
            result = self.engine.dispatch(req)
            if result.success:
                return result.data.get("blueprint_content", "Distillation complete, but the Gnosis was a void.")
            else:
                return f"Heresy during distillation: {result.message}"
        except Exception as e:
            return f"Catastrophic paradox in Distill tool: {e}"


class ScaffoldInspectTool(BaseTool):
    """
    =============================================================================
    == THE ORACLE OF PROPHECY                                                  ==
    =============================================================================
    The Agent's 'what-if' engine. It allows the Agent to take a blueprint it has
    dreamed of, and ask the God-Engine, "What would happen if I made this real?"
    It reveals creations, modifications, and deletions *before* they occur. This
    is the cornerstone of safe, autonomous planning.
    """
    name: str = "scaffold_inspect"
    description: str = "Takes a blueprint string and returns a simulation of the changes it would make to the filesystem (creates, modifies, deletes). Use this to verify your plan before writing any files."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "blueprint_content": {
                "type": "string",
                "description": "The full, raw content of the .scaffold blueprint to inspect."
            }
        },
        "required": ["blueprint_content"]
    }

    def execute(self, blueprint_content: str) -> str:
        """Summons the InspectArtisan via an ephemeral scripture."""
        import tempfile
        from pathlib import Path

        try:
            # Create a temporary file to hold the blueprint
            with tempfile.NamedTemporaryFile(mode='w+', suffix=".scaffold", delete=False, encoding='utf-8') as tmp_file:
                tmp_file.write(blueprint_content)
                tmp_path = Path(tmp_file.name)

            # Summon the Inspector in JSON mode for machine-readable output
            req = InspectRequest(blueprint_path=str(tmp_path), format="json")

            # Capture stdout, as InspectArtisan prints directly in JSON mode
            import io
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                result = self.engine.dispatch(req)

            output = f.getvalue()

            if not result.success:
                return f"Heresy during inspection: {result.message}"

            # Parse the JSON and create a human-readable summary for the agent
            try:
                data = json.loads(output)
                summary = [
                    "Prophecy of Changes:",
                    f"- Variables: {list(data.get('variables', {}).keys())}",
                    f"- Structure: {len(data.get('structure', []))} items prophesied."
                ]
                # A future ascension could provide a more detailed diff summary here.
                return "\n".join(summary)
            except json.JSONDecodeError:
                return f"Failed to parse inspection result. Raw output: {output[:500]}"

        finally:
            if 'tmp_path' in locals() and tmp_path.exists():
                tmp_path.unlink()


class ScaffoldWeaveTool(BaseTool):
    """The Replicator. Summons entire architectural patterns into existence."""
    name: str = "scaffold_weave"
    description: str = "Weaves a multi-file architectural pattern (Archetype) into a target directory. Use `list_archetypes` to see available patterns."
    args_schema: dict = {
        "type": "object",
        "properties": {
            "archetype_name": {"type": "string",
                               "description": "The sacred name of the archetype to weave (e.g., 'fastapi-resource', 'react-component')."},
            "target_directory": {"type": "string",
                                 "description": "The relative path to the directory where the pattern should be woven."},
            "variables": {"type": "object",
                          "description": "A dictionary of key-value pairs to pass to the archetype (e.g., {'name': 'User'})."}
        },
        "required": ["archetype_name", "target_directory"]
    }

    def execute(self, archetype_name: str, target_directory: str, variables: Optional[Dict] = None) -> str:
        """Summons the WeaveArtisan to conduct the rite of composition."""
        try:
            req = WeaveRequest(
                fragment_name=archetype_name,
                target_directory=target_directory,
                variables=(variables or {}),
                non_interactive=True,
                force=True
            )
            result = self.engine.dispatch(req)
            if result.success:
                return f"Successfully wove the '{archetype_name}' archetype, materializing {len(result.artifacts)} artifacts."
            else:
                return f"Heresy weaving archetype '{archetype_name}': {result.message}"
        except Exception as e:
            return f"Catastrophic paradox in Weave tool: {e}"


class ListArchetypesTool(BaseTool):
    """The Gaze upon the Loom."""
    name: str = "list_archetypes"
    description: str = "Gazes into the Gnostic Forge to perceive all available archetypes that can be used with the `scaffold_weave` tool."
    args_schema: dict = {"type": "object", "properties": {}}

    def execute(self) -> str:
        """Summons the WeaveArtisan's oracle and purifies its output."""
        try:
            req = WeaveRequest(list=True, non_interactive=True)

            import io
            from contextlib import redirect_stdout
            from rich.console import Console

            f = io.StringIO()
            plain_console = Console(file=f, force_terminal=False, no_color=True)
            original_console = self.engine.console
            self.engine.console = plain_console
            try:
                self.engine.dispatch(req)
            finally:
                self.engine.console = original_console

            output = f.getvalue()

            # Extract archetype names from the plain text table for the AI
            lines = [line.strip() for line in output.splitlines() if line.strip()]
            archetypes = [line.split()[0] for line in lines if
                          line and not line.startswith(('┌', '│', '└', '─', 'The'))]
            return f"Available Archetypes: {', '.join(archetypes)}"
        except Exception as e:
            return f"Failed to list archetypes: {e}"


class ScaffoldBlameTool(BaseTool):
    """The Oracle of Causality."""
    name: str = "scaffold_blame"
    description: str = "Performs a deep Gnostic inquest on a file to understand its history, purpose, and dependencies. Use this to understand why a file exists or who is responsible for it."
    args_schema: dict = {
        "type": "object",
        "properties": {"file_path": {"type": "string", "description": "The relative path to the scripture."}},
        "required": ["file_path"]
    }

    def execute(self, file_path: str) -> str:
        """Summons the BlameArtisan and transmutes its Gnosis."""
        import io
        from contextlib import redirect_stdout

        req = BlameRequest(target_path=file_path, json_output=True)
        f = io.StringIO()
        with redirect_stdout(f):
            result = self.engine.dispatch(req)
        output = f.getvalue()

        if not result.success:
            return f"Error conducting inquest on '{file_path}': {result.message}"
        try:
            data = json.loads(output)
            summary = [
                f"Gnostic Dossier for: {data.get('path')}",
                f"  - Status: {data.get('status')}",
                f"  - Last Updated By: {data.get('lineage', {}).get('last_updated', {}).get('architect', 'Unknown')}",
                f"  - Last Rite: {data.get('lineage', {}).get('last_updated', {}).get('name', 'Unknown')}",
                f"  - Dependencies (Imports): {len(data.get('graph', {}).get('dependencies', []))} files",
                f"  - Dependents (Impact): {len(data.get('graph', {}).get('dependents', []))} files"
            ]
            return "\n".join(summary)
        except (json.JSONDecodeError, KeyError) as e:
            return f"Failed to parse the Oracle's Gnosis: {e}. Raw output: {output[:500]}"

