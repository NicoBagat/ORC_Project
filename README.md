# ORC_Project
Neural Network powered MPC vs normal MPC

# INTRO
## 1. Project entrypoint
The project's pipeline in handled directly in <code>main.py</code> (it will be our entrypoint), where the various functionalities (each defined and handled in dedicated files) are 'called'.

This modularity ensures that, once the core of the mathematical processes (from Network training to basic pendulum dynamics) are defined, we can 'play around' in the main file, like using a GUI with multi selection to decide if we want to operate with a either Single or Double pendulum, the number of initial conditions etc.

## 2. Structure

### :file_folder: /models
Holds the trained neural network models
### :file_folder: /traing_data
Holds the training dataset/s used to train the neural networks
### :file_folder: /plots
Holds the initial conditions plots (states & torques):

🔹<code>/plots/SP</code> : plots for single pendulum 

🔹<code>/plots/DP</code> : Plots for double pendulum
### :file_folder: /scripts
Contains the "main" scripts, that handle more complex functionalities (compared to basic mathematical operations and processes)

N.B. The calling order is defined in the user entrypoint <code>main.py</code>

🔸<code>MPC_with_NN.py</code>: The core of the project, evaluates OCPs with the different models. Compares the produced results with non-NN assited computation (as per requirements)

🔸<code>NN_training.py</code>: Trains different neural models based on the datasets saved (so as to underline the importance of datasets in deep learning).

🔸<code>Data_generation.py</code>: Generates training data based on the set hyperparameters (random vs grid, # of samples) and saves them in the dedicated path. 

### :file_folder: /src
Contains the files that handle the more "basic" aspects of the project (Neural Network definition, Dynamics, Parameters etc...)

🔹<code>config.yaml</code>:

🔹<code>ocp_solver.py</code>: 

🔹<code>dynamics.py</code>:

🔹<code>neural_network.py</code>:

🔹<code>IC_plots.py</code>:
