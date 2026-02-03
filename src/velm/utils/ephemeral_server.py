# Path: scaffold/utils/ephemeral_server.py

"""
=================================================================================
== THE EPHEMERAL SERVER OF LUMINOUS REALITIES                                  ==
=================================================================================
This divine artisan awakens a tiny, hyper-intelligent web server for the sole
purpose of serving a single, in-memory scripture to the Architect's browser,
transcending the security wards of the mortal realm (`file:///`).
=================================================================================
"""
import http.server
import socketserver
import webbrowser

from ..logger import Scribe, get_console

Logger = Scribe("EphemeralServer")


def launch_ephemeral_server(content: str, content_type: str = 'image/svg+xml'):
    """The one true rite of the Ephemeral Server."""

    class GnosticHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.send_header("Content-length", str(len(content)))
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_error(404, "Gnosis Not Found")

    # The Gaze for a free port in the cosmos.
    with socketserver.TCPServer(("", 0), GnosticHandler) as httpd:
        port = httpd.server_address[1]
        url = f"http://127.0.0.1:{port}"

        Logger.success(f"The Luminous Canvas has been forged. Gaze upon its soul at:")
        get_console().print(f"  [bold link={url}]{url}[/bold link]")

        # The Rite of Revelation
        webbrowser.open(url)

        console = get_console()
        console.print("\n[dim]The Ephemeral Server is awake. Press [bold]Ctrl+C[/bold] to return it to the void.[/dim]")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            console.print("\n[yellow]Architect's will perceived. The Ephemeral Server returns to the void.[/yellow]")
            httpd.shutdown()