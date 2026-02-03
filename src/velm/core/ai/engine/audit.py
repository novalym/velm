# Path: scaffold/core/ai/engine/audit.py
# --------------------------------------
import json
import time
import uuid
from pathlib import Path
from ..contracts import NeuralPrompt, NeuralRevelation


class ForensicScribe:
    """The Keeper of the Cognitive Log."""

    LOG_PATH = Path(".scaffold/ai_audit.jsonl")

    @staticmethod
    def log(provider: str, prompt: NeuralPrompt, result: NeuralRevelation, duration: float):
        if not ForensicScribe.LOG_PATH.parent.exists(): return

        entry = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "provider": provider,
            "model": result.model_used,
            "duration": round(duration, 3),
            "rag_used": bool(result.context_used),
            "prompt_len": len(prompt.user_query),
            "response_len": len(result.content),
            "tokens": result.token_usage,
            "query_preview": prompt.user_query[:100]
        }

        try:
            with open(ForensicScribe.LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except:
            pass

