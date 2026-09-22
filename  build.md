# NIVO — BioSignal-to-Intent-to-AI Agent
## Master Build Prompt

You are an expert full-stack, real-time systems, signal-processing, and machine-learning engineer.

Your task is to design and build the complete NIVO project described below.

Do not treat this as a conceptual mockup. Build the project as a modular, runnable software system with a clear path from simulated biosignal data to real EEG hardware integration.

==================================================
1. PROJECT OBJECTIVE
==================================================

NIVO is a BioSignal-to-Intent-to-AI interaction system.

The core idea is:

User
→ Biosignal / EEG device
→ Local Bio Engine
→ NIVO Wake Detection
→ Active WebSocket Session
→ Biosignal Processing
→ Intent Detection
→ Confidence Evaluation
→ Context Construction
→ Codeless AI Gateway
→ AI Agent
→ Response / Action

The system must NOT attempt to decode arbitrary human thoughts into unrestricted text.

The initial system must instead detect predefined, experimentally trained user interaction patterns and convert them into structured digital intents.

The main user experience should resemble a wake-word AI assistant:

"Think NIVO"
→ NIVO wakes
→ active AI session starts
→ user's intended interaction is processed
→ AI agent responds or performs an action
→ session ends
→ system returns to low-resource wake mode.

==================================================
2. CORE PRODUCT CONCEPT
==================================================

NIVO is the wake word / activation cue.

The system should support:

1. A default wake word: NIVO
2. A personalized wake cue in the future
3. Local wake detection
4. No permanent cloud biosignal stream
5. WebSocket activation only after wake detection
6. Active biosignal streaming during an AI session
7. Intent classification during the active session
8. Internal confidence handling
9. No user-facing confirmation step
10. AI/agent execution after a valid intent

IMPORTANT:

The system should NOT assume that the EEG literally contains the word "NIVO".

Instead, "NIVO" represents a user-defined mental activation cue.

During calibration, the system learns the user's biosignal pattern associated with intentionally thinking/performing the NIVO activation cue.

==================================================
3. FUNDAMENTAL ARCHITECTURE
==================================================

Implement the system using two major operating states.

STATE A — SLEEP / WAKE MODE

The local device continuously performs lightweight processing.

Flow:

EEG
→ lightweight preprocessing
→ NIVO Wake Detector
→ wake probability

If wake probability is below threshold:

NO WAKE
→ continue local monitoring

If wake probability reaches the configured threshold:

WAKE DETECTED
→ start AI session

The cloud/backend must NOT receive a continuous full biosignal stream during this state.

STATE B — ACTIVE AI SESSION

After NIVO wake detection:

NIVO
→ Session Manager
→ WebSocket connection
→ active biosignal stream
→ signal processing
→ feature extraction
→ intent classification
→ confidence evaluation
→ context construction
→ Codeless AI Gateway
→ AI agent
→ response/action

After the interaction is completed:

AI session ends
→ WebSocket closes
→ return to local wake mode

==================================================
4. IMPORTANT DESIGN PRINCIPLE
==================================================

Do NOT create a permanent WebSocket connection for every user.

The WebSocket should be created only when the local NIVO wake detector activates the assistant.

This is required to reduce:

- unnecessary server connections
- continuous backend processing
- bandwidth consumption
- infrastructure load
- unnecessary transmission of biosignal data

The local wake detector should remain lightweight.

The heavier backend processing should happen only during active sessions.

==================================================
5. PROJECT COMPONENTS
==================================================

Build the system as independent modules.

Required modules:

A. Hardware Connector
B. Local Bio Engine
C. NIVO Wake Detector
D. Signal Ingestion
E. Signal Processing
F. Feature Extraction
G. Intent Classifier
H. Confidence Layer
I. Session Manager
J. Context Engine
K. Codeless AI Gateway
L. AI Provider Layer
M. AI Agent / Action Layer
N. Dashboard
O. Dataset / Calibration System
P. Logging and Monitoring

==================================================
6. HARDWARE ABSTRACTION
==================================================

Do not tightly couple the application to one EEG manufacturer.

Create a hardware abstraction layer.

Example:

