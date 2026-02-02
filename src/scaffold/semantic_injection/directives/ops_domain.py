from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("ops")
class OpsDomain(BaseDirectiveDomain):
    """
    The Guardian of Production Stability.
    """

    @property
    def namespace(self) -> str:
        return "ops"

    def help(self) -> str:
        return "Generates operational config (Nginx, Systemd, Prometheus, Grafana)."

    def _directive_nginx(self, context: Dict[str, Any], domain: str = "example.com", port: int = 8000, ssl: bool = False, *args, **kwargs) -> str:
        """
        @ops/nginx(domain="api.app.com", port=8000, ssl=true)
        Generates a reverse proxy configuration.
        """
        ssl_block = ""
        listen_port = 80
        if str(ssl).lower() == "true":
            listen_port = 443
            ssl_block = dedent(f"""
                ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
                ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
                include /etc/letsencrypt/options-ssl-nginx.conf;
                ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
            """)

        return dedent(f"""
            server {{
                listen {listen_port};
                server_name {domain};

                {ssl_block}

                location / {{
                    proxy_pass http://localhost:{port};
                    proxy_set_header Host $host;
                    proxy_set_header X-Real-IP $remote_addr;
                    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                    proxy_set_header X-Forwarded-Proto $scheme;
                }}

                location /static/ {{
                    alias /var/www/{domain}/static/;
                }}
            }}
        """).strip()

    def _directive_systemd(self, context: Dict[str, Any], service: str, user: str = "ubuntu", cmd: str = "", *args, **kwargs) -> str:
        """
        @ops/systemd(service="gunicorn", cmd="/env/bin/gunicorn main:app")
        Generates a Linux service file.
        """
        return dedent(f"""
            [Unit]
            Description={service} Daemon
            After=network.target

            [Service]
            User={user}
            Group=www-data
            WorkingDirectory=/home/{user}/{service}
            ExecStart={cmd}
            Restart=always

            [Install]
            WantedBy=multi-user.target
        """).strip()

    def _directive_prometheus(self, context: Dict[str, Any], targets: str = "localhost:8000", *args, **kwargs) -> str:
        """
        @ops/prometheus(targets="app:8000,db:5432")
        Generates a prometheus.yml scrape config.
        """
        target_list = [f"'{t}'" for t in targets.split(',')]
        return dedent(f"""
            global:
              scrape_interval: 15s

            scrape_configs:
              - job_name: 'scaffold_app'
                scrape_interval: 5s
                static_configs:
                  - targets: [{', '.join(target_list)}]
        """).strip()