import numpy as np
from backend.app.core.config import settings
class WakeDetector:
    def __init__(self, threshold:float=settings.wake_threshold, cooldown_seconds:float=2): self.threshold=threshold; self.cooldown_seconds=cooldown_seconds; self._last=-1e9
    def predict(self, samples, timestamp:float=0) -> dict:
        x=np.asarray(samples); freqs=np.fft.rfftfreq(x.shape[1],1/settings.sampling_rate); p=np.abs(np.fft.rfft(x,axis=1))**2
        score=float(p[:,(freqs>=16)&(freqs<=20)].mean()/(p.mean()+1e-9)); confidence=float(min(1,score/15))
        wake=confidence>=self.threshold and timestamp-self._last>=self.cooldown_seconds
        if wake:self._last=timestamp
        return {"wake":wake,"confidence":confidence}
