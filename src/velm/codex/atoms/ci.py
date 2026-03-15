# Path: src/velm/codex/atoms/ci.py
# -------------------------------

"""
=================================================================================
== THE PIPELINE WEAVER (V-Ω-CI-DOMAIN)                                         ==
=================================================================================
LIF: 50,000,000,000 | ROLE: AUTOMATION_ARCHITECT

Generates CI/CD configurations. It sutures the VELM CLI directly into the
pipeline for "Sovereign Verification" in the cloud.
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any
from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("ci")
class CIDomain(BaseDirectiveDomain):
    """The Automator of Will."""

    @property
    def namespace(self) -> str: return "ci"

    def help(self) -> str: return "Generates CI/CD pipelines (GitHub Actions, GitLab)."

    def _directive_github_python(self, context: Dict[str, Any], python_version: str = "3.11",
                                 check_security: bool = True) -> str:
        """ci.github_python(check_security=True)"""
        security_step = ""
        if check_security:
            security_step = dedent("""
            - name: Security Scan (Bandit)
              run: pip install bandit && bandit -r src/
            """)

        return dedent(f"""
            name: Python CI

            on: [push, pull_request]

            jobs:
              build:
                runs-on: ubuntu-latest
                steps:
                - uses: actions/checkout@v4
                - name: Set up Python {python_version}
                  uses: actions/setup-python@v4
                  with:
                    python-version: '{python_version}'
                - name: Install dependencies
                  run: |
                    python -m pip install --upgrade pip
                    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                - name: Lint with Ruff
                  run: |
                    pip install ruff
                    ruff check .
                - name: Test with Pytest
                  run: |
                    pip install pytest
                    pytest
                {security_step}
        """).strip()

    def _directive_github_node(self, context: Dict[str, Any], node_version: str = "20") -> str:
        """ci.github_node(node_version="20")"""
        return dedent(f"""
            name: Node.js CI

            on: [push, pull_request]

            jobs:
              build:
                runs-on: ubuntu-latest
                steps:
                - uses: actions/checkout@v4
                - name: Use Node.js {node_version}
                  uses: actions/setup-node@v3
                  with:
                    node-version: '{node_version}'
                    cache: 'npm'
                - run: npm ci
                - run: npm run build --if-present
                - run: npm test
        """).strip()

    def _directive_velm_verify(self, context: Dict[str, Any]) -> str:
        """
        ci.velm_verify()
        The Ultimate CI Step. Runs the God-Engine inside GitHub Actions to
        verify the blueprint integrity.
        """
        return dedent("""
            - name: Velm Architectural Audit
              run: |
                pip install velm-cli
                velm verify --strict
                velm analyze
        """).strip()