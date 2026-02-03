# Path: scaffold/artisans/hover/command_grimoire.py
# -----------------------------------------------

"""
=================================================================================
== THE SUPREME GRIMOIRE OF KINETIC VERBS (V-Ω-ETERNAL-APOTHEOSIS-FINALIS)      ==
=================================================================================
LIF: INFINITY
AUTHORITY: IBQ-GENESISENGINE-PRIME

The definitive knowledge base for shell-level Gnosis. This file enables the
Hierophant to recognize and explain the kinetic intent of the Maestro's Edicts.
=================================================================================
"""

COMMAND_BINDINGS = {
    # =========================================================================
    # I. THE SCAFFOLD TRIAD (INTERNAL GOD-ENGINES)
    # =========================================================================
    "scaffold": {
        "title": "🏗️ The God-Engine",
        "desc": "The primary artisan of creation, transmutation, and architectural alignment.",
        "usage": "scaffold [rite] --root [sanctum]",
        "safety": "SACRED"
    },
    "symphony": {
        "title": "🎵 The Sovereign Conductor",
        "desc": "Orchestrates the Language of Will (.symphony) and complex automated workflows.",
        "usage": "symphony conduct [script.symphony]",
        "safety": "SACRED"
    },
    "apeiron": {
        "title": "🌌 The Infinite Core",
        "desc": "The legacy and internal kernel name of the Scaffold Engine's heart.",
        "usage": "N/A",
        "safety": "SACRED"
    },

    # =========================================================================
    # II. VCS & CELESTIAL REPOSITORIES (CHRONOMANCY)
    # =========================================================================
    "git": {
        "title": "📜 The Chronomancer",
        "desc": "Manages the temporal history, versioning, and branching of the project reality.",
        "usage": "git [commit|push|pull|branch|merge|rebase]",
        "safety": "SAFE"
    },
    "gh": {
        "title": "🌐 The GitHub Emissary",
        "desc": "Communes with the GitHub celestial realm for Pull Requests, Issues, and Actions.",
        "usage": "gh [pr|issue|run|repo] [list|create|view]",
        "safety": "SAFE"
    },
    "glab": {
        "title": "🦊 The GitLab Emissary",
        "desc": "The primary interface for interacting with the GitLab forge.",
        "usage": "glab [mr|issue|pipeline] status",
        "safety": "SAFE"
    },

    # =========================================================================
    # III. CLOUD REALMS (CELESTIAL PROVIDERS)
    # =========================================================================
    "aws": {
        "title": "☁️ The Amazonian Cloud-King",
        "desc": "Manages resources in the AWS celestial realm.",
        "usage": "aws s3 sync . s3://my-bucket",
        "safety": "DANGEROUS"
    },
    "gcloud": {
        "title": "🌈 The Google Cloud Prophet",
        "desc": "Commands the GCP (Google Cloud Platform) infrastructure.",
        "usage": "gcloud compute instances list",
        "safety": "DANGEROUS"
    },
    "az": {
        "title": "🟦 The Azure Warden",
        "desc": "Manages the Microsoft Azure cloud ecosystem.",
        "usage": "az webapp up",
        "safety": "DANGEROUS"
    },

    # =========================================================================
    # IV. CONTAINER & INFRASTRUCTURE (CELESTIAL VESSELS)
    # =========================================================================
    "docker": {
        "title": "🐳 The Vessel Smith",
        "desc": "Forges, manages, and executes isolated celestial containers.",
        "usage": "docker [build|run|ps|rmi|exec]",
        "safety": "CAUTIOUS"
    },
    "docker-compose": {
        "title": "🚢 The Fleet Admiral",
        "desc": "Orchestrates multi-vessel realities and complex local environments.",
        "usage": "docker-compose [up|down|logs|restart]",
        "safety": "CAUTIOUS"
    },
    "kubectl": {
        "title": "☸️ The Star-Cluster Pilot",
        "desc": "The primary interface for commanding the Kubernetes star-cluster.",
        "usage": "kubectl [get|describe|apply|delete|logs] [resource]",
        "safety": "DANGEROUS"
    },
    "helm": {
        "title": "⛑️ The Chart Weaver",
        "desc": "The package manager for Kubernetes. Manages complex deployments (Charts).",
        "usage": "helm [install|upgrade|rollback] [release] [chart]",
        "safety": "DANGEROUS"
    },
    "terraform": {
        "title": "🏗️ The World Weaver",
        "desc": "Inscribes the immutable laws of infrastructure-as-code.",
        "usage": "terraform [init|plan|apply|destroy]",
        "safety": "DANGEROUS"
    },
    "pulumi": {
        "title": "🪄 The Code-to-Cloud Alchemist",
        "desc": "Modern IaC using familiar programming languages.",
        "usage": "pulumi [up|preview|destroy]",
        "safety": "DANGEROUS"
    },

    # =========================================================================
    # V. WEB HARVESTERS & NETWORKING
    # =========================================================================
    "curl": {
        "title": "📡 The Ethereal Harvester",
        "desc": "The standard tool for transferring data via URL protocols.",
        "usage": "curl -X [GET|POST] -H 'Content-Type: application/json' [url]",
        "safety": "SAFE"
    },
    "wget": {
        "title": "🎣 The Deep Fisher",
        "desc": "A non-interactive network downloader for retrieving files from the web aether.",
        "usage": "wget -r [url]",
        "safety": "SAFE"
    },
    "http": {
        "title": "🌈 The Luminous Requestor",
        "desc": "HTTPie: A user-friendly, modern CLI for human-to-API communion.",
        "usage": "http POST example.org name=Gnosis",
        "safety": "SAFE"
    },
    "ssh": {
        "title": "🔑 The Secret Gate-Key",
        "desc": "Establishes an encrypted link to a remote mortal shell.",
        "usage": "ssh user@remote-sanctum",
        "safety": "CAUTIOUS"
    },

    # =========================================================================
    # VI. NODE & JAVASCRIPT ECOSYSTEM
    # =========================================================================
    "npm": {
        "title": "📦 The Node Weaver",
        "desc": "The standard manager for JavaScript dependency souls.",
        "usage": "npm [install|run|test|publish]",
        "safety": "SAFE"
    },
    "npx": {
        "title": "⚡ The Ephemeral Messenger",
        "desc": "Executes a Node-based rite without persistent local installation.",
        "usage": "npx [artisan] [args]",
        "safety": "SAFE"
    },
    "yarn": {
        "title": "🧶 The Fast Weaver",
        "desc": "A high-performance alternative Node dependency manager.",
        "usage": "yarn [add|remove|start]",
        "safety": "SAFE"
    },
    "pnpm": {
        "title": "🔗 The Efficient Weaver",
        "desc": "A fast, disk-space efficient Node manager using Gnostic symlinks.",
        "usage": "pnpm [install|add|run]",
        "safety": "SAFE"
    },
    "bun": {
        "title": "🥟 The Swift Soul",
        "desc": "A high-performance JavaScript runtime, package manager, and test runner.",
        "usage": "bun [run|install|test]",
        "safety": "SAFE"
    },
    "tsc": {
        "title": "📘 The Type Consecrator",
        "desc": "The TypeScript compiler. Transmutes type-safe Gnosis into raw JS.",
        "usage": "tsc --noEmit",
        "safety": "SAFE"
    },
    "vite": {
        "title": "⚡ The Radiant Assembler",
        "desc": "A hyper-fast frontend build tool and development server.",
        "usage": "vite build",
        "safety": "SAFE"
    },

    # =========================================================================
    # VII. PYTHON ECOSYSTEM
    # =========================================================================
    "python": {
        "title": "🐍 The Prime Serpent",
        "desc": "The foundational interpreter of our cosmos and primary host for Scaffold.",
        "usage": "python [script.py] --arg value",
        "safety": "SAFE"
    },
    "pip": {
        "title": "💊 The Soul Inhaler",
        "desc": "The primary package installer for the Python ecosystem.",
        "usage": "pip install [package_name]",
        "safety": "SAFE"
    },
    "poetry": {
        "title": "📜 The Gnostic Poet",
        "desc": "A comprehensive dependency manager and packager for modern Python projects.",
        "usage": "poetry [add|remove|install|run|build]",
        "safety": "SAFE"
    },
    "ruff": {
        "title": "✨ The Quick Inquisitor",
        "desc": "A hyper-fast Python linter and formatter that replaces Flake8, Isort, and Black.",
        "usage": "ruff check .",
        "safety": "SAFE"
    },
    "pytest": {
        "title": "🧪 The Adjudicator's Lens",
        "desc": "The standard tool for verifying the logical purity of Python scriptures.",
        "usage": "pytest -v tests/",
        "safety": "SAFE"
    },
    "black": { "title": "🌑 The Totalitarian Formatter", "desc": "Enforces an uncompromising Gnostic style upon Python code.", "usage": "black .", "safety": "SAFE" },
    "uv": { "title": "🚀 The Astral Speedster", "desc": "An extremely fast Python package installer and resolver written in Rust.", "usage": "uv pip install", "safety": "SAFE" },
}


