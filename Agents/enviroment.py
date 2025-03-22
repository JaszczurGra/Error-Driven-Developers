# Imports
from uagents import Agent, Context, Bureau

from data_models import QueryEnv, ResponseAgent
from model import ModelAgent

from simulation_compat_layer import EnvAgent


class Environment():
    """ Environment """

    def __init__(self) -> None:
        self.environment = Agent(name='Environment', seed="khavaioghgjabougrvbosubvisgvgjfkf",
                                 endpoint="https://localhost:4443")
        self.agents: list[Agent] = [ModelAgent(agent_kwargs={'name': f'Agent_{i}'}).agent for i in range(3)]
        self.simulation = EnvAgent().agent
        self.simulation.endpoint = self.environment.address
        self.bureau = Bureau()
        self.bureau.add(self.environment)
        self.bureau.add(self.simulation)
        for agent in self.agents:
            self.bureau.add(agent)

        @self.environment.on_message(QueryEnv)
        async def receive_simulation(ctx: Context, _sender, message: QueryEnv):
            # for a in self.agents:
            # ctx.send(a.address, message)
            return

        @self.environment.on_message(ResponseAgent)
        async def receive_agent(ctx: Context, _sender, message):

            print(message)
            return

    def run(self) -> None:
        """ Runs the environment """
        self.bureau.run()


# Run the agent
if __name__ == "__main__":
    env = Environment()
    env.run()
