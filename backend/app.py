""" Flask app """
from flask import Flask, jsonify
from .storage import SIMULATION_STORAGE

app = Flask(__name__)


@app.route('/api/simulation', methods=['GET'])
def api_get_stock_price():
    """
    Retrieves all data from simulation.
    """
    return jsonify({
        "data": SIMULATION_STORAGE.data
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
