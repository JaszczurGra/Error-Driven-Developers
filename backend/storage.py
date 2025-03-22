""" Storage of simulation data """
from dataclasses import dataclass, field
import pandas as pd
from agents.data_models import QueryEnv,ResponseAgent
import json

@dataclass
class Storage:
    time: list[str] = field(default_factory=list)
    total_consumption: list[float] = field(default_factory=list)
    total_production: list[float] = field(default_factory=list)
    token_balance: list[float] = field(default_factory=list)
    p2p_price: list[float] = field(default_factory=list)
    grid_price: list[float] = field(default_factory=list)
    purchase_price: list[float] = field(default_factory=list)
    energy_deficit: list[float] = field(default_factory=list)
    energy_surplus: list[float] = field(default_factory=list)
    storage_level_s1: list[float] = field(default_factory=list)
    storage_level_s2: list[float] = field(default_factory=list)
    token_mint_rate: list[float] = field(default_factory=list)
    token_burn_rate: list[float] = field(default_factory=list)
    battery_charged: list[float] = field(default_factory=list)
    battery_discharged: list[float] = field(default_factory=list)
    battery_state: list[float] = field(default_factory=list)
    bought: list[float] = field(default_factory=list)
    sold: list[float] = field(default_factory=list)

    """ Storage for data """
    # time: list = field(default_factory=list)
    # total_consumption: list[float] = field(default_factory=list)
    # total_production: list[float] = field(default_factory=list)
    # token_balance: list[float] = field(default_factory=list)
    # p2p_price: list[float] = field(default_factory=list)
    # grid_price: list[float] = field(default_factory=list)
    # purchase_price: list[float] = field(default_factory=list)
    # energy_deficit: list[float] = field(default_factory=list)
    # energy_surplus: list[float] = field(default_factory=list)
    # storage_level_s1: list[float] = field(default_factory=list)
    # storage_level_s2: list[float] = field(default_factory=list)

    @classmethod
    def from_csv(cls, path: str) -> "Storage":
        """ reading_csv """
        data_frame = pd.read_csv(path)
        values = zip(*data_frame.values.tolist())
        return cls(*values)

    def update_all(self, agent, time):
        """ Updates all values """
        self.time = time
        self.total_consumption = agent.history_consumption
        self.total_production = agent.history_production
        self.token_balance = agent.history_token_balance
        self.p2p_price = agent.history_p2p_price
        self.grid_price = agent.history_grid_price
        self.purchase_price = agent.history_purchase_price
        self.energy_deficit = agent.history_energy_deficit
        self.energy_surplus = agent.history_energy_surplus
        levels = []
        for _, storage_levels in agent.history_storage.items():
            levels.append(storage_levels)
        self.storage_level_s1 = levels[0]
        self.storage_level_s2 = levels[1]

        # self.storage_level 


    def set_frame(self, frame, env:QueryEnv,out: ResponseAgent):
        env = json.loads(env)
        out = json.loads(out)


        self.total_consumption.append(env['consumption'])
        self.total_production.append(env['production'])
        self.time.append(env['date'])
        self.grid_price.append(env['grid_price'])
        self.purchase_price.append(env['sale_price'])
        self.p2p_price.append(env['p2p_base_price'])
        self.token_mint_rate.append(env['token_mint_rate'])
        self.token_burn_rate.append(env['token_burn_rate'])

        self.token_balance.append(out['token_balance'])
        self.battery_charged.append(out['battery_charged'])
        self.battery_discharged.append(out['battery_discharged'])
        self.battery_state.append(out['battery_state'])
        self.bought.append(out['bought'])
        self.sold.append(out['sold'])

        print("\n\n\n\n", frame, env, out)



# RANDOM_STORAGE = Storage.from_csv('example_data.csv')
# SIMULATION_STORAGE = RANDOM_STORAGE
SIMULATION_STORAGE = Storage()
