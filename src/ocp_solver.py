#External imports
import casadi as ca

#Local imports
from src.utils import load_config, load_nn_model, lin_normalize, lin_normalize_inv
from src.dynamics import SP_dynamics, DP_dynamics
from src.cost_functions import stage_cost_SP, terminal_cost_SP, stage_cost_DP, terminal_cost_DP

# --------------------------------------------------------------------------------
# SINGLE PENDULUM OCP
# --------------------------------------------------------------------------------
    
class OCPSinglePendulum:

    def __init__(self, dt, u_min=None, u_max=None, l=1.0, m=1.0, g=9.81):
        # edit to load data from config file
        self.dt = dt
        self.u_min = u_min
        self.u_max = u_max
        self.state_dim = 2
        self.control_dim = 1
        self.f_dyn = SP_dynamics()
    
    def solve(self, x0, N, WithNN=False):        
        opti = ca.Opti()
        x = opti.variable(N+1, self.state_dim)
        u = opti.variable(N, self.control_dim)

        # -----------------------------
        # COST FUNCTION
        # -----------------------------
        cost = 0
        for i in range(N):
            cost += stage_cost_SP(x[i,:], u[i])
            opti.sunject_to(x[i+1,:]== x_next.T)
        cost += terminal_cost_SP(x[N,:])
        opti.minimize(cost)

        # ---------------------------------------------
        # DYNAMICS (imported from external module)
        # ---------------------------------------------
        for i in range(N):
            x_next = self.f_dyn(x[i, :], u[i, :])
            opti.subject_to(x[i+1, :] == x_next.T)

        # ---------------------------------------------
        # CONSTRAINTS
        # ---------------------------------------------
        if self.u_min is not None and self.u_max is not None:
            for i in range(N):
                opti.subject_to(opti.bounded(self.u_min, u[i, 0], self.u_max))
        
        opti.subject_to(x[0, :] == x0)

        opti.solver("ipopt", {"ipopt.print_level":0, "print_time":0})
        sol = opti.solve()
        return sol.value(x), sol.value(u)

# --------------------------------------------------------------------------------
# DOUBLE PENDULUM OCP
# -------------------------------------------------------------------------------- 

class OCPDoublePendulum:
    def __init__(self, dt, u_min=None, u_max=None):
        self.dt = dt
        self.u_min = u_min
        self.u_max = u_max
        self.state_dim = 4
        self.control_dim = 2
        self.f_dyn = DP_dynamics()

    def solve(self, x0, N, WithNN=False):
        opti = ca.Opti()
        x = opti.variable(N+1, self.state_dim)
        u = opti.variable(N, self.control_dim)

        cost = 0

        for i in range(N):
            cost += stage_cost_DP(x[i,:])
        cost += terminal_cost_DP(x[N,:])
        opti.minimize(cost)

        for i in range(N):
            x_next = self.f_dyn(x[i,:], u[i,:])
            opti.subject_to(x[i+1,:] == x_next.T)
        
        if self.u_min is not None and self.u_max is not None:
            for i in range(N):
                for j in range(self.control_dim):
                    opti.subject_to(opti.bounded(self.u_min, u[i,j], self.u_max))
        
        opti.subject_to(x[0,:] == x0)
        opti.solver("ipopt", {"ipopt.print_level":0, "print_time":0})
        sol = opti.solve()
        return sol.value(x), sol.value(u)

        

