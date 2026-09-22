class AIAgent:
    def __init__(self,provider): self.provider=provider
    async def act(self,request):
        response=await self.provider.generate(request)
        action={"SEARCH":"search","ASK_AI":"answer","SELECT":"select","NEXT":"navigate_next","BACK":"navigate_back","CANCEL":"cancel"}[request["intent"]]
        return {"action":action,"response":response}
