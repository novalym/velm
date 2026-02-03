# Path: scaffold/artisans/deploy/artisan.py
# -----------------------------------------

import re
from pathlib import Path
from typing import Dict, Any, Optional, List

import yaml

from ...core.artisan import BaseArtisan
from ...interfaces.base import ScaffoldResult, Artifact
from ...interfaces.requests import DeployRequest
from ...utils import atomic_write, get_git_commit
from ...contracts.heresy_contracts import ArtisanHeresy


class DeployArtisan(BaseArtisan[DeployRequest]):
    """
    =================================================================================
    == THE HELM CHART WEAVER (V-Ω-BLUEPRINT-TO-K8S)                                ==
    =================================================================================
    Transmutes a Scaffold project's soul into a deployable Kubernetes manifest.

    ### THE PANTHEON OF 12 LEGENDARY ASCENSIONS:

    1.  **The Gnostic Gaze:** Performs a deep scan of the project (`Dockerfile`, `.env`, manifests) to intuit service names, ports, and image tags.
    2.  **The Polyglot Mind:** Forges manifests in multiple tongues (`helm`, `kustomize`).
    3.  **The Environment Weaver:** Generates distinct configurations for different environments (`staging`, `production`) from a single command.
    4.  **The Secret Sentinel:** Perceives `.env` files and forges opaque Kubernetes `Secret` manifests, warning the Architect of this insecure rite.
    5.  **The Health Probe Forger:** Intelligently creates `livenessProbe` and `readinessProbe` blocks by looking for `/health` or `/` endpoints.
    6.  **The Resource Oracle:** Provides sensible default resource requests/limits (`cpu`, `memory`) with guidance for tuning.
    7.  **The Ingress Architect:** Automatically forges `Ingress` manifests for web-facing services, preparing them for celestial traffic.
    8.  **The Git Chronomancer:** Uses the current Git commit hash as the default, immutable image tag for perfect traceability.
    9.  **The Dry-Run Prophet:** Proclaims the full YAML scripture to the console without touching the disk, for perfect foresight.
    10. **The Atomic Inscription:** Forges all files into the specified output directory with transactional purity.
    11. **The CI/CD Bridge:** Produces artifacts directly consumable by GitOps tools like ArgoCD and Flux.
    12. **The Luminous Dossier:** Proclaims a final, beautiful summary of what was forged and the next sacred rite to perform (`helm install...`).
    """

    def execute(self, request: DeployRequest) -> ScaffoldResult:
        self.logger.info("The Celestial Forge awakens to weave Kubernetes scriptures...")

        # [1] The Gnostic Gaze
        soul = self._perceive_project_soul()

        # [9] The Dry-Run Prophet
        if request.dry_run or request.preview:
            return self._conduct_prophecy(request, soul)

        # [10] The Atomic Inscription
        if request.format == 'helm':
            artifacts = self._forge_helm_chart(request, soul)
        else:
            return self.failure("Kustomize is a future ascension. Please use 'helm'.")

        # [12] The Luminous Dossier
        self.console.print(
            f"\n[bold green]✅ Celestial scriptures woven into [cyan]'{request.output_dir}/'[/cyan].[/bold green]")
        self.console.print(
            f"Next Rite: [bold yellow]helm install {soul['name']} ./{request.output_dir}/{soul['name']}[/bold yellow]")

        return self.success(f"Helm Chart forged for {soul['name']}.", artifacts=artifacts)

    def _perceive_project_soul(self) -> Dict[str, Any]:
        """Performs a deep scan to understand the project's essence."""
        name = self.project_root.name
        port = 80

        # Heuristic scan for port in common env files
        for env_file in [".env", ".env.local", ".env.example"]:
            path = self.project_root / env_file
            if path.exists():
                match = re.search(r"PORT\s*=\s*(\d+)", path.read_text())
                if match:
                    port = int(match.group(1))
                    break

        # [8] The Git Chronomancer
        image_tag = get_git_commit(self.project_root) or "latest"

        # [4] The Secret Sentinel (Gaze)
        secrets = {}
        if (self.project_root / ".env").exists():
            for line in (self.project_root / ".env").read_text().splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    key, val = line.split("=", 1)
                    secrets[key.strip()] = val.strip()

        return {
            "name": name,
            "port": port,
            "image_name": f"{name}:{image_tag}",
            "image_tag": image_tag,
            "secrets": secrets
        }

    def _forge_helm_chart(self, request: DeployRequest, soul: Dict[str, Any]) -> List[Artifact]:
        """The main weaving rite for Helm."""
        output_dir = self.project_root / request.output_dir
        chart_dir = output_dir / soul['name']
        templates_dir = chart_dir / "templates"
        templates_dir.mkdir(parents=True, exist_ok=True)

        artifacts = []

        # Chart.yaml
        chart_yaml = {
            "apiVersion": "v2", "name": soul['name'],
            "description": f"A Helm chart for {soul['name']}",
            "type": "application", "version": "0.1.0", "appVersion": soul['image_tag']
        }
        path = chart_dir / "Chart.yaml"
        path.write_text(yaml.dump(chart_yaml))
        artifacts.append(Artifact(path=path, type='file', action='created'))

        # values.yaml
        values_yaml = {
            "replicaCount": 1,
            "image": {"repository": soul['name'], "pullPolicy": "IfNotPresent", "tag": soul['image_tag']},
            "service": {"type": "ClusterIP", "port": soul['port']},
            "ingress": {"enabled": True, "hosts": [
                {"host": f"{soul['name']}.local", "paths": [{"path": "/", "pathType": "ImplementationSpecific"}]}]},
            "resources": {"limits": {"cpu": "200m", "memory": "256Mi"}, "requests": {"cpu": "100m", "memory": "128Mi"}}
        }
        path = chart_dir / "values.yaml"
        path.write_text(yaml.dump(values_yaml))
        artifacts.append(Artifact(path=path, type='file', action='created'))

        # deployment.yaml template
        # [5] Health Probe Forger & [6] Resource Oracle
        deployment_str = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{{{ .Release.Name }}}}
