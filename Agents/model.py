# Imports
from uagents import Agent, Context, Model

from simulation_compat_layer import QueryEnv


class ResponseAgent(Model):
    frame = 0 
    sell = 0
    store = 0
    buy = 0


class ModelAgent():
    def __init__(self, agent_kwargs: dict) -> None:
        agent = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf", **agent_kwargs)
        agent.storage.set("frame",0)

        async def logic(input: QueryEnv) -> ResponseAgent:
            return ResponseAgent(sell=0, store=0, buy=0)

        agent.logic = logic

        @agent.on_message(QueryEnv, replies=ResponseAgent)
        async def recieve_enviroment(ctx: Context, _sender, message: QueryEnv):
            response = await agent.logic(message)
            response.frame = agent.storage.get("frame")
            agent.storage.set("frame",response.frame+1)
            await ctx.send(_sender, response)

        self.agent = agent
