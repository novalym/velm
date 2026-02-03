# Path: core/daemon/surveyor/sentinels/infra.py
# ---------------------------------------------
import re
from pathlib import Path
from typing import List, Dict
from .base import BaseSentinel
from ..constants import SEVERITY_WARNING, SEVERITY_INFO, SEVERITY_ERROR, CODE_SECURITY, CODE_BEST_PRACTICE


class InfraSentinel(BaseSentinel):
    """
    [THE CONTAINER VESSEL]
    Analyzes Infrastructure as Code (Docker, Compose).
    """

    def analyze(self, content: str, file_path: Path, root_path: Path) -> List[Dict]:
        if file_path.name == 'Dockerfile' or file_path.name.endswith('.Dockerfile'):
            return self._analyze_dockerfile(content, file_path)
        return []

    def _analyze_dockerfile(self, content: str, file_path: Path) -> List[Dict]:
        diagnostics = []
        lines = content.split('\n')

        has_user = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'): continue

            # 1. LATEST TAG
            if re.search(r'^FROM\s+[^:]+:latest', stripped, re.IGNORECASE):
                diagnostics.append(self.forge_diagnostic(
                    i, "Base image uses ':latest' tag. Pin to a specific version for reproducibility.",
                    SEVERITY_WARNING, "Docker Sentinel", CODE_BEST_PRACTICE
                ))

            # 2. ROOT USER CHECK
            if stripped.startswith('USER'):
                has_user = True

            # 3. ADD VS COPY
            if stripped.startswith('ADD') and 'tar' not in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Prefer 'COPY' over 'ADD' unless extracting tarballs.",
                    SEVERITY_INFO, "Docker Sentinel", CODE_BEST_PRACTICE
                ))

            # 4. SUDO USAGE
            if 'sudo' in stripped:
                diagnostics.append(self.forge_diagnostic(
                    i, "Avoid 'sudo' in Dockerfiles. User privileges should be handled by USER directive.",
                    SEVERITY_WARNING, "Docker Sentinel", CODE_SECURITY
                ))

        if not has_user:
            diagnostics.append(self.forge_diagnostic(
                len(lines) - 1, "No USER directive found. Container may run as root.",
                SEVERITY_WARNING, "Docker Sentinel", CODE_SECURITY
            ))

        return diagnostics