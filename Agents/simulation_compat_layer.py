# Imports
from uagents import Agent, Context
from agents.data_models import QueryEnv

from random import randint


class EnvAgent():
    def __init__(self, address: str) -> None:
        self.agent = Agent(name='Simulation', seed="khavaioghgjabougrvbosubvisgvgjfkj")
        self.address = address

        @self.agent.on_interval(1, messages=QueryEnv)
        async def send_data(ctx: Context):
            await ctx.send(self.address, QueryEnv(bought=0, sold=0, storage=[0, 0], price=[0, 0]))