COMMAND_BINDINGS.update({
    # =========================================================================
    # VIII. SYSTEM RITES (MANIPULATING MATTER)
    # =========================================================================
    "mkdir": {
        "title": "📂 The Sanctum Forger",
        "desc": "Forges a new physical directory in the mortal realm.",
        "usage": "mkdir -p [path/to/sanctum]",
        "safety": "SAFE"
    },
    "cp": {
        "title": "👥 The Soul Cloner",
        "desc": "Duplicates a scripture's soul into a new physical location.",
        "usage": "cp -r [source] [destination]",
        "safety": "SAFE"
    },
    "mv": {
        "title": "➡️ The Translocator",
        "desc": "Moves a scripture or sanctum through the filesystem's spacetime.",
        "usage": "mv [old_path] [new_path]",
        "safety": "SAFE"
    },
    "ls": {
        "title": "👁️ The Surveyor",
        "desc": "Lists the manifest of a sanctum, revealing the souls within.",
        "usage": "ls -la [path]",
        "safety": "SAFE"
    },
    "find": {
        "title": "🔍 The Seeker",
        "desc": "Performs a recursive search for scriptures matching specific Gnostic criteria.",
        "usage": "find . -name '*.scaffold'",
        "safety": "SAFE"
    },
    "cat": {
        "title": "📖 The Scribe's Reader",
        "desc": "Streams the entire soul of a scripture to the standard output.",
        "usage": "cat [scripture.txt]",
        "safety": "SAFE"
    },
    "grep": {
        "title": "🔦 The Pattern Searcher",
        "desc": "Filters streams of Gnosis for specific textual resonances.",
        "usage": "grep -r 'TODO' .",
        "safety": "SAFE"
    },
    "sed": {
        "title": "🖋️ The Stream Editor",
        "desc": "Performs basic alchemical transmutations on text streams.",
        "usage": "sed -i 's/old/new/g' [file]",
        "safety": "CAUTIOUS"
    },
    "awk": {
        "title": "📊 The Data Weaver",
        "desc": "A powerful language for scanning and processing structured patterns.",
        "usage": "awk '{print $1}' [file]",
        "safety": "SAFE"
    },
    "chmod": {
        "title": "⚖️ The Consecrator",
        "desc": "Alters the access permissions (The Vow of Privacy) of a scripture.",
        "usage": "chmod +x [script.sh]",
        "safety": "CAUTIOUS"
    },
    "chown": {
        "title": "👤 The Identity Shifter",
        "desc": "Changes the owner of a scripture in the mortal realm.",
        "usage": "chown [user]:[group] [file]",
        "safety": "DANGEROUS"
    },

    # =========================================================================
    # IX. ANNIHILATION RITES (THE PROFANE VOID)
    # =========================================================================
    "rm": {
        "title": "💀 The Eraser",
        "desc": "Returns a scripture or sanctum to the void. Irreversible without a Ledger.",
        "usage": "rm -rf [target]",
        "safety": "DANGEROUS"
    },
    "kill": {
        "title": "🔫 The Executioner",
        "desc": "Sends a termination sigil to a living process.",
        "usage": "kill -9 [pid]",
        "safety": "DANGEROUS"
    },
    "taskkill": {
        "title": "🔨 The Soul Crusher",
        "desc": "Forcefully terminates a Windows process tree. Use for stuck Daemons.",
        "usage": "taskkill /F /T /PID [pid]",
        "safety": "DANGEROUS"
    },

    # =========================================================================
    # X. POLYGLOT ARTISANS (FOREIGN COVENANTS)
    # =========================================================================
    "cargo": {
        "title": "🦀 The Iron Scribe",
        "desc": "The package manager and build tool for the Rust cosmos.",
        "usage": "cargo [build|run|test|check]",
        "safety": "SAFE"
    },
    "rustc": {
        "title": "⚙️ The Iron Smith",
        "desc": "The low-level Rust compiler used by the Fusion Core.",
        "usage": "rustc [file.rs]",
        "safety": "SAFE"
    },
    "go": {
        "title": "🐹 The Gopher King",
        "desc": "Builds and manages the concurrent souls of the Go ecosystem.",
        "usage": "go [build|run|mod tidy]",
        "safety": "SAFE"
    },
    "java": {
        "title": "☕ The Ancient Sentinel",
        "desc": "Executes compiled Gnosis within the JVM (Java Virtual Machine).",
        "usage": "java -jar [app.jar]",
        "safety": "SAFE"
    },
    "ruby": {
        "title": "💎 The Radiant Gem",
        "desc": "The interpreter for the Ruby tongue.",
        "usage": "ruby [script.rb]",
        "safety": "SAFE"
    },
    "gem": { "title": "📦 The Gem Merchant", "desc": "Package manager for Ruby.", "usage": "gem install [name]", "safety": "SAFE" },
    "rake": { "title": "🧹 The Task Master", "desc": "Build utility for Ruby projects.", "usage": "rake [task]", "safety": "SAFE" },

    # =========================================================================
    # XI. EDITOR & CELESTIAL TOOLING
    # =========================================================================
    "code": {
        "title": "👁️ The Omniscient Eye",
        "desc": "VS Code CLI. Opens scriptures or sanctums for the Architect's Gaze.",
        "usage": "code [file|directory]",
        "safety": "SAFE"
    },
    "make": {
        "title": "🛠️ The Ancient Architect",
        "desc": "The Old Testament build system. Orchestrates complex shell-level rites.",
        "usage": "make [target] -j8",
        "safety": "SAFE"
    },
    "openssl": {
        "title": "🛡️ The Cryptographic Mason",
        "desc": "Forges and verifies the sacred seals (SSL/TLS certificates).",
        "usage": "openssl genrsa -out key.pem 2048",
        "safety": "CAUTIOUS"
    },
    "gpg": {
        "title": "🔏 The Keeper of the Keyring",
        "desc": "Signs and encrypts scriptures to ensure Gnostic provenance.",
        "usage": "gpg --sign [blueprint]",
        "safety": "SAFE"
    },
    "sudo": {
        "title": "👑 The Royal Decree",
        "desc": "Escalates a rite to superuser status. Use with extreme prejudice.",
        "usage": "sudo [command]",
        "safety": "CRITICAL"
    },
})

