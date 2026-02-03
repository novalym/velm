# Path: scaffold/genesis_pleas.py

"""
=================================================================================
== THE SACRED GRIMOIRE OF GENESIS PLEAS (V-Ω-LEGENDARY++. THE AI's SOUL)        ==
=================================================================================
LIF: 10,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000,000!

This is not a file of code. It is the living, eternal soul of the Gnostic Oracle's
dialogue. It is a sacred, declarative, and infinitely extensible Grimoire that
contains the complete scripture for every question the Genesis Engine can ask.
It is organized into a Pantheon of Dialogues, each a sacred movement in the
grand symphony of creation.
=================================================================================
"""
from rich.text import Text

from ... import utils
from ...constants import ARCHETYPE_VALIDATION_MAP
from ...contracts.communion_contracts import GnosticPleaType

# =================================================================================
# == I. THE PANTHEON OF DIALOGUES                                                ==
# =================================================================================

# --- MOVEMENT I: THE SOUL OF THE PROJECT (CORE IDENTITY) ---
# This movement forges the project's fundamental Gnosis.
CORE_IDENTITY_PLEAS = [
    {
        "key": "project_name",
        "plea_type": GnosticPleaType.TEXT,
        "prompt_rite": lambda g: Text.assemble(
            ("✨ ", "yellow"),
            "First, what is the sacred name of this new reality? (e.g., ",
            (g.get('prophesied_slug', 'sentinel-api'), "cyan"),
            ")"
        ),
        "validation_rite": lambda g: ARCHETYPE_VALIDATION_MAP.get(g.get('clean_type_name'), 'var_path_safe')
    },
    {
        "key": "author",
        "plea_type": GnosticPleaType.TEXT,
        "prompt_rite": lambda g: Text.assemble(
            ("👤 ", "blue"),
            "Whose hands shall forge this Great Work? (Author / Organization)"
        )
    },
    {
        "key": "description",
        "plea_type": GnosticPleaType.MULTILINE,
        "prompt_rite": lambda g: Text.assemble(
            ("📜 ", "green"),
            "Proclaim its purpose. What is the one-line Gnostic essence of this project?"
        ),
        "default_rite": lambda g: f"A new {g.get('clean_type_name')} project ({g.get('prophesied_slug')}) by {g.get('author')}."
    },
    {
        "key": "project_type",
        "plea_type": GnosticPleaType.CHOICE,
        "prompt_rite": lambda g: Text.assemble(
            ("🛠️ ", "magenta"),
            "Choose its architectural soul. What is the primary archetype of this reality?"
        ),
        "choices_rite": lambda g: g.get('raw_archetype_choices', ['generic'])
    },
]

# --- MOVEMENT II: THE GNOSTIC TOOLCHAIN (LANGUAGES & FRAMEWORKS) ---
# This movement defines the core technologies and their sacred artisans.
TOOLCHAIN_PLEAS = [
    {
        "key": "use_poetry",
        "plea_type": GnosticPleaType.CONFIRM,
        "adjudicator": lambda g: g.get('clean_type_name') in ['python', 'poetry'] and utils.is_poetry_installed(),
        "prompt_rite": lambda g: Text.assemble(("🐍 ", "yellow"), "Shall we summon [cyan]Poetry[/cyan] to conduct the Python dependency rites?"),
        "default_rite": lambda g: True
    },
    {
        "key": "database_type",
        "plea_type": GnosticPleaType.CHOICE,
        "adjudicator": lambda g: g.get('clean_type_name') not in ['frontend-vanilla', 'cli-tool'],
        "prompt_rite": lambda g: Text.assemble(("🗄️ ", "blue"), "Which divine artisan shall guard the project's data? (Database)"),
        "choices_rite": lambda g: ['none', 'postgres', 'mysql', 'sqlite', 'mongodb', 'redis', 'dynamodb']
    },
    {
        "key": "frontend_framework",
        "plea_type": GnosticPleaType.CHOICE,
        "adjudicator": lambda g: g.get('clean_type_name') in ['generic', 'node', 'python', 'frontend-app'] or g.get('database_type') == 'none',
        "prompt_rite": lambda g: Text.assemble(("🌐 ", "yellow"), "Which artistic school shall shape the user's reality? (Frontend Framework)"),
        "choices_rite": lambda g: ['none', 'react', 'vue', 'svelte', 'vanilla-js']
    },
    {
        "key": "testing_framework",
        "plea_type": GnosticPleaType.CHOICE,
        "adjudicator": lambda g: g.get('clean_type_name') not in ['generic', 'docs'],
        "prompt_rite": lambda g: Text.assemble(("🧪 ", "green"), "Which Inquisitor shall adjudicate the project's purity? (Testing Framework)"),
        "choices_rite": lambda g: {
            'python': ['pytest', 'unittest', 'none'], 'poetry': ['pytest'],
            'node': ['jest', 'vitest', 'mocha', 'none'], 'go': ['go test', 'none'],
            'rust': ['cargo test', 'none'], 'java': ['junit', 'mockito', 'none'],
            'cpp': ['gtest', 'catch2', 'none'], 'default': ['none', 'basic']
        }.get(g.get('clean_type_name'), ['none', 'basic'])
    },
]

