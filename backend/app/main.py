import asyncio, time
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.schemas import *
from backend.app.signal_processing.pipeline import SignalProcessor
from backend.app.features.extractor import FeatureExtractor
from backend.app.intent.classifier import BaselineIntentClassifier
from backend.app.intent.confidence import ConfidenceLayer
from backend.app.sessions.manager import SessionManager
from backend.app.context.engine import ContextEngine
from backend.app.gateway.providers import MockProvider
from backend.app.ai.agent import AIAgent
from backend.app.biosignal.ingestion import normalize_packet
from simulator.mock_hardware_streamer import MockHardwareStreamer
app=FastAPI(title="NIVO",version="0.1.0"); app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_methods=["*"],allow_headers=["*"])
sessions=SessionManager(); processor=SignalProcessor(); features=FeatureExtractor(); classifier=BaselineIntentClassifier(); confidence=ConfidenceLayer(settings.intent_threshold); agent=AIAgent(MockProvider()); calibrations={}; simulations={}
def simulation_log(session_id:str, message:str):
    run=simulations.get(session_id)
    if run:
        run["logs"].append({"timestamp":time.strftime("%H:%M:%S"),"message":message})
        run["logs"]=run["logs"][-100:]
@app.get("/health")
def health(): return {"status":"ok","mode":"privacy-first","protocol_version":settings.protocol_version}
@app.post("/api/v1/auth/demo")
def auth(): return {"access_token":"demo-token","token_type":"bearer"}
@app.post("/api/v1/sessions",response_model=SessionView)
def create_session(): return sessions.create()
@app.post("/api/v1/simulations/start")
async def start_simulation():
    """Dashboard-owned simulation: one session and one server-side streamer."""
    session=sessions.create(device="mock-public-artifact")
    simulations[session.id]={"state":"STARTING","packets":0,"logs":[]}
    simulation_log(session.id,"Session created; loading data/mock_signals/example.npy")
    async def run():
        try:
            simulations[session.id]["state"]="STREAMING"
            streamer=MockHardwareStreamer(session.id,url="ws://127.0.0.1:8000",on_log=lambda message:simulation_log(session.id,message))
            await streamer.stream()
            simulations[session.id]["state"]="COMPLETE"
        except Exception as exc:
            simulations[session.id]["state"]="ERROR"; simulation_log(session.id,f"ERROR: {exc}")
    asyncio.create_task(run())
    return {"session":session,"simulation":simulations[session.id]}
@app.get("/api/v1/simulations/{session_id}")
def simulation_status(session_id:str):
    run=simulations.get(session_id)
    if not run: raise HTTPException(404,"simulation not found")
    return {"session":sessions.get(session_id),"simulation":run}
@app.get("/api/v1/sessions/{session_id}",response_model=SessionView)
def session(session_id:str):
    s=sessions.get(session_id)
    if not s: raise HTTPException(404,"session not found")
    return s
@app.get("/api/v1/config")
def config(): return {"sampling_rate":settings.sampling_rate,"wake_threshold":settings.wake_threshold,"intent_threshold":settings.intent_threshold,"raw_eeg_policy":"active-session-only"}
@app.get("/api/v1/models")
def models(): return [{"name":"baseline-spectral","version":"1.0","status":"simulation-ready"}]
@app.post("/api/v1/models/train")
def train(): return {"status":"queued","model_version":"baseline-spectral-1.0"}
@app.post("/api/v1/calibration/start")
def calibration_start(request:CalibrationStart):
    id="cal_"+str(len(calibrations)+1); calibrations[id]={"request":request.model_dump(),"status":"recording"}; return {"calibration_id":id,"instructions":"Perform the NIVO cue when prompted; include resting and artifact negative trials."}
@app.post("/api/v1/calibration/complete")
def calibration_complete(request:CalibrationComplete):
    if request.calibration_id not in calibrations: raise HTTPException(404,"calibration not found")
    calibrations[request.calibration_id].update(status="complete",labels=request.labels,model_version="user-baseline-1.0"); return calibrations[request.calibration_id]
@app.websocket("/ws/v1/session/{session_id}")
@app.websocket("/ws/v1/ingest/{session_id}")
async def stream(websocket:WebSocket,session_id:str):
    if not sessions.get(session_id): await websocket.close(code=4404); return
    await websocket.accept(); sessions.transition(session_id,SessionState.LISTENING); await websocket.send_json({"type":"state","state":"LISTENING","session_id":session_id})
    try:
      while True:
        frame=normalize_packet(await websocket.receive_json()); x=processor.process(frame.samples,frame.sampling_rate); quality=features.extract(x,frame.sampling_rate)["quality"]; sessions.get(session_id).signal_quality=quality
        if session_id in simulations: simulations[session_id]["packets"]+=1
        intent,score=classifier.predict(x,frame.sampling_rate)
        if confidence.accept(intent,score):
          sessions.transition(session_id,SessionState.PROCESSING); event=IntentEvent(session_id=session_id,intent=intent,confidence=score,source=Source(device=frame.device)); sessions.get(session_id).intents.append(event)
          result=await agent.act(ContextEngine().build(event)); sessions.get(session_id).latency_ms=0; sessions.transition(session_id,SessionState.RESPONDING)
          await websocket.send_json({"type":"intent","event":event.model_dump(mode="json"),"result":result,"quality":quality}); sessions.transition(session_id,SessionState.LISTENING)
        else: await websocket.send_json({"type":"telemetry","quality":quality,"candidate":intent.value,"confidence":score})
    except WebSocketDisconnect: pass
    finally:
      if sessions.get(session_id) and sessions.get(session_id).state!=SessionState.SLEEP: sessions.end(session_id)
