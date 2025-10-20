from pyfiglet import figlet_format
import os
import yaml

figlet_format("ORC Project", font="standard")
print(figlet_format("ORC Project", font="standard"))
print("Welcome to the ORC Project!")
print("This is the main entry point of the application.\n")
print("Here you can initialize and run your optimal control problems.")
print("(please refer to the documentation for further instructions)")

#------------------------------------------------------------------------------------
#------------------------------------ PENDULUM SELECTION ----------------------------
#------------------------------------------------------------------------------------
# Load configuration from YAML file
config_path = os.path.join("src", "config.yaml")
with open(config_path, 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Set default if config is None
if config is None:
    config = {"Pendulums": {"Single": False, "Double": False}}
    print("No configuration found. Using default settings.")

# Prompt user in the terminal
pendulum_input = input("Which pendulum to simulate? (Single/Double): ").strip()

# Check if the config has the 'Pendulums' section
if "Pendulums" in config:
    # Reset all pendulum flags to False
    for key in config["Pendulums"]:
        config["Pendulums"][key] = False
    
    # Update based on user input (case-insensitive)Z
    found = False
    for pendulum in config["Pendulums"]:
        if pendulum.lower() == pendulum_input.lower():
            config["Pendulums"][pendulum] = True
            print(f"Selected pendulum: '{pendulum}'.")
            found = True
            break
    if not found:
        print(f"Pendulum '{pendulum_input}' not found in configuration.")
else:
    print("No 'Pendulums' section found in configuration.")

# Save updated configuration back to the file
with open(config_path, 'w') as file:
    yaml.dump(config, file)
    
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------