import numpy as np
from backend.app.core.config import settings
class WakeDetector:
    def __init__(self, threshold:float=settings.wake_threshold, cooldown_seconds:float=2): self.threshold=threshold; self.cooldown_seconds=cooldown_seconds; self._last=-1e9
    def predict(self, samples, timestamp:float=0) -> dict:
        x=np.asarray(samples); freqs=np.fft.rfftfreq(x.shape[1],1/settings.sampling_rate); p=np.abs(np.fft.rfft(x,axis=1))**2
        # The alpha band is the documented public-artifact wake proxy.  The
        # beta-range component preserves the existing calibrated simulator cue.
        cue_band=((freqs>=8)&(freqs<=13))|((freqs>=16)&(freqs<=20))
        score=float(p[:,cue_band].mean()/(p.mean()+1e-9)); confidence=float(min(1,score/15))
        wake=confidence>=self.threshold and timestamp-self._last>=self.cooldown_seconds
        if wake:self._last=timestamp
        return {"wake":wake,"confidence":confidence}
