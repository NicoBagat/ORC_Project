# GENERAL PURPOSE UTILITIES
import yaml
# from src.ocp_solver import OCPSinglePendulum, OCPDoublePendulum

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
# 2. Define model load_path
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