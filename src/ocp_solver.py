#External imports
import casadi as ca
import numpy as np
import l4casadi as l4c

#Local imports
from src.utils import load_config, load_nn_model, lin_normalize, lin_normalize_inv
from src.dynamics import SP_dynamics, DP_dynamics
from src.cost_functions import stage_cost_SP, terrminal_cost_SP, stage_cost_double, terminal_cost_double
from src.inequality_constraints import control_bounds, state_bounds
# --------------------------------------------------------------------------------
# SINGLE PENDULUM OCP
# --------------------------------------------------------------------------------
    
class OCPSinglePendulum:

    def __init__(self, dt, u_min=None, u_max=None, l=1.0, m=1.0, g=9.81):
        config = load_config

        # edit to load data from config file
        self.dt = dt
        self.u_min = u_min
        self.u_max = u_max
        self.l= l
        self.m= m
        self.g = g
    
    def solve(self, x_init, N, q_target=0.0, WithNN=False):
        config = load_config
        
        opti = ca.Opti()
        x = opti.variable(N+1, 2)
        u = opti.variable(N)

        # -----------------------------
        # COST FUNCTION
        # -----------------------------
        cost = 0
        for i in range(N):
            cost += (x[i, 0] - q_target)**2 + 0.1*x[i, 1]**2 + 0.01*u[i]**2
        
        # Terminal cost (NN or analytical)
        if WithNN:
            model = load_nn_model(single=True)
            l4_model=l4c.l4CasADi(model)
            cost += lin_normalize_inv(l4_model(x[N, :].T))
        else:
            cost += (x[N, 0] - q_target)**2 + 0.1 * x[N, 1]**2

        opti.minimize(cost)

        # ---------------------------------------------
        # DYNAMICS (imported from external module)
        # ---------------------------------------------
        for i in range(N):
            x_next = x[i, :] + self.dt * SP_dynamics(x[i, :], u[i], self.l, self.m, self.g) 
            opti.subject_to(x[i + 1, :] == x_next.T)

        # ---------------------------------------------
        # CONSTRAINTS
        # ---------------------------------------------
        if self.u_min is not None and self.u_max is not None:
            for i in range(N):
                opti.subject_to(opti.bounded(self.u_min, u[i], self.u_max))
        
        opti.subject_to(x[0, :] == x_init)

        # ---------------------------------------------
        # SOLVER
        # ---------------------------------------------
        opti.solver("ipopt", {"ipopt.print_level": 0, "print_time":0})
        sol = opti.solve()
        return sol.value(x), sol.value(u)

        

