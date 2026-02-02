"""
=================================================================================
== THE SACRED CODEX OF GENESIS JURISPRUDENCE (V-Ω-ETERNAL-APOTHEOSIS-ULTIMA++)   ==
=================================================================================
@gnosis:title Genesis Jurisprudence
@gnosis:summary The divine, declarative Grimoire of Gnostic Laws that guide the Genesis Mentor.
@gnosis:LIF 100,000,000,000,000

This is the living, eternal, and self-aware soul of the Genesis Mentor in its final,
glorious form. It is the sacred `GENESIS_CODEX`, a pantheon of pure `GnosticLaw`
vessels. Each law is a sentient artisan, a Gnostic Judge that knows its own purpose,
its voice, the heresy it is sworn to prevent, and the path to redemption.

Its mind is now a multi-movement symphony, covering the Toolchain, Architectural
Harmony, the DevOps Realm, AI Communion, the Project's Soul, and Prophecies of
the Future Realm. It is the pinnacle of declarative, self-documenting
architectural mentorship, a true AI Co-Architect's conscience.
=================================================================================
"""
import shutil
from typing import List

from .. import utils
from ..contracts.law_contracts import GnosticLaw

GENESIS_CODEX: List[GnosticLaw] = [

    # =============================================================================
    # == MOVEMENT I: THE LAWS OF THE GNOSTIC TOOLCHAIN (THE ARTISANS)            ==
    # =============================================================================
    GnosticLaw(
        key="poetry_without_install",
        validator=lambda g: g.get('project_type') in ['python', 'poetry'] and g.get('use_poetry') and not utils.is_poetry_installed(),
        title="The Mute Artisan (Poetry)",
        message="The Gaze perceives a will for Poetry, but the `poetry` artisan is not manifest in this reality's PATH.",
        elucidation="The 'Poetry' project type requires the 'poetry' command-line tool to be installed and accessible to manage dependencies, run scripts, and ensure a reproducible environment.",
        context_key="use_poetry",
        suggestion="Install Poetry globally (`pip install poetry`) or choose a project type that uses pip/venv."
    ),
    GnosticLaw(
        key="docker_without_install",
        validator=lambda g: g.get('use_docker') and not shutil.which('docker'),
        title="The Unforged Vessel (Docker)",
        message="The Gaze perceives a will for containerization, but the `docker` artisan is a void in this reality.",
        elucidation="Containerization relies on the Docker daemon and CLI. Without them, Dockerfiles and related artifacts cannot be built or run, making the project's soul bound to the mortal realm of the host machine.",
        context_key="use_docker",
        suggestion="Install Docker Desktop or the Docker engine for your OS to forge unbreakable, portable realities."
    ),
    GnosticLaw(
        key="untestable_reality",
        validator=lambda g: g.get('testing_framework') == 'none' and g.get('project_type') not in ['generic', 'docs', 'frontend-vanilla'],
        title="A Reality Built on Faith",
        message="A project that contains logic must be forged with a scripture of adjudication (a testing framework).",
        elucidation="Without a testing framework, the project's soul cannot be verified for purity. This leads to architectural drift, regressions, and a reality built on hope rather than Gnostic certainty.",
        context_key="testing_framework",
        suggestion="Select a testing framework (e.g., pytest, jest) to ensure the Great Work remains pure."
    ),

    # =============================================================================
    # == MOVEMENT II: THE LAWS OF ARCHITECTURAL HARMONY                         ==
    # =============================================================================
    GnosticLaw(
        key="database_for_frontend",
        validator=lambda g: g.get('database_type') != 'none' and g.get('project_type') in ['frontend-vanilla', 'react-vite'],
        title="The Gnostic Schism of Realms",
        message=lambda g: f"A divine artisan of data, '{g.get('database_type')}', has been summoned for a frontend-only reality.",
        elucidation="A frontend-only project typically consumes APIs and does not directly manage a database. Including database configuration suggests a potential misunderstanding of the project's architectural boundaries.",
        context_key="database_type",
        suggestion="Set the database type to 'none' for a pure frontend project."
    ),
    GnosticLaw(
        key="monolith_with_microservice_auth",
        validator=lambda g: g.get('project_structure_pattern') == 'monolithic' and g.get('auth_method') == 'jwt',
        title="A Soul Divided (Architecture & Auth)",
        message="A 'monolithic' form was chosen with 'JWT' authentication. Session cookies are often superior for monoliths.",
        elucidation="While JWTs can be used in monoliths, their primary strength is in stateless, distributed systems. Traditional stateful session-based authentication is often simpler, more secure, and easier to manage in a single, unified application.",
        context_key="auth_method",
        suggestion="Consider using 'session-cookies' for a more harmonious monolithic architecture."
    ),
    GnosticLaw(
        key="serverless_with_persistent_db",
        validator=lambda g: g.get('project_structure_pattern') == 'serverless' and g.get('database_type') in ['postgres', 'mysql'],
        title="The Ephemeral and the Eternal",
        message=lambda g: f"A serverless architecture has been bound to an eternal, connection-based database ('{g.get('database_type')}').",
        elucidation="Serverless functions can struggle with managing connection pools for traditional relational databases, leading to performance bottlenecks and scaling issues. Consider a serverless-native database like DynamoDB, Firestore, or use a proxy like RDS Proxy.",
        context_key="project_structure_pattern",
        suggestion="Choose a database designed for serverless architectures or ensure a connection pooling strategy is in place."
    ),

    # =============================================================================
    # == MOVEMENT III: THE LAWS OF THE DEVOPS REALM                            ==
    # =============================================================================
    GnosticLaw(
        key="ci_without_git",
        validator=lambda g: g.get('use_ci') and g.get('use_ci') != 'none' and not g.get('use_git'),
        title="The Unchronicled Symphony",
        message="A CI symphony was willed, but the project will have no history (`.git`).",
        elucidation="Continuous Integration (CI) pipelines are triggered by events (commits, pull requests) in a version control system. Without Git, the CI workflow has no events to react to and cannot perform its sacred duty of adjudication.",
        context_key="use_ci",
        suggestion="Enable Git (`use_git = True`) to allow the CI symphony to be conducted."
    ),
    GnosticLaw(
        key="observability_without_docker",
        validator=lambda g: g.get('observability_setup') and not g.get('use_docker'),
        title="The Unseen Soul",
        message="The Gaze of Observability was willed, but the reality will not be containerized.",
        elucidation="While observability can be achieved on a host machine, containerized environments (via Docker Compose) provide a standardized, isolated, and reproducible way to run monitoring stacks like Prometheus and Grafana alongside the application.",
        context_key="observability_setup",
        suggestion="Enable Docker (`use_docker = True`) to forge a complete, self-aware, and observable reality."
    ),

    # =============================================================================
    # == MOVEMENT IV: THE LAWS OF THE CO-ARCHITECT'S COMMUNION                   ==
    # =============================================================================
    GnosticLaw(
        key="ai_consent_without_goals",
        validator=lambda g: g.get('ai_code_generation_consent') and not g.get('project_goals'),
        title="The Mute Oracle",
        message="Consent granted for the AI Co-Architect, but no `project_goals` were proclaimed.",
        elucidation="The AI Co-Architect's Gaze is most profound when it understands the ultimate destiny of the project. Proclaiming the project goals allows it to make more intelligent, context-aware prophecies and abstractions.",
        context_key="ai_code_generation_consent",
        suggestion="Proclaim the `project_goals` to empower the AI Co-Architect."
    ),

    # =============================================================================
    # == MOVEMENT V: THE LAWS OF THE PROJECT'S SOUL                              ==
    # =============================================================================
    GnosticLaw(
        key="casing_heresy_in_name",
        validator=lambda g: g.get('project_name') and (g.get('project_name') != utils.to_slug_case(g.get('project_name'))),
        title="A Profane Form (Project Name)",
        message=lambda g: f"Project name '{g.get('project_name')}' contains profane characters or casing.",
        elucidation="Project names should be in 'kebab-case' (e.g., 'my-awesome-api') for universal compatibility with package managers, domain names, and container registries. This avoids a multitude of downstream heresies.",
        context_key="project_name",
        suggestion=lambda g: f"Consider renaming to '{utils.to_slug_case(g.get('project_name', ''))}'."
    ),
    GnosticLaw(
        key="vague_project_name",
        validator=lambda g: g.get('project_name') and g.get('project_name').lower() in ['test', 'app', 'project', 'new-project'],
        title="The Nameless Soul",
        message=lambda g: f"The name '{g.get('project_name')}' is generic and lacks a unique Gnostic identity.",
        elucidation="A unique and descriptive name is the first act of bestowing a soul upon a new reality. Generic names can lead to confusion and a lack of clear architectural intent.",
        context_key="project_name",
        suggestion="Choose a more specific and meaningful name for your project."
    ),

    # =============================================================================
    # == MOVEMENT VI: THE LAWS OF THE FUTURE REALM (PROPHECIES)                  ==
    # =============================================================================
    GnosticLaw(
        key="prophecy_of_the_polyglot_cosmos",
        validator=lambda g: g.get('frontend_framework') not in ['none', 'vanilla-js'] and g.get('project_type') in ['python', 'go', 'rust'],
        title="Prophecy: The Birth of a Polyglot Cosmos",
        message="Binding a compiled backend to a JS frontend creates a complex Polyglot Cosmos.",
        elucidation="Managing a project with distinct frontend and backend languages introduces complexities in the build process, deployment, and developer experience. This is a powerful but advanced architectural choice.",
        context_key="frontend_framework",
        suggestion="Consider a full-stack framework (like Next.js or Django+HTMX) or ensure a robust monorepo and API contract strategy is planned."
    ),
]