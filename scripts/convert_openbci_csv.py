"""Convert an OpenBCI GUI CSV into NIVO's [time][six EEG channels] artifact.

Usage:
    python3 scripts/convert_openbci_csv.py OpenBCI-RAW-New_Alpha.csv
"""
import argparse
from pathlib import Path

import numpy as np


def convert(source: Path, destination: Path, samples: int = 5000) -> np.ndarray:
    # OpenBCI metadata begins with %, so NumPy safely ignores it. The first
    # numerical field is time in ms; fields 1..8 are EEG; the final fields are
    # accelerometer/auxiliary data. NIVO's public-artifact contract uses six.
    raw = np.loadtxt(source, delimiter=",", comments="%", dtype=np.float64)
    if raw.ndim != 2 or raw.shape[1] < 7:
        raise ValueError("expected time plus at least six EEG columns")
    eeg = raw[:, 1:7]
    if len(eeg) == 0:
        raise ValueError("CSV contains no EEG rows")

    # This recording has large per-electrode DC offsets (for example -42,000).
    # Centering and robustly scaling prevents the processing safety clip from
    # treating every sample as an artifact, while preserving channel dynamics.
    eeg = eeg - np.median(eeg, axis=0, keepdims=True)
    scale = np.quantile(np.abs(eeg), 0.995, axis=0, keepdims=True)
    eeg = eeg / np.maximum(scale / 3.0, 1e-9)
    eeg = np.clip(eeg, -5.0, 5.0)

    repeats = int(np.ceil(samples / len(eeg)))
    artifact = np.tile(eeg, (repeats, 1))[:samples].astype(np.float32)
    destination.parent.mkdir(parents=True, exist_ok=True)
    np.save(destination, artifact)
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/mock_signals/example.npy"))
    parser.add_argument("--samples", type=int, default=5000, help="250 Hz samples; 5000 is 20 seconds")
    args = parser.parse_args()
    artifact = convert(args.source, args.output, args.samples)
    print(f"Saved {args.output}: {artifact.shape[0]} samples × {artifact.shape[1]} channels")


if __name__ == "__main__":
    main()
