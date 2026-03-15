# scaffold/semantic_injection/directives/neuron_knowledge/edge.py

"""
=================================================================================
== THE LOCAL FOUNDRY (V-Ω-EDGE-ULTIMA)                                         ==
=================================================================================
LIF: 10,000,000,000,000,000,000

This artisan generates production-grade Infrastructure as Code (IaC) for
running Large Language Models on local silicon.

It creates optimized Docker Compose definitions for:
1. Ollama (Ease of use)
2. vLLM (High Throughput)
3. TGI (Hugging Face Standard)
4. Llama.cpp (CPU/Apple Silicon efficient)

It handles complex hardware negotiation (GPU/IPC/SHM) automatically.
=================================================================================
"""
from contextlib import contextmanager
from typing import List


# =============================================================================
# == THE GNOSTIC YAML BUILDER (2-Space Indentation)                          ==
# =============================================================================

class GnosticYAMLBuilder:
    """
    A stateful engine for constructing valid YAML structure.
    """

    def __init__(self):
        self.lines: List[str] = []
        self.level: int = 0
        self.indent_str: str = "  "  # YAML standard

    def add(self, line: str = ""):
        if not line:
            self.lines.append("")
        else:
            self.lines.append((self.indent_str * self.level) + line)

    def add_comment(self, text: str):
        self.add(f"# {text}")

    @contextmanager
    def block(self, header: str):
        self.add(header)
        self.level += 1
        try:
            yield
        finally:
            self.level -= 1

    def render(self) -> str:
        return "\n".join(self.lines).strip()


# =============================================================================
# == THE FORGE (GENERATION LOGIC)                                            ==
# =============================================================================

def forge_inference_service(
        runtime: str = "ollama",
        model: str = "llama3",
        port: int = 0,
        gpu: bool = True,
        quantization: str = ""
) -> str:
    """
    Forges a Docker Compose service definition for a local LLM.
    """
    yb = GnosticYAMLBuilder()
    r = runtime.lower()

    # Defaults
    if not port:
        port_map = {
            "ollama": 11434,
            "vllm": 8000,
            "tgi": 8080,
            "llamacpp": 8080
        }
        port = port_map.get(r, 8000)

    service_name = f"llm_{r}"

    yb.add_comment(f"--- Local Intelligence ({r.upper()}) ---")
    yb.add_comment(f"Model: {model}")

    with yb.block(f"{service_name}:"):

        # --- 1. OLLAMA ---
        if r == "ollama":
            yb.add("image: ollama/ollama:latest")
            yb.add(f"container_name: scaffold_ollama")
            yb.add("restart: unless-stopped")

            # Ports
            with yb.block("ports:"):
                yb.add(f'- "{port}:11434"')

            # Volumes
            with yb.block("volumes:"):
                yb.add("- ollama_data:/root/.ollama")

            # Healthcheck
            with yb.block("healthcheck:"):
                yb.add("test: [\"CMD-SHELL\", \"ollama list || exit 1\"]")
                yb.add("interval: 10s")
                yb.add("timeout: 5s")
                yb.add("retries: 5")

            # GPU Support
            if gpu:
                _inject_gpu_config(yb)

        # --- 2. vLLM (High Performance) ---
        elif r == "vllm":
            yb.add("image: vllm/vllm-openai:latest")
            yb.add("container_name: scaffold_vllm")
            # [ELEVATION 3] Memory Sentinel
            yb.add("ipc: host # Required for PyTorch shared memory")
            yb.add("restart: unless-stopped")

            with yb.block("environment:"):
                yb.add("- HUGGING_FACE_HUB_TOKEN=${HF_TOKEN} # Required for gated models")

            with yb.block("ports:"):
                yb.add(f'- "{port}:8000"')

            with yb.block("volumes:"):
                yb.add("- ~/.cache/huggingface:/root/.cache/huggingface")

            # Command construction
            cmd = f"--model {model}"
            if quantization:
                cmd += f" --quantization {quantization}"
            # Safe defaults for compatibility
            cmd += " --gpu-memory-utilization 0.95 --max-model-len 4096 --trust-remote-code"

            yb.add(f'command: {cmd}')

            with yb.block("healthcheck:"):
                yb.add("test: [\"CMD-SHELL\", \"curl -f http://localhost:8000/health || exit 1\"]")
                yb.add("interval: 30s")
                yb.add("timeout: 10s")
                yb.add("retries: 3")

            if gpu:
                _inject_gpu_config(yb)

        # --- 3. TGI (Hugging Face Standard) ---
        elif r == "tgi":
            yb.add("image: ghcr.io/huggingface/text-generation-inference:latest")
            yb.add("container_name: scaffold_tgi")
            yb.add("shm_size: 1g # Prevent OOM on big models")

            with yb.block("environment:"):
                yb.add(f"- MODEL_ID={model}")
                yb.add("- HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}")
                if quantization:
                    yb.add(f"- QUANTIZE={quantization}")

            with yb.block("ports:"):
                yb.add(f'- "{port}:80"')

            with yb.block("volumes:"):
                yb.add("- ~/.cache/huggingface:/data")

            if gpu:
                _inject_gpu_config(yb)
            else:
                # TGI needs explicit CPU warning/config if possible, but usually requires GPU
                yb.add_comment("WARNING: TGI is optimized for GPU. CPU performance may be poor.")

        # --- 4. Llama.cpp (Server) ---
        elif r == "llamacpp":
            image = "ghcr.io/ggerganov/llama.cpp:server-cuda" if gpu else "ghcr.io/ggerganov/llama.cpp:server"
            yb.add(f"image: {image}")
            yb.add("container_name: scaffold_llama")

            with yb.block("ports:"):
                yb.add(f'- "{port}:8080"')

            with yb.block("volumes:"):
                yb.add("- ./models:/models")

            # Auto-detect GGUF convention
            model_file = model if model.endswith(".gguf") else f"{model}.gguf"
            yb.add(f'command: -m /models/{model_file} -c 2048 --host 0.0.0.0 --port 8080')

            if gpu:
                _inject_gpu_config(yb)

        else:
            return f"# Unknown runtime '{runtime}'. Supported: ollama, vllm, tgi, llamacpp."

    return yb.render()


