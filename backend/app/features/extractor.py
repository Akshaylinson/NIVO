import numpy as np
class FeatureExtractor:
    bands={"theta":(4,8),"alpha":(8,13),"beta":(13,30),"gamma":(30,45)}
    def extract(self, x: np.ndarray, sampling_rate: int) -> dict[str,float]:
        freqs=np.fft.rfftfreq(x.shape[1],1/sampling_rate); psd=np.abs(np.fft.rfft(x,axis=1))**2
        out={"rms":float(np.sqrt(np.mean(x*x))),"variance":float(np.var(x)),"quality":float(max(0,1-np.mean(np.abs(x)>4)))}
        for name,(lo,hi) in self.bands.items(): out[name]=float(psd[:,(freqs>=lo)&(freqs<hi)].mean())
        return out
