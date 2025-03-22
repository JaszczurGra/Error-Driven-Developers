import sys
import csv
from datetime import datetime
from pathlib import Path

from simulation.utils.helper_functions import plot_results, save_results_to_csv, load_profiles, load_storages
from simulation.models.cooperative import Cooperative
from backend.storage import SIMULATION_STORAGE
from backend.app import Server


def load_grid_costs(filepath):
    grid_costs = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            grid_costs.append({
                'hour': row['Hour'],
                'purchase': float(row['Purchase'].replace(',', '.')),
                'sale': float(row['Sale'].replace(',', '.'))
            })
    return grid_costs


class SimEnv:
    def __init__(self, storage_fp, profile_fp, logs_fp, grid_costs_fp) -> None:

        self.storage_fp = storage_fp
        self.profile_fp = profile_fp
        self.logs_fp = logs_fp
        self.grid_costs_fp = grid_costs_fp

        profiles = load_profiles(profile_fp)

        # Determine the number of steps based on the number of hours in the profiles
        self.max_steps = len(next(iter(profiles.values())))
        steps = self.max_steps
        # Prepare hourly data based on the loaded profiles
        hourly_data = []
        time_labels = []
        for hour in range(steps):
            total_consumption = 0
            total_production = 0
            for ppe, profile in profiles.items():
                total_consumption += profile.iloc[hour]['consumption']
                total_production += profile.iloc[hour]['production']
            date = profile.iloc[hour]['hour']  # Assuming 'hour' column contains date information
            time_labels.append(date)
            hourly_data.append({'hour': hour, 'consumption': total_consumption, 'production': total_production, 'date': date})

        self.grid_costs = load_grid_costs(grid_costs_fp)
        self.p2p_base_price = 0.5
        self.min_price = 0.2
        self.token_mint_rate = 0.1
        self.token_burn_rate = 0.1

        self.hourly_data = hourly_data
        self.time_labels = time_labels

        self._step_count = 0

    def _calc_reward(self, agent):
        return 1

    def step(self, agent, action) -> tuple[list, float, bool]:
        hour_data = self.hourly_data[self._step_count]
        consumption = hour_data['consumption']
        production = hour_data['production']
        date = hour_data['date']

        grid_price = self.grid_costs[self._step_count % len(self.grid_costs)]['purchase']
        sale_price = self.grid_costs[self._step_count % len(self.grid_costs)]['sale']

        self._step_count += 1

        return ([
                consumption,
                production,
                date,
                grid_price,
                sale_price,
                self.p2p_base_price,
                self.min_price,
                self.token_mint_rate,
                self.token_burn_rate
                ],
                self._calc_reward(agent),
                self._step_count >= self.max_steps
                )


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("No required parameter: storage file path")
        sys.exit(1)
    if len(sys.argv) < 2:
        print("No required parameter: profiles directory path")
        sys.exit(1)
    if len(sys.argv) < 3:
        print("No required parameter: logs directory path")
        sys.exit(1)
    if len(sys.argv) < 4:
        print("No required parameter: grid costs file path")
        sys.exit(1)
    server = Server()
    server.start()
    sim = SimEnv(*sys.argv[1:])
    agent = Cooperative({'storages': load_storages(sim.storage_fp)}, 100)

    done = False
    while not done:
        space, reward, done = sim.step(agent, 0)
        agent.simulate_step(*space)

    results_dir = Path("results")
    results_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d_%H:%M:%S")

    # Save results to CSV files
    SIMULATION_STORAGE.update_all(agent, sim.time_labels)
    # save_results_to_csv(agent, sim.time_labels, results_dir, formatted_date)

    # Save logs to a text file
    # log_dir = Path(sys.argv[3])
    # log_dir.mkdir(parents=True, exist_ok=True)

    # agent.save_logs(str(log_dir / f'simulation_{formatted_date}.log'))

    # Generate labels for the X-axis
    # labels = sim.time_labels

    # Assign the modified method to the agent object
    # agent.plot_results = plot_results.__get__(agent)
    # agent.plot_results(len(sim.hourly_data), labels, results_dir, formatted_date)
    import time
    time.sleep(10)
    server.stop()
