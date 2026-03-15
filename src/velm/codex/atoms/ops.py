# Path: src/velm/codex/atoms/ops.py
# ---------------------------------

"""
=================================================================================
== THE GUARDIAN OF PRODUCTION STABILITY: OMEGA POINT (V-Ω-TOTALITY-V100)       ==
=================================================================================
LIF: INFINITY | ROLE: OPERATIONAL_MATERIALIZER | RANK: OMEGA_SOVEREIGN

This artisan implements the `@ops` (or `ops.*`) namespace. It transmutes the
Architect's intent into hardened, observable, and resilient production matter.
=================================================================================
"""
import json
from textwrap import dedent
from typing import Dict, Any, List, Optional, Union
from ..contract import BaseDirectiveDomain
from ..loader import domain
from ...logger import Scribe

Logger = Scribe("OpsArtisan")


@domain("ops")
class OpsDomain(BaseDirectiveDomain):
    """
    The Master of the Substrate Edge.
    """

    @property
    def namespace(self) -> str:
        return "ops"

    def help(self) -> str:
        return "Generates Hardened Nginx, Systemd, Prometheus, and Grafana Gnosis."

    # =========================================================================
    # == STRATUM 0: THE NETWORK APERTURE (NGINX)                            ==
    # =========================================================================

    def _directive_nginx(self,
                         context: Dict[str, Any],
                         domain: str = "example.com",
                         port: int = 8000,
                         ssl: bool = False,
                         harden: bool = True,
                         compression: str = "zstd") -> str:
        """
        ops.nginx(domain="api.velm.io", port=8000, ssl=True)

        [ASCENSION 1]: Generates a high-status, hardened Nginx configuration.
        """
        ssl_block = ""
        listen_ports = "listen 80;"

        if str(ssl).lower() == "true":
            listen_ports = "listen 443 ssl http2;\n    listen [::]:443 ssl http2;"
            ssl_block = dedent(f"""
                # --- SSL CONSECRATION ---
                ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
                ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
                ssl_session_timeout 1d;
                ssl_session_cache shared:MozSSL:10m;
                ssl_session_tickets off;

                # modern configuration
                ssl_protocols TLSv1.3;
                ssl_prefer_server_ciphers off;

                # HSTS (6 months)
                add_header Strict-Transport-Security "max-age=15768000" always;
            """)

        security_headers = ""
        if harden:
            security_headers = dedent("""
                # --- SECURITY SIEVE ---
                add_header X-Frame-Options "DENY";
                add_header X-Content-Type-Options "nosniff";
                add_header X-XSS-Protection "1; mode=block";
                add_header Content-Security-Policy "default-src 'self'; frame-ancestors 'none';";
                add_header Referrer-Policy "strict-origin-when-cross-origin";
            """)

        comp_logic = ""
        if compression == "zstd":
            comp_logic = "zstd on;\n    zstd_types text/plain text/css application/json;"
        elif compression == "gzip":
            comp_logic = "gzip on;\n    gzip_types text/plain text/css application/json;"

        return dedent(f"""
            # === GNOSTIC APERTURE: NGINX VHOST [{domain}] ===
            # Generated via VELM @ops domain

            server {{
                {listen_ports}
                server_name {domain};

                {ssl_block}
                {security_headers}

                access_log /var/log/nginx/{domain}.access.log combined;
                error_log /var/log/nginx/{domain}.error.log warn;

                {comp_logic}

                location / {{
                    proxy_pass http://localhost:{port};
                    proxy_http_version 1.1;
                    proxy_set_header Upgrade $http_upgrade;
                    proxy_set_header Connection 'upgrade';
                    proxy_set_header Host $host;
                    proxy_cache_bypass $http_upgrade;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;

                    # [METABOLIC TUNING]
                    proxy_connect_timeout 60s;
                    proxy_send_timeout 60s;
                    proxy_read_timeout 60s;
                }}

                location /static/ {{
                    alias /var/www/{domain}/static/;
                    expires 30d;
                    add_header Cache-Control "public, no-transform";
                }}
            }}
        """).strip()

    # =========================================================================
    # == STRATUM 1: THE HARDENED UNIT (SYSTEMD)                             ==
    # =========================================================================

    def _directive_systemd(self,
                           context: Dict[str, Any],
                           service: str,
                           user: str = "scaf_artisan",
                           cmd: str = "",
                           memory_limit: str = "512M") -> str:
        """
        ops.systemd(service="api-node", cmd="/usr/bin/python main.py")

        [ASCENSION 2]: Forges a sandboxed Systemd unit file.
        """
        description = f"Gnostic Daemon for {service}"
        work_dir = f"/home/{user}/{service}"

        return dedent(f"""
            [Unit]
            Description={description}
            After=network.target postgresql.service redis.service
            StartLimitIntervalSec=0

            [Service]
            Type=simple
            User={user}
            Group=www-data
            WorkingDirectory={work_dir}
            ExecStart={cmd}
            Restart=always
            RestartSec=5

            # --- METABOLIC GOVERNANCE ---
            MemoryLimit={memory_limit}
            LimitNOFILE=65536

            # --- THE WARD OF LEAST PRIVILEGE ---
            PrivateTmp=true
            ProtectSystem=full
            NoNewPrivileges=true
            PrivateDevices=true
            DeviceAllow=/dev/null rw
            DevicePolicy=closed

            # Environment DNA
            Environment=NODE_ENV=production
            Environment=PYTHONUNBUFFERED=1
            EnvironmentFile=-{work_dir}/.env

            [Install]
            WantedBy=multi-user.target
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE OBSERVABILITY ORACLE (PROMETHEUS)                   ==
    # =========================================================================

    def _directive_prometheus(self,
                              context: Dict[str, Any],
                              targets: str = "localhost:8000",
                              job_name: str = "velm_node") -> str:
        """
        ops.prometheus(targets="app:8000,db:5432")
        """
        target_list = [f"'{t.strip()}'" for t in targets.split(',')]

        return dedent(f"""
            # === GNOSTIC MONITOR: PROMETHEUS SCRAPE ===
            - job_name: '{job_name}'
              scrape_interval: 10s
              metrics_path: '/metrics'
              static_configs:
                - targets: [{', '.join(target_list)}]
                  labels:
                    reality: '{context.get("project_slug", "unknown")}'
                    stratum: 'production'
        """).strip()

    # =========================================================================
    # == STRATUM 3: THE OCULAR HUD (GRAFANA)                                ==
    # =========================================================================

    def _directive_grafana_dashboard(self,
                                     context: Dict[str, Any],
                                     title: str = "System Vitals") -> str:
        """
        ops.grafana_dashboard(title="Core Metabolism")

        [ASCENSION 4]: Generates a raw Grafana JSON dashboard model.
        """
        dashboard = {
            "title": title,
            "uid": f"gnostic-{context.get('project_slug', 'v1')}",
            "panels": [
                {
                    "title": "CPU Metabolism",
                    "type": "timeseries",
                    "targets": [{"expr": "rate(node_cpu_seconds_total[5m])"}]
                },
                {
                    "title": "Memory Mass",
                    "type": "gauge",
                    "targets": [{"expr": "node_memory_Active_bytes"}]
                }
            ],
            "schemaVersion": 36,
            "timezone": "browser"
        }
        return json.dumps(dashboard, indent=2)

    # =========================================================================
    # == STRATUM 4: THE PERIMETER WARD (FIREWALL)                           ==
    # =========================================================================

    def _directive_ufw(self,
                       context: Dict[str, Any],
                       allowed_ports: List[int] = None) -> str:
        """
        ops.ufw(allowed_ports=[80, 443, 8000])
        """
        ports = allowed_ports or [80, 443]
        rules = [f"ufw allow {p}/tcp" for p in ports]

        return dedent(f"""
            #!/bin/bash
            # === GNOSTIC WALL: UFW CONFIGURATION ===
            # Warding ports: {ports}

            ufw --force reset
            ufw default deny incoming
            ufw default allow outgoing

            {chr(10).join(rules)}

            ufw allow ssh
            ufw --force enable
            echo "🛡️  Perimeter secured."
        """).strip()

    # =========================================================================
    # == STRATUM 5: THE INTRUSION SENTINEL (FAIL2BAN)                       ==
    # =========================================================================

    def _directive_fail2ban(self,
                            context: Dict[str, Any],
                            target_log: str = "/var/log/nginx/access.log") -> str:
        """
        ops.fail2ban(target_log="/var/log/app/security.log")
        """
        service_name = context.get("project_slug", "app")

        return dedent(f"""
            # === GNOSTIC SENTINEL: FAIL2BAN JAIL ===
            [{service_name}-warden]
            enabled = true
            port = http,https
            filter = {service_name}-filter
            logpath = {target_log}
            maxretry = 5
            bantime = 3600

            # --- FILTER DEFINITION ---
            # Path: /etc/fail2ban/filter.d/{service_name}-filter.conf
            # [Definition]
            # failregex = ^<HOST> .* "POST /api/v1/auth/login .* 401
            # ignoreregex = 
        """).strip()

    # =========================================================================
    # == STRATUM 6: THE LOG INQUEST (LOKI)                                  ==
    # =========================================================================

    def _directive_promtail(self,
                            context: Dict[str, Any],
                            loki_url: str = "http://loki:3100/loki/api/v1/push") -> str:
        """
        ops.promtail()
        """
        return dedent(f"""
            server:
              http_listen_port: 9080

            positions:
              filename: /tmp/positions.yaml

            clients:
              - url: {loki_url}

            scrape_configs:
              - job_name: system
                static_configs:
                - targets:
                    - localhost
                  labels:
                    job: varlogs
                    __path__: /var/log/*log
        """).strip()

    # =========================================================================
    # == STRATUM 7: THE HEALTH VIGIL (PROBES)                               ==
    # =========================================================================

    def _directive_health_probe(self,
                                context: Dict[str, Any],
                                url: str = "http://localhost:8000/health") -> str:
        """
        ops.health_probe(url="...")
        """
        return dedent(f"""
            #!/bin/bash
            # === GNOSTIC VIGIL: HEALTH PROBE ===

            STATUS=$(curl -s -o /dev/null -w "%{{http_code}}" {url})

            if [ "$STATUS" -eq 200 ]; then
                echo "RESONANT"
                exit 0
            else
                echo "FRACTURED: $STATUS"
                exit 1
            fi
        """).strip()