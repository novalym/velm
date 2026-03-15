# Path: src/velm/artisans/codex_oracle/artisan.py
# -----------------------------------------------

"""
=================================================================================
== THE CODEX ORACLE (V-Ω-SCHEMA-RADIATOR)                                      ==
=================================================================================
LIF: ∞ | ROLE: VISUAL_UI_BRIDGE | RANK: OMEGA_SOVEREIGN

This artisan bridges the Python Engine to the React Flow UI. It exports the
entire mathematical schema of the Codex, allowing the web frontend to dynamically
render drag-and-drop nodes for every domain without manual frontend hardcoding.
=================================================================================
"""
from typing import Any

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...codex.loader import CodexRegistry
from .requests import CodexOracleRequest


class CodexOracleArtisan(BaseArtisan[CodexOracleRequest]):
    """The Radiant Voice of the Codex Schema."""

    def execute(self, request: CodexOracleRequest) -> ScaffoldResult:
        self.logger.info("Awakening the Codex Oracle for Schema Radiation...")

        try:
            # Wake the Codex and ingest all user plugins and internal domains
            CodexRegistry.awaken()

            # Scry the grand schema
            schema = CodexRegistry.generate_schema()

            return self.success(
                message="Codex Schema radiated successfully.",
                data={
                    "total_domains": len(schema.get("properties", {})),
                    "schema": schema,
                    # Provide an immediate flat map for UI node registries
                    "flat_nodes": self._flatten_for_ui(schema)
                }
            )
        except Exception as e:
            return self.failure(f"The Oracle's Gaze fractured: {e}")

    def _flatten_for_ui(self, schema: dict) -> list:
        """Transmutes the deep JSON schema into a flat array for React Flow node generation."""
        nodes = []
        properties = schema.get("properties", {})

        for domain_name, domain_data in properties.items():
            for rite_name, rite_data in domain_data.get("rites", {}).items():
                node_id = f"{domain_name}.{rite_name}"
                nodes.append({
                    "id": node_id,
                    "domain": domain_name,
                    "name": rite_name,
                    "description": rite_data.get("description", ""),
                    "inputs": rite_data.get("parameters", {}).get("properties", {}),
                    "required": rite_data.get("parameters", {}).get("required", []),
                    "output": "string"
                })
        return nodes