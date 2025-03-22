from simulation.env.simulation_env import SimEnv
from simulation.models.stat_agent import StatAgent

from simulation.utils.helper_functions import load_profiles, load_storages, save_results_to_csv, plot_results

storage_fp, profile_fp, logs_fp, grid_costs_fp = './storages.csv', 'pv_profiles', 'logs', 'grid_costs'

simenv = SimEnv(storage_fp, profile_fp, logs_fp, grid_costs_fp)

agent = StatAgent({'storages': load_storages(simenv.storage_fp)}, 100)


done = False
i = 0
while not done:
    print(i)
    i += 1
    state, done = simenv.step()
    agent.step(*state)

print(agent.token_balances)

agent.plot()
