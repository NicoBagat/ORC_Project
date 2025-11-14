import numpy as np
from src.utils import get_ocp_solver, load_nn_model

def run_mpc_with_nn(config, N_steps=50):
    ocp_solver = get_ocp_solver(config, dt=config["OCP"]["dt"], u_min=config["OCP"]["u_min"], u_max=config["OCP"]["u_max"])
    model = load_nn_model(single=config["Pendulums"]["single"])

    x_current = np.random.uniform(-np.pi, np.pi, size=(ocp_solver.state_dim,))
    traj = [x_current]
    u_seq = []

    for _ in range(N_steps):
        x_traj, u_traj = ocp_solver.solve(x_current, N=config["OCP"]["horizon"], WithNN=True)
        u_current = u_traj[0] if ocp_solver.control_dim>1 else u_traj[0,0]
        u_seq.append(u_current)
        x_current = x_traj[1]
        traj.append(x_current)

    print("[INFO] MPC run completed")
    return np.array(traj), np.array(u_seq)
