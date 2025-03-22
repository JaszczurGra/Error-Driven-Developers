from .storage import Storage
from abc import ABC, abstractmethod


class AIAgent(ABC):
    def __init__(self, config, initial_token_balance, *args, **kwargs) -> None:
        self.config = config
        self.storages = [Storage(**storage_config) for storage_config in config.get('storages', [])]
        self.token_balances = {'community': initial_token_balance}
        for storage in self.storages:
            self.token_balances[storage.name] = initial_token_balance

    @abstractmethod
    def step(
        self,
        consumption,
        production,
        date,
        grid_price,
        sell_price,
        p2p_base_price,
        min_price,
        mint_rate,
        burn_rate,
    ) -> float:
        pass
