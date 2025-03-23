# Imports
from uagents import Agent, Context
from agents.data_models import QueryEnv

from random import randint
from simulation.env.simulation_env import SimEnv

class EnvAgent():
    def __init__(self, address: str) -> None:
        self.agent = Agent(name='Simulation', seed="khavaioghgjabougrvbosubvisgvgjfkj")
        self.address = address

        storage_fp, profile_fp, logs_fp, grid_costs_fp = './storages.csv', 'pv_profiles', 'logs', 'grid_costs'

        self.simenv = SimEnv(storage_fp, profile_fp, logs_fp, grid_costs_fp)

        @self.agent.on_interval(0.01, messages=QueryEnv)
        async def send_data(ctx: Context):
            


            step = self.simenv.step()
            print(step)
            q = QueryEnv()
            q.consumption = step[0][0]
            q.production = step[0][1]
            q.date = step[0][2]
            q.grid_price = step[0][3]
            q.sale_price = step[0][4]
            q.p2p_base_price = step[0][5]
            q.min_price = step[0][6]
            q.token_mint_rate = step[0][7]
            q.token_burn_rate = step[0][8]


            await ctx.send(self.address, q)
