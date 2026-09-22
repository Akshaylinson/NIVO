from backend.app.core.schemas import IntentEvent
class ContextEngine:
    def build(self,event:IntentEvent, application="dashboard", task=None): return {"protocol_version":"1.0","intent":event.intent.value,"confidence":event.confidence,"context":{"application":application,"session":event.session_id,"task":task}}
