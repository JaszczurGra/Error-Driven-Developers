# Imports
from uagents import Agent, Context

from agents.data_models import QueryEnv, ResponseAgent
from agents.model import ModelAgent

from simulation.models.stat_agent import StatAgent
from simulation.utils.helper_functions import load_storages


class ModelStatAgent(ModelAgent):
    def __init__(self, env, agent_kwargs):
        super().__init__(agent_kwargs)
        # TODO czy tu powinno byc  100 tokenow na start
        self.model = StatAgent({'storages': load_storages(env.storage_fp)}, 100)

    def logic(self, input: QueryEnv) -> ResponseAgent:
        self.model.step(input.consumption, input.production,input.date, input.grid_price, input.sale_price, input.p2p_base_price, input.min_price, input.token_mint_rate, input.token_burn_rate)


        res = ResponseAgent()

        res.token_balance = self.model.token_balances['community']
        # MOZNA
        res.battery_charged = 0
        # MOZNA
        res.battery_discharged = 0

        res.battery_state = self.model._get_charge()



        # TODO
        res.bought = self.model.buys_history[-1]
        # TODO
        res.sold = self.model.sells_history[-1]

        print("TYLE POWINNO BYC", input.production + res.bought - res.sold - input.consumption ) 


        return res
