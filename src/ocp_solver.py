# PYTHON LIBRARIES
import casadi
import numpy as np
import torch 
import l4casadi as l4c

# CUSTOM LIBRARIES
from src import utils

# ------------------------------------------------------------------------------------
# SINGLE PENDULUM OCP
# -----------------------------------------------------------------------------------
class OCPSinglePendulum:
    def __init__(self, dt, u_min=None, u_max=None, l=1.0, m=1.0, g=9.81):
        self.dt = dt
        self.u_min = u_min
        self.u_max = u_max
        self.l = l
        self.m = m
        self.g = g

    def solve(self, x_init, N, q_target=0.0, WithNN=False):
        opti = casadi.Opti()
        x = opti.varaible(N +1, 2)  # State: [theta, theta_dot]
        u = opti.variable(N)
        
        # Cost
        cost = 0
        for i in range(N):
            cost += (x[i, 0] - q_target)**2 + 0.1*x[i, 1]**2 + 0.01*u[i]**2
        
        # Terminal csot (NN or analytical)
        if WithNN:
            model = utils.load_nn_model(single=True) # Load PyTorch model
            l4_model = l4casadi.L4CasADi(model) # wrap PyTorch model
            cost += utils.lin_normalize_inv(l4_model(x[N, :].T)) #  unnormalize
        else:
            cost += (x[N, 0] - q_target)**2 + 0.1*x[N, 1]**2
        opti.minimize(cost)
    
        # Dynamics
        for i in range(N):
            ddq = (u[i] + self.l * self.m * self.g * casadi.sin(x[i, 0])) / (self.l**2 * self.m)
            opti.subject_to(x[i +1, 0] == x[i, 0] + self.dt * x[i, 1] + 0.5 * self.dt**2 * ddq)
            opti.subject_to(x[i +1, 1] == x[i, 1] + self.dt * ddq)

        # Bounds
        if self.u_min is not None and self.u_max is not None:
            for i in range(N): 
                opti.subject_to(opti.bounded(self.u_min, u[i], self.u_max))
                
        opti.subject_to(x[0, :] == x_init) 
        
        opti.solver("ipopt", {"ipopt.print_level": 0, "print_time": 0})
        sol = opti.solve()
        return sol.value(x), sol.value(u)
    
    
# ------------------------------------------------------------------------------------
# DOUBLE PENDULUM OCP
# -----------------------------------------------------------------------------------

# placeholder for double pendulum OCP class
