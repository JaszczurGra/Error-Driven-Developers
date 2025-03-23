from .agent import AIAgent
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
""" Class for helper agents """
from darts import TimeSeries
from darts.models import Prophet
from typing import Literal
import numpy as np
import pandas as pd


class StatAgent(AIAgent):
    def __init__(self, config, initial_token_balance, *args, steps_per_day=24, **kwargs) -> None:
        self.grid_prices = []

        self.consumption_history = []
        self.production_history = []
        self.dates = []

        self.steps_per_day = steps_per_day
        self._steps = 0

        self.prime_buy = 0
        self.prime_sell = -1

        self.tokens_history = []
        self.energy_history = []
        self.surplus_history = []
        self.sells_history = []
        self.buys_history = []

        self.consumption_model = Prophet()
        self.production_model = Prophet()

        super().__init__(config, initial_token_balance, *args, **kwargs)

    def _register_grid_prices(self, buy, sell):
        if len(self.grid_prices) < self.steps_per_day:
            self.grid_prices.append((buy, sell))
        else:
            self.grid_prices[self._steps % self.steps_per_day] = (buy, sell)

    def _log_history(self, surplus):
        self.tokens_history.append(self.token_balances['community'])
        self.energy_history.append(self._get_charge())
        self.surplus_history.append(surplus)

    def _predict_grid_prices(self, tod):
        if len(self.grid_prices) > tod:
            return self.grid_prices[tod]
        return self.grid_prices[-1]

    def _register_consumption_production(self, consumption, production):
        self.consumption_history.append(consumption)
        self.production_history.append(production)

    def _get_charge(self):
        return sum([s.current_level for s in self.storages])

    def _predict(self, col: Literal["consumption", "production"], n) -> np.ndarray:
        model = self.consumption_model if col == 'consumption' else self.production_model
        data = self.consumption_history if col == "consumption" else self.production_history
        if len(data) <= 2:
            return np.array([data[-1]])
        series = TimeSeries.from_times_and_values(pd.to_datetime(self.dates), np.array(data))[-24:]
        model.fit(series)
        return np.array(model.predict(n=n).values())

    def _predict_consumption_production(self, n):
        return self._predict("consumption", n), self._predict("production", n)

    def _charge_storages(self, amount, p2p_base) -> float:
        for storage in self.storages:
            charged_energy = storage.charge(amount)
            amount -= charged_energy
            if charged_energy > 0:
                self.token_balances['community'] += charged_energy * p2p_base
            if amount <= 0:
                break

        return amount  # rest of amount

    def _discharge_storages(self, amount, p2p_base) -> float:
        for storage in self.storages:
            discharged_energy = storage.discharge(amount)
            amount -= discharged_energy
            if discharged_energy > 0:
                self.token_balances['community'] -= discharged_energy * p2p_base
            if amount <= 0:
                break
        return amount

    def _sell_to_grid(self, amount, sell_price, mint_rate):
        self.sells_history[self._steps] += amount
        self.token_balances['community'] += amount * sell_price

    def _buy_from_grid(self, amount, grid_price, burn_rate):
        self.buys_history[self._steps] += amount
        self.token_balances['community'] -= amount * burn_rate
        self.token_balances['community'] -= amount * grid_price

    def _max_buy(self, grid_price, burn_rate) -> float:
        return self.token_balances['community']/(grid_price + burn_rate)

    def step(self, consumption, production, date, grid_price, sell_price, p2p_base_price, min_price, mint_rate, burn_rate):
        self.sells_history.append(0)
        self.buys_history.append(0)
        self._register_grid_prices(grid_price, sell_price)
        self._register_consumption_production(consumption, production)
        self.dates.append(date)

        tod = self._steps % self.steps_per_day

        surplus = production - consumption

        if surplus < 0:
            self.token_balances['community'] += (production)*mint_rate
            rest = self._discharge_storages(-surplus, p2p_base_price)
            if rest > 0:
                self._buy_from_grid(rest, grid_price, burn_rate)
        else:
            self.token_balances['community'] += (consumption)*mint_rate
            rest = self._charge_storages(surplus, p2p_base_price)
            self.token_balances['community'] += (surplus-rest) * mint_rate
            sell = rest
            if sell > 0:
                self._sell_to_grid(sell, sell_price, mint_rate)

        predicted_cons, predicted_prod = self._predict_consumption_production(1)

        # predicted_surplus = predicted_prod - predicted_cons
        predicted_surpluses = predicted_prod-predicted_cons

        for i, predicted_surplus in enumerate(predicted_surpluses):
            if isinstance(predicted_surplus, np.ndarray):
                predicted_surplus = predicted_surplus[0]
            if predicted_surplus > 0:
                break
            predicted_grid_buy, predicted_grid_sell = self._predict_grid_prices(tod+1+i % self.steps_per_day)

            if predicted_surplus < 0 and predicted_grid_buy > grid_price and self._get_charge() < -predicted_surplus:
                charge = min(-predicted_surplus, self._max_buy(grid_price, burn_rate))
                self._charge_storages(-predicted_surplus - self._get_charge(), p2p_base_price)
                self._buy_from_grid(-predicted_surplus - self._get_charge(), grid_price, burn_rate)

        if self.token_balances['community'] < 0:
            raise ValueError("Community without power... No 'Świat Według Kiepskich' on TV... All hope is lost...")

        self._log_history(surplus)
        self._steps += 1
        print(self.token_balances)

    def plot(self):
        sns.lineplot(self.tokens_history)
        plt.savefig("tokens.png")
        plt.close()

        sns.lineplot(self.surplus_history)
        plt.savefig("surplus.png")
        plt.close()

        sns.lineplot(self.energy_history)
        plt.savefig("energy.png")
        plt.close()
