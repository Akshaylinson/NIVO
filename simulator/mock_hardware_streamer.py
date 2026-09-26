"""Stream static public-style EEG artifacts to NIVO's ingestion WebSocket.

Run after creating a session:
``python -m simulator.mock_hardware_streamer --session nivo_xxx --loop``.
The default artifact is generated only when no local .npy/.json artifact exists.
"""
import argparse
import asyncio
import json
import time
from pathlib import Path

import numpy as np
import websockets

from backend.app.core.config import settings

DEFAULT_CHANNELS = ["Fp1", "Fp2", "C3", "C4", "O1", "O2"]


def generate_artifact(seconds: float = 20, sampling_rate: int = 250, channels: int = 6) -> np.ndarray:
    """Create a deterministic microvolt-like sample-major fallback artifact."""
    rng = np.random.default_rng(17)
    t = np.arange(int(seconds * sampling_rate)) / sampling_rate
    signal = rng.normal(0, 0.16, (t.size, channels)) + 0.30 * np.sin(2 * np.pi * 10 * t)[:, None]
    # A short alpha burst makes the fallback useful in wake-cue demos.
    cue = (t > 5) & (t < 6)
    signal[cue] += 1.2 * np.sin(2 * np.pi * 10 * t[cue])[:, None]
    return signal.astype(np.float32)


def load_artifact(path: str | None = None) -> tuple[np.ndarray, list[str]]:
    if settings.environment.lower() != "development":
        raise RuntimeError("MockHardwareStreamer is limited to ENVIRONMENT=development")
    root = Path(settings.mock_signal_dir)
    selected = Path(path) if path else next(iter([*root.glob("*.npy"), *root.glob("*.json")]), None) if root.exists() else None
    if selected and selected.exists():
        data = np.load(selected) if selected.suffix == ".npy" else np.asarray(json.loads(selected.read_text())["data"])
        if data.ndim != 2:
            raise ValueError("mock artifact must be [time][channel]")
        return data.astype(float), DEFAULT_CHANNELS[: data.shape[1]]
    return generate_artifact(), DEFAULT_CHANNELS


class MockHardwareStreamer:
    def __init__(self, session_id: str, url: str = "ws://localhost:8000", artifact: str | None = None, batch_ms: int = settings.stream_batch_ms):
        self.session_id, self.url, self.batch_ms = session_id, url.rstrip("/"), batch_ms
        self.data, self.channels = load_artifact(artifact)

    async def stream(self, loop: bool = False) -> None:
        chunk = max(1, round(settings.sampling_rate * self.batch_ms / 1000))
        endpoint = f"{self.url}/ws/v1/ingest/{self.session_id}"
        while True:
            try:
                async with websockets.connect(endpoint) as socket:
                    await socket.recv()  # LISTENING acknowledgement
                    for start in range(0, len(self.data), chunk):
                        await socket.send(json.dumps({"timestamp": time.time(), "channels": self.channels, "data": self.data[start:start + chunk].tolist(), "sampling_rate": settings.sampling_rate, "device": "mock-public-artifact"}))
                        await socket.recv()  # consume telemetry / intent output
                        await asyncio.sleep(self.batch_ms / 1000)
            except (OSError, websockets.WebSocketException):
                if not loop:
                    raise
                await asyncio.sleep(1)
                continue
            if not loop:
                return


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session", required=True)
    parser.add_argument("--url", default="ws://localhost:8000")
    parser.add_argument("--artifact")
    parser.add_argument("--loop", action="store_true")
    args = parser.parse_args()
    asyncio.run(MockHardwareStreamer(args.session, args.url, args.artifact).stream(args.loop))


if __name__ == "__main__":
    main()
