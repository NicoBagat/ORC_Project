import os
from utils import load_config

# Pendulum selection
if pendulum_type == "Single":
    from scripts.NeuralNetwork_Training import train_single_pendulum
    train_single_pendulum()