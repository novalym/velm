from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("diagram")
class DiagramDomain(BaseDirectiveDomain):
    """
    The Illustrator of Systems.
    """

    @property
    def namespace(self) -> str:
        return "diagram"

    def help(self) -> str:
        return "Generates Mermaid.js diagrams (sequence, erd, flow) for documentation."

    def _directive_sequence(self, context: Dict[str, Any], flow: str, title: str = "System Flow", *args,
                            **kwargs) -> str:
        """
        @diagram/sequence(title="Login Flow", flow="User->API:Login;API->DB:Check;DB-->API:OK;API-->User:Token")
        Generates a Sequence Diagram.
        """
        # Parse the simple flow syntax: A->B:Message; B-->A:Response
        steps = flow.split(';')
        mermaid_lines = []
        for step in steps:
            mermaid_lines.append(step.strip())

        body = "\n    ".join(mermaid_lines)

        return dedent(f"""
            ```mermaid
            sequenceDiagram
                autonumber
                title {title}
                {body}
            ```
        """).strip()

    def _directive_erd(self, context: Dict[str, Any], entities: str, *args, **kwargs) -> str:
        """
        @diagram/erd(entities="User:id,email;Post:id,user_id,title")
        Generates a simple Entity Relationship Diagram.
        """
        # Parse: Entity:field,field;Entity2:field
        mermaid_lines = []
        definitions = entities.split(';')

        for definition in definitions:
            if ':' in definition:
                name, fields = definition.split(':', 1)
                mermaid_lines.append(f"{name.strip()} {{")
                for field in fields.split(','):
                    mermaid_lines.append(f"    string {field.strip()}")
                mermaid_lines.append("}")

        # Simple heuristic for relationships (if id names match)
        # Future ascension: Explicit relationship syntax

        body = "\n    ".join(mermaid_lines)

        return dedent(f"""
            ```mermaid
            erDiagram
                {body}
            ```
        """).strip()

    def _directive_graph(self, context: Dict[str, Any], direction: str = "TD", nodes: str = "", *args, **kwargs) -> str:
        """
        @diagram/graph(nodes="A[Client] --> B(Server); B --> C{Database}")
        Generates a Flowchart.
        """
        # Clean up the semi-colons for newlines
        clean_nodes = nodes.replace(';', '\n    ')

        return dedent(f"""
            ```mermaid
            graph {direction}
                {clean_nodes}
            ```
        """).strip()