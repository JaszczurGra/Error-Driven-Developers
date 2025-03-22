# Imports
from uagents import Agent, Context,Model

from simulation_compat_layer import QueryEnv

class ResponseAgent(Model):
    produced = 0
    consumed = 0
    pass    

class QueryAgent(Model):
    sell = 0
    store  =0 
    buy = 0




class ModelAgent():
    agent = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf",endpoint="None")

    @agent.on_message(messages=QueryEnv)
    async def recieve_enviroment(ctx: Context, _sender, message: QueryEnv):
        await ctx.send(ctx.agent.address,QueryEnv(bought=0,sold=0,storage=[0,0],price=[0,0]))







# # Startup task
# @ag.on_message()
# async def say_hello(ctx: Context):
#     print('Wysylam')
#     # ctx.logger.info(f"Hello, I'm agent!")
#     # ctx.send(alice.end,"Hello, I'm agent!")
#     # ctx.logger.info(f"Hello, I'm agent!")
    
#     await ctx.send('https://localhost:4443',json.dumps({"message":"Hello, I'm agent!"}))
# # Run the agent
# if __name__ == "__main__":
#     alice.run()