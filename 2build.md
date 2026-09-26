Here is the comprehensive architecture update layout and a structured, ready-to-use prompt designed specifically for your development agent.First, let's address how to store and access this data within your repository, and then we will jump straight into the implementation prompt.Data Storage & Integration ArchitectureTo integrate this without breaking your existing tech stack, you should treat the public files as "Static Mock Artifacts."Where to store it:Create a dedicated directory inside your repository: /data/mock_signals/. Do not store raw .edf or massive datasets inside Git if they exceed a few megabytes; instead, save a few standardized NumPy arrays (.npy) or high-fidelity JSON array snippets representing 10–20 seconds of continuous brain activity.How to access it:Your Hardware Connector service should check an environment variable (e.g., ENVIRONMENT=DEVELOPMENT). If it is set to development, it bypasses the physical Bluetooth/USB device driver and targets the local files using Python's numpy.load() or json.load().Data Format Structure:Your mock stream should emit data as a continuous stream of JSON packets over the WebSocket. A standard package looks like this:json{
  "timestamp": 1790419200.125,
  "channels": ["Fp1", "Fp2", "C3", "C4", "O1", "O2"],
  "data": [
    [-12.45, -14.21, 5.82, 12.11, -2.04, 8.44], 
    [-11.20, -13.88, 6.10, 11.95, -1.89, 7.90]
  ],
  "sampling_rate": 250
}
Use code with caution.Each sub-array inside "data" represents a microvolt reading across all configured scalp channels at a precise millisecond snapshot.Master Prompt for Your Development AgentCopy and paste the block below directly to your development AI or engineering agent to automatically update the project architecture and generate the code modules.markdown# Context & Objective
We are building a BioSignal-to-Intent-to-AI prototype named NIVO. The project relies on an EEG/Biosignal wake-word and real-time intent workflow. Because physical BCI hardware is currently unavailable, we need to adapt our architecture to run on open-source, public EEG data streams using a simulation layer.

You must update the current architecture to implement a three-step simulation framework:
1. Public Data Handling Strategy (Reading pre-processed/saved signal structures).
2. Mock Hardware Stream (Simulating the Hardware Connector & WebSocket broadcast loop).
3. Pipeline Signal-to-Intent Mapping (Mapping public structural data features to NIVO intents).

# Reference Technical Stack
- Local Processing & Automation: Python
- Backend Services: FastAPI
- Protocols: Real-time WebSockets
- Signal Analytics: NumPy, SciPy
- Architecture Layers to Modify: Hardware Connector, Local Bio Engine, Signal Ingestion Service.

# Tasks to Execute

## Task 1: Update System Architecture Documentation
Modify Section 4 (System Architecture) of our specifications to natively support the simulation injection layer:
- Old Path: User → EEG/Biosignal Device → Hardware Connector → Local Bio Engine...
- New Path: [Static Mock Artifact Repository (.npy / JSON matrix)] → Python Simulated Hardware Streamer → FastAPI Ingestion Endpoint → Local Bio Engine...

## Task 2: Code Implementation - Mock Hardware Streamer
Generate a robust Python module (`mock_hardware_streamer.py`) that performs the following procedures:
1. Simulates a standard 4 to 8-channel EEG array with a fixed sampling rate (e.g., 250 Hz).
2. Loads a pre-existing matrix array (generate a mock NumPy array or multi-dimensional array representing microvolt float fluctuations if no file is present).
3. Implements an asynchronous loop that fragments the matrix array into precise time windows (e.g., streaming every 4ms to emulate 250Hz, or batching 100ms packets).
4. Connects via WebSockets to our FastAPI backend (`Signal Ingestion Service`) and continuous streams the chunks without crashing.

## Task 3: Code Implementation - Pipeline Intake & Intent Mapping
Update the `Signal Ingestion Service` and `Intent Model` frameworks to process the simulated incoming format:
1. Create a configuration matrix mapping public data signatures to our proprietary system requirements:
   - Baseline/Resting data chunks map to -> Lightweight Local Wake State (NO WAKE)
   - Alpha-wave power bursts or distinct motor imagery anomalies map to -> "NIVO" Wake Cue (WAKE - detected)
   - Left/Right movement imagery anomalies map to -> SELECT, NEXT, or SEARCH intents.
2. Provide a sample routing dictionary or conditional structure showing how these microvolt patterns stream through the Intent Model and feed cleanly into the Codeless AI Gateway as structured JSON schemas.