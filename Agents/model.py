# Imports
from uagents import Agent, Context

from agents.data_models import QueryEnv, ResponseAgent


class ModelAgent():
    def __init__(self, agent_kwargs: dict) -> None:
        agent = Agent( **agent_kwargs)
        agent.storage.set("frame", 0)

        @agent.on_message(QueryEnv, replies=ResponseAgent)
        async def recieve_enviroment(ctx: Context, _sender, message: QueryEnv):
            # print(ctx, _sender, message)
            response = self.logic(message)
            response.frame = agent.storage.get("frame")
            agent.storage.set("frame", response.frame+1)
            await ctx.send(_sender, response)

        self.agent = agent

    def logic(self, input: QueryEnv) -> ResponseAgent:
        return ResponseAgent(sell=0, store=0, buy=0)
