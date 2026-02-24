# artisans/dream/agentic_limb/reflex/lexicon.py
# ---------------------------------------------
"""
=================================================================================
== THE IMMUTABLE LEXICON (V-Ω-SEMANTIC-TRUTH)                                  ==
=================================================================================
The dictionary of Gnostic Roots. It defines the vocabulary of the God-Engine.
[THE CURE]: The Type Heresy is annihilated. Dict[str, List[str]] is Law.
"""
from typing import Set, Dict, List

# --- THE VOID WORDS (Noise to be incinerated) ---
STOP_WORDS: Set[str] = {
    "i", "want", "to", "please", "can", "you", "just", "do", "it", "the", "a", "an",
    "my", "our", "for", "in", "of", "with", "about", "like", "need", "could", "would",
    "should", "hey", "velm", "scaffold", "make", "let", "us", "me", "some"
}

# --- THE MODIFIERS OF WILL (Flags) ---
MODIFIER_MAP: Dict[str, List[str]] = {
    "dry_run": ["simulate", "what if", "dry run", "pretend", "test out", "without saving", "fake"],
    "force": ["force", "just do it", "overwrite", "now", "absolutely", "hard"],
    "adrenaline": ["fast", "quick", "quickly", "speed", "hurry", "rush", "adrenaline"],
    "silent": ["quietly", "silently", "shh", "no logs", "quiet", "mute"],
}

# --- THE STEMS OF ACTION (Roots of Verbs) ---
# We use root stems to match "refactoring", "refactored", "refactor" mathematically.
ACTION_ROOTS: Dict[str, List[str]] = {
    # Architecture & Creation
    "refactor": ["refactor", "rewrit", "restructur", "redesign", "optimiz", "clean"],
    "weave": ["weav", "add", "inject", "includ", "combin", "merg"],
    "create": ["creat", "generat", "forg", "build", "scaffold", "init", "start new", "spin up"],

    # Adjudication & Healing
    "lint": ["lint", "fix", "heal", "repair", "audit", "scan", "inspect", "check"],
    "verify": ["verif", "validat", "assur", "test truth"],

    # Metaphysics & State
    "adopt": ["adopt", "assimil", "ingest", "absorb"],
    "undo": ["undo", "revert", "rollback", "back", "zctrlz"],
    "save": ["sav", "commit", "checkpoint", "record", "preserv"],

    # Kinetic Mutation
    "move": ["mov", "renam", "transfer", "mv", "transloc"],
    "delete": ["delet", "remov", "destroy", "annihilat", "rm", "excis"],

    # Perception
    "tree": ["tree", "structur", "map", "visualiz", "show me"],
    "graph": ["graph", "dependenc", "diagram", "chart"],
    "distill": ["distill", "compress", "shrink", "extract soul"],

    # Execution & Cloud
    "run": ["run", "execut", "exec", "start", "launch", "trigger"],
    "cloud": ["provision", "deploy", "ship", "host", "aws", "ovh", "azure", "server"],

    # Identity & UI
    "identity": ["login", "auth", "whoami", "status", "credential"],
    "gui": ["gui", "ui", "dashboard", "panel", "studio", "pad"]
}

# --- THE ARCHITECTURAL NOUNS ---
# Helps the engine identify the targets of an action if paths are not provided.
TARGET_NOUNS: Set[str] = {
    "api", "backend", "frontend", "database", "db", "auth", "security",
    "project", "app", "service", "module", "component", "router", "model"
}