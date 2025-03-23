""" Class for helper agents """
from typing import Literal
import numpy as np
import dill
from qiskit_ibm_runtime import QiskitRuntimeService, EstimatorV2
from qiskit_machine_learning.algorithms import NeuralNetworkRegressor
from sklearn.preprocessing import MinMaxScaler
from .stat_agent import StatAgent

with open('quantum_model', 'rb') as f:
    QUANTUM_MODEL, SCALER = dill.load(f)
    QUANTUM_MODEL: NeuralNetworkRegressor
    SCALER: MinMaxScaler


class QuantumAgent(StatAgent):
    """ Quantum AI Agent """

    def _predict(self, col: Literal["consumption", "production"], n) -> np.ndarray:
        data = self.consumption_history if col == "consumption" else self.production_history
        if len(data) <= 2:
            return np.array([data[-1]])
        prediction = QUANTUM_MODEL.predict(np.array(data[-10:]))

        return SCALER.inverse_transform(prediction.reshape(-1, 1)).flatten()


class RealQuantumAgent(StatAgent):
    """ Quantum AI Agent to run on real quantum device """

    def _predict(self, col: Literal["consumption", "production"], n) -> np.ndarray:
        raise NotImplementedError
        data = self.consumption_history if col == "consumption" else self.production_history
        if len(data) <= 2:
            return np.array([data[-1]])
        service = QiskitRuntimeService(channel='ibm_quantum')
        backend = service.backend('ibm_brisbane')
        estimator = EstimatorV2(backend)
        prediction = QUANTUM_MODEL.predict(np.array(data[-10:]))

        return SCALER.inverse_transform(prediction.reshape(-1, 1)).flatten()
