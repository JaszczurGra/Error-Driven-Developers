# Imports
from uagents import Agent, Context, Model

from simulation_compat_layer import QueryEnv


class ResponseAgent(Model):
    sell = 0
    store = 0
    buy = 0


class ModelAgent():
    def __init__(self, agent_kwargs: dict) -> None:
        agent = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf", **agent_kwargs)

        async def logic(input: QueryEnv) -> ResponseAgent:
            return ResponseAgent(sell=0, store=0, buy=0)

        agent.logic = logic

        @agent.on_message(QueryEnv, replies=ResponseAgent)
        async def recieve_enviroment(ctx: Context, _sender, message: QueryEnv):
            await ctx.send(_sender, await agent.logic(message))

        self.agent = agent
