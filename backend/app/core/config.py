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
    environment: str = os.getenv("ENVIRONMENT", "development")
    mock_signal_dir: str = os.getenv("NIVO_MOCK_SIGNAL_DIR", "data/mock_signals")
    stream_batch_ms: int = int(os.getenv("NIVO_STREAM_BATCH_MS", "100"))
settings = Settings()
