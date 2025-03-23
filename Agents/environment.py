# Imports
from uagents import Agent, Context, Bureau

from agents.data_models import QueryEnv, ResponseAgent
from agents.model import ModelAgent
from agents.model_stat_agent import ModelStatAgent

from agents.simulation_compat_layer import EnvAgent


from backend.storage import SIMULATION_STORAGE
from backend.app import Server

import json

run_server = False
class Environment():
    """ Environment """

    def __init__(self) -> None:

        if run_server:
            self.server = Server()
            self.server.start()


        self.storage = SIMULATION_STORAGE

        self.environment = Agent(name='Environment', seed="asdfadsf",
                                 endpoint="https://localhost:4443")
        # self.environment.storage.set("frame_counter", [0])


        self.environment.storage.set("state", [])
        self.environment.storage.set("agents_output", [])
        self.environment.storage.set("current_frame", 0)


        evntAgent = EnvAgent(self.environment.address)
        self.simenv = evntAgent.simenv 
        self.simulation = evntAgent.agent

        self.agents: list[Agent] = [ModelStatAgent(self.simenv,agent_kwargs={'name': f'Agent_{i}'  }).agent for i in range(3)]

        

        self.bureau = Bureau()
        self.bureau.add(self.environment)
        self.bureau.add(self.simulation)
        for agent in self.agents:
            self.bureau.add(agent)

 
        @self.environment.on_message(QueryEnv)
        async def receive_simulation(ctx: Context, _sender, message: QueryEnv):
            # print(message)

            self.environment.storage.set("state",self.environment.storage.get("state") + [message.json()])
            # self.environment.storage.set("agents_output", self.environment.storage.get("agents_output") + [])

            for a in self.agents:
                await ctx.send(a.address, message)

        @self.environment.on_message(ResponseAgent)
        async def receive_agent(ctx: Context, _sender, message:ResponseAgent):
            received_frame = message.frame 
            #just to be safe could be in recieve simulation as it shouldn't exceed the nr of simulation frames  
            outputs = self.environment.storage.get('agents_output')
            while len(outputs) < received_frame+1:
                outputs.append([])  


            outputs[received_frame].append(message.json()) 
            

            if len(outputs[self.environment.storage.get("current_frame")]) == len(self.agents):
                output_all = outputs[self.environment.storage.get("current_frame")]

                # TODO implement logic for combining outputs from agents
                output = output_all[0]

                self.storage.set_frame(self.environment.storage.get("current_frame"), self.environment.storage.get("state")[self.environment.storage.get("current_frame")], output)

                self.environment.storage.set("current_frame",self.environment.storage.get("current_frame") + 1)
                self.environment.storage.set("agents_output", outputs)

            return

    def run(self) -> None:
        """ Runs the environment """
        self.bureau.run()


# Run the agent
if __name__ == "__main__":
    env = Environment()
    env.run()
    if run_server:
        env.server.stop()
