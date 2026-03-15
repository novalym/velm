# =============================================================================
# == THE GNOSTIC CODE BUILDER (REUSED FOR CONSISTENCY)                       ==
# =============================================================================
from contextlib import contextmanager
from typing import List, Set, Dict


class GnosticCodeBuilder:
    """
    A stateful engine for constructing indented code without string-mashing.
    Ensures atomic indentation and import management.
    """

    def __init__(self, indent_char: str = "    "):
        self.lines: List[str] = []
        self.level: int = 0
        self.indent_char: str = indent_char
        self.imports: Set[str] = set()
        self.from_imports: Dict[str, Set[str]] = {}
        self.metadata: List[str] = []

    def add_import(self, module: str):
        self.imports.add(module)

    def add_from_import(self, module: str, name: str):
        if module not in self.from_imports:
            self.from_imports[module] = set()
        self.from_imports[module].add(name)

    def add_metadata(self, key: str, value: str):
        self.metadata.append(f"# {key}: {value}")

    def add(self, line: str = ""):
        if not line:
            self.lines.append("")
        else:
            self.lines.append((self.indent_char * self.level) + line)

    @contextmanager
    def block(self, header: str):
        self.add(header)
        self.level += 1
        try:
            yield
        finally:
            self.level -= 1

    def render(self) -> str:
        output = []
        if self.metadata:
            output.extend(self.metadata)
            output.append("")

        if self.imports:
            output.extend([f"import {m}" for m in sorted(self.imports)])
        if self.from_imports:
            for mod in sorted(self.from_imports.keys()):
                names = ", ".join(sorted(self.from_imports[mod]))
                output.append(f"from {mod} import {names}")

        if self.imports or self.from_imports:
            output.append("")
            output.append("")

        output.extend(self.lines)
        return "\n".join(output).strip()


# =============================================================================
# == THE PROVIDER MATRIX                                                     ==
# =============================================================================

PROVIDER_CONFIGS = {
    "openai": {
        "pkg": "openai",
        "sync_cls": "OpenAI",
        "async_cls": "AsyncOpenAI",
        "env_key": "OPENAI_API_KEY",
        "base_url_default": None
    },
    "anthropic": {
        "pkg": "anthropic",
        "sync_cls": "Anthropic",
        "async_cls": "AsyncAnthropic",
        "env_key": "ANTHROPIC_API_KEY",
        "base_url_default": None
    },
    "azure": {
        "pkg": "openai",
        "sync_cls": "AzureOpenAI",
        "async_cls": "AsyncAzureOpenAI",
        "env_key": "AZURE_OPENAI_API_KEY",
        "extra_env": ["AZURE_OPENAI_ENDPOINT"],
        "base_url_default": None
    },
    "ollama": {
        "pkg": "openai",
        "sync_cls": "OpenAI",
        "async_cls": "AsyncOpenAI",
        "env_key": None,  # No key needed
        "base_url_default": "http://localhost:11434/v1"
    },
    "groq": {
        "pkg": "openai",
        "sync_cls": "OpenAI",
        "async_cls": "AsyncOpenAI",
        "env_key": "GROQ_API_KEY",
        "base_url_default": "https://api.groq.com/openai/v1"
    },
    "deepseek": {
        "pkg": "openai",
        "sync_cls": "OpenAI",
        "async_cls": "AsyncOpenAI",
        "env_key": "DEEPSEEK_API_KEY",
        "base_url_default": "https://api.deepseek.com/v1"
    }
}


# =============================================================================
# == THE FORGE (GENERATION LOGIC)                                            ==
# =============================================================================

