import numpy as np
from src.utils import get_ocp_solver, save_data

def generate_training_data(config, N_samples=100):
    dt = config["OCP"]["dt"]
    horizon = config["OCP"]["horizon"]
    u_min = config["OCP"]["u_min"]
    u_max = config["OCP"]["u_max"]

    ocp_solver = get_ocp_solver(config, dt=dt, u_min=u_min, u_max=u_max)

    training_data = {"x0": [], "J": []}
    for _ in range(N_samples):
        x0 = np.random.uniform(-np.pi, np.pi, size=(ocp_solver.state_dim,))
        x_traj, u_traj = ocp_solver.solve(x0, horizon, WithNN=False)
        J = np.sum(u_traj**2) + np.sum((x_traj[:-1,0])**2)
        training_data["x0"].append(x0)
        training_data["J"].append(J)

    save_data("results/training_data.pkl", training_data)
    print("[INFO] Training data saved: results/training_data.pkl")