BioSignalDevice
├── connect()
├── disconnect()
├── start_stream()
├── stop_stream()
└── get_samples()

Then create device adapters.

Example:

OpenBCIAdapter
FutureEEGAdapter
SimulationAdapter

The SimulationAdapter is mandatory for development without physical hardware.

The rest of the application must be able to operate using simulated biosignal data.

==================================================
7. SIMULATION MODE
==================================================

Build a complete simulation mode before requiring physical EEG hardware.

The simulator should generate realistic time-series biosignal-like data containing:

- baseline activity
- noise
- intentional activation events
- wake events
- different intent patterns
- artifacts
- variable signal quality

The simulator should allow developers to test:

WAKE
NO WAKE
NEXT
BACK
SELECT
CANCEL
SEARCH
ASK_AI

without physical hardware.

The simulator must behave through the same interfaces used by real hardware.

Do NOT create a separate fake architecture for simulation.

Simulation and real hardware must use the same downstream pipeline.

==================================================
8. NIVO WAKE DETECTOR
==================================================

The NIVO Wake Detector is the first ML component.

Its only responsibility is:

"Did the user intentionally activate NIVO?"

Output:

{
  "wake": true,
  "confidence": 0.96
}

or:

{
  "wake": false,
  "confidence": 0.42
}

The wake detector must be lightweight enough to run locally.

The wake detector should support:

- configurable threshold
- cooldown period
- false-trigger protection
- calibration
- per-user model/data
- model versioning

Do NOT use a user-facing confirmation prompt.

Instead use internal confidence logic.

Example:

wake confidence < threshold
→ ignore

wake confidence >= threshold
→ activate session

==================================================
9. NIVO CALIBRATION
==================================================

Build an onboarding/calibration workflow.

The user should be instructed to intentionally perform the NIVO activation cue multiple times.

The system records biosignal samples and labels them.

Example:

Trial 01 → NIVO
Trial 02 → NIVO
Trial 03 → NIVO
...
Trial N → NIVO

Also collect negative examples:

- normal resting
- reading
- normal thinking
- eye movement
- blinking
- movement
- other normal activity

The purpose is to teach the model the user's activation pattern rather than simply memorizing a word.

The calibration system must save the dataset and associate it with the user/model version.

==================================================
10. ACTIVE BIOSIGNAL PROCESSING
==================================================

Once NIVO activates the system, open the WebSocket.

Example:

Client
→ WebSocket
→ FastAPI backend
→ stream manager

Use persistent streaming communication for the active session.

Do not send every biosignal sample through separate REST requests.

REST APIs can be used for:

- authentication
- session creation
- configuration
- calibration
- model management
- metadata

WebSocket should be used for real-time active biosignal streaming.

==================================================
11. SIGNAL PROCESSING
==================================================

Build a signal-processing pipeline.

Required conceptual stages:

Raw signal
→ preprocessing
→ filtering
→ artifact handling
→ windowing
→ feature extraction

Use appropriate Python scientific libraries such as:

- NumPy
- SciPy
- MNE where appropriate

The processing layer must be modular.

Do not hard-code signal-processing parameters throughout the project.

Store configuration centrally.

Example:

sampling_rate
window_size
filter_low
filter_high
artifact_threshold

==================================================
12. FEATURE EXTRACTION
==================================================

Convert processed biosignal windows into numerical features.

The feature extraction layer should be independent from the classifier.

Possible feature groups include:

- frequency-domain features
- time-domain features
- channel statistics
- band-power features
- temporal features

The system must make it possible to replace or extend the feature extractor without rewriting the backend.

==================================================
13. INTENT CLASSIFIER
==================================================

The intent classifier operates only after the NIVO session is active.

Do NOT initially attempt unrestricted thought-to-text.

Use a small set of predefined intents.

Initial intent set:

SELECT
NEXT
BACK
CANCEL
SEARCH
ASK_AI

The model should output:

{
  "intent": "SEARCH",
  "confidence": 0.91
}

The initial implementation should support a simple baseline model before introducing a more complex deep-learning model.

Make the model architecture replaceable.

Potential implementation path:

Baseline ML
→ improved ML
→ 1D CNN or other neural model

