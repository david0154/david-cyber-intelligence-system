"""
LLM Brain Module - Mixtral GGUF via ctransformers
FIXED: Proper error handling, fallback stub, offline mode
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
from loguru import logger


class LLMBrain:
    def __init__(self, model_path: str = None, model_type: str = "mistral"):
        self.model_path = model_path or os.getenv("LLM_MODEL_PATH", "models/mixtral.gguf")
        self.model_type = model_type
        self.model = None
        self._load_model()

    def _load_model(self):
        try:
            from ctransformers import AutoModelForCausalLM
            if not os.path.exists(self.model_path):
                logger.warning(f"[LLM] Model not found: {self.model_path} — running in stub mode.")
                return
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path, model_type=self.model_type, gpu_layers=0
            )
            logger.success("[LLM] Mixtral brain loaded.")
        except ImportError:
            logger.warning("[LLM] ctransformers not installed. Stub mode active.")
        except Exception as e:
            logger.error(f"[LLM] Load failed: {e}")

    def think(self, prompt: str, max_tokens: int = 512) -> str:
        if self.model is None:
            return self._stub(prompt)
        try:
            return self.model(prompt, max_new_tokens=max_tokens)
        except Exception as e:
            logger.error(f"[LLM] Inference error: {e}")
            return f"LLM error: {e}"

    def explain_threat(self, threat_data: dict) -> str:
        prompt = (
            "You are a cybersecurity expert AI.\n"
            "Analyze this threat data and give:\n"
            "1. Threat summary\n2. Attack type\n"
            "3. Risk level (LOW/MEDIUM/HIGH/CRITICAL)\n"
            "4. Recommended actions\n\n"
            f"Data: {threat_data}\n\nAnalysis:"
        )
        return self.think(prompt)

    def _stub(self, prompt: str) -> str:
        return (
            f"[LLM OFFLINE] Received: '{prompt[:80]}...'\n"
            "Download Mixtral GGUF and set LLM_MODEL_PATH in .env\n"
            "Get model: https://huggingface.co/TheBloke/Mixtral-8x7B-Instruct-v0.1-GGUF"
        )
