import asyncio
from backend.app.biosignal.simulation import SimulationAdapter
from backend.app.signal_processing.pipeline import SignalProcessor
from backend.app.features.extractor import FeatureExtractor
from backend.app.wake_detection.detector import WakeDetector
from backend.app.intent.classifier import BaselineIntentClassifier
from backend.app.intent.confidence import ConfidenceLayer
from backend.app.sessions.manager import SessionManager
from backend.app.core.schemas import SessionState
from backend.app.biosignal.ingestion import normalize_packet
from simulator.mock_hardware_streamer import generate_artifact
def test_device_and_pipeline():
 async def run():
  d=SimulationAdapter("SEARCH"); await d.connect(); await d.start_stream(); frame=await d.get_samples(); return frame
 frame=asyncio.run(run()); x=SignalProcessor().process(frame.samples); assert FeatureExtractor().extract(x,250)["quality"]>.9
def test_wake_and_intent():
 d=SimulationAdapter(); assert WakeDetector(threshold=.1).predict(d.window("NIVO"),10)["wake"]
 intent, confidence=BaselineIntentClassifier().predict(d.window("SEARCH"),250); assert intent.value=="SEARCH" and confidence>.3
def test_confidence_and_states():
 c=ConfidenceLayer(.5,cooldown=1); assert c.accept("SEARCH",.9,1); assert not c.accept("SEARCH",.9,1.1)
 m=SessionManager(); s=m.create(); m.transition(s.id,SessionState.LISTENING); m.transition(s.id,SessionState.PROCESSING); assert m.end(s.id).state==SessionState.SLEEP

def test_public_packet_is_normalized_to_pipeline_shape():
 frame=normalize_packet({"timestamp":1790419200.125,"channels":["Fp1","Fp2"],"data":[[-12.45,-14.21],[-11.2,-13.88]],"sampling_rate":250})
 assert frame.samples == [[-12.45,-11.2],[-14.21,-13.88]]
 assert SignalProcessor().process(frame.samples,frame.sampling_rate).shape == (2,2)

def test_fallback_mock_artifact_has_public_matrix_shape():
 artifact=generate_artifact(seconds=.1,channels=6)
 assert artifact.shape == (25,6)
