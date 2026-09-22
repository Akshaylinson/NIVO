import numpy as np
from backend.app.core.schemas import Intent
class BaselineIntentClassifier:
    frequencies={Intent.SELECT:7,Intent.NEXT:12,Intent.BACK:16,Intent.CANCEL:4,Intent.SEARCH:22,Intent.ASK_AI:28}
    def predict(self,samples,sampling_rate:int) -> tuple[Intent,float]:
        x=np.asarray(samples); f=np.fft.rfftfreq(x.shape[1],1/sampling_rate); p=np.abs(np.fft.rfft(x,axis=1))**2; values=[]
        for intent,hz in self.frequencies.items(): values.append((intent,float(p[:,np.argmin(abs(f-hz))].mean())))
        intent,best=max(values,key=lambda e:e[1]); conf=best/(sum(v for _,v in values)+1e-9)
        return intent,float(conf)