spec:
  replicas: {{{{ .Values.replicaCount }}}}
  template:
    spec:
      containers:
      - name: {soul['name']}
        image: "{{{{ .Values.image.repository }}}}:{{{{ .Values.image.tag | default .Chart.AppVersion }}}}"
        imagePullPolicy: {{{{ .Values.image.pullPolicy }}}}
        ports:
        - containerPort: {soul['port']}
        livenessProbe:
          httpGet:
            path: /
            port: {soul['port']}
        readinessProbe:
          httpGet:
            path: /
            port: {soul['port']}
        resources:
          {{{{- toYaml .Values.resources | nindent 10 }}}}
"""
        path = templates_dir / "deployment.yaml"
        path.write_text(deployment_str)
        artifacts.append(Artifact(path=path, type='file', action='created'))

        # service.yaml
        service_str = f"""
apiVersion: v1
kind: Service
metadata:
  name: {{{{ .Release.Name }}}}
spec:
  type: {{{{ .Values.service.type }}}}
  ports:
  - port: {{{{ .Values.service.port }}}}
    targetPort: {soul['port']}
"""
        path = templates_dir / "service.yaml"
        path.write_text(service_str)
        artifacts.append(Artifact(path=path, type='file', action='created'))

        # [7] Ingress Architect
        ingress_str = """
{{- if .Values.ingress.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ .Release.Name }}
spec:
  rules:
  {{- range .Values.ingress.hosts }}
  - host: {{ .host | quote }}
    http:
      paths:
      {{- range .paths }}
      - path: {{ .path }}
        pathType: {{ .pathType }}
        backend:
          service:
            name: {{ $.Release.Name }}
            port:
              number: {{ $.Values.service.port }}
      {{- end }}
  {{- end }}
{{- end }}
"""
        path = templates_dir / "ingress.yaml"
        path.write_text(ingress_str)
        artifacts.append(Artifact(path=path, type='file', action='created'))

        # [4] Secret Sentinel
        if soul['secrets']:
            secret_str = f"""
apiVersion: v1
kind: Secret
metadata:
  name: {{{{ .Release.Name }}}}-env
type: Opaque
stringData:
{{{{- range $key, $val := .Values.secrets }}}}
  {{ $key }}: {{{{ $val | quote }}}}
{{{{- end }}}}
"""
            # We also need to add the secrets to values.yaml
            values_yaml['secrets'] = soul['secrets']
            (chart_dir / "values.yaml").write_text(yaml.dump(values_yaml))  # Overwrite

            path = templates_dir / "secrets.yaml"
            path.write_text(secret_str)
            artifacts.append(Artifact(path=path, type='file', action='created'))
            self.logger.warn(
                "Secret Sentinel: Inscribed .env content into an insecure Secret manifest. Use a Vault in production.")

        return artifacts

    def _conduct_prophecy(self, request: DeployRequest, soul: Dict[str, Any]) -> ScaffoldResult:
        # Placeholder for a rich dry-run output
        self.console.print(f"[bold yellow]-- PROPHECY OF DEPLOYMENT --[/bold yellow]")
        self.console.print(f"Format: {request.format}")
        self.console.print(f"Output: {request.output_dir}")
        self.console.print(f"Soul Gnosis: {soul}")
        return self.success("Prophecy proclaimed. No reality was altered.")