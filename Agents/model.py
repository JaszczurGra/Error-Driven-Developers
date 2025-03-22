# Imports
from uagents import Agent, Context,Model

from simulation_compat_layer import QueryEnv

class ResponseAgent(Model):
    sell = 0
    store  =0 
    buy = 0

class ModelAgent():
    def __init__(self):
        
        agent = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf")


        async def logic(input: QueryEnv) -> ResponseAgent:
            return ResponseAgent(sell=0,store=0,buy=0)


        agent.logic = logic

        @agent.on_message(QueryEnv,replies=ResponseAgent)
        async def recieve_enviroment(ctx: Context, _sender, message: QueryEnv):
            response = await agent.logic(message) 
            print(response)
            await ctx.send(_sender, response)



        
        self.agent = agent


