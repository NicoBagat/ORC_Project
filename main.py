from pyfiglet import figlet_format
import os
import yaml
from scripts.generate_training_data import generate_training_data
from scripts.train_nn import train_neural_network
from scripts.run_mpc_with_nn import run_mpc_with_nn
from src.utils import load_config

#----------------------------------------------------------------------------------------------------------------
# DISPLAY HEADER
#----------------------------------------------------------------------------------------------------------------

print(figlet_format("ORC Project v2.1", font="standard"))
print("Written by Bagattini Nicola & Ballarini Luigi).\n")
print("This is the main entry point of the application.")
print("(please refer to the documentation/README.md file for further instructions)")
print("-----------------------------------------------------------------------------\n")

#-----------------------------------------------------------------------------------------------------------------
# PENDULUM SELECTION
#-----------------------------------------------------------------------------------------------------------------

print(figlet_format("Pendulum selection", font="smslant"))

# Load configuration from YAML file
config_path = os.path.join("src", "config.yaml")

# Ensure the config file exists
with open(config_path, 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    
# If Pendulums section does not exist, create it (set Single as default)S
if "Pendulums" not in config:
    config["Pendulums"] = {"single": True, "souble": False}    

# Prompt user for pendulum selection
pendulum_input = input("Which pendulum would you like to work with? (single/double): \n").strip().lower()
found = False   # Flag to check if a valid pendulum was selected

# Update configuration based on user input
for key in config["Pendulums"]:
    config["Pendulums"][key] = (key.lower()==pendulum_input)
    if config["Pendulums"][key]:
        print(f"\nSELECTED: {key} Pendulum")
        found = True
# If no valid pendulum was selected, default to Single  
if not found:
    print(f"WARNING: Invalid pendulum type, defaulting to Single!")
    config["Pendulums"]["single"] =  True

# Save updated configuration back to YAML file  
with open(config_path, "w") as file:
    yaml.dump(config, file)
    
#----------------------------------------------------------------------------------------------------------------
# GUIDED PIPELINE EXECUTION
#----------------------------------------------------------------------------------------------------------------
config = load_config(config_path) # Load updated configuration

# Execute each step based on user confirmation

# Step 1: Generate training data
print("\n----------------------------------------------------------------")
if input("Step 1: Generate training data? (Y/N): ").strip().upper() == "Y":
    generate_training_data(config)
else:
    print("Skipping training data generation.")

# Step 2: Train neural network
print("\n----------------------------------------------------------------")
if input("Step 2: Train neural network? (Y/N): ").strip().upper() == "Y":
    train_neural_network(config)
else:
    print("Skipping neural network training.")

# Step 3: Run MPC with trained neural network
print("\n----------------------------------------------------------------")
if input("Step 3: Run MPC with trained NN? (Y/N)").strip().upper() == "Y":
    run_mpc_with_nn(config)
else:
    print("Skipping MPC execution with neural network.")

# Final message
print("\n----------------------------------------------------------------")
print("Pipeline execution completed. Check /plots and /results folders for outputs.")  