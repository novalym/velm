# Path: src/velm/codex/atoms/k8s.py
# ---------------------------------

"""
=================================================================================
== THE ORCHESTRATOR (V-Ω-K8S-DOMAIN)                                           ==
=================================================================================
LIF: 500,000,000,000 | ROLE: CLUSTER_ARCHITECT | RANK: OMEGA_SOVEREIGN

This artisan implements the `@k8s` namespace. It transmutes intent into
verbose, error-prone YAML manifests for Kubernetes.

Usage:
    manifests/deploy.yaml :: {{ k8s.deployment(name="api", image="my-api", replicas=3) }}
    manifests/service.yaml :: {{ k8s.service(name="api", port=80) }}
    manifests/ingress.yaml :: {{ k8s.ingress(host="api.velm.io", service="api") }}
=================================================================================
"""
from textwrap import dedent
from typing import Dict, Any, List, Optional
from ..contract import BaseDirectiveDomain
from ..loader import domain

@domain("k8s")
class KubernetesDomain(BaseDirectiveDomain):
    """The Master of Pods."""

    @property
    def namespace(self) -> str: return "k8s"
    def help(self) -> str: return "Generates Kubernetes manifests (Deploy, Svc, Ingress, HPA)."

    def _directive_deployment(self,
                             context: Dict[str, Any],
                             name: str,
                             image: str,
                             replicas: int = 2,
                             port: int = 8000,
                             env_vars: Dict[str, str] = None) -> str:
        """
        k8s.deployment(name="worker", image="repo/img:tag", replicas=3)
        """
        env_block = ""
        if env_vars:
            props = "\n        ".join([f"- name: {k}\n          value: \"{v}\"" for k, v in env_vars.items()])
            env_block = f"\n        env:\n        {props}"

        return dedent(f"""
            apiVersion: apps/v1
            kind: Deployment
            metadata:
              name: {name}
              labels:
                app: {name}
                managed-by: velm
            spec:
              replicas: {replicas}
              selector:
                matchLabels:
                  app: {name}
              template:
                metadata:
                  labels:
                    app: {name}
                spec:
                  containers:
                  - name: {name}
                    image: {image}
                    ports:
                    - containerPort: {port}{env_block}
                    resources:
                      requests:
                        memory: "128Mi"
                        cpu: "100m"
                      limits:
                        memory: "512Mi"
                        cpu: "500m"
                    livenessProbe:
                      httpGet:
                        path: /health
                        port: {port}
                      initialDelaySeconds: 15
                      periodSeconds: 20
        """).strip()

    def _directive_service(self, context: Dict[str, Any], name: str, port: int = 80, target_port: int = 8000, type: str = "ClusterIP") -> str:
        """k8s.service(name="api", port=80, target_port=8000)"""
        return dedent(f"""
            apiVersion: v1
            kind: Service
            metadata:
              name: {name}
              labels:
                app: {name}
            spec:
              selector:
                app: {name}
              ports:
              - protocol: TCP
                port: {port}
                targetPort: {target_port}
              type: {type}
        """).strip()

    def _directive_ingress(self, context: Dict[str, Any], name: str, host: str, service: str, port: int = 80) -> str:
        """k8s.ingress(name="web", host="app.com", service="frontend")"""
        return dedent(f"""
            apiVersion: networking.k8s.io/v1
            kind: Ingress
            metadata:
              name: {name}
              annotations:
                kubernetes.io/ingress.class: nginx
                cert-manager.io/cluster-issuer: letsencrypt-prod
            spec:
              tls:
              - hosts:
                - {host}
                secretName: {name}-tls
              rules:
              - host: {host}
                http:
                  paths:
                  - path: /
                    pathType: Prefix
                    backend:
                      service:
                        name: {service}
                        port:
                          number: {port}
        """).strip()