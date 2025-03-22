# Imports
from uagents import Agent, Context

from data_models import QueryEnv, ResponseAgent


class ModelAgent():
    def __init__(self, agent_kwargs: dict) -> None:
        agent = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf", **agent_kwargs)

        def logic(input: QueryEnv) -> ResponseAgent:
            return ResponseAgent(sell=0, store=0, buy=0)

        agent.logic = logic

        @agent.on_message(QueryEnv, replies=ResponseAgent)
        async def recieve_enviroment(ctx: Context, _sender, message: QueryEnv):
            await ctx.send(_sender, agent.logic(message))

        self.agent = agent
