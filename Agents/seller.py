# Imports
from uagents import Agent, Context
import json

# Create an agent named Alice
seller = Agent(seed="khavaioghgjabougrvbosubvisgvgjfkf", endpoint="https://localhost:4443")



# Startup task
@seller.on_message
async def say_hello(ctx: Context, message):
    print('Wysylam')
    # ctx.logger.info(f"Hello, I'm agent!")

# Run the agent
if __name__ == "__main__":
    seller.run()