"""Local wake loop. It deliberately opens no backend connection while sleeping."""
import asyncio
import json
import time
from urllib.request import Request, urlopen
import websockets
from backend.app.biosignal.simulation import SimulationAdapter
from backend.app.wake_detection.detector import WakeDetector

API="http://localhost:8000"
class LocalBioEngine:
    def __init__(self): self.device=SimulationAdapter(); self.wake=WakeDetector()
    async def run_demo(self, intent="SEARCH"):
        await self.device.connect(); await self.device.start_stream()
        # In production this loop only examines local samples and never contacts API.
        result=self.wake.predict(self.device.window("NIVO"), time.monotonic())
        if not result["wake"]: return {"woke":False,**result}
        req=Request(API+"/api/v1/sessions",method="POST")
        with urlopen(req) as response: session=json.load(response)
        async with websockets.connect(f"ws://localhost:8000/ws/v1/session/{session['id']}") as ws:
            await ws.recv() # LISTENING state
            frame={"samples":self.device.window(intent).tolist(),"sampling_rate":250,"device":"simulation"}
            await ws.send(json.dumps(frame)); message=json.loads(await ws.recv())
        await self.device.stop_stream(); await self.device.disconnect()
        return {"woke":True,"wake_confidence":result["confidence"],"session_id":session["id"],"message":message}
if __name__=="__main__": print(asyncio.run(LocalBioEngine().run_demo()))
