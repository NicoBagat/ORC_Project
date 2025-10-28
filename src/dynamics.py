import casadi as ca

from utils.py import load_config

# --------------------------------------------------------------------------------
# Single Pendulum Dynamics
# --------------------------------------------------------------------------------

def SP_dynamics(dt, l, m, g):
    '''
    Returns a CasADi function f(x, u) -> x_next for the single pendulum
    '''
    # Import physical parameters from config file
    config = load_config()
    
    l = config["Dynamics"]["l1"]
    m = config["Dynamics"]["m1"]
    g = config["Dynamics"]["g"]

    # CasADi  symbolic implementation (load from config file)
    x = ca.SX.sym("x", config["ocp"]["state_dim_single"])
    u = ca.SX.sym("u", config["ocp"]["control_dim_single"])

    # State variables
    theta = x[0] #position
    theta_dot = x[1] #velocity
    tau = u [0] #(control) torque

    # Equation of motion
    theta_ddot = (tau - m*g*l*ca.sin(theta)) / (m*l**2)

    # Discretized dynamics (Euler or RK2)
    x_next = ca.vertcat(
        theta + dt * theta_dot,
        theta_dot + dt *theta_ddot
    )

    return ca.Function("f_single", [x, u], [x_next])

# --------------------------------------------------------------------------------
# Double Pendulum Dynamics
# --------------------------------------------------------------------------------

def DP_dynamics(dt, l1, l2, m1, m2, g):
    '''
    Returns a CasADi function f(x, u) -> x_next for the double pendulum
    State: [q1, q2, dq1, dq2]
    Control: [tau1, tau2]
    '''
    # Import physical parameters from config file
    config = load_config()

    l1 = config["Dynamics"]["l1"]
    l2 = config["Dynamics"]["l2"]
    m1 = config["Dynamics"]["m1"]
    m2 = config["Dynamics"]["m2"]
    g = config["Dynamics"]["g"]

    # CasADi  symbolic implementation (load from config file)
    x = ca.SX.sym("x", config["ocp"]["state_dim_double"])
    u = ca.SX.sym("u", config["ocp"]["control_dim_double"])

    # State variables
    q1, q2 = x[0], x[1] #positions
    dq1, dq2 = x[2], x[3] #velocities
    tau1, tau2 = u[0], u[1] # (control) torques

    # Simplified symbolic EOM (not coupled - replace with full version later)
    ddq1 = (tau1 -m1 * g * l1 * ca.sin(q1)) / (m1 * l1**2)
    ddq2 = (tau2 - m2 * g * l2 * ca.sin(q2)) / (m2 * l2**2)

    # Discretized dynamics (Euler or RK2)
    x_next = ca.vertcat(
        q1 + dt * dq1,
        q2 + dt * dq2,
        dq1 + dt * ddq1,
        dq2 + dt * ddq2
    )

    return ca.Function("f_double", [x, u], [x_next])

    