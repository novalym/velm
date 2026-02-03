# Path: symphony/polyglot/grimoire.py
# -----------------------------------

"""
=================================================================================
== THE SACRED GRIMOIRE OF TONGUES (V-Ω-OMNIGLOT-ARCHIVE)                       ==
=================================================================================
LIF: 100,000,000,000,000 (THE UNIVERSAL ROSETTA STONE)

This scripture is the definitive database of execution strategies. It teaches the
God-Engine how to:
1.  **Interpret** script languages (Python, JS, Ruby).
2.  **Compile** system languages (C, C++, Rust, Go).
3.  **Serve** web assets (HTML, PHP).
4.  **Manage** projects (Make, NPM, Cargo, Maven).
5.  **Debug** via DAP (Debug Adapter Protocol) where supported.

The Sacred Contract of a Recipe:
  - interpreter: The command template. {{script_path}} is the file/dir.
  - execution_style: 'temp_file' (write & run), 'direct' (run file), 'project_context' (run in dir).
  - file_extension: For temp files.
  - setup_commands: Pre-flight rites (compilation).
  - cleanup_commands: Post-flight purification (rm binary).
  - env: Environment injections.
=================================================================================
"""
from typing import Dict, Any

POLYGLOT_GRIMOIRE: Dict[str, Dict[str, Any]] = {

    # --- TIER I: THE INTERPRETED SOULS ---

    "python": {
        "interpreter": ["python", "-u", "{{script_path}}"],
        "debug_interpreter": ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client",
                              "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".py",
        "env": {"PYTHONUNBUFFERED": "1"}
    },
    "node": {
        "interpreter": ["node", "{{script_path}}"],
        "debug_interpreter": ["node", "--inspect-brk=0.0.0.0:9229", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".js",
    },
    "ts": {
        "interpreter": ["npx", "tsx", "{{script_path}}"],  # Modern TS execution
        "debug_interpreter": ["npx", "tsx", "--inspect-brk=0.0.0.0:9229", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".ts",
    },
    "deno": {
        "interpreter": ["deno", "run", "-A", "{{script_path}}"],
        "debug_interpreter": ["deno", "run", "-A", "--inspect-brk=0.0.0.0:9229", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".ts",
    },
    "ruby": {
        "interpreter": ["ruby", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".rb",
    },
    "lua": {
        "interpreter": ["lua", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".lua",
    },
    "perl": {
        "interpreter": ["perl", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".pl",
    },
    "php": {
        "interpreter": ["php", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".php",
    },
    "bash": {
        "interpreter": ["bash", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".sh",
    },
    "powershell": {
        "interpreter": ["pwsh", "-File", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".ps1",
    },

    # --- TIER II: THE COMPILED SOULS (THE FORGE) ---

    "go": {
        # Go run handles compilation in tmp automatically
        "interpreter": ["go", "run", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".go",
        "debug_interpreter": ["dlv", "debug", "--headless", "--listen=:2345", "--api-version=2", "{{script_path}}"]
    },
    "rust": {
        "interpreter": ["{{script_path.parent}}/{{script_path.stem}}"],
        "execution_style": "temp_file",
        "file_extension": ".rs",
        # The Rite of Compilation
        "setup_commands": [
            ["rustc", "{{script_path}}", "-o", "{{script_path.parent}}/{{script_path.stem}}"]
        ],
        # The Rite of Purification
        "cleanup_commands": [
            ["rm", "{{script_path.parent}}/{{script_path.stem}}"],
            ["rm", "{{script_path.parent}}/{{script_path.stem}}.pdb"]  # Windows artifact
        ]
    },
    "cpp": {
        "interpreter": ["{{script_path.parent}}/{{script_path.stem}}"],
        "execution_style": "temp_file",
        "file_extension": ".cpp",
        "setup_commands": [
            ["g++", "-std=c++17", "{{script_path}}", "-o", "{{script_path.parent}}/{{script_path.stem}}"]
        ],
        "cleanup_commands": [
            ["rm", "{{script_path.parent}}/{{script_path.stem}}"]
        ]
    },
    "c": {
        "interpreter": ["{{script_path.parent}}/{{script_path.stem}}"],
        "execution_style": "temp_file",
        "file_extension": ".c",
        "setup_commands": [
            ["gcc", "{{script_path}}", "-o", "{{script_path.parent}}/{{script_path.stem}}"]
        ],
        "cleanup_commands": [
            ["rm", "{{script_path.parent}}/{{script_path.stem}}"]
        ]
    },
    "java": {
        # Single-file source-code launch (Java 11+)
        "interpreter": ["java", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".java",
    },
    "kotlin": {
        "interpreter": ["kotlin", "{{script_path}}"],
        "execution_style": "temp_file",
        "file_extension": ".kts",
    },

    # --- TIER III: THE WEB REALM (SERVING) ---

    "html": {
        "interpreter": ["python", "-m", "http.server", "8000", "--directory", "{{script_path.parent}}"],
        "execution_style": "direct",
        "file_extension": ".html",
        "metadata": {"open_browser": "http://localhost:8000/{{script_path.name}}"}
    },

    # --- TIER IV: THE PROJECT CONTEXT (MANAGED RUNTIMES) ---

    "npm": {
        "interpreter": ["npm", "start"],
        "debug_interpreter": ["npm", "run", "debug"],
        "execution_style": "project_context",
    },
    "yarn": {
        "interpreter": ["yarn", "start"],
        "execution_style": "project_context",
    },
    "pnpm": {
        "interpreter": ["pnpm", "start"],
        "execution_style": "project_context",
    },
    "bun": {
        "interpreter": ["bun", "run", "dev"],
        "execution_style": "project_context",
    },
    "poetry": {
        "interpreter": ["poetry", "run", "python", "src/main.py"],  # Heuristic default
        "execution_style": "project_context",
    },
    "pipenv": {
        "interpreter": ["pipenv", "run", "python", "main.py"],
        "execution_style": "project_context",
    },
    "cargo": {
        "interpreter": ["cargo", "run"],
        "execution_style": "project_context",
    },
    "maven": {
        "interpreter": ["mvn", "spring-boot:run"],
        "execution_style": "project_context",
    },
    "gradle": {
        "interpreter": ["./gradlew", "bootRun"],
        "execution_style": "project_context",
    },
    "make": {
        "interpreter": ["make"],
        "execution_style": "project_context",
    },
    "docker_compose": {
        "interpreter": ["docker-compose", "up"],
        "execution_style": "project_context",
    },
    "terraform": {
        "interpreter": ["terraform", "apply", "-auto-approve"],
        "execution_style": "project_context",
    },

    # --- TIER V: FRAMEWORK SPECIFICS (INFERRED) ---

    "fastapi": {
        "interpreter": ["uvicorn", "{{script_path.stem}}:app", "--reload"],
        "execution_style": "direct",
    },
    "flask": {
        "interpreter": ["flask", "run"],
        "env": {"FLASK_APP": "{{script_path.name}}", "FLASK_DEBUG": "1"},
        "execution_style": "direct",
    },
    "django": {
        "interpreter": ["python", "manage.py", "runserver"],
        "execution_style": "project_context",
    },
    "streamlit": {
        "interpreter": ["streamlit", "run", "{{script_path}}"],
        "execution_style": "direct",
    }
}