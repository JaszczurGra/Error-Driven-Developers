# Imports
from uagents import Agent, Context
from agents.data_models import QueryEnv


class EnvAgent():
    agent = Agent(name='Simulation', seed="khavaioghgjabougrvbosubvisgvgjfkf", endpoint="None")

    @agent.on_interval(1, messages=QueryEnv)
    async def send_data(ctx: Context):
        await ctx.send(ctx.agent.address, QueryEnv(bought=0, sold=0, storage=[0, 0], price=[0, 0]))
