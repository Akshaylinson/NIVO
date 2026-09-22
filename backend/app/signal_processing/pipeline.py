import numpy as np
from scipy.signal import butter, sosfiltfilt
from backend.app.core.config import settings

class SignalProcessor:
    def process(self, samples: list[list[float]]|np.ndarray, sampling_rate: int=settings.sampling_rate) -> np.ndarray:
        x=np.asarray(samples, dtype=float)
        if x.ndim!=2 or x.shape[0] < 1: raise ValueError("samples must be channels x time")
        x=x-np.median(x,axis=1,keepdims=True)
        x=np.clip(x, -5, 5)  # artifact containment
        sos=butter(4, [1, 45], btype="bandpass", fs=sampling_rate, output="sos")
        return sosfiltfilt(sos,x,axis=1) if x.shape[1]>30 else x
