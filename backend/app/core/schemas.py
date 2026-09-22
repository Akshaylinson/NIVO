from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal
from pydantic import BaseModel, Field

def now() -> datetime: return datetime.now(timezone.utc)
class Intent(str, Enum): SELECT="SELECT"; NEXT="NEXT"; BACK="BACK"; CANCEL="CANCEL"; SEARCH="SEARCH"; ASK_AI="ASK_AI"
class SessionState(str, Enum): SLEEP="SLEEP"; STARTING="STARTING"; LISTENING="LISTENING"; PROCESSING="PROCESSING"; RESPONDING="RESPONDING"; ENDING="ENDING"
class Source(BaseModel): type: Literal["EEG"]="EEG"; device: str
class IntentEvent(BaseModel):
    protocol_version: str="1.0"; session_id: str; intent: Intent; confidence: float=Field(ge=0, le=1)
    timestamp: datetime=Field(default_factory=now); source: Source
class SignalFrame(BaseModel):
    protocol_version: str="1.0"; samples: list[list[float]]; sampling_rate: int=250; device: str="simulation"; timestamp: datetime=Field(default_factory=now)
class SessionView(BaseModel):
    id: str; user_id: str; device: str; state: SessionState; started_at: datetime; ended_at: datetime|None=None
    signal_quality: float=0; intents: list[IntentEvent]=[]; latency_ms: float|None=None; error: str|None=None
class CalibrationStart(BaseModel): user_id: str="demo-user"; device: str="simulation"; trials: int=8
class CalibrationComplete(BaseModel): calibration_id: str; labels: list[str]
class ContextRequest(BaseModel): application: str="dashboard"; task: str|None=None
