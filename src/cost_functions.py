import casadi as ca

from utils.py import load_config    

# --------------------------------------------------------------------------------
# Single Pendulum Cost Functions
# --------------------------------------------------------------------------------
# STAGE COST
def stage_cost_SP(x, u, q_target):
    '''
    Quadratic cost for single pendulum
    '''
    config = load_config()
    q_target = config["ocp"]["q_target"]

    theta, theta_dot = x[0], x[1]
    s_cost_SP = (theta - q_target)**2 + 0.1 * theta_dot**2 + 0.01*u**2

    return s_cost_SP

# TERMINAL COST
def terrminal_cost_SP(x, q_target):
    '''
    Terminal cost for single pendulum
    '''
    config = load_config()
    q_target = config["ocp"]["q_target"]

    theta, theta_dot = x[0], x[1]
    t_cost_SP = (theta - q_target)**2 + 0.1 * theta_dot**2

    return t_cost_SP

# --------------------------------------------------------------------------------
# Double Pendulum Cost Functions
# --------------------------------------------------------------------------------
# STAGE COST
def stage_cost_double(x, u):
    '''
    Quadratic cost for double pendulum
    '''
    s_cost_DP = ca.sumsqr(x) * 0.1 * ca.sumsqr(u)
    return s_cost_DP

# TERMINAL COST
def terminal_cost_double(x):
    t_cost_DP = ca.sumsqr(x)
    return t_cost_DP