"""Normalization at the simulated-hardware / FastAPI boundary.

Public artifacts are sample-major (``data[time][channel]``); the processing
pipeline is channel-major (``samples[channel][time]``).  Keeping that
translation here lets physical adapters retain the same downstream contract.
"""
from datetime import datetime, timezone
from typing import Any

import numpy as np

from backend.app.core.schemas import SignalFrame


def normalize_packet(packet: dict[str, Any]) -> SignalFrame:
    """Accept the documented public packet or the legacy SignalFrame shape."""
    if "data" in packet:
        data = np.asarray(packet["data"], dtype=float)
        channels = packet.get("channels", [])
        if data.ndim != 2 or data.shape[0] == 0:
            raise ValueError("data must be a non-empty [time][channel] matrix")
        if channels and len(channels) != data.shape[1]:
            raise ValueError("channels must match the data matrix width")
        timestamp = packet.get("timestamp")
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp, timezone.utc)
        return SignalFrame(
            samples=data.T.tolist(),
            sampling_rate=int(packet.get("sampling_rate", 250)),
            device=packet.get("device", "mock-public-artifact"),
            timestamp=timestamp or datetime.now(timezone.utc),
        )
    return SignalFrame.model_validate(packet)
