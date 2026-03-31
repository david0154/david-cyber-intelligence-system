"""
IDS ML Model — LSTM / Autoencoder for anomaly detection
Developed by Devil Pvt Ltd & Nexuzy Tech Pvt Ltd
"""

import os
import numpy as np
from loguru import logger


class IDSModel:
    """
    Intrusion Detection System using LSTM Autoencoder.
    Trained on network flow features.
    """

    def __init__(self, model_path: str = "models/ids_autoencoder.pt"):
        self.model_path = model_path
        self.model = None
        self.threshold = 0.05
        self._load()

    def _load(self):
        if not os.path.exists(self.model_path):
            logger.warning(f"IDS model not found at {self.model_path}. Train or download first.")
            return
        try:
            import torch
            self.model = torch.load(self.model_path, map_location="cpu")
            self.model.eval()
            logger.success("IDS model loaded.")
        except Exception as e:
            logger.error(f"IDS model load failed: {e}")

    def predict(self, features: np.ndarray) -> dict:
        """
        Predict anomaly from network flow features.
        features: numpy array shape (1, timesteps, feature_dim)
        """
        if self.model is None:
            return {"anomaly": False, "score": 0.0, "message": "Model not loaded."}
        try:
            import torch
            x = torch.FloatTensor(features)
            with torch.no_grad():
                reconstructed = self.model(x)
                loss = ((x - reconstructed) ** 2).mean().item()
            is_anomaly = loss > self.threshold
            return {
                "anomaly": is_anomaly,
                "reconstruction_error": round(loss, 6),
                "threshold": self.threshold,
                "verdict": "ATTACK" if is_anomaly else "NORMAL",
            }
        except Exception as e:
            logger.error(f"IDS predict error: {e}")
            return {"anomaly": False, "score": 0.0, "error": str(e)}

    def train(self, X_train: np.ndarray, epochs: int = 20, lr: float = 1e-3):
        """Basic training loop for the autoencoder."""
        try:
            import torch
            import torch.nn as nn
            from torch.optim import Adam

            class LSTMAutoencoder(nn.Module):
                def __init__(self, input_dim, hidden_dim=64):
                    super().__init__()
                    self.encoder = nn.LSTM(input_dim, hidden_dim, batch_first=True)
                    self.decoder = nn.LSTM(hidden_dim, input_dim, batch_first=True)

                def forward(self, x):
                    enc_out, (h, _) = self.encoder(x)
                    h_rep = h.permute(1, 0, 2).repeat(1, x.size(1), 1)
                    dec_out, _ = self.decoder(h_rep)
                    return dec_out

            input_dim = X_train.shape[-1]
            model = LSTMAutoencoder(input_dim)
            optimizer = Adam(model.parameters(), lr=lr)
            criterion = nn.MSELoss()
            X_tensor = torch.FloatTensor(X_train)

            for epoch in range(epochs):
                model.train()
                optimizer.zero_grad()
                output = model(X_tensor)
                loss = criterion(output, X_tensor)
                loss.backward()
                optimizer.step()
                if epoch % 5 == 0:
                    logger.info(f"Epoch {epoch}/{epochs} | Loss: {loss.item():.6f}")

            os.makedirs("models", exist_ok=True)
            torch.save(model, self.model_path)
            self.model = model
            logger.success("IDS model trained and saved.")
        except Exception as e:
            logger.error(f"Training failed: {e}")
