""" Flask app """
from threading import Thread
import os

import flask
from werkzeug.serving import make_server
from flask_cors import CORS

from backend.storage import SIMULATION_STORAGE


APP = flask.Flask(__name__)


@APP.route('/api/simulation', methods=['GET'])
def api_get_stock_price():
    """
    Retrieves all data from simulation.
    """

    fields = [
        "token_balance",
        "total_consumption",
        "total_production",
        "time",
        "grid_price",
        "purchase_price",
        "battery_state",
        "p2p_price",
        "token_mint_rate",
        "token_burn_rate"
    ]

    length = len(SIMULATION_STORAGE.time)





    return flask.jsonify([{key: value[i]  for key, value in SIMULATION_STORAGE.__dict__.items() if key in fields } for i in range(length)]), 200



@APP.route('/api/actions', methods=['GET'])
def api_get_actions():
    """
    Retrieves all data from simulation.
    """
    fields = [
        "token_balance",
        "battery_charged",
        "battery_discharged",
        "grid_price",
        "purchase_price",
        "battery_state",
        "bought",
        "sold",
        "time",
    ]

    length = len(SIMULATION_STORAGE.time)
    return flask.jsonify([{key: value[i]  for key, value in SIMULATION_STORAGE.__dict__.items() if key in fields } for i in range(length)]), 200
    
class Server():
    """ Server class """
    port: int
    host: str
    static_path: str

    app: flask.Flask

    def __init__(self, port: int = 8080, host: str = '127.0.0.1') -> None:
        static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dist')
        self.port = port
        self.host = host
        self.static_path = static_path
        self.app = APP
        self.__flask_process = None

        CORS(self.app, resources={r"/*": {"origins": "*"}})  # TODO: Change origins to specific domain

        self.server = make_server(self.host, self.port, self.app, threaded=True)
        self.server.daemon_threads = True

    def start(self) -> None:
        """ Starts server on separate thread """
        if self.__flask_process:
            return
        self.__flask_process = Thread(target=self.server.serve_forever)
        self.__flask_process.daemon = True
        self.__flask_process.start()
        print(f'Started server at http://{self.host}:{self.port}')

    def stop(self) -> None:
        """ Kills the server process """
        if not self.__flask_process:
            return
        self.__flask_process.join()
        self.__flask_process = None

    def __del__(self):
        self.stop()


if __name__ == '__main__':
    server = Server()
    server.start()
    import time
    time.sleep(10)