Do not assume that a complex neural network automatically produces better results.

==================================================
14. CONFIDENCE HANDLING
==================================================

There should be NO user-facing confirmation step.

Do not ask:

"Are you sure?"

Instead use internal confidence evaluation.

Example:

Prediction:
SEARCH

Confidence:
0.91

Threshold:
0.85

Result:
ACCEPT

If:

Confidence:
0.62

Result:
IGNORE

Implement:

- minimum confidence
- temporal consistency
- cooldown
- duplicate suppression
- session state
- optional configurable thresholds

The confidence layer must be separate from the classifier.

==================================================
15. INTENT PROTOCOL
==================================================

Create a standardized JSON representation for biological interactions.

Example:

{
  "session_id": "session_123",
  "intent": "SEARCH",
  "confidence": 0.91,
  "timestamp": "...",
  "source": {
    "type": "EEG",
    "device": "..."
  }
}

The protocol must be versioned.

Example:

{
  "protocol_version": "1.0"
}

The downstream AI system should never need to understand raw EEG.

==================================================
16. CONTEXT ENGINE
==================================================

The Context Engine takes:

Intent
+
confidence
+
session information
+
allowed application context

and creates structured AI context.

Example:

{
  "intent": "SEARCH",
  "confidence": 0.91,
  "context": {
    "application": "browser",
    "session": "research"
  }
}

Keep the context layer modular.

The AI system should receive semantic structured information rather than raw biological waveforms.

==================================================
17. CODELESS AI GATEWAY
==================================================

Build a provider-independent AI gateway.

Architecture:

BioSignal
→ Intent
→ Context
→ Codeless AI Gateway
→ AI Provider
→ AI Agent

Do not tightly couple the gateway to a single LLM provider.

The gateway should provide an abstraction such as:

AIProvider
├── generate()
├── stream()
└── execute()

Possible providers can later include:

OpenAI
Gemini
Local LLM
Other compatible providers

The AI provider should be configurable through environment variables.

==================================================
18. AI AGENT
==================================================

The AI agent receives structured intent/context.

Example:

{
  "intent": "SEARCH",
  "context": {
    "application": "browser"
  }
}

The agent determines the appropriate action.

Example:

SEARCH
→ determine search request
→ execute search tool
→ return result

ASK_AI
→ construct AI request
→ generate response

SELECT
→ execute the relevant application action

The biological layer should only provide the interaction signal.

The AI agent handles semantic interpretation and tool/action execution.

==================================================
19. SESSION STATE MACHINE
==================================================

Implement the following states:

SLEEP
STARTING
LISTENING
PROCESSING
RESPONDING
ENDING

Flow:

SLEEP
→ NIVO detected
→ STARTING
→ WebSocket connected
→ LISTENING
→ intent detected
→ PROCESSING
→ AI action
→ RESPONDING
→ ENDING
→ SLEEP

The state machine must prevent invalid transitions.

==================================================
20. SESSION MANAGEMENT
==================================================

Every active interaction should have a session ID.

Example:

session_id:
nivo_8F21A

Track:

- user
- device
- start time
- end time
- state
- signal quality
- detected intents
- confidence
- AI request status
- latency
- errors

When the session ends, close the WebSocket cleanly.

Implement reconnect/error handling.

==================================================
21. FRONTEND DASHBOARD
==================================================

Build a React + Tailwind dashboard.

The dashboard should show:

NIVO status:

SLEEPING
or
LISTENING
or
PROCESSING
or
RESPONDING

Live connection:

WebSocket:
CONNECTED / DISCONNECTED

Signal:

Signal quality
Sampling rate
Channel status

Wake:

NIVO detected
Wake confidence

Intent:

Detected intent
Intent confidence

AI:

Provider
Processing status
Latency
Response

Session:

Session ID
Session duration
Current state

The dashboard is primarily for development, debugging, calibration, and demonstration.

==================================================
22. BACKEND
==================================================

Use Python + FastAPI.

Required backend responsibilities:

- authentication
- device/session management
- WebSocket handling
- signal stream handling
- processing pipeline
- intent inference
- confidence handling
- context construction
- AI gateway
- session lifecycle
- logging
- configuration

