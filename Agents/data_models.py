""" Data """
from uagents import Model
import numpy as np


#Agents decisions 
class ResponseAgent(Model):
    frame = 0
    token_balance = 0 
    battery_charged = 0
    battery_discharged = 0 
    battery_state = 0
    bought = 0 
    sold = 0


#Data from simulation
class QueryEnv(Model):
    consumption: np.float64 = 0.0
    production: np.float64 = 0.0
    date: str = ""
    grid_price: float = 0.0
    sale_price: float = 0.0
    p2p_base_price: float = 0.0
    min_price: float = 0.0
    token_mint_rate: float = 0.0
    token_burn_rate: float = 0.0
