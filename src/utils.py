# GENERAL PURPOSE UTILITIES
from ast import If
from matplotlib.pylab import single
import yaml
import torch

# LOCAL IMPORTS
from src.ocp_solver import OCPSinglePendulum, OCPDoublePendulum
from src.neural_network import SP_NNmodel, DP_NNmodel

#------------------------------------------------------------------------------------
# 1. LOAD CONFIG FILE
def load_config(config_path = "src/config.yaml"):
    """
    Load configuration from a YAML file.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# 2. OCP SOLVER 
def get_ocp_solver(config, dt=0.05, u_min=-2, u_max=2):
    """
    Load the appropriate OCP solver based on the pendulum type specified in the config.
    """
    pend = config["Pendulums"]
    if pend.get("double", False):
        print("[....] Loading Double Pendulum OCP solver ... ")
        return OCPDoublePendulum(dt, u_min, u_max)
    elif pend.get("Single", False):
        print("[....] Loading Single Pendulum OCP solver ... ")
        return OCPSinglePendulum(dt, u_min, u_max)
    else:
        raise ValueError("No pendulum selected in configuration.")
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# 3. NN MODEL LOADER and NORMALIZATION FUNCTIONS
def load_NN_model(single=True):
    model = SP_NNmodel() if single else DP_NNmodel()
    if single:
        model_path = "models/SP_NNmodel.pt"
    else:
        model_path = "models/DP_NNmodel.pt"
    
    model.load_state_dict(torch.load(model_path, map_location=torch.device("cpu")))
    model.eval()
    return model
    
def lin_normalize_inv(nn_output):
    """ Inverse linear normalization for NN output."""
    return 10 * nn_output # assuming original scaling was dividing by 10
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# 3. Define plot save_path]
#------------------------------------------------------------------------------------



#------------------------------------------------------------------------------------
# 5. OCP loader (Load the correct OCP class based on the config file)
#def load_ocp(config):
    if config["Pendulums"]["Single"]:
        ocp = SinglePendulum_OCP(config)
    elif config["Pendulums"]["Double"]:
        ocp = DoublePendulum_OCP(config)
    else:
        raise ValueError("No valid pendulum configuration found in configuration file")
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# 6. 
#------------------------------------------------------------------------------------