"""
=================================================================================
== THE ORACLE OF DESTINY (V-Ω-GOD-ENGINE. THE GNOSTIC PROPHET ASCENDED)          ==
=================================================================================
LIF: 10,000,000,000,000,000,000 (ABSOLUTE PROPHETIC & CONTEXTUAL AUTHORITY)

This is the God-Engine of Gnostic Prophecy in its final, eternal form. Its mind is
no longer a profane script, but a divine, declarative Grimoire of Gnostic Laws.
It gazes upon the manifest reality and the Architect's original will to prophesy
the one true path forward with the profound wisdom of a true AI Mentor.
=================================================================================
"""
import os
from pathlib import Path
from typing import List, Dict, Any, Set, Optional


class NextStepsOracle:
    """The God-Engine of Gnostic Prophecy."""

    def __init__(
        self,
        project_root: Path,
        created_files: Optional[Set[str]] = None,
        *, # The Vow of Gnostic Clarity
        gnosis: Optional[Dict[str, Any]] = None
    ):
        """
        The Rite of Gnostic Inception, forged for eternal compatibility and deep context.
        """
        self.root = project_root
        self.gnosis = gnosis or {}
        self.files = created_files or {p.name for p in self.root.iterdir() if p.exists()}
        self._file_cache: Dict[Path, str] = {} # The Gnostic Chronocache

    def _read_safely(self, path: Path) -> str:
        """The Unbreakable Ward of Grace."""
        if path in self._file_cache: return self._file_cache[path]
        if not path.is_file(): return ""
        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
            self._file_cache[path] = content
            return content
        except Exception:
            return ""

    def prophesy(self) -> List[str]:
        """
        [ELEVATION 9 & 11] The one true rite of prophecy. It is a pure Conductor that
        walks the Grimoire of Gnostic Laws to forge its luminous prophecies.
        """
        steps: List[str] = []

        # ELEVATION 1: The Gnostic Grimoire
        PROPHECY_GRIMOIRE: List[Dict[str, Any]] = [
            # --- MOVEMENT I: NAVIGATION ---
            {
                "predicate": lambda: not self.root.resolve().samefile(Path.cwd().resolve()),
                "proclamation": lambda: f"Enter the sanctum: [bold cyan]cd {os.path.relpath(self.root.resolve(), Path.cwd().resolve())}[/bold cyan]",
            },
            # --- MOVEMENT II: CONFIGURATION ---
            {
                "predicate": lambda: ".env.example" in self.files and not (self.root / ".env").exists(),
                "proclamation": "Configure reality: [bold yellow]cp .env.example .env[/bold yellow] and fill in secrets.",
            },
            # --- MOVEMENT III: DEPENDENCIES (HIERARCHY OF WILL) ---
            {
                "group": "install", "stop_on_success": True, # ELEVATION 5
                "laws": [
                    {
                        "predicate": lambda: "install:" in self._read_safely(self.root / "Makefile"),
                        "proclamation": "Conduct rites: [bold green]make install[/bold green]",
                    },
                    {
                        "predicate": lambda: (self.root / "poetry.lock").exists() or "[tool.poetry]" in self._read_safely(self.root / "pyproject.toml"),
                        "proclamation": "Conduct rites: [bold green]poetry install[/bold green]",
                    },
                    {
                        "predicate": lambda: (self.root / "package.json").exists(),
                        "proclamation": "Conduct rites: [bold green]npm install[/bold green]", # This is a fallback; a deeper gaze could detect yarn/pnpm
                    },
                    {
                        "predicate": lambda: (self.root / "requirements.txt").exists(),
                        "proclamation": "Conduct rites: [bold green]pip install -r requirements.txt[/bold green]",
                    },
                    {
                        "predicate": lambda: (self.root / "go.mod").exists(),
                        "proclamation": "Conduct rites: [bold green]go mod tidy[/bold green]",
                    },
                    {
                        "predicate": lambda: (self.root / "Cargo.toml").exists(),
                        "proclamation": "Conduct rites: [bold green]cargo build[/bold green]",
                    },
                ]
            },
            # --- MOVEMENT IV: ACTIVATION (HIERARCHY OF WILL) ---
            {
                "group": "activation", "stop_on_success": True,
                "laws": [
                    {
                        "predicate": lambda: "docker-compose.yml" in self.files and self.gnosis.get('use_docker'),
                        "proclamation": "Awaken the celestial vessel: [bold blue]docker compose up --build -d[/bold blue]",
                    },
                    {
                        "predicate": lambda: "dev:" in self._read_safely(self.root / "Makefile"),
                        "proclamation": "Awaken the reality: [bold magenta]make dev[/bold magenta]",
                    },
                    {
                        "predicate": lambda: "run:" in self._read_safely(self.root / "Makefile"),
                        "proclamation": "Awaken the reality: [bold magenta]make run[/bold magenta]",
                    },
                    {
                        "predicate": lambda: '"dev":' in self._read_safely(self.root / "package.json"),
                        "proclamation": "Awaken the reality: [bold magenta]npm run dev[/bold magenta]",
                    },
                    {
                        "predicate": lambda: '"start":' in self._read_safely(self.root / "package.json"),
                        "proclamation": "Awaken the reality: [bold magenta]npm start[/bold magenta]",
                    },
                ]
            },
            # --- MOVEMENT V: THE FINAL GAZE (FALLBACK) ---
            {
                "predicate": lambda: not steps, # Only if no other steps were found
                "proclamation": lambda: f"Gaze upon its soul: [bold]{'dir' if os.name == 'nt' else 'ls -la'}[/bold]",
            },
        ]

        # The Conductor walks the Grimoire.
        for rule in PROPHECY_GRIMOIRE:
            if "group" in rule:
                for law in rule["laws"]:
                    if law["predicate"]():
                        proclamation = law["proclamation"]() if callable(law["proclamation"]) else law["proclamation"]
                        steps.append(proclamation)
                        if rule.get("stop_on_success"):
                            break # The Hierarchy of Will is honored.
            else:
                if rule["predicate"]():
                    proclamation = rule["proclamation"]() if callable(rule["proclamation"]) else rule["proclamation"]
                    steps.append(proclamation)

        return steps