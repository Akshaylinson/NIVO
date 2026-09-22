from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    sampling_rate: int = 250
    channels: int = 4
    window_seconds: float = 1.0
    wake_threshold: float = float(os.getenv("NIVO_WAKE_THRESHOLD", "0.82"))
    intent_threshold: float = float(os.getenv("NIVO_INTENT_THRESHOLD", "0.78"))
    protocol_version: str = "1.0"
    ai_provider: str = os.getenv("NIVO_AI_PROVIDER", "mock")
settings = Settings()
