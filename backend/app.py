""" Flask app """
from flask import Flask, jsonify
from backend.storage import SIMULATION_STORAGE

app = Flask(__name__)


@app.route('/api/simulation', methods=['GET'])
def api_get_stock_price():
    """
    Retrieves all data from simulation.
    """
    return jsonify({
        "Time": SIMULATION_STORAGE.time,
        "Total Consumption": SIMULATION_STORAGE.total_consumption,
        "Total Production": SIMULATION_STORAGE.total_production,
        "Token Balance": SIMULATION_STORAGE.token_balance,
        "P2P Price": SIMULATION_STORAGE.p2p_price,
        "Grid Price": SIMULATION_STORAGE.grid_price,
        "Purchase Price": SIMULATION_STORAGE.purchase_price,
        "Energy Deficit": SIMULATION_STORAGE.energy_deficit,
        "Energy Surplus": SIMULATION_STORAGE.energy_surplus,
        "Storage Level S1": SIMULATION_STORAGE.storage_level_s1,
        "Storage Level S2": SIMULATION_STORAGE.storage_level_s2,
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