COMMAND_BINDINGS.update({
    # =========================================================================
    # XI. THE SCAFFOLD RITES (INTERNAL SOVEREIGNTY)
    # =========================================================================
    "scaffold save": {
        "title": "💾 The Neural Scribe",
        "desc": "An AI-augmented commit rite. Gazes at staged flux, generates Conventional Commit Gnosis, and runs the Lazarus Self-Healing protocol if tests fail.",
        "usage": "scaffold save 'feat: add auth'",
        "safety": "SAFE"
    },
    "scaffold weave": {
        "title": "🕸️ The Pattern Weaver",
        "desc": "Materializes an Archetype (multi-file pattern) from the Gnostic Forge into the living fabric of the project.",
        "usage": "scaffold weave [archetype] [target_dir]",
        "safety": "SAFE"
    },
    "scaffold adopt": {
        "title": "⚓ The Gnostic Anchor",
        "desc": "Brings an unmanaged directory under the control of the God-Engine by forging a `scaffold.lock` and initial blueprint.",
        "usage": "scaffold adopt [path]",
        "safety": "CAUTIOUS"
    },
    "scaffold distill": {
        "title": "⚗️ The Alchemical Distiller",
        "desc": "Reverse-materialization. Transmutes an existing directory into an executable `.scaffold` blueprint.",
        "usage": "scaffold distill [path] --output [file]",
        "safety": "SAFE"
    },
    "scaffold transmute": {
        "title": "⚡ The Rite of Sync",
        "desc": "Forces the mortal realm (disk) into perfect alignment with the Gnostic Law (blueprint). Performs non-destructive diffs first.",
        "usage": "scaffold transmute [blueprint]",
        "safety": "CAUTIOUS"
    },
    "scaffold blame": {
        "title": "🧐 The Forensic Seer",
        "desc": "Reconstructs the causal history of a single scripture, revealing who willed it and which transaction last transfigured it.",
        "usage": "scaffold blame [path]",
        "safety": "SAFE"
    },

    # =========================================================================
    # XII. THE HIGH INQUISITORS (FORENSICS & MONITORING)
    # =========================================================================
    "systemctl": {
        "title": "⚙️ The System Governor",
        "desc": "The primary interface for commanding Systemd services and units.",
        "usage": "systemctl [start|stop|status|restart] [service]",
        "safety": "DANGEROUS"
    },
    "journalctl": {
        "title": "📖 The Eternal Log-Book",
        "desc": "Queries the system's binary journal logs for forensic diagnostics.",
        "usage": "journalctl -u [service] -f",
        "safety": "SAFE"
    },
    "top": { "title": "📈 The Resource Gazer", "desc": "Live display of process vital signs (CPU/RAM).", "usage": "top", "safety": "SAFE" },
    "htop": { "title": "📊 The Luminous Monitor", "desc": "Advanced, interactive resource monitor with process-tree visualization.", "usage": "htop", "safety": "SAFE" },
    "ps": { "title": "👻 The Spirit Tracer", "desc": "Snapshots the current processes manifest in the system.", "usage": "ps aux | grep [name]", "safety": "SAFE" },
    "df": { "title": "💾 The Space Sentinel", "desc": "Reports the remaining capacity of the mortal disk sanctums.", "usage": "df -h", "safety": "SAFE" },
    "du": { "title": "⚖️ The Mass Calculator", "desc": "Measures the physical size (mass) of a directory or file.", "usage": "du -sh [path]", "safety": "SAFE" },

    # =========================================================================
    # XIII. THE WARDS OF SECURITY (AUDITORS)
    # =========================================================================
    "nmap": { "title": "🛰️ The Network Surveyor", "desc": "Performs deep port-scanning and network discovery.", "usage": "nmap -A [host]", "safety": "DANGEROUS" },
    "snyk": { "title": "🛡️ The Vulnerability Ward", "desc": "Scans dependency souls for known security heresies.", "usage": "snyk test", "safety": "SAFE" },
    "trivy": { "title": "🐳 The Container Auditor", "desc": "Comprehensive security scanner for celestial vessels (images) and config files.", "usage": "trivy image [name]", "safety": "SAFE" },
    "bandit": { "title": "🐍 The Python Sentinel", "desc": "Scans Python source code for common security pitfalls.", "usage": "bandit -r src/", "safety": "SAFE" },

    # =========================================================================
    # XIV. THE ARCHIVE MANTLE (MATTER COMPRESSION)
    # =========================================================================
    "tar": { "title": "📦 The Tape Weaver", "desc": "Encapsulates multiple scriptures into a single archive (Tape Archive).", "usage": "tar -czvf [name.tar.gz] [path]", "safety": "SAFE" },
    "zip": { "title": "🤐 The Compressor", "desc": "Forges a compressed ZIP archive from physical files.", "usage": "zip -r [name.zip] [path]", "safety": "SAFE" },
    "unzip": { "title": "🔓 The Liberator", "desc": "Extracts souls from a ZIP container back into the mortal realm.", "usage": "unzip [file.zip]", "safety": "SAFE" },
})


