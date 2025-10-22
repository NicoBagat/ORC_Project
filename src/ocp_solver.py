from src.utils import config
import casadi as ca
import numpy as np
import l4casadi as l4c

class Base_OCP:
    def __init__(self, config):
        self.config = config
        self.N = config["ocp"]["horizon"]

    def setup(self):
        raise NotImplementedError
    
class SinglePendulum_OCP(Base_OCP):
    def __init__(self, config):
        super().__init__(config)
        self.state_dim = 2
        self.control_dim = 1

class DoublePendulum_OCP(Base_OCP):
    def __init__(self, config):
        super().__init__(config)
        self.state_dim = 4
        self.control_dim = 1