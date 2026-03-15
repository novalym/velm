# scaffold/semantic_injection/directives/ui_knowledge/html_ui/html_forge.py

from textwrap import dedent
from typing import List, Tuple

from ..registry import ComponentRegistry


@ComponentRegistry.register("html-card")
def forge_html_card(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Glassmorphism Card (HTML).
    Usage: index.html :: @ui/component(name="html-card", props="title:Vision, text:The future is code.")
    """
    config = {k: v for k, v in props}
    title = config.get("title", "Gnostic Card")
    text = config.get("text", "Content goes here.")

    # We utilize the class 'glass-card' defined in your gnostic_html_kit
    return dedent(f"""
        <div class="glass-card">
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
    """).strip()


@ComponentRegistry.register("html-navbar")
def forge_html_navbar(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Responsive Navbar (HTML).
    Usage: index.html :: @ui/component(name="html-navbar", props="brand:Scaffold")
    """
    config = {k: v for k, v in props}
    brand = config.get("brand", "SCAFFOLD")

    return dedent(f"""
        <nav class="navbar">
            <a href="#" class="logo">{brand}</a>
            <ul class="nav-links">
                <li><a href="#">Docs</a></li>
                <li><a href="#">Forge</a></li>
                <li><a href="#">Login</a></li>
            </ul>
            <button class="btn btn-primary btn-sm">Connect</button>
        </nav>
    """).strip()


@ComponentRegistry.register("html-hero")
def forge_html_hero(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a Hero Section.
    Usage: index.html :: @ui/component(name="html-hero", props="headline:Welcome, sub:Weave your reality.")
    """
    config = {k: v for k, v in props}
    headline = config.get("headline", "Forge Your Destiny")
    sub = config.get("sub", "The Scaffold engine awaits your command.")

    return dedent(f"""
        <section class="hero">
            <h1>{headline}</h1>
            <p>{sub}</p>
            <div style="display: flex; gap: 1rem; justify-content: center;">
                <button class="btn btn-primary">Get Started</button>
                <button class="btn btn-outline">Learn More</button>
            </div>
        </section>
    """).strip()


@ComponentRegistry.register("html-skeleton")
def forge_html_skeleton(name: str, props: List[Tuple[str, str]]) -> str:
    """
    Forges a full HTML5 Boilerplate with Gnostic UI Kit integration.
    Usage: index.html :: @ui/component(name="html-skeleton", props="title:My App")
    """
    config = {k: v for k, v in props}
    title = config.get("title", "Gnostic App")

    return dedent(f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
            <!-- Gnostic UI Kit Connection -->
            <link rel="stylesheet" href="src/css/variables.css">
        </head>
        <body>
            <!-- Navigation -->
            <nav class="navbar">
                <a href="#" class="logo">{title}</a>
            </nav>

            <!-- Main Content -->
            <main style="max-width: 1200px; margin: 0 auto;">
                <!-- Inject components here -->
                @ui/component(name="html-hero", props="headline:Hello World")
            </main>
        </body>
        </html>
    """).strip()