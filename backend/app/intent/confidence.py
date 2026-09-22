import time
from backend.app.core.schemas import Intent
class ConfidenceLayer:
    def __init__(self, threshold=.78, cooldown=1.0, consistency=1): self.threshold,self.cooldown,self.consistency=threshold,cooldown,consistency; self.last={}; self.pending={}
    def accept(self,intent:Intent,confidence:float,now:float|None=None)->bool:
        now=now or time.monotonic()
        if confidence<self.threshold or now-self.last.get(intent,-1e9)<self.cooldown:return False
        count=self.pending.get(intent,0)+1; self.pending={intent:count}
        if count<self.consistency:return False
        self.last[intent]=now; self.pending={}; return True
