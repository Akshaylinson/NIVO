from abc import ABC,abstractmethod
class AIProvider(ABC):
    @abstractmethod
    async def generate(self, request:dict)->str: ...
    async def stream(self,request:dict): yield await self.generate(request)
    async def execute(self,request:dict)->dict: return {"response":await self.generate(request)}
class MockProvider(AIProvider):
    async def generate(self,request): return f"NIVO received {request['intent']} for {request['context']['application']}."
