# Path: scaffold/core/ignition/diviner/sentinel/grimoire.py
# --------------------------------------------------------
# LIF: INFINITY // AUTH_CODE: SENTINEL_GRIMOIRE_V1

from typing import Dict, Any
from ..contracts import IgnitionAura

# [ASCENSION 11]: THE REGISTRY OF FAITH
TOOL_GRIMOIRE: Dict[str, Dict[str, Any]] = {
    "npm": {
        "redemption": "npm install -g npm",
        "label": "Node Package Manager",
        "aura_bonds": [IgnitionAura.VITE, IgnitionAura.NEXT, IgnitionAura.NUXT],
        "binary_alternatives": ["npm.cmd", "npm.exe"]
    },
    "python": {
        "redemption": "https://www.python.org/downloads/",
        "label": "Python Interpreter",
        "aura_bonds": [IgnitionAura.FASTAPI, IgnitionAura.FLASK, IgnitionAura.DJANGO],
        "binary_alternatives": ["python3", "python.exe", "py"]
    },
    "docker": {
        "redemption": "https://docs.docker.com/get-docker/",
        "label": "Docker Engine",
        "aura_bonds": [IgnitionAura.GENERIC],
        "check_cmd": ["info"]
    },
    "cargo": {
        "redemption": "https://rustup.rs/",
        "label": "Rust Toolchain",
        "aura_bonds": [IgnitionAura.CARGO],
        "binary_alternatives": ["cargo.exe"]
    },
    "go": {
        "redemption": "https://go.dev/dl/",
        "label": "Go Compiler",
        "aura_bonds": [IgnitionAura.GO_MOD],
        "binary_alternatives": ["go.exe"]
    },
    "uvicorn": {
        "redemption": "pip install uvicorn",
        "label": "Uvicorn ASGI Server",
        "aura_bonds": [IgnitionAura.FASTAPI]
    }
}