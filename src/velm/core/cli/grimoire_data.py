# Path: scaffold/core/cli/grimoire_data.py
# ----------------------------------------
"""
=================================================================================
== THE SACRED CODEX OF LAZY GNOSIS (V-Ω-ETERNAL. THE PURE LAW)                 ==
=================================================================================
This scripture is the pure, declarative data-soul of the Scaffold CLI's dynamic
invocation system. It contains no logic. It is the single source of truth for
the Gnostic Conductor to find the path to an Artisan's soul.

This is the one true LAZY_RITE_MAP, forged during the Great Apotheosis.
=================================================================================
"""
LAZY_RITE_MAP = {
    # Core Rites of Creation & Execution
    "genesis": ("artisans.genesis", "GenesisArtisan", "GenesisRequest"),
    "init": ("artisans.init", "InitArtisan", "InitRequest"),
    "run": ("artisans.run.conductor", "RunArtisan", "RunRequest"),
    "create": ("artisans.create", "CreateArtisan", "CreateRequest"),
    "preview": ("artisans.preview", "PreviewArtisan", "PreviewRequest"),
    # Architectural Evolution & Refactoring
    "transmute": ("artisans.transmute", "TransmuteArtisan", "TransmuteRequest"),
    "patch": ("artisans.patch", "PatchArtisan", "PatchRequest"),
    "translocate": ("artisans.translocate", "TranslocateArtisan", "TranslocateRequest"),
    "conform": ("artisans.conform", "ConformArtisan", "ConformRequest"),
    "refactor": ("artisans.refactor", "RefactorArtisan", "RefactorRequest"),
    "excise": ("artisans.excise", "ExciseArtisan", "ExciseRequest"),
    "weave": ("artisans.weave", "WeaveArtisan", "WeaveRequest"),
    "compose": ("artisans.compose", "ComposeArtisan", "ComposeRequest"),
    "arch": ("artisans.arch", "ArchArtisan", "ArchRequest"),
    "upgrade": ("artisans.upgrade", "UpgradeArtisan", "UpgradeRequest"),
    "hover": ("artisans.hover", "HoverArtisan", "HoverRequest"),
    # Gnostic Perception & Analysis
    "distill": ("artisans.distill", "DistillArtisan", "DistillRequest"),
    "adopt": ("artisans.adopt", "AdoptArtisan", "AdoptRequest"),
    "verify": ("artisans.verify", "VerifyArtisan", "VerifyRequest"),
    "analyze": ("artisans.analyze", "AnalyzeArtisan", "AnalyzeRequest"),
    "inspect": ("artisans.inspect", "InspectArtisan", "InspectRequest"),
    "tree": ("artisans.tree", "TreeArtisan", "TreeRequest"),
    "graph": ("artisans.graph", "GraphArtisan", "GraphRequest"),
    "matrix": ("artisans.matrix", "MatrixArtisan", "MatrixRequest"),
    "mri": ("artisans.mri", "MRIArtisan", "MRIRequest"),
    "risk": ("artisans.risk", "BusFactorArtisan", "BusFactorRequest"),
    "hunt": ("artisans.ghost_hunter", "GhostHunterArtisan", "GhostRequest"),
    "summarize": ("artisans.summarize", "SummarizeArtisan", "SummarizeRequest"),
    "sgrep": ("artisans.sgrep", "SgrepArtisan", "SgrepRequest"),
    "scribe": ("artisans.scribe.conductor", "ScribeConductor", "ScribeRequest"),
    "semdiff": ("artisans.semdiff", "SemDiffArtisan", "SemDiffRequest"),
    "holographic": ("artisans.holographic", "HolographicBlueprintArtisan", "HolographicBlueprintRequest"),


    # AI & Language Server Integration
    "daemon": ("artisans.daemon_artisan", "DaemonArtisan", "DaemonRequest"),
    "neural": ("artisans.neural", "NeuralArtisan", "NeuralRequest"),
    "architect": ("artisans.architect", "ArchitectArtisan", "ArchitectRequest"),
    "manifest": ("artisans.manifest", "ManifestArtisan", "ManifestRequest"),
    "introspect": ("artisans.introspect", "IntrospectionArtisan", "IntrospectionRequest"),
    "vector": ("artisans.vector.artisan", "VectorArtisan", "VectorRequest"),
    "resonate": ("artisans.resonate", "ResonateArtisan", "ResonateRequest"),
    "translate": ("artisans.translate", "TranslateArtisan", "TranslateRequest"),
    "dream": ("artisans.dream", "DreamArtisan", "DreamRequest"),
    "muse": ("artisans.muse", "MuseArtisan", "MuseRequest"),
    "agent": ("artisans.agent", "AgentArtisan", "AgentRequest"),
    "train": ("artisans.train", "TrainArtisan", "TrainRequest"),
    "debate": ("artisans.hivemind.artisan", "HivemindArtisan", "DebateRequest"),
    # History & Reversibility
    "history": ("artisans.history", "HistoryArtisan", "HistoryRequest"),
    "undo": ("artisans.undo", "UndoArtisan", "UndoRequest"),
    "blame": ("artisans.blame", "BlameArtisan", "BlameRequest"),
    "time-branch": ("artisans.time_branch", "TimeBranchArtisan", "TimeBranchRequest"),
    "time-machine": ("artisans.time_machine", "TimeMachineArtisan", "TimeMachineRequest"),
    "replay": ("artisans.replay", "ReplayArtisan", "ReplayRequest"),
    "akasha": ("artisans.akasha.artisan", "AkashaArtisan", "AkashaRequest"),
    "survey": ("artisans.surveyor.artisan", "GrandSurveyArtisan", "GrandSurveyRequest"),
    # UI & Interaction
    "pad": ("artisans.pad", "PadArtisan", "PadRequest"),
    "studio": ("artisans.studio", "StudioArtisan", "StudioRequest"),
    "shell": ("artisans.shell", "ShellArtisan", "ShellRequest"),
    "gui": ("artisans.gui", "GuiArtisan", "GuiRequest"),
    "help": ("artisans.help", "HelpArtisan", "HelpRequest"),
    "repl": ("artisans.repl_artisan", "ReplArtisan", "ReplRequest"),
    "telepathy": ("artisans.telepathy", "TelepathyArtisan", "TelepathyRequest"),
    # Automation & CI/CD
    "symphony": ("artisans.symphony", "SymphonyArtisan", "SymphonyRequest"),
    "watch": ("artisans.watchman", "WatchmanArtisan", "WatchmanRequest"),
    "save": ("artisans.save_artisan", "SaveArtisan", "SaveRequest"),
    "changelog": ("artisans.changelog.artisan", "ChangelogArtisan", "ChangelogRequest"),
    "ci-optimize": ("artisans.ci_optimize", "OptimizeCIArtisan", "OptimizeCIRequest"),

    # Security, Compliance & Deployment
    "isolate": ("artisans.isolate", "IsolateArtisan", "IsolateRequest"),
    "signature": ("artisans.signature_artisan", "SignatureArtisan", "SignatureRequest"),
    "with": ("artisans.with_secrets", "WithSecretsArtisan", "WithSecretsRequest"),
    "deploy": ("artisans.deploy", "DeployArtisan", "DeployRequest"),
    "expose": ("artisans.expose", "ExposeArtisan", "ExposeRequest"),
    "prophesy": ("artisans.prophesy", "ProphesyArtisan", "ProphesyRequest"),
    "query": ("artisans.query", "QueryArtisan", "QueryRequest"),
    # Tooling & Utilities
    "settings": ("artisans.settings", "SettingsArtisan", "SettingsRequest"),
    "runtimes": ("artisans.runtimes", "RuntimesArtisan", "RuntimesRequest"),
    "templates": ("artisans.templates", "TemplateManagerCLI", "TemplateRequest"),
    "alias": ("artisans.alias.artisan", "AliasArtisan", "AliasRequest"),
    "beautify": ("artisans.beautify", "BeautifyArtisan", "BeautifyRequest"),
    "lint-blueprint": ("artisans.lint_blueprint.artisan", "BlueprintLinterArtisan", "LintBlueprintRequest"),
    "lint": ("artisans.lint", "LintArtisan", "LintRequest"),
    "tool": ("artisans.tool.tool_cli", "ToolArtisan", "ToolRequest"),
    "self-test": ("artisans.self_test", "SelfTestArtisan", "SelfTestRequest"),
    "add": ("artisans.blueprint_add", "BlueprintAddArtisan", "AddRequest"),
    "remove": ("artisans.blueprint_remove", "BlueprintExciseArtisan", "BlueprintExciseRequest"),
    "optimize": ("artisans.blueprint_optimize", "BlueprintOptimizerArtisan", "OptimizeBlueprintRequest"),
    "freeze": ("artisans.freeze_artisan", "FreezeArtisan", "FreezeRequest"),
    "forge": ("artisans.forge", "ForgeArtisan", "ForgeArtisanRequest"),
    "ignore": ("artisans.ignore.artisan", "IgnoreArtisan", "IgnoreRequest"),
    "mock": ("artisans.mock", "MockingbirdArtisan", "MockRequest"),
    "qr": ("artisans.qr", "QRArtisan", "QRRequest"),
    "snippet": ("artisans.snippet.artisan", "SnippetArtisan", "SnippetRequest"),
    "read-soul": ("artisans.read_soul", "ReadSoulArtisan", "ReadSoulRequest"),
    "guild": ("artisans.guild.artisan", "GuildArtisan", "GuildRequest"),
    "mimic": ("artisans.mimic.artisan", "MimicArtisan", "MimicRequest"),
    "garden": ("artisans.garden.artisan", "GardenArtisan", "GardenRequest"),
    "fuse": ("artisans.fusion.artisan", "FusionArtisan", "FusionRequest"),  # Updated mapping
    "shadow": ("artisans.shadow_clone.artisan", "ShadowCloneArtisan", "ShadowCloneRequest"),  # Updated mapping
    "evolve": ("artisans.schema.artisan", "SchemaArtisan", "EvolveRequest"),
    "resurrect": ("artisans.lazarus.artisan", "LazarusArtisan", "LazarusRequest"),
    "fortify": ("artisans.fortress.artisan", "FortressArtisan", "FortressRequest"),
    "port": ("artisans.babel.artisan", "BabelArtisan", "BabelRequest"),
    "holocron": ("artisans.holocron.artisan", "HolocronArtisan", "HolocronRequest"), # Causal Context
    "ocular": ("artisans.ocular.artisan", "OcularArtisan", "OcularRequest"), # Multimodal Sight
    "aether": ("artisans.aether.artisan", "AetherArtisan", "AetherRequest"), # Collective Wisdom
    "workspace": ("artisans.workspace", "WorkspaceArtisan", "WorkspaceRequest"),
    "archetypes": ("artisans.archetypes.artisan", "ArchetypeArtisan", "ArchetypeRequest"),
    "simulate": ("artisans.simulacrum.artisan", "SimulacrumArtisan", "SimulateRequest"),
    "plugins": ("artisans.plugins.artisan", "PluginsArtisan", "PluginsRequest"),
    "index": ("artisans.indexer.artisan", "IndexerArtisan", "IndexRequest"),
    "supabase": ("artisans.services.supabase.artisan", "SupabaseArtisan", "SupabaseRequest"),
    "msg": ("artisans.services.communication.artisan", "CommunicationArtisan", "CommunicationRequest"),
    "billing": ("artisans.services.billing.artisan", "BillingArtisan", "BillingRequest"),
    "store": ("artisans.services.storage.artisan", "StorageArtisan", "StorageRequest"),
    "http": ("artisans.services.network.artisan", "NetworkArtisan", "NetworkRequest"),
    "crm": ("artisans.services.crm.artisan", "CRMArtisan", "CRMRequest"),
    "ask-ai": ("artisans.services.intelligence.artisan", "IntelligenceArtisan", "IntelligenceRequest"),
    "browse": ("artisans.services.browser.artisan", "BrowserArtisan", "BrowserRequest"),
    "doc": ("artisans.services.document.artisan", "DocumentArtisan", "DocumentRequest"),
    "queue": ("artisans.services.worker.artisan", "WorkerArtisan", "WorkerRequest"),
    "memory": ("artisans.services.memory.artisan", "MemoryArtisan", "MemoryRequest"),
    "cache": ("artisans.services.cache.artisan", "CacheArtisan", "CacheRequest"),
    "sheet": ("artisans.services.sheets.artisan", "SheetArtisan", "SheetRequest"),
}