COMMAND_BINDINGS.update({
    # --- GIT SUB-COMMANDS (THE CHRONOMANCER'S ARTS) ---
    "git add": {
        "title": "➕ Git: Stage Changes",
        "desc": "Transmutes modified content in the working tree into the Gnostic Index (Staging Area).",
        "usage": "git add [file|.]", "safety": "SAFE"
    },
    "git commit": {
        "title": "💾 Git: Inscribe History",
        "desc": "Enshrines the staged index as a permanent verse in the project's chronicle.",
        "usage": "git commit -m 'message'", "safety": "SAFE"
    },
    "git checkout": {
        "title": "🔄 Git: Spacetime Jump",
        "desc": "Switches branches or restores working tree files to a previous state.",
        "usage": "git checkout [branch|file]", "safety": "CAUTIOUS"
    },
    "git branch": {
        "title": "🌿 Git: Timeline Fork",
        "desc": "Lists, creates, or deletes the parallel timelines (branches) of the project.",
        "usage": "git branch [name]", "safety": "SAFE"
    },
    "git status": {
        "title": "👁️ Git: Gaze upon Flux",
        "desc": "Shows the difference between the Index, the HEAD, and the Working Tree.",
        "usage": "git status", "safety": "SAFE"
    },
    "git push": {
        "title": "🚀 Git: Celestial Proclamation",
        "desc": "Transmits local history to a remote celestial repository.",
        "usage": "git push origin [branch]", "safety": "CAUTIOUS"
    },
    "git pull": {
        "title": "📥 Git: Celestial Inhalation",
        "desc": "Fetches and integrates Gnosis from a remote repository into the local branch.",
        "usage": "git pull origin [branch]", "safety": "CAUTIOUS"
    },

    # --- DOCKER SUB-COMMANDS (THE VESSEL SMITH'S RITES) ---
    "docker run": {
        "title": "🏃 Docker: Ignite Vessel",
        "desc": "Creates and starts a new container instance from an image soul.",
        "usage": "docker run --rm -it [image]", "safety": "CAUTIOUS"
    },
    "docker build": {
        "title": "⚒️ Docker: Forge Vessel",
        "desc": "Transmutes a Dockerfile scripture into a shippable image artifact.",
        "usage": "docker build -t [name] .", "safety": "SAFE"
    },
    "docker exec": {
        "title": "🧠 Docker: Mental Projection",
        "desc": "Runs a command inside an already living container process.",
        "usage": "docker exec -it [container] bash", "safety": "CAUTIOUS"
    },
    "docker rmi": {
        "title": "🔥 Docker: Annihilate Image",
        "desc": "Returns an image artifact to the void to reclaim disk mass.",
        "usage": "docker rmi [image_id]", "safety": "DANGEROUS"
    },
    "docker ps": {
        "title": "📋 Docker: Vessel Census",
        "desc": "Lists the living and dormant containers currently manifest.",
        "usage": "docker ps -a", "safety": "SAFE"
    },

    # --- NODE & NPM RITES ---
    "npm install": {
        "title": "📥 NPM: Summon Dependencies",
        "desc": "Downloads and installs library souls defined in package.json.",
        "usage": "npm install [package]", "safety": "SAFE"
    },
    "npm run": {
        "title": "🏃 NPM: Conduct Script",
        "desc": "Executes a named automation rite defined in the package manifest.",
        "usage": "npm run [script_name]", "safety": "SAFE"
    },
    "npm ci": {
        "title": "🛡️ NPM: Clean Inception",
        "desc": "Performs a deterministic, strictly warded installation for CI/CD.",
        "usage": "npm ci", "safety": "SAFE"
    },
})

