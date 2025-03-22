# Imports
from uagents import Agent, Context, Bureau, Model
import json
from typing import List

from model import ResponseAgent, QueryAgent

from simulation_compat_layer import QueryEnv, EnvAgent

enviroment = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf", endpoint="https://localhost:4443")


# List of agents 
agents: List[Agent] = []


simulation = EnvAgent().agent
simulation.endpoint = enviroment.address


class FrontendMessage(Model):
    bought = 0
    sold = 0
    # current/max
    storage =[0,0]
    # buy/sell 
    price = [0,0]

    

# Values from simulation







# Startup task
@enviroment.on_message(QueryEnv, replies=ResponseAgent)
async def receive_simulation(ctx: Context,_sender, message: QueryEnv):
    for a in agents:
        await ctx.send(a.address,message)
    



@enviroment.on_message(QueryAgent)
async def receive_agent(ctx: Context, message):
    ctx.storage.set('')





bureau = Bureau()
bureau.add(enviroment)
bureau.add(simulation)  
for a in agents:
    bureau.add(a)

# Run the agent
if __name__ == "__main__":
    bureau.run()