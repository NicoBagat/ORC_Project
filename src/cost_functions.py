# EXTERNAL IMPORTS
import casadi as ca

# LOCAL IMPORTS
from utils.py import load_config    

# Load from configuration file
config = load_config() 

# --------------------------------------------------------------------------------
# SINGLE PENDULUM
# --------------------------------------------------------------------------------
# Stage cost (quadratic cost)

def stage_cost_SP(x, u):
    '''
    Quadratic cost for single pendulum
    '''
    q_target = config["OCP"]["q_target"]

    theta, theta_dot = x[0], x[1] # Optional, done for algebraic clarity sake
    s_cost_SP = (theta - q_target)**2 + 0.1 * theta_dot**2 + 0.01*u**2

    return s_cost_SP

# Terminal cost
def terrminal_cost_SP(x):
    '''
    Terminal cost for single pendulum
    '''
    q_target = config["OCP"]["q_target"]

    theta, theta_dot = x[0], x[1]
    t_cost_SP = (theta - q_target)**2 + 0.1 * theta_dot**2

    return t_cost_SP

# --------------------------------------------------------------------------------
# DOUBLE PENDULUM
# --------------------------------------------------------------------------------
# Stage cost (quadratic cost)
def stage_cost_double(x, u):

    s_cost_DP = ca.sumsqr(x) * 0.1 * ca.sumsqr(u)
    return s_cost_DP

# Terminal cost
def terminal_cost_double(x):
    t_cost_DP = ca.sumsqr(x)
    return t_cost_DP