COMMAND_BINDINGS.update({
    # =========================================================================
    # XV. INFRASTRUCTURE & ORCHESTRATION (THE ARCHITECT'S WILL)
    # =========================================================================
    "pulumi preview": {
        "title": "🪄 Pulumi: Simulation",
        "desc": "Simulates the materialization of infrastructure to show the Gnostic Delta before it is willed into the cloud.",
        "usage": "pulumi preview", "safety": "SAFE"
    },
    "terraform workspace list": {
        "title": "🏗️ Terraform: Realm Census",
        "desc": "Lists the active parallel realities (workspaces) managed by the state.",
        "usage": "terraform workspace list", "safety": "SAFE"
    },
    "kubectl port-forward": {
        "title": "🚇 K8s: Quantum Tunnel",
        "desc": "Forges a temporary link between a local port and a pod in the star-cluster.",
        "usage": "kubectl port-forward [pod] [port]", "safety": "CAUTIOUS"
    },
    "kubectl rollout status": {
        "title": "📈 K8s: Deployment Pulse",
        "desc": "Watches the state of a deployment transition in real-time.",
        "usage": "kubectl rollout status deployment/[name]", "safety": "SAFE"
    },
    "kubectl exec -it": {
        "title": "🧠 K8s: Core Projection",
        "desc": "Opens an interactive conduit into a living pod.",
        "usage": "kubectl exec -it [pod] -- /bin/bash", "safety": "DANGEROUS"
    },

    # =========================================================================
    # XVI. VCS ADVANCED RITES (TEMPORAL RECOVERY)
    # =========================================================================
    "git remote -v": {
        "title": "🌐 Git: Celestial Links",
        "desc": "Lists the upstream repositories this project is bonded to.",
        "usage": "git remote -v", "safety": "SAFE"
    },
    "git cherry-pick": {
        "title": "🍒 Git: Verse Grafting",
        "desc": "Surgically copies a specific commit from one timeline into the current one.",
        "usage": "git cherry-pick [commit_hash]", "safety": "CAUTIOUS"
    },
    "git stash pop": {
        "title": "📤 Git: Resurrect Flux",
        "desc": "Retrieves the most recently hidden flux from the temporal buffer.",
        "usage": "git stash pop", "safety": "SAFE"
    },
    "git reset --hard": {
        "title": "🛑 Git: Timeline Rewind",
        "desc": "Forcefully resets the working tree to a previous state, annihilating all uncommitted flux.",
        "usage": "git reset --hard [hash]", "safety": "CRITICAL"
    },

    # =========================================================================
    # XVII. SYSTEM HYGIENE & DB CONDUITS
    # =========================================================================
    "docker system prune": {
        "title": "🧹 Docker: Deep Cleanse",
        "desc": "Annihilates all unused containers, networks, and images to reclaim host mass.",
        "usage": "docker system prune -a", "safety": "DANGEROUS"
    },
    "docker volume ls": {
        "title": "💾 Docker: Mass Census",
        "desc": "Lists the persistent data sanctums (volumes) willed into existence.",
        "usage": "docker volume ls", "safety": "SAFE"
    },
    "psql": {
        "title": "🐘 Postgres: Oracle Entry",
        "desc": "The primary interactive terminal for the PostgreSQL database.",
        "usage": "psql -U [user] -d [db]", "safety": "CAUTIOUS"
    },
    "redis-cli monitor": {
        "title": "📡 Redis: Live Pulse",
        "desc": "Streams every command perceived by the Redis server in real-time.",
        "usage": "redis-cli monitor", "safety": "SAFE"
    },
    "ollama run": {
        "title": "🧠 Ollama: Neural Ignition",
        "desc": "Launches a local large language model for private Gnostic processing.",
        "usage": "ollama run [model_name]", "safety": "SAFE"
    },

    # =========================================================================
    # XVIII. UTILITY & SECURITY RITES (THE MORTAL TOOLS)
    # =========================================================================
    "ssh-keygen": {
        "title": "🔑 Key Forger",
        "desc": "Forges new RSA/EdDSA keys for secure celestial communion.",
        "usage": "ssh-keygen -t ed25519", "safety": "SAFE"
    },
    "lsof -i": {
        "title": "👂 Port Listener",
        "desc": "Identifies which processes are currently listening on the network aether.",
        "usage": "lsof -i :[port]", "safety": "SAFE"
    },
    "brew upgrade": {
        "title": "🍺 Brew: Higher Gnosis",
        "desc": "Updates all manifest system artisans to their latest versions.",
        "usage": "brew upgrade", "safety": "SAFE"
    },
    "systemctl daemon-reload": {
        "title": "🔄 Systemd: Mind Refresh",
        "desc": "Commands the OS to re-parse all service definitions after transfiguration.",
        "usage": "systemctl daemon-reload", "safety": "CAUTIOUS"
    },
    "crontab -e": {
        "title": "⏰ Chronos Scheduler",
        "desc": "Edits the list of recurring rites scheduled to execute in the background.",
        "usage": "crontab -e", "safety": "DANGEROUS"
    },
    "dig +short": {
        "title": "🗺️ DNS Seer",
        "desc": "Queries the celestial name records for a concise IP mapping.",
        "usage": "dig +short example.org", "safety": "SAFE"
    },
})