def _inject_gpu_config(yb: GnosticYAMLBuilder):
    """
    [ELEVATION 6] The GPU Architect.
    Injects the standard NVIDIA container runtime configuration.
    """
    with yb.block("deploy:"):
        with yb.block("resources:"):
            with yb.block("reservations:"):
                with yb.block("devices:"):
                    with yb.block("- driver: nvidia"):
                        yb.add("count: 1 # all or number")
                        yb.add("capabilities: [gpu]")


def forge_model_puller(runtime: str, model: str) -> str:
    """
    Generates a robust script to ensure the model is manifest in the local runtime.
    """
    r = runtime.lower()

    # Gnostic Shell Builder (Simple string is sufficient here, but structured is better)
    lines = [
        "#!/bin/bash",
        "set -e",  # Exit on error
        "",
        "echo \"[Scaffold] Awakening Model Manager for {r}...\"",
    ]

    if r == "ollama":
        lines.extend([
            "CONTAINER_NAME=scaffold_ollama",
            "",
            "# 1. Wait for Daemon",
            "echo \"Waiting for Ollama to wake up...\"",
            "until [ \"$(docker inspect -f {{.State.Health.Status}} $CONTAINER_NAME)\" == \"healthy\" ]; do",
            "    sleep 1; echo -n \".\"",
            "done",
            "echo \"\"",
            "",
            f"# 2. Pull Model: {model}",
            f"echo \"Summoning {model}...\"",
            f"docker exec -it $CONTAINER_NAME ollama pull {model}",
            "echo \"[Scaffold] Model materialized.\""
        ])

    elif r == "llamacpp":
        lines.extend([
            "MODEL_URL=\"https://huggingface.co/TheBloke/{model}-GGUF/resolve/main/{model}.Q4_K_M.gguf\"",
            "TARGET_DIR=\"./models\"",
            "mkdir -p $TARGET_DIR",
            "",
            "echo \"Downloading GGUF from HuggingFace...\"",
            "wget -nc -P $TARGET_DIR $MODEL_URL || echo \"Model already exists or download failed.\"",
            "echo \"[Scaffold] Model verified in $TARGET_DIR.\""
        ])

    else:
        lines.append(f"echo \"No manual pull required for {r}. The container handles this on startup.\"")

    return "\n".join(lines).strip()