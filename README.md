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
