# NIVO

Privacy-first, simulator-first BioSignal-to-Intent-to-AI reference implementation. It classifies deliberately calibrated interaction patterns; it does **not** read arbitrary thoughts.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install -r backend/requirements.txt
.venv/bin/uvicorn backend.app.main:app --reload
cd frontend && npm install && npm run dev
```

Open `http://localhost:5173`; API docs are at `http://localhost:8000/docs`. Run backend checks with `.venv/bin/pytest backend/tests -q`.

The architecture keeps wake detection local (see `wake_detection/`). A WebSocket at `/ws/v1/session/{id}` exists only for active sessions. The built-in simulator has deterministic test signatures for NIVO and the six supported intents; replace it with a hardware adapter without changing downstream interfaces. With the API running, `python3 -m simulator.local_bio_engine` performs the specified wake → WebSocket → SEARCH → agent → close demo.

## Simulation injection architecture

The development data path is intentionally equivalent to a future hardware path:

```text
Static mock artifact (.npy / JSON matrix)
  → Python MockHardwareStreamer
  → FastAPI /ws/v1/ingest/{session_id}
  → normalize public packet to channel × time samples
  → processing → features → intent → structured AI gateway request
```

`data/mock_signals/` is reserved for small, pre-processed public artifacts.
Files must contain a two-dimensional `time × channel` float matrix.  The
directory is suitable for 10–20 second snippets, not raw datasets. In
`ENVIRONMENT=development` (the default), the streamer generates a deterministic
microvolt-like fallback matrix when no `.npy` artifact is available.

The ingestion WebSocket accepts the documented public packet format:

```json
{"timestamp": 1790419200.125, "channels": ["Fp1", "Fp2"], "data": [[-12.45, -14.21]], "sampling_rate": 250}
```

`data` is sample-major on the wire and is normalized once at the boundary;
downstream modules retain their channel-major device contract. Resting data is
a **NO WAKE** condition. The explicit development routing labels live in
`backend/app/intent/routing.py`: an alpha/wake cue activates NIVO locally, and
left/right motor-imagery labels map to NEXT/SELECT, with a SEARCH signature
available for end-to-end testing. These labels are calibration aids, not claims
of general thought decoding.

To stream an artifact, first create an active session, then run:

```bash
python3 -m simulator.mock_hardware_streamer --session nivo_your_session_id
```

Use `--artifact data/mock_signals/example.npy` to select a file and `--loop` to
reconnect after temporary WebSocket failures. Packet batches default to 100 ms;
set `NIVO_STREAM_BATCH_MS` to adjust them.
