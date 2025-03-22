# Imports
import time

from uagents import Agent, Context, Bureau

from model import ResponseAgent, ModelAgent

from simulation_compat_layer import QueryEnv, EnvAgent


class Environment():
    """ Environment """

    def __init__(self) -> None:
        self.environment = Agent(name='Environment', seed="khavaioghgjabougrvbosubvisgvgjfkf",
                                 endpoint="https://localhost:4443")
        self.environment.storage.set("frame_counter", [0])
        self.environment.storage.set("current_frame", 0)
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
            for a in self.agents:
                ctx.send(a.address, message)
            return

        @self.environment.on_message(ResponseAgent)
        async def receive_agent(ctx: Context, _sender, message):
            print(message)
            received_frame = message.frame
            counter = self.environment.storage.get("frame_counter")
            while len(counter) <= received_frame:
                counter.append(0)
            counter[received_frame] += 1    

            current_frame = self.environment.storage.get("current_frame")   
            if counter[current_frame] == len(self.agents):
                print('Updatuj stan ', current_frame)
                self.environment.storage.set("current_frame", current_frame+1)



            self.environment.storage.set("frame_counter", counter)

            return

    def run(self) -> None:
        """ Runs the environment """
        self.bureau.run()


# Run the agent
if __name__ == "__main__":
    env = Environment()
    env.run()
