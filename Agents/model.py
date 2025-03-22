# Imports
from uagents import Agent, Context,Model

from simulation_compat_layer import QueryEnv

class ResponseAgent(Model):
    sell = 0
    store  =0 
    buy = 0

# class QueryAgent(Model):
#     produced = 0
#     consumed = 0




class ModelAgent():
    agent = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf")

    @agent.on_message(QueryEnv,replies=ResponseAgent)
    async def recieve_enviroment(ctx: Context, _sender, message: QueryEnv):
        #LOGIKA MODELU
        await ctx.send(_sender,ResponseAgent(sell=0,store=0,buy=0))







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