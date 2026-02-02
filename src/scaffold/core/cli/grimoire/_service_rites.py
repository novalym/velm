# Path: scaffold/src/scaffold/core/cli/grimoire/_service_rites.py
from ..cli_utils import add_common_flags
import json

RITES = {
    "supabase": {
        "module_path": "artisans.services.supabase.artisan", # UPDATED PATH
        "artisan_class_name": "SupabaseArtisan",
        "request_class_name": "SupabaseRequest",
        "help": "Direct interaction with the Akashic Record (DB, Auth, Storage).",
        "flags": [add_common_flags],
        "args": [
            ("domain", {"choices": ["database", "auth", "storage"], "help": "Target Domain."}),
            ("--table", {"help": "DB Table or Function name."}),
            ("--action", {"help": "Method (insert, select, upload, etc.)."}),
            ("--data", {"type": json.loads, "help": "JSON payload."}),
            ("--filters", {"type": json.loads, "help": "JSON filters (e.g. {'id': 'eq:5'})."})
        ]
    },
    "msg": {
        "module_path": "artisans.services.communication_artisan",
        "artisan_class_name": "CommunicationArtisan",
        "request_class_name": "CommunicationRequest",
        "help": "Send a signal via the Herald.",
        "flags": [add_common_flags],
        "args": [
            ("channel", {"choices": ["sms", "email"]}),
            ("recipient", {"help": "Target address."}),
            ("content", {"help": "Message body."}),
            ("--subject", {"help": "Email subject."})
        ]
    },
    "http": {
        "module_path": "artisans.services.network.artisan", # UPDATED PATH
        "artisan_class_name": "NetworkArtisan",
        "request_class_name": "NetworkRequest",
        "help": "Perform a network rite (REST/GraphQL/Webhook).",
        "flags": [add_common_flags],
        "args": [
            ("url", {"help": "Target URL."}),
            ("--method", {"default": "GET", "help": "HTTP Method."}),
            ("--protocol", {"choices": ["http", "graphql", "webhook"], "default": "http"}),
            ("--body", {"dest": "json_body", "type": json.loads, "help": "JSON Payload."}),
            ("--headers", {"type": json.loads, "help": "Header map."}),
            ("--auth", {"type": json.loads, "help": "Auth config {'type': 'bearer', 'token': '...'}"}),
            ("--retries", {"type": int, "default": 0})
        ]
    },

    # --- THE NEW SOVEREIGNS ---
    "billing": {
        "module_path": "artisans.services.billing.artisan", # UPDATED PATH
        "artisan_class_name": "BillingArtisan",
        "request_class_name": "BillingRequest",
        "help": "The Treasury. Interact with the Stripe Lattice.",
        "flags": [add_common_flags],
        "args": [
            ("entity", {"choices": ["customer", "subscription", "product", "price", "invoice", "portal", "payment_link"], "help": "Target fiscal entity."}),
            ("action", {"choices": ["create", "retrieve", "update", "list", "search", "cancel", "pay", "finalize"], "help": "Fiscal operation."}),
            ("--id", {"help": "Target ID (cus_..., sub_...)."}),
            ("--payload", {"type": json.loads, "help": "JSON parameters (metadata, items, etc.)."}),
            ("--expand", {"nargs": "+", "help": "Fields to expand (e.g. customer latest_invoice)."}),
            ("--limit", {"type": int, "default": 10, "help": "List pagination limit."})
        ]
    },
    "store": {
        "module_path": "artisans.services.storage.artisan", # UPDATED PATH
        "artisan_class_name": "StorageArtisan",
        "request_class_name": "StorageRequest",
        "help": "The Archive. Manage heavy matter (S3).",
        "flags": [add_common_flags],
        "args": [
            ("action", {"choices": ["upload", "download", "delete", "list", "sign_url", "create_bucket"], "help": "Operation."}),
            ("bucket", {"help": "Target Bucket."}),
            ("path", {"help": "Cloud path / Key."}),
            ("--source", {"dest": "source_path", "help": "Local source file (for upload)."}),
            ("--dest", {"dest": "destination_path", "help": "Local dest file (for download)."}),
            ("--expiry", {"dest": "expiry_seconds", "type": int, "help": "Seconds until URL expires."})
        ]
    },
    "crm": {
        "module_path": "artisans.services.crm.artisan", # UPDATED PATH
        "artisan_class_name": "CRMArtisan",
        "request_class_name": "CRMRequest",
        "help": "The Diplomat. Manage CRM entities.",
        "flags": [add_common_flags],
        "args": [
            ("entity", {"choices": ["contact", "company", "deal", "ticket"], "help": "Target Object."}),
            ("action", {"choices": ["create", "update", "upsert", "search", "get"], "help": "Operation."}),
            ("--provider", {"default": "hubspot", "help": "CRM Provider."}),
            ("--id", {"help": "Target Record ID."}),
            ("--match", {"dest": "match_value", "help": "Value to match for upsert/search."}),
            ("--by", {"dest": "match_key", "default": "email", "help": "Field to match by (default: email)."}),
            ("--data", {"type": json.loads, "help": "JSON payload."}),
            ("--props", {"dest": "properties", "nargs": "+", "help": "Properties to return."})
        ]
    },
    "ask-ai": {
        "module_path": "artisans.services.intelligence.artisan",
        "artisan_class_name": "IntelligenceArtisan",
        "request_class_name": "IntelligenceRequest",
        "help": "The Oracle. Runtime AI queries across any provider.",
        "flags": [add_common_flags],
        "args": [
            ("user_prompt", {"help": "The query/instruction."}),
            ("--provider",
             {"choices": ["openai", "anthropic", "ollama", "lmstudio", "huggingface"], "default": "openai"}),
            ("--model", {"default": "gpt-4-turbo", "help": "Target model ID."}),
            ("--system", {"dest": "system_prompt", "help": "System context/persona."}),
            ("--json", {"dest": "json_mode", "action": "store_true", "help": "Enforce JSON output."}),
            ("--temp", {"dest": "temperature", "type": float, "default": 0.7}),
            ("--context", {"type": json.loads, "help": "Data context (JSON string)."})
        ]
    },
    "browse": {
        "module_path": "artisans.services.browser.artisan",
        "artisan_class_name": "BrowserArtisan",
        "request_class_name": "BrowserRequest",
        "help": "The Navigator. Headless browser automation.",
        "flags": [add_common_flags],
        "args": [
            ("url", {"help": "Target URL."}),
            ("action", {"choices": ["screenshot", "scrape", "pdf"], "help": "Action."}),
            ("--selector", {"help": "CSS Selector to target."}),
            ("--wait", {"dest": "wait_for", "help": "Wait for selector."})
        ]
    },
    "doc": {
        "module_path": "artisans.services.document.artisan",
        "artisan_class_name": "DocumentArtisan",
        "request_class_name": "DocumentRequest",
        "help": "The Scribe. Generate or Parse PDF/CSV/Excel.",
        "flags": [add_common_flags],
        "args": [
            ("action", {"choices": ["generate", "parse"], "help": "Operation."}),
            ("format", {"choices": ["pdf", "csv", "xlsx"], "help": "File format."}),
            ("--in", {"dest": "source_path", "help": "Input file."}),
            ("--out", {"dest": "output_path", "help": "Output file."}),
            ("--data", {"type": json.loads, "help": "JSON data for generation."}),
            ("--template", {"dest": "template_path", "help": "HTML template for PDF."})
        ]
    },
    "queue": {
        "module_path": "artisans.services.worker.artisan",
        "artisan_class_name": "WorkerArtisan",
        "request_class_name": "WorkerRequest",
        "help": "The Taskmaster. Enqueue background jobs.",
        "flags": [add_common_flags],
        "args": [
            ("task", {"help": "Python path to function (e.g. app.tasks.send_email)."}),
            ("--queue", {"default": "default", "help": "Target queue."}),
            ("--delay", {"dest": "delay_seconds", "type": int, "help": "Delay in seconds."}),
            ("--args", {"nargs": "+", "help": "Positional args."}),
            ("--kwargs", {"type": json.loads, "help": "Keyword args JSON."})
        ]
    },
    "memory": {
        "module_path": "artisans.services.memory.artisan",
        "artisan_class_name": "MemoryArtisan",
        "request_class_name": "MemoryRequest",
        "help": "The Cortex Keeper. Semantic search and storage.",
        "flags": [add_common_flags],
        "args": [
            ("collection", {"help": "Target table/collection."}),
            ("action", {"choices": ["upsert", "query"], "help": "Operation."}),
            ("--text", {"help": "Content to embed/search."}),
            ("--meta", {"dest": "metadata", "type": json.loads, "help": "Metadata JSON."})
        ]
    },
"cache": {
        "module_path": "artisans.services.cache.artisan",
        "artisan_class_name": "CacheArtisan",
        "request_class_name": "CacheRequest",
        "help": "The Timekeeper. Manage Redis keys and locks.",
        "flags": [add_common_flags],
        "args": [
            ("key", {"help": "Target Key."}),
            ("action", {"choices": ["get", "set", "delete", "increment", "lock"], "help": "Operation."}),
            ("--val", {"dest": "value", "help": "Value to set."}),
            ("--ttl", {"type": int, "default": 3600, "help": "Expiry seconds."})
        ]
    },
    "sheet": {
        "module_path": "artisans.services.sheets.artisan",
        "artisan_class_name": "SheetArtisan",
        "request_class_name": "SheetRequest",
        "help": "The Grid Master. Read/Write Spreadsheets.",
        "flags": [add_common_flags],
        "args": [
            ("provider", {"choices": ["google", "airtable"], "help": "Provider."}),
            ("action", {"choices": ["read", "append", "update"], "help": "Action."}),
            ("base_id", {"help": "Sheet ID or Base ID."}),
            ("table_name", {"help": "Tab Name or Table Name."}),
            ("--data", {"dest": "rows", "type": json.loads, "help": "JSON list of rows."})
        ]
    }
}