# --- MOVEMENT III: ARCHITECTURAL PHILOSOPHY (STRUCTURE & SECURITY) ---
# This movement defines the high-level patterns and safeguards of the new reality.
ARCHITECTURAL_PLEAS = [
    {
        "key": "project_structure_pattern",
        "plea_type": GnosticPleaType.CHOICE,
        "adjudicator": lambda g: g.get('clean_type_name') not in ['docs', 'cli-tool'],
        "prompt_rite": lambda g: Text.assemble(("🏗️ ", "yellow"), "Which grand architectural philosophy shall we follow?"),
        "choices_rite": lambda g: ['monolithic', 'modular-monolith', 'microservice-style', 'serverless'],
        "default_rite": lambda g: 'modular-monolith'
    },
    {
        "key": "auth_method",
        "plea_type": GnosticPleaType.CHOICE,
        "adjudicator": lambda g: g.get('database_type') != 'none' or g.get('clean_type_name') in ['api-service', 'node', 'python', 'go'],
        "prompt_rite": lambda g: Text.assemble(("🔐 ", "cyan"), "Which sacred key shall guard the gates of this reality? (Authentication)"),
        "choices_rite": lambda g: ['none', 'jwt', 'oauth2', 'session-cookies', 'api-key']
    },
    {
        "key": "env_vars_setup",
        "plea_type": GnosticPleaType.CONFIRM,
        "adjudicator": lambda g: g.get('database_type') != 'none' or g.get('auth_method') != 'none' or g.get('use_docker'),
        "prompt_rite": lambda g: Text.assemble(("🍃 ", "green"), "Forge a `.env.example` scripture to proclaim the required secrets?"),
        "default_rite": lambda g: True
    },
    {
        "key": "default_port",
        "plea_type": GnosticPleaType.TEXT,
        "adjudicator": lambda g: g.get('clean_type_name') in ['python', 'node', 'go', 'frontend-app', 'api-service'] or g.get('frontend_framework') != 'none',
        "prompt_rite": lambda g: Text.assemble(("🔌 ", "yellow"), "On which port shall this reality listen to the cosmos?"),
        "default_rite": lambda g: '8000' if g.get('clean_type_name') == 'python' else '3000',
        "validation_rite": lambda g: 'var_int'
    },
]

# --- MOVEMENT IV: THE ORCHESTRATION & DEVOPS REALM ---
# This movement forges the tools for building, testing, and deploying the Great Work.
DEVOPS_PLEAS = [
    {
        "key": "license",
        "plea_type": GnosticPleaType.CONFIRM,
        "prompt_rite": lambda g: Text.assemble("Proclaim the project's vow to the cosmos with a [yellow]LICENSE[/yellow] file (MIT)?"),
        "default_rite": lambda g: g.get('clean_type_name') not in ['cli-tool', 'library']
    },
    {
        "key": "use_git",
        "plea_type": GnosticPleaType.CONFIRM,
        # =============================================================================
        # ==         BEGIN SACRED TRANSMUTATION: THE GAZE OF THE MISSING ARTISAN       ==
        # =============================================================================
        # The plea is now a true Mentor. It perceives reality before it speaks.
        "prompt_rite": lambda g: Text.assemble(
            "Forge a ",
            ("[yellow]Git[/yellow] soul", "yellow") if utils.is_git_installed() else (
                "[red]Git[/red] soul (Artisan not found!)", "bold red"),
            " to chronicle this project's history?"
        ),
        # The default is now a logical AND: it defaults to True only if git is installed.
        "default_rite": lambda g: utils.is_git_installed(),
        # =============================================================================
    },
    {
        "key": "initial_commit_message",
        "plea_type": GnosticPleaType.TEXT,
        "adjudicator": lambda g: g.get('use_git'),
        "prompt_rite": lambda g: Text.assemble(("📝 ", "dim"), "Inscribe the first verse in the Gnostic Chronicle (Initial Commit Message)"),
        "default_rite": lambda g: f"feat(init): Initial {g.get('prophesied_slug')} project setup via Scaffold"
    },
    {
        "key": "use_ci",
        "plea_type": GnosticPleaType.CONFIRM,
        "adjudicator": lambda g: g.get('use_git'),
        "prompt_rite": lambda g: Text.assemble("Forge a [yellow]GitHub Actions CI[/yellow] symphony to adjudicate future changes?")
    },
    {
        "key": "use_docker",
        "plea_type": GnosticPleaType.CONFIRM,
        "adjudicator": lambda g: g.get('clean_type_name') not in ['frontend-vanilla', 'docs'],
        "prompt_rite": lambda g: Text.assemble(("🐳 ", "blue"), "Forge a [cyan]Dockerfile[/cyan] to grant this reality a portable, universal form?"),
        "default_rite": lambda g: True
    },
    {
        "key": "observability_setup",
        "plea_type": GnosticPleaType.CONFIRM,
        "adjudicator": lambda g: g.get('use_docker') and g.get('clean_type_name') not in ['cli-tool', 'docs'],
        "prompt_rite": lambda g: Text.assemble(("👁️ ", "cyan"), "Bestow the gift of a second sight with [cyan]Observability[/cyan] scriptures (Prometheus/Grafana)?")
    },
    {
        "key": "cloud_provider",
        "plea_type": GnosticPleaType.CHOICE,
        "adjudicator": lambda g: g.get('use_docker') and g.get('use_ci'),
        "prompt_rite": lambda g: Text.assemble(("☁️ ", "blue"), "To which celestial realm shall this reality ascend? (Deployment Target)"),
        "choices_rite": lambda g: ['none', 'aws', 'gcp', 'azure', 'kubernetes', 'fly.io']
    },
]

