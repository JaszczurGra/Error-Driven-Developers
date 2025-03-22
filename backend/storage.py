""" Storage of simulation data """
import random
from dataclasses import dataclass
import pandas as pd


@dataclass
class BStorage:
    """ Storage for data """
    time: list
    total_consumption: list[float]
    total_production: list[float]
    token_balance: list[float]
    p2p_price: list[float]
    grid_price: list[float]
    purchase_price: list[float]
    energy_deficit: list[float]
    energy_surplus: list[float]
    storage_level_s1: list[float]
    storage_level_s2: list[float]

    @classmethod
    def from_csv(cls, path: str) -> "BStorage":
        """ reading_csv """
        data_frame = pd.read_csv(path)
        values = zip(*data_frame.values.tolist())
        return cls(*values)


class Storage:
    """ Storage singleton """

    def __init__(self) -> None:
        self.data: list[float] = []
        self.current_time = []

    def create_random_data(self):
        """ Initializes with random Data """
        self.data = [random.random() * i for i in range(random.randint(15, 100))]


RANDOM_STORAGE = Storage()
RANDOM_STORAGE.create_random_data()
SIMULATION_STORAGE = RANDOM_STORAGE
# SIMULATION_STORAGE = Storage()

if __name__ == '__main__':
    BStorage.from_csv('example_data.csv')