COMMAND_BINDINGS.update({
    # --- VCS: TEMPORAL MANIPULATION (GIT) ---
    "git stash list": {
        "title": "📤 Git: Temporal Buffer Census",
        "desc": "Lists the fragments of flux currently held in the temporal stash, waiting to be resurrected.",
        "usage": "git stash list", "safety": "SAFE"
    },
    "git log -n": {
        "title": "📜 Git: Limited Historical Gaze",
        "desc": "Displays a truncated chronicle of the project's timeline, focusing only on the last N verses.",
        "usage": "git log -n 5", "safety": "SAFE"
    },
    "git commit --amend": {
        "title": "🖋️ Git: Temporal Retrofit",
        "desc": "Transfigures the most recent verse in the chronicle, allowing the Architect to correct errors or add forgotten Gnosis without creating a new commit.",
        "usage": "git commit --amend -m 'new message'", "safety": "CAUTIOUS"
    },
    "git push -u": {
        "title": "🔗 Git: Upstream Bonding",
        "desc": "Transmits local history and establishes a persistent tracking link between the local branch and its celestial counterpart.",
        "usage": "git push -u origin [branch]", "safety": "SAFE"
    },

    # --- INFRASTRUCTURE: KINETIC ORCHESTRATION (DOCKER) ---
    "docker run -p": {
        "title": "🚇 Docker: Port Portal Forge",
        "desc": "Spawns a container and forges a network wormhole between a host port and a container port.",
        "usage": "docker run -p 8080:80 [image]", "safety": "CAUTIOUS"
    },
    "docker run -v": {
        "title": "💾 Docker: Mass Volume Binding",
        "desc": "Mounts a physical sanctum from the host machine directly into the container's reality for persistent data storage.",
        "usage": "docker run -v /host/path:/container/path [image]", "safety": "CAUTIOUS"
    },
    "docker system prune": {
        "title": "🧹 Docker: Deep Cleanse",
        "desc": "Annihilates all unused containers, networks, and images to reclaim host mass. A ruthless purification.",
        "usage": "docker system prune -a", "safety": "DANGEROUS"
    },

    # --- NODE: ECOSYSTEM EVOLUTION (NPM) ---
    "npm install --save-dev": {
        "title": "🛠️ NPM: Developer Soul Binding",
        "desc": "Adds a dependency that is only required for the creation and adjudication phases (development), not for the final manifestation.",
        "usage": "npm i -D [package]", "safety": "SAFE"
    },
    "npm run dev": {
        "title": "🧪 NPM: Igniting the Sandbox",
        "desc": "Launches the development environment, often with a live-reloading Gaze to see changes manifest in real-time.",
        "usage": "npm run dev", "safety": "SAFE"
    },
    "npm audit fix": {
        "title": "🛡️ NPM: Automated Purification",
        "desc": "Scans the dependency tree for security heresies and automatically applies the recommended cures.",
        "usage": "npm audit fix", "safety": "SAFE"
    },

    # --- PYTHON: ISOLATED REALITIES ---
    "python -m venv": {
        "title": "🪐 Python: Isolated Realm Genesis",
        "desc": "Forges a new, hermetically sealed virtual environment to isolate the project's library dependencies from the host system.",
        "usage": "python -m venv .venv", "safety": "SAFE"
    },
    "pip install -U": {
        "title": "🚀 Pip: Soul Evolution",
        "desc": "Upgrades a manifest package to its latest, most enlightened form.",
        "usage": "pip install -U [package]", "safety": "SAFE"
    },

    # --- K8S & CLOUD: CELESTIAL CONTROL ---
    "kubectl get configmap": {
        "title": "🗃️ K8s: Static Gnosis Census",
        "desc": "Lists the key-value configuration sanctums currently manifest in the cluster.",
        "usage": "kubectl get cm", "safety": "SAFE"
    },
    "kubectl delete pod": {
        "title": "🔫 K8s: Surgical Annihilation",
        "desc": "Returns a specific living pod to the void. The cluster will immediately attempt to resurrect a new one.",
        "usage": "kubectl delete pod [name]", "safety": "DANGEROUS"
    },
    "aws configure list": {
        "title": "👤 AWS: Identity Census",
        "desc": "Proclaims which celestial credentials and regions are currently being used to conduct rites.",
        "usage": "aws configure list", "safety": "SAFE"
    },
    "gcloud auth list": {
        "title": "🔑 GCP: Credential Gaze",
        "desc": "Lists the authenticated identities manifest in the Google Cloud SDK.",
        "usage": "gcloud auth list", "safety": "SAFE"
    },

    # --- SYSTEM & UTILITY ---
    "openssl s_client -connect": {
        "title": "📡 OpenSSL: Ethereal Handshake Probe",
        "desc": "Performs a direct TLS handshake with a remote host to verify certificate integrity.",
        "usage": "openssl s_client -connect [host]:443", "safety": "SAFE"
    },
    "ssh-add -l": {
        "title": "🗝️ SSH: Key Census",
        "desc": "Lists the fingerprints of all secret gate-keys currently held by the SSH Agent.",
        "usage": "ssh-add -l", "safety": "SAFE"
    },
    "go mod download": {
        "title": "📥 Go: Inhaling the Gopher Soul",
        "desc": "Downloads the specific versions of modules willed in the `go.mod` manifest to the local cache.",
        "usage": "go mod download", "safety": "SAFE"
    },
    "shadcn-ui@latest add": {
        "title": "🎨 Shadcn: Weaving Visual Organs",
        "desc": "Surgically injects beautifully forged UI components into your React project.",
        "usage": "npx shadcn-ui@latest add [component]", "safety": "SAFE"
    },
})



COMMAND_BINDINGS.update({
    # =========================================================================
    # XV. THE ETERNAL STREAMS (LOGGING & VIGILANCE)
    # =========================================================================
    "tail -f": {
        "title": "🚀 The Eternal Vigil",
        "desc": "Follows the soul of a scripture in real-time. As new verses are inscribed, they are instantly proclaimed to the standard output.",
        "usage": "tail -f [logfile.log]", "safety": "SAFE"
    },
    "watch -n": {
        "title": "⏰ The Pulsing Vigil",
        "desc": "Repeatedly conducts a rite at a specific Gnostic interval, allowing the Architect to observe the flux of reality.",
        "usage": "watch -n 2 'ls -la'", "safety": "SAFE"
    },
    "xargs": {
        "title": "⛓️ The Pipe Multiplier",
        "desc": "Transmutes standard input into arguments for other edicts. The bridge between the river of data and the hand of action.",
        "usage": "find . -name '*.tmp' | xargs rm", "safety": "CAUTIOUS"
    },

    # =========================================================================
    # XVI. NETWORK CARTOGRAPHY (ETHEREAL LINKS)
    # =========================================================================
    "netstat -an": {
        "title": "🕸️ The Network Grid",
        "desc": "Displays all active network connections and listening ports manifest in this reality.",
        "usage": "netstat -an | grep LISTEN", "safety": "SAFE"
    },
    "ping": {
        "title": "🏓 The Echo Probe",
        "desc": "Sends a heartbeat to a remote host to measure the latency and vitality of the celestial link.",
        "usage": "ping -c 4 [host]", "safety": "SAFE"
    },
    "nslookup": {
        "title": "🗺️ The Celestial Navigator",
        "desc": "Queries the celestial name servers to resolve a domain's IP soul.",
        "usage": "nslookup [domain.com]", "safety": "SAFE"
    },
    "ssh-copy-id": {
        "title": "📂 The Identity Projector",
        "desc": "Transmits your public gate-key to a remote sanctum to enable passwordless celestial communion.",
        "usage": "ssh-copy-id user@host", "safety": "SAFE"
    },

    # =========================================================================
    # XVII. SPACETIME MULTIPLEXING (PERSISTENCE)
    # =========================================================================
    "tmux": {
        "title": "🪟 The Multiplexed Sanctuary",
        "desc": "Forges a persistent terminal reality that survives the closing of the mortal shell (SSH session).",
        "usage": "tmux [attach|new-session]", "safety": "SAFE"
    },
    "screen": {
        "title": "📺 The Ancient Sanctuary",
        "desc": "The legacy terminal multiplexer for managing long-running background rites.",
        "usage": "screen -S [name]", "safety": "SAFE"
    },

    # =========================================================================
    # XVIII. ADVANCED VCS & RUNTIME RITES
    # =========================================================================
    "git rebase -i": {
        "title": "🖋️ Git: The Temporal Editor",
        "desc": "Opens the interactive timeline editor, allowing the Architect to squash, edit, or reorder the verses of history.",
        "usage": "git rebase -i HEAD~[N]", "safety": "DANGEROUS"
    },
    "git diff --staged": {
        "title": "👁️ Git: The Staging Gaze",
        "desc": "Perceives the difference between the Gnostic Index and the last commit, revealing the truth of the next save.",
        "usage": "git diff --staged", "safety": "SAFE"
    },
    "python -c": {
        "title": "🐍 The Ephemeral Serpent",
        "desc": "Conducts a Python rite directly from the shell without forging a physical script file.",
        "usage": "python -c 'import os; print(os.getcwd())'", "safety": "SAFE"
    },
    "ln -s": {
        "title": "🔗 The Ethereal Bridge",
        "desc": "Forges a symbolic link (Symlink), a portal where one path represents another's soul.",
        "usage": "ln -s [target] [link_name]", "safety": "SAFE"
    },

    # =========================================================================
    # XIX. SYSTEM FORENSICS & REAPING
    # =========================================================================
    "killall": {
        "title": "🗡️ The Named Reaper",
        "desc": "Returns all processes matching a specific name to the void.",
        "usage": "killall [process_name]", "safety": "DANGEROUS"
    },
    "fuser -k": {
        "title": "⚔️ The Port Assassin",
        "desc": "Forcefully terminates any process currently occupying a specific port or file.",
        "usage": "fuser -k [port]/tcp", "safety": "DANGEROUS"
    },
    "lsblk": {
        "title": "🧱 The Block Surveyor",
        "desc": "Lists the physical block devices (disks) manifest in the system.",
        "usage": "lsblk", "safety": "SAFE"
    },
    "lsof -i tcp": {
        "title": "👂 TCP Listener Census",
        "desc": "Specifically lists all processes currently listening or communicating via the TCP protocol.",
        "usage": "lsof -i tcp:[port]", "safety": "SAFE"
    },
    "env | sort": {
        "title": "📊 The Ordered Environment",
        "desc": "Proclaims a sorted manifest of every environment variable currently anointing the shell.",
        "usage": "env | sort", "safety": "SAFE"
    },
    "uptime": {
        "title": "⏳ The Vitality Gauge",
        "desc": "Reports how long the host reality has been manifest and its current load average.",
        "usage": "uptime", "safety": "SAFE"
    },
    "history": {
        "title": "🧠 The Mind's Archive",
        "desc": "Retrieves the chronicle of all past edicts spoken in this shell session.",
        "usage": "history | grep [command]", "safety": "SAFE"
    },
})


