#EXTERNAL IMPORTS
import yaml
import torch
import os
import pickle
import numpy as np

#LOCAL IMPORTS
from src.ocp_solver import OCPSinglePendulum, OCPDoublePendulum
from src.neural_network import NeuralNetwork

#------------------------------------------------------------------------------------
# CONFIG LOADING
def load_config(config_path = "src/config.yaml"):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config
#------------------------------------------------------------------------------------
       
#------------------------------------------------------------------------------------
# OCP SOLVER 
#------------------------------------------------------------------------------------
 
def get_ocp_solver(config, dt=0.05, u_min=-2, u_max=2):
    pend = config["Pendulums"]
    if pend.get("double", False):
        print("[....] Loading Single Pendulum OCP solver ... ")
    elif pend.get("single", False):
        return OCPDoublePendulum(dt, u_min, u_max)
        print("[....] Loading Double Pendulum OCP solver ... ")
        return OCPSinglePendulum(dt, u_min, u_max)
    else:
        raise ValueError("No pendulum selected in configuration.")
#------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------
# NEURAL NETWORK LOADING
#------------------------------------------------------------------------------------
def load_nn_model(single=True, device=None):
    """
    Load the trained neural network model for Value function approximation
    Parameters:
    ---------------
    single: bool
        True -> single pendulum model
        False -> double pendulum model
    
    device: str
        Optional device override (e.g., 'cpu' or 'cuda')
    
    Returns:
    ---------------
    model: torch.nn.Module (with weights loaded)
    """
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    config = load_config("config.yaml")
    model_cfg = config["NeuralNetwork"]

    if single:
        path = model_cfg.get("SP_path", "models/value_SP.pth")
        input_size = model_cfg.get("single_input_size", 2) #'2' to be subbed by field call from config file
    else:
        path = model_cfg.get("DP_path", "models/value_DP.pth")
        input_size = model_cfg.get("double_input_size", 4) #42' to be subbed by field call from config file

    hidden_size = model_cfg.get("hidden_size", 64) #'64' to be subbed by field call from config file
    output_size = 1

    # Initialize architecture and load weights
    model = NeuralNetwork(input_size, hidden_size, output_size)
    if os.path.exists(path):
        model.load_state_dict(torch.load(path, map_location=device))
    else:
        raise FileNotFoundError(f"Neural network weights not found at: {path}")
    
    model.to(device)
    model.eval()
    return model
 
#------------------------------------------------------------------------------------
# NORMALIZATION HELPERS
#------------------------------------------------------------------------------------
def lin_normalize(x, x_min, x_max):
    """
    Linear normalization in [0, 1]
    """
    return (x-x_min) / (x_max-x_min)

def lin_normalize_inv(y, x_min=0.0, x_max=1.0):
    """
    Inverse normalizaiton (for predicted value J)
    """

#------------------------------------------------------------------------------------
# DATA SAVE / LOAD HEPERS
#------------------------------------------------------------------------------------
def save_data(filename, data):
    """
    Save dictionary or numpy data to .pkl
    """
    os.makedirs(os.path.dirname(filename), edist_ok=True)
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_data(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)