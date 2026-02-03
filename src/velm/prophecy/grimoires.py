# Path: scaffold/prophecy/grimoires.py

"""
=================================================================================
== THE SACRED GRIMOIRE OF THE LIVING SOUL (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)      ==
=================================================================================
This is the eternal, extensible scripture that teaches the OracleOfTheLivingSoul
how to perceive the Gnostic essence of any project in the cosmos. It is the one
true, declarative mind of our Gnostic AI.
=================================================================================
"""

# =================================================================================
# == THE CODEX OF LIVING SOULS (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)                 ==
# =================================================================================
# LIF: 10,000,000,000,000
#
# This is the sacred, extensible Grimoire for the Oracle of the Living Soul. It is
# the hyper-sentient mind of the `distill` command's AI Prophet. It teaches the
# Oracle how to perceive a project's technological soul not just by its manifest
# scriptures, but by the very Gnosis inscribed within them.
#
# Each verse is a Gnostic Law with this sacred contract:
#   "name": The luminous name of the soul.
#   "scripture": The manifest file that is the primary vessel of this soul.
#   "gaze_pattern": A divine regex to be cast upon the scripture's content.
#   "guard_artisan": The mortal name of the tool required for this soul's rites.
#   "edict": The prophesied Maestro's Edict to give the soul life.
#   "badge": The scripture for a shields.io badge, a luminous sigil of this soul.
#   "rank": The Gnostic precedence of this soul (higher is more specific).
# =================================================================================
SOUL_CODEX = [
    # --- I. The Pantheon of JavaScript/TypeScript Souls ---
    {
        "name": "Node.js", "rank": 10, "scripture": "package.json",
        "gaze_pattern": r'"(node|express|next)"', "guard_artisan": "node",
        "edict": "npm install",
        "badge": "[![Node.js version](https://img.shields.io/node/v/{{pkg_name}}.svg)](https://nodejs.org/)"
    },
    {
        "name": "React", "rank": 20, "scripture": "package.json",
        "gaze_pattern": r'"react"', "guard_artisan": "npm",
        "edict": "npm install",
        "badge": "[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://react.dev/)"
    },
    {
        "name": "Vite", "rank": 25, "scripture": "package.json",
        "gaze_pattern": r'"vite"', "guard_artisan": "npm",
        "edict": "npm install",
        "badge": "[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)"
    },
    {
        "name": "Vue.js", "rank": 20, "scripture": "package.json",
        "gaze_pattern": r'"vue"', "guard_artisan": "npm",
        "edict": "npm install",
        "badge": "[![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)](https://vuejs.org/)"
    },

    # --- II. The Pantheon of Python Souls ---
    {
        "name": "Python", "rank": 10, "scripture": "requirements.txt",
        "gaze_pattern": None, "guard_artisan": "pip",
        "edict": "pip install -r requirements.txt",
        "badge": "[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)"
    },
    {
        "name": "Poetry (Python)", "rank": 15, "scripture": "pyproject.toml",
        "gaze_pattern": r'\[tool\.poetry\]', "guard_artisan": "poetry",
        "edict": "poetry install", # The Wise Transmuter will handle this.
        "badge": "[![Poetry](https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white)](https://python-poetry.org/)"
    },
    {
        "name": "FastAPI", "rank": 20, "scripture": "pyproject.toml",
        "gaze_pattern": r'fastapi', "guard_artisan": "pip",
        "edict": "pip install -r requirements.txt", # Assumes universal form
        "badge": "[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)"
    },
    {
        "name": "Django", "rank": 20, "scripture": "pyproject.toml",
        "gaze_pattern": r'django', "guard_artisan": "pip",
        "edict": "pip install -r requirements.txt",
        "badge": "[![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)"
    },

    # --- III. The Pantheon of Go Souls ---
    {
        "name": "Go", "rank": 10, "scripture": "go.mod",
        "gaze_pattern": r'module\s+', "guard_artisan": "go",
        "edict": "go mod tidy",
        "badge": "[![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)](https://golang.org/)"
    },

    # --- IV. The Pantheon of Rust Souls ---
    {
        "name": "Rust", "rank": 10, "scripture": "Cargo.toml",
        "gaze_pattern": r'\[package\]', "guard_artisan": "cargo",
        "edict": "cargo build",
        "badge": "[![Rust](https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white)](https://www.rust-lang.org/)"
    },

    # --- V. The Pantheon of Java Souls ---
    {
        "name": "Java (Maven)", "rank": 10, "scripture": "pom.xml",
        "gaze_pattern": r'<project.*>', "guard_artisan": "mvn",
        "edict": "mvn install",
        "badge": "[![Maven Central](https://img.shields.io/maven-central/v/{{group_id}}/{{artifact_id}})](https://search.maven.org/)"
    },
    {
        "name": "Java (Gradle)", "rank": 11, "scripture": "build.gradle",
        "gaze_pattern": r'plugins\s*\{', "guard_artisan": "gradle",
        "edict": "gradle build",
        "badge": "[![Gradle](https://img.shields.io/badge/Gradle-02303A?style=for-the-badge&logo=gradle&logoColor=white)](https://gradle.org/)"
    },

    # --- VI. The Pantheon of C# Souls ---
    {
        "name": "C# (.NET)", "rank": 10, "scripture": "*.csproj", # Gaze needs to support globs
        "gaze_pattern": r'<Project Sdk="Microsoft.NET.Sdk.*">', "guard_artisan": "dotnet",
        "edict": "dotnet restore",
        "badge": "[![.NET](https://img.shields.io/badge/.NET-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)"
    },

    # --- VII. The Pantheon of DevOps & Containerization Souls ---
    {
        "name": "Docker", "rank": 5, "scripture": "Dockerfile",
        "gaze_pattern": r'FROM', "guard_artisan": "docker",
        "edict": "docker build -t {{project_slug}} .",
        "badge": "[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)"
    },
    {
        "name": "PostgreSQL", "rank": 5, "scripture": "docker-compose.yml",
        "gaze_pattern": r'image:\s*postgres', "guard_artisan": "docker",
        "edict": "docker-compose up -d",
        "badge": "[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)"
    },
    # Future Gnosis can be added here (e.g., Cargo.toml for Rust, pom.xml for Maven)
]