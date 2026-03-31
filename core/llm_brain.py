"""
LLM Brain Module — Mixtral GGUF via ctransformers
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
from loguru import logger

try:
    from ctransformers import AutoModelForCausalLM
    CTRANSFORMERS_AVAILABLE = True
except ImportError:
    CTRANSFORMERS_AVAILABLE = False
    logger.warning("ctransformers not installed. Using fallback mode.")


class LLMBrain:
    """
    Core LLM Brain powered by Mixtral GGUF model.
    Handles: understanding, reasoning, explanation, action suggestions.
    """

    def __init__(self, model_path: str = None, model_type: str = "mistral"):
        self.model_path = model_path or os.getenv("LLM_MODEL_PATH", "models/mixtral.gguf")
        self.model_type = model_type
        self.model = None
        self._load_model()

    def _load_model(self):
        if not CTRANSFORMERS_AVAILABLE:
            logger.warning("LLM running in offline/stub mode.")
            return
        if not os.path.exists(self.model_path):
            logger.warning(f"Model not found at {self.model_path}. Download required.")
            return
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_path,
                model_type=self.model_type,
                gpu_layers=0  # CPU mode; increase for GPU
            )
            logger.success("LLM Brain loaded successfully.")
        except Exception as e:
            logger.error(f"LLM load failed: {e}")

    def think(self, prompt: str, max_tokens: int = 512) -> str:
        """
        Generate a response from the LLM given a prompt.
        Returns a string explanation/analysis.
        """
        if self.model is None:
            return self._fallback_response(prompt)
        try:
            response = self.model(prompt, max_new_tokens=max_tokens)
            return response
        except Exception as e:
            logger.error(f"LLM inference error: {e}")
            return f"LLM Error: {e}"

    def explain_threat(self, threat_data: dict) -> str:
        prompt = f"""
You are a cybersecurity expert AI.
Analyze the following threat data and provide:
1. Threat summary
2. Attack type
3. Risk level (LOW/MEDIUM/HIGH/CRITICAL)
4. Recommended actions

Threat Data:
{threat_data}

Response:"""
        return self.think(prompt)

    def _fallback_response(self, prompt: str) -> str:
        return (
            f"[LLM OFFLINE] Query received: '{prompt[:100]}...'"
            " Please download the Mixtral GGUF model and set LLM_MODEL_PATH."
        )
