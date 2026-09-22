import numpy as np
from backend.app.biosignal.device import BioSignalDevice
from backend.app.core.config import settings
from backend.app.core.schemas import SignalFrame

class SimulationAdapter(BioSignalDevice):
    """Synthetic device that shares the production device contract."""
    def __init__(self, intent: str="REST", seed: int|None=7): self.intent, self.rng, self.connected, self.streaming = intent, np.random.default_rng(seed), False, False
    async def connect(self): self.connected=True
    async def disconnect(self): self.connected=False; self.streaming=False
    async def start_stream(self):
        if not self.connected: raise RuntimeError("device not connected")
        self.streaming=True
    async def stop_stream(self): self.streaming=False
    def window(self, intent: str|None=None) -> np.ndarray:
        label=intent or self.intent; n=int(settings.sampling_rate*settings.window_seconds); t=np.arange(n)/settings.sampling_rate
        data=self.rng.normal(0, .16, (settings.channels,n)) + .30*np.sin(2*np.pi*10*t)
        # Deliberately synthetic signatures, never a claim of real thought decoding.
        patterns={"NIVO":(18,1.25),"SELECT":(7,.95),"NEXT":(12,.95),"BACK":(16,.95),"CANCEL":(4,.95),"SEARCH":(22,.95),"ASK_AI":(28,.95)}
        if label in patterns:
            f,a=patterns[label]; data += a*np.sin(2*np.pi*f*t)[None,:]
        if label=="ARTIFACT": data[:, n//3:n//3+8] += 6
        return data
    async def get_samples(self) -> SignalFrame:
        if not self.streaming: raise RuntimeError("stream not started")
        return SignalFrame(samples=self.window().tolist(), sampling_rate=settings.sampling_rate)
class OpenBCIAdapter(BioSignalDevice):
    """Integration seam; install a vendor SDK and implement transport here."""
    async def connect(self): raise NotImplementedError("OpenBCI adapter requires vendor integration")
    async def disconnect(self): pass
    async def start_stream(self): pass
    async def stop_stream(self): pass
    async def get_samples(self): raise NotImplementedError
