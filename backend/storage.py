""" Storage of simulation data """
import random
from dataclasses import dataclass
import pandas as pd


@dataclass
class Storage:
    """ Storage for data """
    time: list = []
    total_consumption: list[float] = []
    total_production: list[float] = []
    token_balance: list[float] = []
    p2p_price: list[float] = []
    grid_price: list[float] = []
    purchase_price: list[float] = []
    energy_deficit: list[float] = []
    energy_surplus: list[float] = []
    storage_level_s1: list[float] = []
    storage_level_s2: list[float] = []

    @classmethod
    def from_csv(cls, path: str) -> "Storage":
        """ reading_csv """
        data_frame = pd.read_csv(path)
        values = zip(*data_frame.values.tolist())
        return cls(*values)

    def update_all(self, cooperative, time):
        """ Updates all values """
        self.time = time
        self.total_consumption = cooperative.history_consumption
        self.total_production = cooperative.history_production
        self.token_balance = cooperative.history_token_balance
        self.p2p_price = cooperative.history_p2p_price
        self.grid_price = cooperative.history_grid_price
        self.purchase_price = cooperative.history_purchase_price
        self.energy_deficit = cooperative.history_energy_deficit
        self.energy_surplus = cooperative.history_energy_surplus
        levels = []
        for _, storage_levels in cooperative.history_storage.items():
            levels.append(storage_levels)
        self.storage_level_s1 = levels[0]
        self.storage_level_s2 = levels[1]


RANDOM_STORAGE = Storage.from_csv('example_data.csv')
SIMULATION_STORAGE = RANDOM_STORAGE
SIMULATION_STORAGE = Storage()