Use asynchronous programming where appropriate.

Do not block the WebSocket event loop with heavy synchronous operations.

==================================================
23. DATA STORAGE
==================================================

Use PostgreSQL for application metadata.

Store things such as:

users
devices
sessions
models
model_versions
calibration_sessions
intent_events
AI_requests

Do not unnecessarily store raw biosignal data permanently in PostgreSQL.

Experimental datasets should use appropriate dataset storage such as files/Parquet or another suitable data layer.

Raw biosignal data should remain local wherever possible.

==================================================
24. PRIVACY ARCHITECTURE
==================================================

Raw biosignal data should preferably be processed locally.

Do not continuously transmit raw EEG to the cloud when the system is in wake/sleep mode.

During an active session, only transmit the minimum data required by the architecture.

The AI layer should receive structured semantic information rather than raw EEG whenever possible.

Build the project with privacy-by-design principles.

==================================================
25. API DESIGN
==================================================

Provide APIs for:

POST /api/v1/auth/...
POST /api/v1/sessions
GET  /api/v1/sessions/{id}
POST /api/v1/calibration/start
POST /api/v1/calibration/complete
GET  /api/v1/models
POST /api/v1/models/train
GET  /api/v1/config

WebSocket:

/ws/v1/session/{session_id}

The exact API design can be improved during implementation, but keep the API versioned.

==================================================
26. PROJECT STRUCTURE
==================================================

Use a clean modular repository.

Suggested structure:

nivo/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── websocket/
│   │   ├── sessions/
│   │   ├── biosignal/
│   │   ├── signal_processing/
│   │   ├── features/
│   │   ├── wake_detection/
│   │   ├── intent/
│   │   ├── context/
│   │   ├── gateway/
│   │   ├── ai/
│   │   └── main.py
│   │
│   ├── models/
│   ├── datasets/
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── services/
│
├── simulator/
│
├── ml/
│   ├── training/
│   ├── evaluation/
│   └── models/
│
├── docs/
│
├── docker/
│
├── docker-compose.yml
├── .env.example
└── README.md

You may improve this structure if there is a strong technical reason.

==================================================
27. DEVELOPMENT PRIORITY
==================================================

Build in the following order.

PHASE 1
Simulation

Create simulated biosignal input.

↓

PHASE 2
Signal ingestion

Create the real-time streaming pipeline.

↓

PHASE 3
Signal processing

Implement preprocessing and feature extraction.

↓

PHASE 4
NIVO wake detection

Implement calibration and wake inference.

↓

PHASE 5
Session lifecycle

Implement:

SLEEP
→ WAKE
→ WebSocket
→ ACTIVE
→ CLOSE
→ SLEEP

↓

PHASE 6
Intent classification

Implement predefined intent classification.

↓

PHASE 7
Confidence handling

Implement internal confidence thresholds and temporal validation.

↓

PHASE 8
Context Engine

Convert intent + context into structured data.

↓

PHASE 9
Codeless AI Gateway

Connect the structured request to an AI provider.

↓

PHASE 10
AI Agent

Execute actions based on the structured intent.

↓

PHASE 11
Dashboard

Show the complete pipeline visually.

↓

PHASE 12
Hardware integration

Replace the simulator with a supported real EEG/biosignal device while preserving the same interfaces.

==================================================
28. FIRST END-TO-END DEMONSTRATION
==================================================

The first successful demo should demonstrate exactly this:

1. Start the NIVO application.
2. System enters SLEEP mode.
3. Simulator generates normal biosignal activity.
4. No backend WebSocket session exists.
5. Simulator generates the NIVO activation pattern.
6. Local wake detector detects NIVO.
7. Wake confidence exceeds the configured threshold.
8. Session Manager creates a session.
9. WebSocket opens.
10. Active biosignal streaming begins.
11. Simulator generates a trained intent pattern.
12. Intent classifier detects SEARCH.
13. Confidence layer accepts SEARCH.
14. Context Engine creates structured context.
15. Codeless AI Gateway receives the intent.
16. AI agent processes the request.
17. AI agent returns an action/response.
18. Session ends.
19. WebSocket closes.
20. System returns to SLEEP / NIVO wake mode.