def forge_client_setup(
        provider: str = "openai",
        async_mode: bool = True,
        custom_base: str = "",
        retries: bool = True,
        debug: bool = False
) -> str:
    """
    Forges a robust, self-validating client factory.
    """
    p_key = provider.lower()
    config = PROVIDER_CONFIGS.get(p_key, PROVIDER_CONFIGS["openai"])

    cb = GnosticCodeBuilder()

    # --- 1. Configuration & Metadata ---
    reqs = [config["pkg"]]
    if retries: reqs.append("tenacity")
    cb.add_metadata("requirements", ", ".join(reqs))

    cb.add_import("os")
    cb.add_import("logging")
    cb.add_from_import("typing", "Optional")

    # Import the client class
    cls_name = config["async_cls"] if async_mode else config["sync_cls"]
    cb.add_from_import(config["pkg"], cls_name)

    if retries:
        cb.add_import("tenacity")
        cb.add_from_import("tenacity", "retry")
        cb.add_from_import("tenacity", "stop_after_attempt")
        cb.add_from_import("tenacity", "wait_exponential")

    # --- 2. Logger Setup ---
    cb.add("")
    cb.add('logger = logging.getLogger("neural_gateway")')

    # --- 3. The Environment Sentinel ---
    # Helper function to validate env vars
    with cb.block("def _validate_env(var_name: str, default: Optional[str] = None) -> str:"):
        cb.add("value = os.getenv(var_name, default)")
        with cb.block("if not value:"):
            cb.add(f'raise ValueError(f"Neural Pathway Blocked: Missing Environment Variable {{var_name}}")')
        cb.add("return value")

    # --- 4. The Client Factory ---
    cb.add("")
    func_name = "get_async_client" if async_mode else "get_client"

    with cb.block(f"def {func_name}() -> {cls_name}:"):
        cb.add(f'"""Summons the {p_key.title()} client with Gnostic configuration."""')

        # A. API Key Resolution
        if config.get("env_key"):
            cb.add(f'api_key = _validate_env("{config["env_key"]}")')
        else:
            cb.add('api_key = "gnostic-dummy-key" # Key not required for this provider')

        # B. Base URL Resolution
        base_url = custom_base or config.get("base_url_default")
        if p_key == "azure":
            cb.add(f'azure_endpoint = _validate_env("AZURE_OPENAI_ENDPOINT")')
            # Azure doesn't use base_url in the constructor exactly the same way,
            # it uses azure_endpoint and api_version
        elif base_url:
            cb.add(f'base_url = os.getenv("{p_key.upper()}_API_BASE", "{base_url}")')

        # C. Instantiation
        cb.add(f"client = {cls_name}(")

        if p_key == "azure":
            cb.add("    api_key=api_key,")
            cb.add("    azure_endpoint=azure_endpoint,")
            cb.add("    api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2023-05-15'),")
        else:
            cb.add("    api_key=api_key,")
            if base_url or custom_base:
                cb.add("    base_url=base_url,")

        cb.add("    max_retries=0, # We handle retries via tenacity" if retries else "    max_retries=2,")
        cb.add(")")

        cb.add("return client")

    # --- 5. The Retry Decorator (Optional) ---
    if retries:
        cb.add("")
        cb.add("# Gnostic Retry Policy: Exponential Backoff")
        cb.add("retry_policy = retry(")
        cb.add("    stop=stop_after_attempt(3),")
        cb.add("    wait=wait_exponential(multiplier=1, min=4, max=10),")
        cb.add("    reraise=True")
        cb.add(")")

    # --- 6. The Inference Wrapper (Generative Action) ---
    # Generates a sample function showing how to use the client
    cb.add("")
    wrapper_def = "async def" if async_mode else "def"

    with cb.block(f"{wrapper_def} generate_thought(prompt: str, model: str = 'gpt-3.5-turbo') -> str:"):
        if retries:
            cb.add("@retry_policy")
            with cb.block(f"{wrapper_def} _call_api():"):
                cb.add(f"client = {func_name}()")
                if async_mode:
                    cb.add("return await client.chat.completions.create(")
                else:
                    cb.add("return client.chat.completions.create(")
                cb.add("    model=model,")
                cb.add("    messages=[{\"role\": \"user\", \"content\": prompt}]")
                cb.add(")")

            if async_mode:
                cb.add("response = await _call_api()")
            else:
                cb.add("response = _call_api()")
        else:
            cb.add(f"client = {func_name}()")
            if async_mode:
                cb.add("response = await client.chat.completions.create(")
            else:
                cb.add("response = client.chat.completions.create(")
            cb.add("    model=model,")
            cb.add("    messages=[{\"role\": \"user\", \"content\": prompt}]")
            cb.add(")")

        cb.add("return response.choices[0].message.content or ''")

    # --- 7. The Self-Diagnostic Main (The Ping) ---
    cb.add("")
    with cb.block('if __name__ == "__main__":'):
        if async_mode:
            cb.add("import asyncio")

        cb.add(f'print("⚡ Awakening Neural Gateway for {p_key.title()}...")')

        # Determine default model for the check
        test_model = "gpt-3.5-turbo"
        if p_key == "anthropic": test_model = "claude-3-haiku-20240307"
        if p_key == "ollama": test_model = "llama3"
        if p_key == "azure": test_model = "gpt-35-turbo"  # Azure requires deployment name

        with cb.block("try:"):
            if async_mode:
                cb.add(f'result = asyncio.run(generate_thought("Hello, world!", model="{test_model}"))')
            else:
                cb.add(f'result = generate_thought("Hello, world!", model="{test_model}")')

            cb.add('print(f"✅ Connection Secured. Response: {result}")')

        with cb.block("except Exception as e:"):
            cb.add('print(f"🔥 Connection Failed: {e}")')
            cb.add('print("Check your API Keys and Base URLs.")')

    return cb.render()