# Imports
from uagents import Agent, Context
import json

# Create an agent named Alice
alice = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf", endpoint="https://localhost:4443")



# Startup task
@alice.on_interval(0.2, model=)
async def say_hello(ctx: Context):
    print('Wysylam')
    # ctx.logger.info(f"Hello, I'm agent!")
    # ctx.send(alice.end,"Hello, I'm agent!")
    # ctx.logger.info(f"Hello, I'm agent!")
    
    await ctx.send('https://localhost:4443',json.dumps({"message":"Hello, I'm agent!"}))
# Run the agent
if __name__ == "__main__":
    alice.run()