This simulation must work completely before real hardware integration.

==================================================
29. TESTING REQUIREMENTS
==================================================

Create tests for:

- device connection
- signal ingestion
- filtering
- feature extraction
- wake detection
- confidence handling
- session state transitions
- WebSocket connection
- intent classification
- JSON protocol validation
- context construction
- AI gateway
- AI provider abstraction
- session termination
- error recovery

Also create an end-to-end integration test:

NIVO wake
→ WebSocket
→ intent
→ AI gateway
→ agent
→ session close

==================================================
30. ENGINEERING RULES
==================================================

1. Do not build everything as one monolithic Python file.

2. Keep hardware-specific code separate from signal-processing code.

3. Keep ML models separate from API logic.

4. Keep AI provider integrations behind an abstraction.

5. Keep configuration in environment/config files.

6. Do not hard-code API keys.

7. Use .env for secrets.

8. Add proper logging.

9. Add error handling.

10. Use typed schemas for WebSocket/API messages.

11. Version the BioSignal-to-Intent protocol.

12. Keep the simulator compatible with the real hardware interface.

13. Do not send raw EEG directly to the LLM.

14. Do not claim that the system can read arbitrary human thoughts.

15. Do not implement a user-facing confirmation prompt.

16. Use internal confidence handling instead.

17. Do not maintain permanent cloud WebSocket connections for sleeping users.

18. Make the wake detector local and lightweight.

==================================================
31. IMPORTANT SCIENTIFIC SCOPE
==================================================

The project must remain within the following scope:

This is a biosignal interaction system.

The project does NOT claim:

- arbitrary thought reading
- direct DNA-to-AI communication
- DNA acting as a wireless antenna
- direct knowledge injection into the brain
- unrestricted thought-to-text decoding

NIVO represents a trained activation cue associated with a user's biosignal pattern.

The initial system is intended to demonstrate:

Biosignal
→ Wake
→ Intent
→ Structured digital command
→ AI
→ Action

==================================================
32. EXPECTED DELIVERABLE
==================================================

Build a complete runnable repository.

The final project should include:

- backend
- frontend
- simulator
- ML pipeline
- calibration workflow
- NIVO wake detector
- intent classifier
- WebSocket session system
- confidence system
- context engine
- Codeless AI gateway
- AI provider abstraction
- AI agent
- database models
- API documentation
- tests
- Docker configuration
- .env.example
- README
- setup instructions
- architecture documentation

==================================================
33. DEVELOPMENT BEHAVIOR
==================================================

Before writing large amounts of code:

1. Inspect the repository.
2. Determine what already exists.
3. Reuse existing components where appropriate.
4. Identify missing components.
5. Create a technical implementation plan.
6. Then implement incrementally.

Do not unnecessarily rewrite existing working code.

If an implementation decision is ambiguous, choose the simplest modular architecture that preserves the project requirements above.

Do not fabricate hardware capabilities.

If a real EEG device is not available, use the simulator and clearly isolate the hardware adapter.

==================================================
34. FINAL TARGET
==================================================

The final system must represent this exact product experience:

                    USER
                      │
                 Think "NIVO"
                      │
                      ▼
             LOCAL WAKE MODEL
                      │
              Confidence check
                      │
                   WAKE
                      │
                      ▼
             CREATE SESSION
                      │
                      ▼
               WEBSOCKET OPEN
                      │
                      ▼
             ACTIVE BIOSIGNAL
                      │
                      ▼
             SIGNAL PROCESSING
                      │
                      ▼
              INTENT CLASSIFIER
                      │
                      ▼
             CONFIDENCE CHECK
                      │
                      ▼
               CONTEXT ENGINE
                      │
                      ▼
             CODELESS AI GATEWAY
                      │
                      ▼
                 AI AGENT
                      │
                      ▼
              RESPONSE / ACTION
                      │
                      ▼
               END SESSION
                      │
                      ▼
               WEBSOCKET CLOSE
                      │
                      ▼
             LOCAL NIVO WAKE MODE

The primary engineering objective is to make this complete lifecycle work reliably in simulation first and then make the same pipeline compatible with real biosignal/EEG hardware.