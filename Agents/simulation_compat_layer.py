# Imports
from uagents import Agent, Context, Model
import json
from typing import List


class QueryEnv(Model):
    bought: int
    sold: int
    # current/max
    storage: List[int]
    # buy/sell
    price: List[int]


class EnvAgent():
    agent = Agent(name='Simulation', seed="khavaioghgjabougrvbosubvisgvgjfkf", endpoint="None")

    @agent.on_interval(0.2, messages=QueryEnv)
    async def send_data(ctx: Context):
        await ctx.send(ctx.agent.address, QueryEnv(bought=0, sold=0, storage=[0, 0], price=[0, 0]))