COMMAND_BINDINGS.update({
    # =========================================================================
    # XX. SHELL INTERNALS (THE RITES OF REFRESH & IDENTITY)
    # =========================================================================
    "source": {
        "title": "🔄 The Rite of Refresh",
        "desc": "Executes a scripture within the current shell's soul, instantly applying changes to environment variables or Gnostic aliases.",
        "usage": "source .env", "safety": "SAFE"
    },
    "alias": {
        "title": "🏷️ The Macro Forge",
        "desc": "Forges a memorable shortcut for a complex edict, mapping intent to a single keyword.",
        "usage": "alias k='kubectl'", "safety": "SAFE"
    },
    "export": {
        "title": "📢 The Gnostic Proclamation",
        "desc": "Bestows a variable upon the current reality and all its future child processes.",
        "usage": "export NODE_ENV=production", "safety": "SAFE"
    },
    "type": {
        "title": "🔍 The Essence Diviner",
        "desc": "Perceives the true nature of a command—whether it is a binary artisan, a shell builtin, or a macro alias.",
        "usage": "type [command]", "safety": "SAFE"
    },

    # =========================================================================
    # XXI. CELESTIAL DISPLACEMENT & NETWORKING
    # =========================================================================
    "scp": {
        "title": "🛸 Celestial Displacement",
        "desc": "Securely translocates scriptures between the local reality and a remote celestial sanctum via the SSH wormhole.",
        "usage": "scp [file] user@remote:/path", "safety": "SAFE"
    },
    "telnet": {
        "title": "👂 The Ethereal Whisper",
        "desc": "Performs a raw, unencrypted probe of a TCP port to verify if a service is listening in the void.",
        "usage": "telnet localhost 8080", "safety": "SAFE"
    },
    "traceroute": {
        "title": "🛣️ The Path of Pilgrimage",
        "desc": "Maps the hop-by-hop journey a packet takes through the network aether to reach its destination.",
        "usage": "traceroute google.com", "safety": "SAFE"
    },
    "openssl req": {
        "title": "🖋️ The Signature of Identity",
        "desc": "Generates a Certificate Signing Request (CSR) to forge new cryptographic identities.",
        "usage": "openssl req -new -key key.pem", "safety": "SAFE"
    },

    # =========================================================================
    # XXII. ADVANCED BUILD & ECOSYSTEM RITES
    # =========================================================================
    "mvn": {
        "title": "🏗️ The Heavy Mason (Maven)",
        "desc": "The primary architect and manager for Java-based realities.",
        "usage": "mvn clean install", "safety": "SAFE"
    },
    "gradle": {
        "title": "🐘 The Versatile Weaver",
        "desc": "A modern, flexible build conductor for the JVM and Android ecosystems.",
        "usage": "gradle build", "safety": "SAFE"
    },
    "npm prune": {
        "title": "🧹 The Purity Rite",
        "desc": "Surgically removes extraneous dependency souls that are no longer willed in the manifest.",
        "usage": "npm prune --production", "safety": "SAFE"
    },
    "docker volume prune": {
        "title": "👻 The Data Exorcist",
        "desc": "Annihilates all orphaned data sanctums (volumes) to reclaim host mass.",
        "usage": "docker volume prune -f", "safety": "DANGEROUS"
    },

    # =========================================================================
    # XXIII. TEMPORAL & PHANTOM MANIPULATION (GIT)
    # =========================================================================
    "git reset --soft": {
        "title": "⏪ The Temporal Revision",
        "desc": "Rewinds the chronicle by one verse but preserves the flux in the staging area, allowing for re-inscription.",
        "usage": "git reset --soft HEAD~1", "safety": "CAUTIOUS"
    },
    "git clean -fd": {
        "title": "🔥 The Phantom Purge",
        "desc": "Annihilates all untracked scriptures and sanctums that were not born through a Git rite.",
        "usage": "git clean -fd", "safety": "DANGEROUS"
    },

    # =========================================================================
    # XXIV. KERNEL FORENSICS & IMMORTALITY
    # =========================================================================
    "nohup": {
        "title": "🕯️ The Eternal Rite",
        "desc": "Conducts an edict that is immune to the termination of the mortal shell (SIGHUP). The process becomes immortal.",
        "usage": "nohup ./script.sh &", "safety": "SAFE"
    },
    "strace": {
        "title": "👁️ The Gaze of the System",
        "desc": "Forensicly monitors the system calls made by an artisan, revealing its direct interaction with the OS kernel.",
        "usage": "strace -p [pid]", "safety": "DANGEROUS"
    },
    "sudo -u": {
        "title": "🎭 The Mask of Identity",
        "desc": "Usurps the identity of a specific user to conduct a rite within their sanctum (e.g. running DB commands).",
        "usage": "sudo -u postgres psql", "safety": "DANGEROUS"
    },
    "df -i": {
        "title": "⚖️ The Soul Census (Inodes)",
        "desc": "Reports the remaining capacity for new scriptures (Inodes) in the filesystem, rather than just raw mass (Bytes).",
        "usage": "df -i", "safety": "SAFE"
    },
    "chmod -R": {
        "title": "📜 Recursive Consecration",
        "desc": "Massively alters permissions across an entire hierarchy of scriptures and sanctums.",
        "usage": "chmod -R 755 .", "safety": "CAUTIOUS"
    },
    "tar -xvf": {
        "title": "🔓 The Soul's Release",
        "desc": "Extracts the contents of a Tape Archive back into the physical reality, preserving the original structure.",
        "usage": "tar -xvf archive.tar", "safety": "SAFE"
    },
})

