from datetime import datetime, timezone
from uuid import uuid4
from backend.app.core.schemas import SessionState, SessionView
class SessionManager:
    transitions={SessionState.SLEEP:{SessionState.STARTING},SessionState.STARTING:{SessionState.LISTENING,SessionState.ENDING},SessionState.LISTENING:{SessionState.PROCESSING,SessionState.ENDING},SessionState.PROCESSING:{SessionState.RESPONDING,SessionState.ENDING},SessionState.RESPONDING:{SessionState.LISTENING,SessionState.ENDING},SessionState.ENDING:{SessionState.SLEEP}}
    def __init__(self): self.sessions={}
    def create(self,user_id="demo-user",device="simulation"):
        s=SessionView(id="nivo_"+uuid4().hex[:8],user_id=user_id,device=device,state=SessionState.STARTING,started_at=datetime.now(timezone.utc)); self.sessions[s.id]=s; return s
    def get(self,id): return self.sessions.get(id)
    def transition(self,id,state):
        s=self.sessions[id]
        if state not in self.transitions[s.state]: raise ValueError(f"invalid transition {s.state} -> {state}")
        s.state=state
        if state==SessionState.SLEEP:s.ended_at=datetime.now(timezone.utc)
        return s
    def end(self,id):
        s=self.sessions[id]
        if s.state != SessionState.ENDING:self.transition(id,SessionState.ENDING)
        return self.transition(id,SessionState.SLEEP)