# --- MOVEMENT V: THE CO-ARCHITECT'S COMMUNION (AI & MENTORSHIP) ---
# This movement forges the Gnostic Bridge between the Architect and the AI.
CO_ARCHITECT_PLEAS = [
    {
        "key": "use_vscode",
        "plea_type": GnosticPleaType.CONFIRM,
        "prompt_rite": lambda g: Text.assemble("Forge sacred scriptures to make this reality luminous in [cyan]Visual Studio Code[/cyan]?"),
        "default_rite": lambda g: True
    },
    {
        "key": "project_goals",
        "plea_type": GnosticPleaType.MULTILINE,
        "prompt_rite": lambda g: Text.assemble(("🎯 ", "magenta"),
                                               "What is the ultimate destiny of this project? (For the AI Co-Architect's Gaze)"),
        "special_rite": "editor_inquest",
        # [FIX] We only ask this if the user hasn't opted out or provided it.
        # It's a heavy question.
        "adjudicator": lambda g: not g.get('quick', False)
    },
    {
        "key": "custom_globals",
        "plea_type": GnosticPleaType.MULTILINE,
        # [FIX] The Gnostic Ward: We only ask for custom YAML logic in VERBOSE mode.
        # This prevents confusing new architects with advanced metaphysics.
        "adjudicator": lambda g: g.get('verbose', False) and not g.get('quick', False),
        "prompt_rite": lambda g: Text.assemble(("🧩 ", "yellow"), "Define optional global key-value Gnosis (YAML structure expected)."),
        "special_rite": "editor_inquest_yaml_dict",
        "default_rite": lambda g: {"build_id": 1, "environment": "dev"}
    },
    {
        "key": "ai_code_generation_consent",
        "plea_type": GnosticPleaType.CONFIRM,
        "prompt_rite": lambda g: Text.assemble(("🧠 ", "blue"), "Grant the AI Co-Architect the authority to synthesize code snippets based on your will?"),
        "default_rite": lambda g: True,
        "adjudicator": lambda g: not g.get('quick', False)
    },
    {
        "key": "generate_ai_description",
        "plea_type": GnosticPleaType.CONFIRM,
        "adjudicator": lambda g: g.get('ai_code_generation_consent') and g.get('project_goals') and not g.get('quick', False),
        "prompt_rite": lambda g: Text.assemble(("🤖 ", "cyan"), "Allow the AI to synthesize a more luminous project description from your stated goals?")
    },
]


# =================================================================================
# == II. THE DIVINE SYNTHESIS: FORGING THE COMPLETE SCRIPTURE                    ==
# =================================================================================
# The final, complete Grimoire is a glorious synthesis of the entire Pantheon.
GENESIS_PLEAS_GRIMOIRE = (
    CORE_IDENTITY_PLEAS +
    TOOLCHAIN_PLEAS +
    ARCHITECTURAL_PLEAS +
    DEVOPS_PLEAS +
    CO_ARCHITECT_PLEAS
)