# Path: src/velm/codex/atoms/policy.py
# ------------------------------------

"""
=================================================================================
== THE SCRIBE OF LAW (V-Ω-POLICY-DOMAIN-ULTIMA)                                ==
=================================================================================
LIF: INFINITY | ROLE: GOVERNANCE_ARCHITECT | RANK: OMEGA_SOVEREIGN

This artisan implements the `@policy` namespace. It generates the high-fidelity
governance documents required for Enterprise-grade and Open-Source maturity.

Usage:
    SECURITY.md           :: {{ policy.security(email="sec@corp.com") }}
    CODE_OF_CONDUCT.md    :: {{ policy.coc(email="conduct@corp.com") }}
    docs/adr/001-init.md  :: {{ policy.adr(title="Use Python", status="Accepted") }}
    .github/PULL_REQUEST_TEMPLATE.md :: {{ policy.pr_template() }}
=================================================================================
"""
from datetime import datetime
from textwrap import dedent
from typing import Dict, Any, Optional

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("policy")
class PolicyDomain(BaseDirectiveDomain):
    """
    The Keeper of the Covenant.
    """

    @property
    def namespace(self) -> str:
        return "policy"

    def help(self) -> str:
        return "Generates governance docs (Security, CoC, ADR, Contributing, PR Templates)."

    # =========================================================================
    # == INTERNAL RITES (METADATA SCRYING)                                   ==
    # =========================================================================

    def _get_metadata(self, context: Dict[str, Any], **kwargs) -> Dict[str, str]:
        """
        [THE GAZE OF IDENTITY]
        Resolves project metadata from the Gnostic Context or System Environment.
        """
        return {
            "year": str(datetime.now().year),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "project": kwargs.get('project_name') or context.get('project_name', 'This Project'),
            "author": kwargs.get('author') or context.get('author', 'The Architect'),
            "email": kwargs.get('email') or context.get('email', 'security@example.com'),
            "repo": kwargs.get('repo_url') or context.get('repo_url', 'https://github.com/org/repo')
        }

    # =========================================================================
    # == STRATUM 0: THE SECURITY SHIELD (RFC 9116)                           ==
    # =========================================================================

    def _directive_security(self, context: Dict[str, Any], email: str = "", encryption_key: str = "") -> str:
        """
        policy.security(email="sec@novalym.com")
        Generates a standard SECURITY.md file.
        """
        meta = self._get_metadata(context, email=email)

        pgp_section = ""
        if encryption_key:
            pgp_section = dedent(f"""
            ## Encryption

            When reporting a vulnerability, please encrypt your report using our PGP key:

            ```text
            {encryption_key}
            ```
            """)

        return dedent(f"""
            # Security Policy

            ## Supported Versions

            Use this section to tell people about which versions of your project are
            currently being supported with security updates.

            | Version | Supported          |
            | ------- | ------------------ |
            | 1.0.x   | :white_check_mark: |
            | < 1.0   | :x:                |

            ## Reporting a Vulnerability

            We take the security of **{meta['project']}** seriously. If you believe you have found a security vulnerability, please report it to us as described below.

            **Please do not report security vulnerabilities through public GitHub issues.**

            Instead, please send an email to **{meta['email']}**.

            You should receive a response within 24 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

            {pgp_section}

            ## Disclosure Policy

            We follow a [Responsible Disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure) policy:
            1. You privately report the vulnerability.
            2. We acknowledge receipt and verify the issue.
            3. We develop a patch and release it.
            4. We publicly credit you (if desired) in the release notes.
        """).strip()

    # =========================================================================
    # == STRATUM 1: THE SOCIAL CONTRACT (CODE OF CONDUCT)                    ==
    # =========================================================================

    def _directive_coc(self, context: Dict[str, Any], email: str = "") -> str:
        """
        policy.coc(email="community@novalym.com")
        Generates the Contributor Covenant Code of Conduct v2.1.
        """
        meta = self._get_metadata(context, email=email)
        return dedent(f"""
            # Contributor Covenant Code of Conduct

            ## Our Pledge

            We as members, contributors, and leaders pledge to make participation in our
            community a harassment-free experience for everyone, regardless of age, body
            size, visible or invisible disability, ethnicity, sex characteristics, gender
            identity and expression, level of experience, education, socio-economic status,
            nationality, personal appearance, race, religion, or sexual identity
            and orientation.

            We pledge to act and interact in ways that contribute to an open, welcoming,
            diverse, inclusive, and healthy community.

            ## Our Standards

            Examples of behavior that contributes to a positive environment for our
            community include:

            * Demonstrating empathy and kindness toward other people
            * Being respectful of differing opinions, viewpoints, and experiences
            * Giving and gracefully accepting constructive feedback
            * Accepting responsibility and apologizing to those affected by our mistakes
            * Focusing on what is best not just for us as individuals, but for the
              overall community

            ## Enforcement

            Instances of abusive, harassing, or otherwise unacceptable behavior may be
            reported to the community leaders responsible for enforcement at
            **{meta['email']}**.

            All complaints will be reviewed and investigated promptly and fairly.

            ## Attribution

            This Code of Conduct is adapted from the [Contributor Covenant][homepage],
            version 2.1, available at
            [https://www.contributor-covenant.org/version/2/1/code_of_conduct.html][v2.1].

            [homepage]: https://www.contributor-covenant.org
            [v2.1]: https://www.contributor-covenant.org/version/2/1/code_of_conduct.html
        """).strip()

    # =========================================================================
    # == STRATUM 2: THE ARCHITECTURAL MEMORY (ADR)                           ==
    # =========================================================================

    def _directive_adr(self,
                       context: Dict[str, Any],
                       title: str,
                       status: str = "Proposed",
                       deciders: str = "",
                       context_text: str = "") -> str:
        """
        policy.adr(title="Use Postgres", status="Accepted")
        Generates an Architecture Decision Record (MADR format).
        """
        meta = self._get_metadata(context)
        deciders_line = f"* Deciders: {deciders}" if deciders else f"* Deciders: {meta['author']}"
        context_block = context_text or "[Describe the context and problem statement here.]"

        return dedent(f"""
            # ADR: {title}

            * Status: {status}
            * Date: {meta['date']}
            {deciders_line}

            ## Context and Problem Statement

            {context_block}

            ## Decision Drivers

            * [e.g., Performance requirements]
            * [e.g., Developer experience]
            * [e.g., Maintenance cost]

            ## Considered Options

            * [Option 1]
            * [Option 2]
            * [Option 3]

            ## Decision Outcome

            Chosen option: **[Option 1]**, because [justification. e.g., only option, which meets k.o. criterion decision driver | which resolves force force | ... | comes out best (see below)].

            ## Pros and Cons of the Options

            ### [Option 1]

            * Good, because [argument a]
            * Good, because [argument b]
            * Bad, because [argument c]
        """).strip()

    # =========================================================================
    # == STRATUM 3: THE GATEWAY OF CONTRIBUTION                              ==
    # =========================================================================

    def _directive_contributing(self, context: Dict[str, Any]) -> str:
        """
        policy.contributing()
        Generates a CONTRIBUTING.md guide.
        """
        meta = self._get_metadata(context)
        return dedent(f"""
            # Contributing to {meta['project']}

            First off, thanks for taking the time to contribute! ❤️

            ## Code of Conduct

            This project and everyone participating in it is governed by the
            [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

            ## How Can I Contribute?

            ### Reporting Bugs

            This section guides you through submitting a bug report for {meta['project']}. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

            ### Suggesting Enhancements

            This section guides you through submitting an enhancement suggestion, including completely new features and minor improvements to existing functionality.

            ### Pull Requests

            1.  Fork the repo and create your branch from `main`.
            2.  If you've added code that should be tested, add tests.
            3.  If you've changed APIs, update the documentation.
            4.  Ensure the test suite passes.
            5.  Make sure your code lints.

            ## Styleguides

            ### Git Commit Messages

            * Use the present tense ("Add feature" not "Added feature")
            * Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
            * Limit the first line to 72 characters or less
            * Reference issues and pull requests liberally after the first line

            ## Tools

            * We use [Velm](https://velm.dev) for architectural governance.
            * We use [Conventional Commits](https://www.conventionalcommits.org/).
        """).strip()

    def _directive_pr_template(self, context: Dict[str, Any]) -> str:
        """
        policy.pr_template()
        Generates a .github/PULL_REQUEST_TEMPLATE.md.
        """
        return dedent("""
            ## Description

            Please include a summary of the change and which issue is fixed. Please also include relevant motivation and context.

            Fixes # (issue)

            ## Type of change

            - [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
            - [ ] ✨ New feature (non-breaking change which adds functionality)
            - [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
            - [ ] 📝 Documentation update

            ## How Has This Been Tested?

            Please describe the tests that you ran to verify your changes.

            - [ ] Unit Test A
            - [ ] Integration Test B

            ## Checklist:

            - [ ] My code follows the style guidelines of this project
            - [ ] I have performed a self-review of my own code
            - [ ] I have commented my code, particularly in hard-to-understand areas
            - [ ] I have made corresponding changes to the documentation
            - [ ] My changes generate no new warnings
            - [ ] I have added tests that prove my fix is effective or that my feature works
            - [ ] New and existing unit tests pass locally with my changes
        """).strip()

    def _directive_issue_bug(self, context: Dict[str, Any]) -> str:
        """policy.issue_bug() -> GitHub Issue Template"""
        return dedent("""
            ---
            name: Bug report
            about: Create a report to help us improve
            title: ''
            labels: bug
            assignees: ''
            ---

            **Describe the bug**
            A clear and concise description of what the bug is.

            **To Reproduce**
            Steps to reproduce the behavior:
            1. Go to '...'
            2. Click on '...'
            3. Scroll down to '...'
            4. See error

            **Expected behavior**
            A clear and concise description of what you expected to happen.

            **Screenshots**
            If applicable, add screenshots to help explain your problem.

            **Desktop (please complete the following information):**
             - OS: [e.g. iOS]
             - Browser [e.g. chrome, safari]
             - Version [e.g. 22]

            **Additional context**
            Add any other context about the problem here.
        """).strip()

    # =========================================================================
    # == STRATUM 4: THE CHRONICLE (CHANGELOG)                                ==
    # =========================================================================

    def _directive_changelog(self, context: Dict[str, Any]) -> str:
        """
        policy.changelog()
        Generates a Keep-a-Changelog standard file.
        """
        meta = self._get_metadata(context)
        return dedent(f"""
            # Changelog

            All notable changes to this project will be documented in this file.

            The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
            and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

            ## [Unreleased]

            ### Added
            - Initial inception via Velm God-Engine.

            ## [0.1.0] - {meta['date']}

            ### Added
            - Project foundation established.
        """).strip()

    # =========================================================================
    # == STRATUM 5: THE FILE WARDEN (GITATTRIBUTES)                          ==
    # =========================================================================

    def _directive_gitattributes(self, context: Dict[str, Any]) -> str:
        """
        policy.gitattributes()
        Enforces line endings and linguistic detection.
        """
        return dedent("""
            # Auto-detect text files and perform LF normalization
            * text=auto

            # Custom for Windows
            *.bat      text eol=crlf
            *.ps1      text eol=crlf

            # Custom for Linux/Mac
            *.sh       text eol=lf
            *.py       text eol=lf
            *.js       text eol=lf
            *.ts       text eol=lf

            # Linguist Overrides
            *.scaffold linguist-language=Python
            *.symphony linguist-language=YAML

            # Binary Assets
            *.png binary
            *.jpg binary
            *.woff2 binary
            *.wasm binary
        """).strip()