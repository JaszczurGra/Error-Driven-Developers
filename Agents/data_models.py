""" Data """
from uagents import Model



#Agents decisions 
class ResponseAgent(Model):
    frame = 0
    sell = 0
    store = 0
    buy = 0


#Data from simulation
class QueryEnv(Model):
    # production: int
    # consumption: int
    bought: int
    sold: int
    # current/max
    storage: list[int]
    # buy/sell
    price: list[int]
