# Path: scaffold/artisans/audit/license_auditor.py
# ------------------------------------------------
import json
import requests
import time
from pathlib import Path
from typing import Dict, List, Optional, Set

try:
    import toml

    TOML_AVAILABLE = True
except ImportError:
    TOML_AVAILABLE = False

from rich.table import Table
from rich.panel import Panel

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult
from ...interfaces.requests import AuditRequest
from ...help_registry import register_artisan
from ...settings.manager import SettingsManager


@register_artisan("audit")
class LicenseAuditorArtisan(BaseArtisan[AuditRequest]):
    """
    =============================================================================
    == THE LICENSE AUDITOR (V-Ω-COVENANT-GUARDIAN)                             ==
    =============================================================================
    LIF: 10,000,000,000

    Scans dependency lockfiles to uncover the legal covenants (licenses) bound to
    the project's soul. Warns of viral or forbidden licenses.
    """

    def execute(self, request: AuditRequest) -> ScaffoldResult:
        if request.audit_target != "licenses":
            return self.failure("Only 'licenses' audit is currently supported.")

        self.logger.info("The Auditor awakens to verify covenants...")

        # Load Policy
        settings = SettingsManager(self.project_root)
        allowed = set(
            settings.get("compliance.allowed_licenses", ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Unlicense"]))
        forbidden = set(settings.get("compliance.forbidden_licenses", ["GPL", "AGPL", "CC-BY-SA"]))

        report = []  # List of dicts: {pkg, version, license, status}

        # 1. Scan Python (Poetry)
        if (self.project_root / "poetry.lock").exists() and TOML_AVAILABLE:
            self._audit_poetry(report)

        # 2. Scan Node (NPM)
        if (self.project_root / "package-lock.json").exists():
            self._audit_npm(report)

        if not report:
            return self.success("No lockfiles found to audit.")

        # 3. Adjudicate
        heresies = []
        table = Table(title="Dependency License Audit", border_style="blue")
        table.add_column("Package", style="cyan")
        table.add_column("Version", style="dim")
        table.add_column("License", style="white")
        table.add_column("Verdict", justify="center")

        for item in report:
            lic = item['license']
            status = "UNKNOWN"
            style = "yellow"

            # Normalize for comparison
            lic_clean = lic.upper()

            # Check against lists (naive substring check for now)
            is_allowed = any(a.upper() in lic_clean for a in allowed)
            is_forbidden = any(f.upper() in lic_clean for f in forbidden)

            if is_forbidden:
                status = "HERESY"
                style = "bold red"
                heresies.append(f"{item['pkg']}: Forbidden License {lic}")
            elif is_allowed:
                status = "PURE"
                style = "green"
            else:
                status = "REVIEW"
                style = "yellow"

            table.add_row(item['pkg'], item['version'], lic, f"[{style}]{status}[/{style}]")

        self.console.print(table)

        if heresies and request.fail_on_heresy:
            return self.failure(f"Audit failed. {len(heresies)} covenant violations found.")

        return self.success(f"Audit complete. {len(report)} packages scanned.")

    def _audit_poetry(self, report: List[Dict]):
        try:
            data = toml.loads((self.project_root / "poetry.lock").read_text(encoding='utf-8'))
            for pkg in data.get("package", []):
                # Poetry usually has license info locally?
                # Sometimes it's missing. We check PyPI if missing?
                # For speed, we check local metadata first.
                # Poetry lock file doesn't always store license.
                # We might need to fetch it from PyPI.

                # Fetch from PyPI
                lic = self._fetch_pypi_license(pkg["name"])
                report.append({"pkg": pkg["name"], "version": pkg["version"], "license": lic})
        except Exception as e:
            self.logger.warn(f"Poetry audit failed: {e}")

    def _audit_npm(self, report: List[Dict]):
        try:
            data = json.loads((self.project_root / "package-lock.json").read_text(encoding='utf-8'))
            # Modern lockfile (v2/v3)
            packages = data.get("packages", {})
            for path, info in packages.items():
                if not path: continue  # Root
                name = path.split("node_modules/")[-1]
                # NPM lockfiles don't store license usually.
                # We need to fetch from registry.
                lic = self._fetch_npm_license(name, info.get("version"))
                report.append({"pkg": name, "version": info.get("version"), "license": lic})
        except Exception as e:
            self.logger.warn(f"NPM audit failed: {e}")

    def _fetch_pypi_license(self, pkg_name: str) -> str:
        # Cache this in a real impl
        try:
            r = requests.get(f"https://pypi.org/pypi/{pkg_name}/json", timeout=1)
            if r.status_code == 200:
                return r.json().get("info", {}).get("license", "Unknown")
        except:
            pass
        return "Unknown"

    def _fetch_npm_license(self, pkg_name: str, version: str) -> str:
        # Cache this
        try:
            # NPM registry: https://registry.npmjs.org/package
            # We get latest usually, or specific version
            r = requests.get(f"https://registry.npmjs.org/{pkg_name}/{version}", timeout=1)
            if r.status_code == 200:
                data = r.json()
                lic = data.get("license", "Unknown")
                if isinstance(lic, dict): return lic.get("type", "Unknown")
                return lic
        except:
            pass
        return "Unknown"

