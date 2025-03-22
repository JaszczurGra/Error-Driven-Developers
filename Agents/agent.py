""" Class for helper agents """
from darts import TimeSeries
from darts.models import Prophet
from agents.data_models import QueryEnv, ResponseAgent
from agents.model import ModelAgent
from typing import Literal


class HelperAgent(ModelAgent):
    def __init__(self, agent_kwargs):
        super().__init__(agent_kwargs)
        self.production_history = TimeSeries()
        self.consumption_history = TimeSeries()

    def predict(self, col: Literal["consumption", "production"]) -> TimeSeries:
        model = Prophet()
        if col == "consumption":
            model.fit(self.consumption_history)
        else:
            model.fit(self.production_history)
        return model.predict(n=1)

    def logic(self,input: QueryEnv) -> ResponseAgent:
        # upate history
        self.production_history = self.production_history.append(input.production)
        self.consumption_history = self.consumption_history.append(input.consumption)
        
        # predict
        production_prediction = self.predict("production").values()[0]
        consumption_prediction = self.predict("consumption").values()[0]
        return production_prediction, consumption_prediction

        
        

        
        