COMMAND_BINDINGS.update({
    # =========================================================================
    # XXV. THE CHRONOMANCER'S ADVANCED ARTS (GIT)
    # =========================================================================
    "git lfs install": {
        "title": "🐘 Git: Large File Initialization",
        "desc": "Consecrates the repository to handle massive binary souls (Large File Storage). Replaces the 'git install' hallucination.",
        "usage": "git lfs install", "safety": "SAFE"
    },
    "git remote add": {
        "title": "🔗 Git: Weaving Celestial Links",
        "desc": "Establishes a new bond between the local reality and a remote celestial repository.",
        "usage": "git remote add origin [url]", "safety": "SAFE"
    },
    "git submodule add": {
        "title": "📦 Git: Incepting Sub-Realities",
        "desc": "Embeds the soul of another repository within the current project as a dependent submodule.",
        "usage": "git submodule add [url] [path]", "safety": "CAUTIOUS"
    },
    "git fetch": {
        "title": "📡 Git: Ethereal Update",
        "desc": "Downloads the latest verses from the celestial realm without altering the local timeline.",
        "usage": "git fetch --all", "safety": "SAFE"
    },
    "git merge": {
        "title": "🤝 Git: Timeline Unification",
        "desc": "Combines two divergent branches of history into a single, unified reality.",
        "usage": "git merge [branch_name]", "safety": "CAUTIOUS"
    },
    "git tag": {
        "title": "🎗️ Git: Consecrate Moment",
        "desc": "Bestows a sacred name upon a specific commit hash, usually for versioning (e.g. v1.0).",
        "usage": "git tag -a v1.0 -m 'Release'", "safety": "SAFE"
    },
    "git show": {
        "title": "📖 Git: Reveal Verse",
        "desc": "Displays the complete Gnostic soul and metadata of a specific commit or object.",
        "usage": "git show [commit_hash]", "safety": "SAFE"
    },
    "git revert": {
        "title": "⚖️ Git: Ethical Reversal",
        "desc": "Creates a new verse that perfectly inverts a previous commit, healing history without deleting it.",
        "usage": "git revert [commit_hash]", "safety": "SAFE"
    },
    "git bisect": {
        "title": "🕵️ Git: The Temporal Inquisitor",
        "desc": "Uses binary search to walk the timeline and identify the exact commit where a bug (heresy) was born.",
        "usage": "git bisect start", "safety": "SAFE"
    },
    "git config --global": {
        "title": "🧠 Git: Universal Mind Settings",
        "desc": "Inscribes configuration laws that apply to every project managed by this Architect.",
        "usage": "git config --global user.name 'Architect'", "safety": "SAFE"
    },
    "git checkout -b": {
        "title": "🌿 Git: Parallel Genesis",
        "desc": "Forges a new parallel timeline (branch) and immediately jumps into it.",
        "usage": "git checkout -b [new_branch]", "safety": "SAFE"
    },
    "git push --tags": {
        "title": "🎗️ Git: Proclaim All Moments",
        "desc": "Transmits all locally willed tags to the remote celestial repository.",
        "usage": "git push origin --tags", "safety": "SAFE"
    },
    "git diff --stat": {
        "title": "📊 Git: Quantitative Flux Gaze",
        "desc": "Displays a summary of line changes (added/removed) across the project files.",
        "usage": "git diff --stat", "safety": "SAFE"
    },
    "git rm --cached": {
        "title": "👻 Git: Ghostly Excision",
        "desc": "Removes a file from the Gnostic Index (tracking) but preserves its physical body on the disk.",
        "usage": "git rm --cached [file]", "safety": "CAUTIOUS"
    },
    "git reflog": {
        "title": "🗂️ Git: The Chronomancer's Safety Net",
        "desc": "Retrieves the hidden log of every movement of the HEAD, allowing for recovery from almost any temporal disaster.",
        "usage": "git reflog", "safety": "SAFE"
    },
    "git commit -am": {
        "title": "⚡ Git: Swift Inscription",
        "desc": "Stages all modified tracked files and inscribes them into history in a single, atomic movement.",
        "usage": "git commit -am 'message'", "safety": "SAFE"
    },
    "git push --force-with-lease": {
        "title": "🛡️ Git: Prudent Proclamation",
        "desc": "A safer form of `--force`. Only overwrites the celestial history if no new verses have been added by others.",
        "usage": "git push --force-with-lease", "safety": "CAUTIOUS"
    },
    "git archive": {
        "title": "🏛️ Git: Scribe Export",
        "desc": "Exports the state of a specific point in time into a physical ZIP or Tar archive.",
        "usage": "git archive --format zip HEAD > project.zip", "safety": "SAFE"
    },
    "git worktree": {
        "title": "🏗️ Git: Multi-Sanctum Construction",
        "desc": "Allows the Architect to checkout multiple branches simultaneously into different physical directories.",
        "usage": "git worktree add ../feature-branch", "safety": "SAFE"
    },
    "git sparse-checkout": {
        "title": "🔎 Git: Selective Perception",
        "desc": "Commands the engine to only materialize specific parts of a massive repository, ignoring the rest.",
        "usage": "git sparse-checkout set [dir]", "safety": "SAFE"
    },
})

