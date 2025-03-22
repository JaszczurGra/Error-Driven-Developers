# Imports
from uagents import Agent, Context, Bureau

from agents.data_models import QueryEnv, ResponseAgent
from agents.model import ModelAgent

from agents.simulation_compat_layer import EnvAgent


from backend.storage import SIMULATION_STORAGE


class Environment():
    """ Environment """

    def __init__(self) -> None:
        self.storage = SIMULATION_STORAGE


        self.environment = Agent(name='Environment', seed="aaaaaaaaa",
                                 endpoint="https://localhost:4443")
        # self.environment.storage.set("frame_counter", [0])

        self.state = []
        self.agents_output =[]
        self.current_frame = 0

        # self.environment.storage.set('state', [])
        # self.environment.storage.set("agents_output", [])
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
            print(message)
            
            self.state.append(message)  
            # self.environment.storage.set("agents_output", self.environment.storage.get("agents_output") + [])
            
            for a in self.agents:
                await ctx.send(a.address, message)



        @self.environment.on_message(ResponseAgent)
        async def receive_agent(ctx: Context, _sender, message):
            print(message)
            received_frame = message.frame 
            #just to be safe could be in recieve simulation as it shouldn't exceed the nr of simulation frames  
            while len(self.outputs) < received_frame+1:
                self.outputs.append([])  
            
            self.outputs[received_frame].append(message)



             
            if self.outputs[self.current_frame] == len(self.agents):
                self.current_frame += 1
                
                output_all = self.outputs[self.current_frame]

                # TODO implement logic for combining outputs from agents
                output = output_all[0]

                self.storage.set_frame(self.current_frame, self.state[self.current_frame], output)



            return

    def run(self) -> None:
        """ Runs the environment """
        self.bureau.run()


# Run the agent
if __name__ == "__main__":
    env = Environment()
    env.run()
