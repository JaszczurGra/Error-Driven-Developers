# Imports
from uagents import Agent, Context,Model

from simulation_compat_layer import QueryEnv

class ResponseAgent(Model):
    sell = 0
    store  =0 
    buy = 0

class ModelAgent():
    agent = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf")



    @agent.on_message(QueryEnv,replies=ResponseAgent)
    async def recieve_enviroment(ctx: Context, _sender, message: QueryEnv):
        await ctx.send(_sender,await ModelAgent.logic(message))


    async def logic(input: QueryEnv) -> ResponseAgent:
        await ResponseAgent(sell=0,store=0,buy=0)


