""" Data """
from uagents import Model


class ResponseAgent(Model):
    sell = 0
    store = 0
    buy = 0


class QueryEnv(Model):
    bought: int
    sold: int
    # current/max
    storage: list[int]
    # buy/sell
    price: list[int]
